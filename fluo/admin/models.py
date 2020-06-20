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

# Copyright (C) 2007 Michael Trier
# Autocomplete feature taken from django-extensions

import operator
from functools import reduce, update_wrapper

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import smart_str
from django.utils.text import get_text_list
from django.utils.translation import gettext_lazy as _

from ..db import models
from .nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

__all__ = [
    "ModelAdmin",
    "OrderedModelAdmin",
    "TreeOrderedModelAdmin",
    "CategoryModelAdmin",
    "StackedInline",
    "TabularInline",
    "ReadOnlyMixin",
    "ReadOnlyModelAdmin",
    "ReadOnlyInlineMixin",
    "ReadOnlyStackedInline",
    "ReadOnlyTabularInline",
]

# begin admin customization
# set this field for all models
admin.ModelAdmin.save_on_top = True
admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS[models.OrderField] = {"required": False}
for field in [
    "StringField",
    "CIStringField",
    "URLField",
    "CIURLField",
    "SlugField",
    "CISlugField",
    "EmailField",
    "CIEmailField",
]:
    if hasattr(models, field):
        admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS[getattr(models, field)] = {
            "widget": admin.widgets.AdminTextInputWidget
        }
# end admin customization


class ModelAdmin(NestedModelAdmin):
    pass

class StackedInline(NestedStackedInline):
    pass


class TabularInline(NestedTabularInline):
    pass


class OrderedModelAdmin(ModelAdmin):
    ordering = ["ordering"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("ordering")


class TreeOrderedModelAdmin(OrderedModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)


class CategoryModelAdmin(OrderedModelAdmin):
    search_fields = ["status", "name"]
    ordering = ["ordering", "name"]
    fieldsets = [
        (_("visualization admin"), {"fields": ["ordering"], "classes": ["collapse"]}),
        (_("general admin"), {"fields": ["status", "default"]}),
        (None, {"fields": ["name"]}),
    ]


class ReadOnlyMixin:
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ("GET", "HEAD"):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyModelAdmin(ReadOnlyMixin, admin.ModelAdmin):
    actions = None


class ReadOnlyInlineMixin(ReadOnlyMixin):
    can_delete = False
    extra = 0


class ReadOnlyStackedInline(ReadOnlyInlineMixin, StackedInline):
    pass


class ReadOnlyTabularInline(ReadOnlyInlineMixin, TabularInline):
    pass
