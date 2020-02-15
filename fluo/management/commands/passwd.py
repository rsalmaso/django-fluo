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

# Original code taken from django-extensions
# Copyright (c) 2007 Michael Trier

import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

User = get_user_model()


class Command(BaseCommand):
    help = "Change a user password."
    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument("username", help="user username or email")
        parser.add_argument("password", nargs="?", default="", help="new password")

    def handle(self, *args, **options):
        username = options.get("username")

        try:
            user = User.objects.get(Q(username__iexact=username)|Q(email__iexact=username))
        except User.DoesNotExist:
            raise CommandError("user %s does not exist" % username)

        print("Changing password for user %s" % user.username)
        password = options.get("password")

        p1 = p2 = password

        while "" in (p1, p2) or p1 != p2:
            p1 = getpass.getpass()
            p2 = getpass.getpass("Password (again): ")
            if p1 != p2:
                print("Passwords do not match, try again")
            elif "" in (p1, p2):
                raise CommandError("aborted")

        user.set_password(p1)
        user.save()

        return "Password changed successfully for user %s\n" % user.username
