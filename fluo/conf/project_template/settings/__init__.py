# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

if os.environ.get("DJANGO_SETTINGS_MODULE") == "{{ project_name }}.settings":
    try:
        from {{ project_name }}.settings.local import *
    except ImportError:
        from {{ project_name }}.settings.base import *
# else use the DJANGO_SETTINGS_MODULE one

