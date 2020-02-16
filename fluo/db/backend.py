# Copyright (C) 2007-2020, Raffaele Salmaso <raffaele@salmaso.org>
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

import os
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _

__all__ = [
    "get_backend",
    "Backend",
    "ImproperlyConfigured",
    "ConnectionError",
    "CreateDBError",
    "DropDBError",
]


class ConnectionError(Exception):
    pass


class CreateDBError(Exception):
    pass


class DropDBError(Exception):
    pass


class Backend:
    def __init__(self, options):
        self.host = options.get("host")
        self.port = options.get("port")
        self.password = options.get("password")
        self.name = options.get("name")
        self.user = options.get("user")
        self.engine = options.get("user")
        self.options = options

    def do_createdb(self):
        raise ImproperlyConfigured(
            "%s.%s.do_createdb is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )

    def do_dropdb(self):
        raise ImproperlyConfigured(
            "%s.%s.do_dropdb is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )

    def connect(self):
        raise ImproperlyConfigured(
            "%s.%s.connect is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )

    def close(self):
        raise ImproperlyConfigured(
            "%s.%s.close is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )

    def createdb(self):
        raise ImproperlyConfigured(
            "%s.%s.createdb is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )

    def dropdb(self):
        raise ImproperlyConfigured(
            "%s.%s.dropdb is not implemented." % (self.__class__.__module__, self.__class__.__name__)
        )


class BackendWrapper:
    def __init__(self, database):
        engine = database["ENGINE"].split(".")[-1]
        self.options = {
            "host": database["HOST"],
            "port": database["PORT"],
            "password": database["PASSWORD"],
            "name": database["NAME"],
            "user": database["USER"],
            "engine": engine,
        }
        self.backend = self._get_backend(self.options)

    def connect(self):
        return self.backend.connect()

    def close(self):
        return self.backend.close()

    def createdb(self):
        try:
            print(_("Creating database %(name)s...") % self.options)
            self.backend.createdb()
            print(_("done"))
        except Exception as e:
            raise CreateDBError(_("Cannot create db: %s") % e)

    def dropdb(self):
        try:
            print(_("Dropping database %(name)s...") % self.options)
            self.backend.dropdb()
            print(_("done"))
        except Exception as e:
            raise DropDBError(_("Cannot drop db: %s") % e)

    def _get_backend(self, options):
        engine = options["engine"]
        try:
            module = import_module("fluo.db.backends.%s" % engine)
        except ImportError:
            try:
                module = import_module(".db_commands", engine)
            except ImportError as e_user:
                # The database backend wasn't found. Display a helpful error message
                # listing all possible (built-in) database backends.
                backend_dir = os.path.join(__path__[0], "backends")  # NOQA
                try:
                    available_backends = [
                        f
                        for f in os.listdir(backend_dir)
                        if os.path.isdir(os.path.join(backend_dir, f)) and not f.startswith(".")
                    ]
                except EnvironmentError:
                    available_backends = []
                available_backends.sort()
                if engine not in available_backends:
                    error_msg = "%r isn't an available database backend. Available options are: %s\nError was: %s" % (
                        engine,
                        ", ".join(map(repr, available_backends)),
                        e_user,
                    )
                    raise ImproperlyConfigured(error_msg)
                else:
                    raise  # If there's some other error, this must be an error in Django itself.
        try:
            return module.Backend(options)
        except Exception as e:
            print(e)
            raise Backend.ConnectionError("Cannot connect to database %(name)s" % options)


def get_backend(database):
    return BackendWrapper(database)
