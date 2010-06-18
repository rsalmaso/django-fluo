# -*- coding: utf-8 -*-

import os

PROJECT_PATH, _ = os.path.split(os.path.realpath(__file__))
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_PATH, '{{ project_name }}.db'),
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        # force to use InnoDB storage engine, only for mysql
        'OPTIONS': {"init_command": "SET storage_engine=INNODB"},
    }
}
DEBUG = True

