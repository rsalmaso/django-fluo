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

import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, close_old_connections, connections
from fluo.db.backend import get_backend


class DatabaseCommand(BaseCommand):
    output_transaction = True
    requires_system_checks = False

    message = """You have requested to drop "%(name)s" database.
This will IRREVERSIBLY DELETE all data currently in the "%(name)s" database.
Are you sure you want to do this?"""
    ask_message = """

    Type 'yes' to continue, or 'no' to cancel: """
    error_message = """Database %(name)s couldn't be dropped. Possible reasons:
  * The database isn't running or isn't configured correctly.
  * The database is in use by another user.
The full error: %(error)s"""
    default = "yes"
    should_ask = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            action="store_false",
            dest="interactive",
            default=True,
            help="Tells Django to NOT prompt the user for input of any kind.",
        )
        parser.add_argument(
            "--database",
            action="store",
            dest="database",
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database. Defaults to the "default" database.',
        )

    def handle(self, *args, **options):
        close_old_connections()

        db = options.get("database")
        connection = connections[db]
        interactive = options.get("interactive")
        settings = dict(connection.settings_dict)
        name = settings["NAME"]
        if interactive and self.should_ask:
            msg = "".join([self.message % {"name": name}, self.ask_message])
            confirm = input(msg)
        else:
            confirm = self.default

        if confirm == "yes":
            backend = get_backend(settings)
            backend.connect()
            try:
                self.execute_sql(backend, **options)
            except Exception as e:
                raise CommandError(CommandError(self.error_message % {"name": name, "error": e})).with_traceback(
                    sys.exc_info()[2]
                )
            finally:
                backend.close()

            self.post_execute(**options)

    def execute_sql(self, backend):
        raise NotImplementedError

    def post_execute(self, **options):
        pass
