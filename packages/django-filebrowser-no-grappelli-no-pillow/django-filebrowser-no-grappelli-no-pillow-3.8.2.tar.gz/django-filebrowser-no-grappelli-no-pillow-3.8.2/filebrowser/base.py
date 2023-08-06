# coding: utf-8

import datetime
import mimetypes
import os
import platform
import tempfile
import time

from django.core.files import File
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from six import python_2_unicode_compatible, string_types

from filebrowser.compat import get_modified_time
from filebrowser.settings import EXTENSIONS
from filebrowser.utils import path_strip


class FileListing():
    """
    The FileListing represents a group of FileObjects/FileDirObjects.

    An example::

        from filebrowser.base import FileListing
        filelisting = FileListing(path, sorting_by='date', sorting_order='desc')
        print filelisting.files_listing_total()
        print filelisting.results_listing_total()
        for fileobject in filelisting.files_listing_total():
            print fileobject.filetype

    where path is a relative path to a storage location
    """
    # Four variables to store the length of a listing obtained by various listing methods
    # (updated whenever a particular listing method is called).
    _results_listing_total = None
    _results_walk_total = None
    _results_listing_filtered = None
    _results_walk_total = None

    def __init__(self, path, filter_func=None, sorting_by=None, sorting_order=None, site=None):
        self.path = path
        self.filter_func = filter_func
        self.sorting_by = sorting_by
        self.sorting_order = sorting_order
        if not site:
            from filebrowser.sites import site as default_site
            site = default_site
        self.site = site

    # HELPER METHODS
    # sort_by_attr

    def sort_by_attr(self, seq, attr):
        """
        Sort the sequence of objects by object's attribute

        Arguments:
        seq  - the list or any sequence (including immutable one) of objects to sort.
        attr - the name of attribute to sort by

        Returns:
        the sorted list of objects.
        """
        from operator import attrgetter
        if isinstance(attr, string_types):  # Backward compatibility hack
            attr = (attr, )
        return sorted(seq, key=attrgetter(*attr))

    @cached_property
    def is_folder(self):
        return self.site.storage.isdir(self.path)

    def listing(self):
        "List all files for path"
        if self.is_folder:
            dirs, files = self.site.storage.listdir(self.path)
            return (f for f in dirs + files)
        return []

    def _walk(self, path, filelisting):
        """
        Recursively walks the path and collects all files and
        directories.

        Danger: Symbolic links can create cycles and this function
        ends up in a regression.
        """
        dirs, files = self.site.storage.listdir(path)

        if dirs:
            for d in dirs:
                self._walk(os.path.join(path, d), filelisting)
                filelisting.extend([path_strip(os.path.join(path, d), self.site.directory)])

        if files:
            for f in files:
                filelisting.extend([path_strip(os.path.join(path, f), self.site.directory)])

    def walk(self):
        "Walk all files for path"
        filelisting = []
        if self.is_folder:
            self._walk(self.path, filelisting)
        return filelisting

    # Cached results of files_listing_total (without any filters and sorting applied)
    _fileobjects_total = None

    def files_listing_total(self):
        "Returns FileObjects for all files in listing"
        if self._fileobjects_total is None:
            self._fileobjects_total = []
            for item in self.listing():
                fileobject = FileObject(os.path.join(self.path, item), site=self.site)
                self._fileobjects_total.append(fileobject)

        files = self._fileobjects_total

        if self.sorting_by:
            files = self.sort_by_attr(files, self.sorting_by)
        if self.sorting_order == "desc":
            files.reverse()

        self._results_listing_total = len(files)
        return files

    def files_walk_total(self):
        "Returns FileObjects for all files in walk"
        files = []
        for item in self.walk():
            fileobject = FileObject(os.path.join(self.site.directory, item), site=self.site)
            files.append(fileobject)
        if self.sorting_by:
            files = self.sort_by_attr(files, self.sorting_by)
        if self.sorting_order == "desc":
            files.reverse()
        self._results_walk_total = len(files)
        return files

    def files_listing_filtered(self):
        "Returns FileObjects for filtered files in listing"
        if self.filter_func:
            listing = list(filter(self.filter_func, self.files_listing_total()))
        else:
            listing = self.files_listing_total()
        self._results_listing_filtered = len(listing)
        return listing

    def files_walk_filtered(self):
        "Returns FileObjects for filtered files in walk"
        if self.filter_func:
            listing = list(filter(self.filter_func, self.files_walk_total()))
        else:
            listing = self.files_walk_total()
        self._results_walk_filtered = len(listing)
        return listing

    def results_listing_total(self):
        "Counter: all files"
        if self._results_listing_total is not None:
            return self._results_listing_total
        return len(self.files_listing_total())

    def results_walk_total(self):
        "Counter: all files"
        if self._results_walk_total is not None:
            return self._results_walk_total
        return len(self.files_walk_total())

    def results_listing_filtered(self):
        "Counter: filtered files"
        if self._results_listing_filtered is not None:
            return self._results_listing_filtered
        return len(self.files_listing_filtered())

    def results_walk_filtered(self):
        "Counter: filtered files"
        if self._results_walk_filtered is not None:
            return self._results_walk_filtered
        return len(self.files_walk_filtered())


@python_2_unicode_compatible
class FileObject():
    """
    The FileObject represents a file (or directory) on the server.

    An example::

        from filebrowser.base import FileObject
        fileobject = FileObject(path)

    where path is a relative path to a storage location
    """

    def __init__(self, path, site=None):
        if not site:
            from filebrowser.sites import site as default_site
            site = default_site
        self.site = site
        if platform.system() == 'Windows':
            self.path = path.replace('\\', '/')
        else:
            self.path = path
        self.head = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.filename_lower = self.filename.lower()
        self.filename_root, self.extension = os.path.splitext(self.filename)
        self.mimetype = mimetypes.guess_type(self.filename)

    def __str__(self):
        return force_text(self.path)

    def __fspath__(self):
        return self.__str__()

    @property
    def name(self):
        return self.path

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self or "None")

    def __len__(self):
        return len(self.path)

    # HELPER METHODS
    # _get_file_type

    def _get_file_type(self):
        "Get file type as defined in EXTENSIONS."
        file_type = ''
        for k, v in EXTENSIONS.items():
            for extension in v:
                if self.extension.lower() == extension.lower():
                    file_type = k
        return file_type

    # GENERAL ATTRIBUTES/PROPERTIES
    # filetype
    # filesize
    # date
    # datetime
    # exists

    @cached_property
    def filetype(self):
        "Filetype as defined with EXTENSIONS"
        return 'Folder' if self.is_folder else self._get_file_type()

    @cached_property
    def filesize(self):
        "Filesize in bytes"
        return self.site.storage.size(self.path) if self.exists else None

    @cached_property
    def date(self):
        "Modified time (from site.storage) as float (mktime)"
        if self.exists:
            return time.mktime(get_modified_time(self.site.storage, self.path).timetuple())
        return None

    @property
    def datetime(self):
        "Modified time (from site.storage) as datetime"
        if self.date:
            return datetime.datetime.fromtimestamp(self.date)
        return None

    @cached_property
    def exists(self):
        "True, if the path exists, False otherwise"
        return self.site.storage.exists(self.path)

    # PATH/URL ATTRIBUTES/PROPERTIES
    # path (see init)
    # path_relative_directory
    # path_full
    # dirname
    # url

    @property
    def path_relative_directory(self):
        "Path relative to site.directory"
        return path_strip(self.path, self.site.directory)

    @property
    def path_full(self):
        "Absolute path as defined with site.storage"
        return self.site.storage.path(self.path)

    @property
    def dirname(self):
        "The directory (not including site.directory)"
        return os.path.dirname(self.path_relative_directory)

    @property
    def url(self):
        "URL for the file/folder as defined with site.storage"
        return self.site.storage.url(self.path)

    # FOLDER ATTRIBUTES/PROPERTIES
    # is_folder
    # is_empty

    @cached_property
    def is_folder(self):
        "True, if path is a folder"
        return self.site.storage.isdir(self.path)

    @property
    def is_empty(self):
        "True, if folder is empty. False otherwise, or if the object is not a folder."
        if self.is_folder:
            dirs, files = self.site.storage.listdir(self.path)
            if not dirs and not files:
                return True
        return False

    # DELETE METHODS
    # delete()

    def delete(self):
        "Delete FileObject (deletes a folder recursively)"
        if self.is_folder:
            self.site.storage.rmtree(self.path)
        else:
            self.site.storage.delete(self.path)
