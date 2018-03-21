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

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.utils.translation import gettext_lazy as _


class FluoConfig(AppConfig):
    name = "fluo"
    verbose_name = _("Fluo")


class FluoAdminConfig(AdminConfig):
    default_site = "fluo.admin.sites.AdminSite"

    def ready(self):
        try:
            from django.contrib.admin.sites import DefaultAdminSite  # noqa
        except ImportError:
            self.override_admin_site()
        super().ready()

    def override_admin_site(self):
        from django.contrib import admin as django_admin
        from django.contrib.admin import sites as django_sites
        from fluo import admin as fluo_admin
        from fluo.admin.sites import DefaultAdminSite

        site = DefaultAdminSite()

        setattr(django_admin, "site", site)
        setattr(django_sites, "site", site)
        setattr(django_sites, "DefaultAdminSite", DefaultAdminSite)
        setattr(fluo_admin, "site", site)
