# Copyright (C) 2007-2022, Raffaele Salmaso <raffaele@salmaso.org>
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

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Set some data useful for local development."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--username",
            "-u",
            action="store",
            dest="username",
            default="admin",
            help="Use username as admin user.",
        )
        parser.add_argument(
            "--password",
            "-p",
            action="store",
            dest="password",
            default="admin",
            help='New password for "admin" user.',
        )
        parser.add_argument(
            "--site",
            "-s",
            action="store",
            dest="site",
            default="1",
            help="Update this SITE_ID domain/name.",
        )
        parser.add_argument(
            "--domain",
            "-d",
            action="store",
            dest="domain",
            default="localhost:8000",
            help="Use this domain/name for SITE_ID.",
        )

    def handle(self, **options):
        user = User.objects.get(username=options.get("username"))
        user.set_password(options.get("password"))
        user.save()

        site = Site.objects.get(pk=options.get("site"))
        domain = options.get("domain")
        site.domain = domain
        site.name = domain
        site.save()
