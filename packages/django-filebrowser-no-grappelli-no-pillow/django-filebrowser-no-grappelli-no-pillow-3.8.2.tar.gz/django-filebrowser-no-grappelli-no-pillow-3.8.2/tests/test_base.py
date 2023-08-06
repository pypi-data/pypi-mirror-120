# coding: utf-8

import os
import ntpath
import posixpath
import shutil

from mock import patch

from filebrowser.base import FileObject, FileListing
from filebrowser.sites import site
from tests.base import FilebrowserTestCase as TestCase


class FileObjectPathTests(TestCase):

    def setUp(self):
        super(FileObjectPathTests, self).setUp()
        shutil.copy(self.STATIC_IMG_PATH, self.FOLDER_PATH)

    @patch('filebrowser.base.os.path', ntpath)
    def test_windows_paths(self):
        """
        Use ntpath to test windows paths independently from current os
        """
        f = FileObject('_test\\uploads\\folder\\testfile.jpg', site=site)

        self.assertEqual(f.path_relative_directory, 'folder\\testfile.jpg')
        self.assertEqual(f.dirname, r'folder')

    @patch('filebrowser.base.os.path', posixpath)
    def test_posix_paths(self):
        """
        Use posixpath to test posix paths independently from current os
        """
        f = FileObject('_test/uploads/folder/testfile.jpg', site=site)

        self.assertEqual(f.path_relative_directory, 'folder/testfile.jpg')
        self.assertEqual(f.dirname, r'folder')


class FileObjectUnicodeTests(TestCase):

    def setUp(self):
        super(FileObjectUnicodeTests, self).setUp()
        shutil.copy(self.STATIC_IMG_PATH, self.FOLDER_PATH)

    @patch('filebrowser.base.os.path', ntpath)
    def test_windows_paths(self):
        """
        Use ntpath to test windows paths independently from current os
        """
        f = FileObject('_test\\uploads\\$%^&*\\測試文件.jpg', site=site)

        self.assertEqual(f.path_relative_directory, '$%^&*\\測試文件.jpg')
        self.assertEqual(f.dirname, r'$%^&*')

    @patch('filebrowser.base.os.path', posixpath)
    def test_posix_paths(self):
        """
        Use posixpath to test posix paths independently from current os
        """
        f = FileObject('_test/uploads/$%^&*/測試文件.jpg', site=site)

        self.assertEqual(f.path_relative_directory, '$%^&*/測試文件.jpg')
        self.assertEqual(f.dirname, r'$%^&*')


class FileObjectAttributeTests(TestCase):

    def setUp(self):
        super(FileObjectAttributeTests, self).setUp()
        shutil.copy(self.STATIC_IMG_PATH, self.FOLDER_PATH)

    def test_init_attributes(self):
        """
        FileObject init attributes

        # path
        # head
        # filename
        # filename_lower
        # filename_root
        # extension
        # mimetype
        """
        self.assertEqual(self.F_IMAGE.path, "_test/uploads/folder/testimage.jpg")
        self.assertEqual(self.F_IMAGE.head, '_test/uploads/folder')
        self.assertEqual(self.F_IMAGE.filename, 'testimage.jpg')
        self.assertEqual(self.F_IMAGE.filename_lower, 'testimage.jpg')
        self.assertEqual(self.F_IMAGE.filename_root, 'testimage')
        self.assertEqual(self.F_IMAGE.extension, '.jpg')
        self.assertEqual(self.F_IMAGE.mimetype, ('image/jpeg', None))

    def test_general_attributes(self):
        """
        FileObject general attributes

        # filetype
        # filesize
        # date
        # datetime
        # exists
        """
        self.assertEqual(self.F_IMAGE.filetype, 'Image')

        self.assertEqual(self.F_IMAGE.filetype, 'Image')
        self.assertEqual(self.F_IMAGE.filesize, 870037)
        # FIXME: test date/datetime
        self.assertEqual(self.F_IMAGE.exists, True)

    def test_path_url_attributes(self):
        """
        FileObject path and url attributes

        # path (see init)
        # path_relative_directory
        # path_full
        # dirname
        # url
        """
        # test with image
        self.assertEqual(self.F_IMAGE.path, "_test/uploads/folder/testimage.jpg")
        self.assertEqual(self.F_IMAGE.path_relative_directory, "folder/testimage.jpg")
        self.assertEqual(self.F_IMAGE.path_full, os.path.join(site.storage.location, site.directory, "folder/testimage.jpg"))
        self.assertEqual(self.F_IMAGE.dirname, "folder")
        self.assertEqual(self.F_IMAGE.url, site.storage.url(self.F_IMAGE.path))

        # test with folder
        self.assertEqual(self.F_FOLDER.path, "_test/uploads/folder")
        self.assertEqual(self.F_FOLDER.path_relative_directory, "folder")
        self.assertEqual(self.F_FOLDER.path_full, os.path.join(site.storage.location, site.directory, "folder"))
        self.assertEqual(self.F_FOLDER.dirname, "")
        self.assertEqual(self.F_FOLDER.url, site.storage.url(self.F_FOLDER.path))

        # test with alternative folder
        self.assertEqual(self.F_SUBFOLDER.path, "_test/uploads/folder/subfolder")
        self.assertEqual(self.F_SUBFOLDER.path_relative_directory, "folder/subfolder")
        self.assertEqual(self.F_SUBFOLDER.path_full, os.path.join(site.storage.location, site.directory, "folder/subfolder"))
        self.assertEqual(self.F_SUBFOLDER.dirname, "folder")
        self.assertEqual(self.F_SUBFOLDER.url, site.storage.url(self.F_SUBFOLDER.path))

    def test_folder_attributes(self):
        """
        FileObject folder attributes

        # directory (deprecated) > path_relative_directory
        # folder (deprecated) > dirname
        # is_folder
        # is_empty
        """
        # test with image
        self.assertEqual(self.F_IMAGE.path_relative_directory, "folder/testimage.jpg")  # equals path_relative_directory
        self.assertEqual(self.F_IMAGE.dirname, "folder")  # equals dirname
        self.assertEqual(self.F_IMAGE.is_folder, False)
        self.assertEqual(self.F_IMAGE.is_empty, False)

        # test with folder
        self.assertEqual(self.F_FOLDER.path_relative_directory, "folder")  # equals path_relative_directory
        self.assertEqual(self.F_FOLDER.dirname, "")  # equals dirname
        self.assertEqual(self.F_FOLDER.is_folder, True)
        self.assertEqual(self.F_FOLDER.is_empty, False)

        # test with alternative folder
        self.assertEqual(self.F_SUBFOLDER.path_relative_directory, "folder/subfolder")  # equals path_relative_directory
        self.assertEqual(self.F_SUBFOLDER.dirname, "folder")  # equals dirname
        self.assertEqual(self.F_SUBFOLDER.is_folder, True)
        self.assertEqual(self.F_SUBFOLDER.is_empty, True)

    def test_delete(self):
        """
        FileObject delete methods

        # delete
        """

        # version does not exist yet
        f_version = FileObject(os.path.join(site.directory, 'folder', "testimage_large.jpg"), site=site)
        self.assertEqual(f_version.exists, False)

class FileListingTests(TestCase):
    """
    /_test/uploads/testimage.jpg
    /_test/uploads/folder/
    /_test/uploads/folder/subfolder/
    /_test/uploads/folder/subfolder/testimage.jpg
    """

    def setUp(self):
        super(FileListingTests, self).setUp()

        self.F_LISTING_FOLDER = FileListing(self.DIRECTORY, sorting_by='date', sorting_order='desc')
        self.F_LISTING_IMAGE = FileListing(os.path.join(self.DIRECTORY, 'folder', 'subfolder', "testimage.jpg"))

        shutil.copy(self.STATIC_IMG_PATH, self.SUBFOLDER_PATH)
        shutil.copy(self.STATIC_IMG_PATH, self.DIRECTORY_PATH)

    def test_init_attributes(self):
        """
        FileListing init attributes

        # path
        # filter_func
        # sorting_by
        # sorting_order
        """
        self.assertEqual(self.F_LISTING_FOLDER.path, '_test/uploads/')
        self.assertEqual(self.F_LISTING_FOLDER.filter_func, None)
        self.assertEqual(self.F_LISTING_FOLDER.sorting_by, 'date')
        self.assertEqual(self.F_LISTING_FOLDER.sorting_order, 'desc')

    def test_listing(self):
        """
        FileObject listing

        # listing
        # files_listing_total
        # files_listing_filtered
        # results_listing_total
        # results_listing_filtered
        """

        self.assertEqual(self.F_LISTING_IMAGE.listing(), [])
        self.assertEqual(list(self.F_LISTING_FOLDER.listing()), [u'folder', u'testimage.jpg'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_listing_total()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_listing_filtered()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder'])
        self.assertEqual(self.F_LISTING_FOLDER.results_listing_total(), 2)
        self.assertEqual(self.F_LISTING_FOLDER.results_listing_filtered(), 2)

    def test_listing_filtered(self):
        """
        FileObject listing

        # listing
        # files_listing_total
        # files_listing_filtered
        # results_listing_total
        # results_listing_filtered
        """

        self.assertEqual(self.F_LISTING_IMAGE.listing(), [])
        self.assertEqual(list(self.F_LISTING_FOLDER.listing()), [u'folder', u'testimage.jpg'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_listing_total()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_listing_filtered()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder'])
        self.assertEqual(self.F_LISTING_FOLDER.results_listing_total(), 2)
        self.assertEqual(self.F_LISTING_FOLDER.results_listing_filtered(), 2)

    def test_walk(self):
        """
        FileObject walk

        # walk
        # files_walk_total
        # files_walk_filtered
        # results_walk_total
        # results_walk_filtered
        """

        self.assertEqual(self.F_LISTING_IMAGE.walk(), [])
        self.assertEqual(list(self.F_LISTING_FOLDER.walk()), [u'folder/subfolder/testimage.jpg', u'folder/subfolder', u'folder', u'testimage.jpg'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_walk_total()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder', u'_test/uploads/folder/subfolder', u'_test/uploads/folder/subfolder/testimage.jpg'])
        self.assertEqual(list(f.path for f in self.F_LISTING_FOLDER.files_walk_filtered()), [u'_test/uploads/testimage.jpg', u'_test/uploads/folder', u'_test/uploads/folder/subfolder', u'_test/uploads/folder/subfolder/testimage.jpg'])
        self.assertEqual(self.F_LISTING_FOLDER.results_walk_total(), 4)
        self.assertEqual(self.F_LISTING_FOLDER.results_walk_filtered(), 4)


class FileObjecNamerTests(TestCase):
    def setUp(self):
        super(FileObjecNamerTests, self).setUp()
        shutil.copy(self.STATIC_IMG_PATH, self.FOLDER_PATH)

    def test_init_attributes(self):
        """
        FileObject init attributes

        # path
        # head
        # filename
        # filename_lower
        # filename_root
        # extension
        # mimetype
        """
        self.assertEqual(self.F_IMAGE.path, "_test/uploads/folder/testimage.jpg")
        self.assertEqual(self.F_IMAGE.head, '_test/uploads/folder')
        self.assertEqual(self.F_IMAGE.filename, 'testimage.jpg')
        self.assertEqual(self.F_IMAGE.filename_lower, 'testimage.jpg')
        self.assertEqual(self.F_IMAGE.filename_root, 'testimage')
        self.assertEqual(self.F_IMAGE.extension, '.jpg')
        self.assertEqual(self.F_IMAGE.mimetype, ('image/jpeg', None))
