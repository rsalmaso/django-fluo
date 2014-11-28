# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
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

from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings
from django.db.models.loading import get_model
from south.migration.base import Migrations
from south.exceptions import NoMigrations
from south.creator.freezer import freeze_apps


__all__ = [
    'get_user_model',
    'update_south_migration',
]


def get_user_model():
    model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    if model != 'auth.User':
        if get_model(*model.split('.'))._meta.proxy:
            model = 'auth.User'
    return model


def update_south_migration(model_):
    class Ns(object):
        pass
    Ns.model = model_

    def class_rebuilder(migration):
        migration_name = getattr(settings, 'INITIAL_CUSTOM_USER_MIGRATION', '0001_initial.py')
        if Ns.model != 'auth.User':
            app_name, model = Ns.model.split('.')
            try:
                migration_app = Migrations(app_name)
            except NoMigrations:
                extra_model = freeze_apps(app_name)
            else:
                initial = migration_app.migration(migration_name)
                extra_model = initial.migration_class().models
        else:
            extra_model = {}
        migration.models.update(extra_model)
        depends_on = (
            (app_name, migration_name),
        )
        if hasattr(migration, 'depends_on'):
            append = True
            for depend in migration.depends_on:
                if depend[0] == app_name and depend[1] == migration_name:
                    append = False
            if append:
                migration.depends_on += depends_on
        else:
            migration.depends_on = depends_on
        return migration
    return class_rebuilder
