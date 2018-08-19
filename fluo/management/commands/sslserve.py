
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

import os
import socket
import ssl
from datetime import datetime

from django.core.management.base import CommandError
from django.core.servers.basehttp import WSGIRequestHandler, WSGIServer
from django.utils.functional import cached_property
from django.utils.translation import gettext, gettext_lazy as _

from .serve import Command as BaseCommand


class SecureWSGIServer(WSGIServer):
    def __init__(self, address, handler_cls, cert_file, key_file, *args, **kwargs):
        super().__init__(address, handler_cls, *args, **kwargs)
        self.socket = ssl.wrap_socket(
            self.socket,
            certfile=cert_file,
            keyfile=key_file,
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            cert_reqs=ssl.CERT_NONE,
        )


class SecureWSGIRequestHandler(WSGIRequestHandler):
    def get_environ(self):
        env = super().get_environ()
        env['HTTPS'] = 'on'
        return env


def default_ssl_files_dir():
    import fluo
    return os.path.join(os.path.dirname(fluo.__file__), "certs")


class Command(BaseCommand):
    help = "Run a Django development server over HTTPS"
    server_cls = SecureWSGIServer
    handler_cls = SecureWSGIRequestHandler

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--certificate",
            action="store",
            default=self.get_cert_file(),
            dest="cert_file",
            help=gettext("Path to the certificate"),
        )
        parser.add_argument(
            "--key",
            action="store",
            default=self.get_key_file(),
            dest="key_file",
            help=gettext("Path to the key file"),
        )

    @cached_property
    def cert_file(self):
        return self.options.get("cert_file", self.get_cert_file())

    @cached_property
    def key_file(self):
        return self.options.get("key_file", self.get_key_file())

    def get_cert_file(self):
        return os.environ.get('DJANGO_CERT_FILE', os.path.join(default_ssl_files_dir(), "development.crt"))

    def get_key_file(self):
        return os.environ.get('DJANGO_KEY_FILE', os.path.join(default_ssl_files_dir(), "development.key"))

    def get_protocol(self):
        return "https"

    def check_certs(self, *, key_file, cert_file):
        cert_file_doesnt_exists, key_file_doesnt_exists = not os.path.exists(cert_file), not os.path.exists(key_file)

        if cert_file_doesnt_exists and key_file_doesnt_exists:
            msg = gettext("Can't find key '%(key_file)s' and certificates '%(cert_file)s'")
        elif cert_file_doesnt_exists:
            msg = gettext("Can't find certificate '%(cert_file)s'")
        elif key_file_doesnt_exists:
            msg = gettext("Can't find key '%(key_file)s'")
        else:
            msg = ""

        if msg:
            raise CommandError(msg % {"key_file": key_file, "cert_file": cert_file})

    def handle(self, *args, **options):
        self.options = options
        self.check_certs(key_file=self.key_file, cert_file=self.cert_file)
        return super().handle(*args, **options)

    def get_extra_messages(self, *args, **options):
        return [
            "Using SSL certificate: %(cert_file)s",
            "Using SSL key: %(key_file)s",
        ], self.get_extra_params(*args, **options)

    def get_extra_params(self, *args, **options):
        return {
            "key_file": self.key_file,
            "cert_file": self.cert_file,
        }
