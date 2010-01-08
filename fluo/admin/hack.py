# -*- coding: utf-8 -*-

# Copyright (C) 2007-2010, Salmaso Raffaele <raffaele@salmaso.org>
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

def __init__():
    from django.conf import settings
    from django import VERSION
    from django.contrib import admin

    if VERSION < (1, 1):
        from django.core.urlresolvers import reverse
        admin.site.root_path = reverse('%sadmin_index' % admin.site.name)

    if 'django.contrib.auth' in settings.INSTALLED_APPS:
        from django.contrib.auth.models import User
        from django.contrib.auth.admin import UserAdmin

        admin.site.unregister(User)
        class FluoUserAdmin(UserAdmin):
            list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff',)
            filter_horizontal = ('user_permissions', 'groups',)
        admin.site.register(User, FluoUserAdmin)
__init__()

