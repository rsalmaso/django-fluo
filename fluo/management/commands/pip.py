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

import subprocess
import sys

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "pip wrapper"
    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument("--install", "-i", action="store_true", default=True, dest="install", help="intall package")
        parser.add_argument("--upgrade", "-u", action="store_true", default=False, dest="upgrade", help="upgrade package")
        parser.add_argument("--uninstall", "-r", action="store_true", default=False, dest="uninstall", help="uninstall package")
        parser.add_argument("--verbose", action="store_true", default=False, dest="verbose", help="verbose")
        parser.add_argument("pkgs", metavar="pkgs", nargs="+", help="package(s)")

    def handle(self, *pkgs, **options):
        pkgs = pkgs or options.get("pkgs")

        if options.get("uninstall"):
            self.uninstall(pkgs, options)
        elif options.get("install") or options.get("upgrade"):
            self.install(pkgs, options)

    def install(self, pkgs, options):
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
        ]
        if options.get("upgrade"):
            cmd.append("--upgrade")
        if options.get("verbosity") > 1 or options.get("verbose"):
            cmd.append("--verbose")
        cmd.extend([
            "--target=%s" % settings.LIB_DIR,
        ])
        cmd.extend(pkgs)
        subprocess.call(cmd)

    def uninstall(self, pkgs, options):
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "uninstall",
        ]
        cmd.extend(pkgs)
        subprocess.call(cmd)
