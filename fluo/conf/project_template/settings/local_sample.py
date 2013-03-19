# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals
import os
from {{ project_name }}.settings.base import *

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
        'NAME': rel('{{ project_name }}.db'),
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
        # For MySQL force to use InnoDB storage engine
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
    #CACHES = {
        #'default': {
            #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            #'LOCATION': '127.0.0.1:11211',
            #'LOCATION': 'unix:/tmp/memcached.sock',
            #'LOCATION': [
                #'172.19.26.240:11211',
                #'172.19.26.242:11211',
            #],
        #},
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
# Don't really send email, but print on console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Send email to
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

