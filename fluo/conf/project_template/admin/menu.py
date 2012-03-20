# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from fluent_dashboard.menu import FluentMenu

class CustomMenu(FluentMenu):
    """
    Custom Menu for project admin site.
    """

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        super(CustomMenu, self).init_with_context(context)
        self.children.pop()

