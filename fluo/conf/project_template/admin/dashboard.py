# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from fluent_dashboard.dashboard import FluentIndexDashboard, FluentAppIndexDashboard
from fluent_dashboard.appgroups import get_application_groups, get_class

class CustomIndexDashboard(FluentIndexDashboard):
    def __init__(self, **kwargs):
        super(FluentIndexDashboard, self).__init__(**kwargs)
        self.children.extend(self.get_application_modules())

    """
    Custom index dashboard for project.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 10))

class CustomAppIndexDashboard(FluentAppIndexDashboard):
    """
    Custom app index dashboard for project.
    """

    # we disable title because its redundant with the model list module
    title = ''

    class Media:
        css = ("fluent_dashboard/dashboard.css",)

    def __init__(self, app_title, models, **kwargs):
        super(FluentAppIndexDashboard, self).__init__(app_title, models, **kwargs)
        self.children.extend(self.get_application_modules())
        self.children.append(self.get_recent_actions_module())

    def get_application_modules(self):
        """
        Instantiate all application modules (i.e.
         :class:`~admin_tools.dashboard.modules.AppList`,
         :class:`~fluent_dashboard.modules.AppIconList` and
         :class:`~fluent_dashboard.modules.CmsAppIconList`)
         for use in the dashboard.
        """
        modules = []
        appgroups = get_application_groups()
        for title, kwargs in appgroups:
            AppListClass = get_class(kwargs.pop('module'))  #e.g. CmsAppIconlist, AppIconlist, Applist
            modules.append(AppListClass(title, **kwargs))
        return modules

