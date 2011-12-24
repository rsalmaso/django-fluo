# -*- coding: utf-8 -*-

"""
WSGI config for {{ project_name }} project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os, sys

# PATH is the absolute path leading to parent directory
PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
LIB_DIR = os.path.join(PATH, 'lib')

for path in os.listdir(LIB_DIR):
    pkg = os.path.join(LIB_DIR, path)
    if os.path.isdir(pkg) and pkg not in sys.path:
        sys.path.insert(0, pkg)
if PATH not in sys.path:
    sys.path.insert(0, PATH)

try:
    from {{ project_name }}.local_pythonpath import *
except ImportError:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
