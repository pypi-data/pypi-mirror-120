# coding: utf-8

# FIXME
# These tests are designed to run against production, not testing. They
# would be better suited for the Django Check Framework.
#
# https://docs.djangoproject.com/en/1.8/topics/checks/


# # PYTHON IMPORTS
# import os

# # DJANGO IMPORTS
# from django.test import TestCase
# from django.conf import settings

# # FILEBROWSER IMPORTS
# from filebrowser.settings import *


# class SettingsTests(TestCase):

#     def setUp(self):
#         pass

#     def test_directory(self):
#         """
#         Test that ``MEDIA_ROOT`` plus ``DIRECTORY`` exists.
#         """
#         self.assertEqual(os.path.exists(os.path.join(settings.MEDIA_ROOT, DIRECTORY)), 1)
#         # Check for trailing slash
#         self.assertEqual(os.path.basename(DIRECTORY), '')

#     def test_normalize_filename(self):
#         """
#         Test if ``NORMALIZE_FILENAME`` is in ``True, False``.
#         """
#         self.assertIn(NORMALIZE_FILENAME, [True, False])

#     def test_convert_filename(self):
#         """
#         Test if ``CONVERT_FILENAME`` is in ``True, False``.
#         """
#         self.assertIn(CONVERT_FILENAME, [True, False])

#     def test_default_sorting_by(self):
#         """
#         Test if ``DEFAULT_SORTING_BY`` is in ``date, filesize, filename_lower, filetype_checked``.
#         """
#         self.assertIn(DEFAULT_SORTING_BY, ['date', 'filesize', 'filename_lower', 'filetype_checked'])

#     def test_default_sorting_order(self):
#         """
#         Test if ``DEFAULT_SORTING_ORDER`` is in ``asc, desc``.
#         """
#         self.assertIn(DEFAULT_SORTING_ORDER, ['asc', 'desc'])

#     def test_search_traverse(self):
#         """
#         Test if ``SEARCH_TRAVERSE`` is in ``True, False``.
#         """
#         self.assertIn(SEARCH_TRAVERSE, [True, False])

#     def test_overwrite_existing(self):
#         """
#         Test if ``OVERWRITE_EXISTING`` is in ``True, False``.
#         """
#         self.assertIn(OVERWRITE_EXISTING, [True, False])
