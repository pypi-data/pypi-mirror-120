Django FileBrowser
==================

**Media-Management** based on https://github.com/sehmaschine/django-filebrowser
and https://github.com/smacker/django-filebrowser-no-grappelli.

The FileBrowser is an extension to the `Django <http://www.djangoproject.com>`_ administration interface in order to:

* browse directories on your server and upload/delete/edit/rename files.

Requirements
------------

FileBrowser 3.8 requires

* Django 1.11/2.2/3.0 (http://www.djangoproject.com)

No Grappelli No Pillow
----------------------

This fork removes the dependency on Grappelli and Pillow (no image processing).

Installation
------------

Stable version:

    pip install django-filebrowser-no-grappelli-no-pillow



Documentation
-------------

http://readthedocs.org/docs/django-filebrowser/

It also has fake model to show filebrowser in admin dashboard, but you can disable it by setting ``FILEBROWSER_SHOW_IN_DASHBOARD = False``.
