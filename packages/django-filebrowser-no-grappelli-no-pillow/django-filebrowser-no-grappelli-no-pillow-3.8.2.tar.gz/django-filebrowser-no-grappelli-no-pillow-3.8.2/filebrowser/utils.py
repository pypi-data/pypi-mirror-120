# coding: utf-8

import re
import os
import unicodedata
import math

import six
from django.utils.module_loading import import_string

from filebrowser.settings import NORMALIZE_FILENAME, CONVERT_FILENAME


def convert_filename(value):
    """
    Convert Filename.
    """

    if NORMALIZE_FILENAME:
        chunks = value.split(os.extsep)
        normalized = []
        for v in chunks:
            v = unicodedata.normalize('NFKD', six.text_type(
                v)).encode('ascii', 'ignore').decode('ascii')
            v = re.sub(r'[^\w\s-]', '', v).strip()
            normalized.append(v)

        if len(normalized) > 1:
            value = '.'.join(normalized)
        else:
            value = normalized[0]

    if CONVERT_FILENAME:
        value = value.replace(" ", "_").lower()

    return value


def path_strip(path, root):
    if not path or not root:
        return path
    path = os.path.normcase(path)
    root = os.path.normcase(root)
    if path.startswith(root):
        return path[len(root):]
    return path
