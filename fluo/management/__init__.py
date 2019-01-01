# Copyright (C) 2007-2019, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Creates permissions for all installed apps that need permissions.
"""

import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS
from django.db.models import signals

from .. import settings

__all__ = ['DatabaseCommand']


log = logging.getLogger("fluo")


class DatabaseCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        )
        parser.add_argument(
            '--no-utf8',
            action='store_true',
            dest='no_utf8_support',
            default=False,
            help='Tells Django to not create a UTF-8 charset database',
        )
        parser.add_argument(
            '-U',
            '--user',
            action='store',
            dest='user',
            default=None,
            help='Use another user for the database then defined in settings.py',
        )
        parser.add_argument(
            '-P',
            '--password',
            action='store',
            dest='password',
            default=None,
            help='Use another password for the database then defined in settings.py',
        )
        parser.add_argument(
            '-D',
            '--dbname',
            action='store',
            dest='dbname',
            default=None,
            help='Use another database name then defined in settings.py (For PostgreSQL this defaults to "template1")',
        )
        parser.add_argument(
            '--database',
            action='store',
            dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to synchronize. Defaults to the "default" database.',
        )
        parser.add_argument(
            '-e',
            '--exclude',
            dest='exclude',
            action='append',
            default=[],
            help='App to exclude (use multiple --exclude to exclude multiple apps).',
        )
    requires_model_validation = False

    def handle(self, *args, **options):
        database = settings.DATABASES[options.get('database', DEFAULT_DB_ALIAS)]

        if options.get('interactive'):
            confirm = input("""
You have requested a database reset.
This will IRREVERSIBLY DESTROY
ALL data in the database "%s".
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """ % database['NAME'])
        else:
            confirm = 'yes'

        if confirm != 'yes':
            print("Reset cancelled.")
            return

        self.db_handle(database, args, options)

    def db_handle(self, database, args, options):
        pass


def _get_permission_codename(action, opts):
    return '%s_%s' % (action, opts.object_name.lower())


def _get_all_permissions(opts):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in settings.DEFAULT_PERMISSIONS:
        perms.append((_get_permission_codename(action, opts), 'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms + list(opts.permissions)


def create_permissions(app_config, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    for klass in app_config.get_models():
        ctype = ContentType.objects.get_for_model(klass)
        for codename, name in _get_all_permissions(klass._meta):
            p, created = Permission.objects.get_or_create(
                codename=codename,
                content_type__pk=ctype.id,
                defaults={'name': name, 'content_type': ctype},
            )
            if created and kwargs.get("verbosity", 0) >= 2:
                log.info("Adding permission '{}'".format(p))

signals.post_migrate.connect(create_permissions, dispatch_uid="fluo.management.create_permissions")
