# -*- coding: utf-8 -*-

import os

PROJECT_PATH, _ = os.path.split(os.path.realpath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DEBUG = True

############
# DATABASE #
############

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
        #'OPTIONS': {"init_command": "SET storage_engine=INNODB"},
    }
}

#########
# CACHE #
#########

#CACHES = {
    ## dummy backend
    #'default': {
        #'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'LOCATION': '',
    #},
    ## filesystem based
    #'default': {
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': base_rel('tmp'),
    #},
    ## memory based
    #'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': '',
    #},
#}
#CACHE_MIDDLEWARE_KEY_PREFIX = ''
#CACHE_MIDDLEWARE_SECONDS = 600
#CACHE_MIDDLEWARE_ALIAS = 'default'

#########
# EMAIL #
#########

#DEFAULT_FROM_EMAIL = 'webmaster@localhost'
#EMAIL_SUBJECT_PREFIX = '[Django] '
#SERVER_EMAIL = 'root@localhost'

# custom smtp account
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 25
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = False

# use gmail account
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True

# custom email backend
#if DEBUG:
    # Don't really send email, but print on console
    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#else:
    #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

