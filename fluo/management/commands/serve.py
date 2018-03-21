# Copyright (C) 2007-2018, Raffaele Salmaso <raffaele@salmaso.org>
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

# Based on django/core/management/commands/runserver.py
# and django/contrib/staticfiles/management/commands/runserver.py which are
# Copyright (c) Django Software Foundation and individual contributors.

import errno
import os
import re
import socket
import socketserver
import sys
from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.runserver import Command as BaseCommand, naiveip_re
from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer
from django.utils import autoreload

use_static = apps.is_installed("django.contrib.staticfiles")


def run(addr, port, wsgi_handler, ipv6=False, threading=False, server_cls=WSGIServer):
    server_address = (addr, port)
    if threading:
        httpd_cls = type('WSGIServer', (socketserver.ThreadingMixIn, server_cls), {})
    else:
        httpd_cls = server_cls
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    if threading:
        # ThreadingMixIn.daemon_threads indicates how threads will behave on an
        # abrupt shutdown; like quitting the server by the user or restarting
        # by the auto-reloader. True means the server will not wait for thread
        # termination before it quits. This will make auto-reloader faster
        # and will prevent the need to kill the server manually if a thread
        # isn't terminating correctly.
        httpd.daemon_threads = True
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()


class Command(BaseCommand):
    server_cls = WSGIServer

    @property
    def default_port(self):
        return self.get_default_port()

    @property
    def default_addr(self):
        return self.get_default_addr()

    @property
    def default_addr_ipv6(self):
        return self.get_default_addr_ipv6()

    @property
    def protocol(self):
        return self.get_protocol()

    def get_default_port(self):
        return os.environ.get('DJANGO_DEFAULT_PORT', '8000')

    def get_default_addr(self):
        return os.environ.get('DJANGO_DEFAULT_ADDR', '127.0.0.1')

    def get_default_addr_ipv6(self):
        return os.environ.get('DJANGO_DEFAULT_ADDR6', '::1')

    def get_protocol(self):
        return os.environ.get('DJANGO_DEFAULT_PROTOCOL', 'http')

    def handle(self, *args, **options):
        # remove when dropping django <= 1.11

        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError('You must set settings.ALLOWED_HOSTS if DEBUG is False.')

        self.use_ipv6 = options['use_ipv6']
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError('Your Python does not support IPv6.')
        self._raw_ipv6 = False
        if not options['addrport']:
            self.addr = ''
            self.port = self.default_port
        else:
            m = re.match(naiveip_re, options['addrport'])
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % options['addrport'])
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)
        if not self.addr:
            self.addr = self.default_addr_ipv6 if self.use_ipv6 else self.default_addr
            self._raw_ipv6 = self.use_ipv6
        self.run(**options)

    def inner_run(self, *args, **options):
        # remove when dropping django <= 1.11

        # If an exception was silenced in ManagementUtility.execute in order
        # to be raised in the child process, raise it now.
        autoreload.raise_last_exception()

        threading = options['use_threading']
        # 'shutdown_message' is a stealth option.
        shutdown_message = options.get('shutdown_message', '')
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

        self.stdout.write("Performing system checks...\n\n")
        self.check(display_num_errors=True)
        # Need to check migrations here, so can't use the
        # requires_migrations_check attribute.
        self.check_migrations()
        now = datetime.now().strftime('%B %d, %Y - %X')
        self.stdout.write(now)
        self.stdout.write((
            "Django version %(version)s, using settings %(settings)r\n"
            "Starting development server at %(protocol)s://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            "version": self.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "protocol": self.protocol,
            "addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
            "port": self.port,
            "quit_command": quit_command,
        })

        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler,
                ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
        except socket.error as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = e
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)


if use_static:
    class Command(Command):
        help = "Starts a lightweight Web server for development and also serves static files."

        def add_arguments(self, parser):
            super().add_arguments(parser)
            parser.add_argument(
                '--nostatic', action="store_false", dest='use_static_handler', default=True,
                help='Tells Django to NOT automatically serve static files at STATIC_URL.',
            )
            parser.add_argument(
                '--insecure', action="store_true", dest='insecure_serving', default=False,
                help='Allows serving static files even if DEBUG is False.',
            )

        def get_handler(self, *args, **options):
            """
            Returns the static files serving handler wrapping the default handler,
            if static files should be served. Otherwise just returns the default
            handler.
            """
            from django.contrib.staticfiles.handlers import StaticFilesHandler
            handler = super().get_handler(*args, **options)
            use_static_handler = options['use_static_handler']
            insecure_serving = options['insecure_serving']
            if use_static_handler and (settings.DEBUG or insecure_serving):
                return StaticFilesHandler(handler)
            return handler
