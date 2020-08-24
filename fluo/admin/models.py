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

from functools import update_wrapper

from django.contrib import admin
from django.forms.widgets import SelectMultiple
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from ..db import models
from .nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from .views import RelatedSearchJsonView
from .widgets import RelatedSearchSelect, RelatedSearchSelectMultiple

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
            "widget": admin.widgets.AdminTextInputWidget,
        }
# end admin customization


class RelatedSearchMixin:
    related_search_fields = {}

    def get_related_search_fields(self, request):
        """
        Return a list of ForeignKey and/or ManyToMany fields which should use
        an related_search widget.
        """
        return self.related_search_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if "widget" not in kwargs:
            if db_field.name in self.get_related_search_fields(request):
                kwargs["widget"] = RelatedSearchSelect(db_field, self.admin_site, using=kwargs.get("using"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Get a form Field for a ManyToManyField.
        """
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.
        if not db_field.remote_field.through._meta.auto_created:
            return None

        if "widget" not in kwargs:
            # autocomplete_fields = self.get_autocomplete_fields(request)
            # if db_field.name in autocomplete_fields:
            if db_field.name in self.get_related_search_fields(request):
                kwargs["widget"] = RelatedSearchSelectMultiple(
                    db_field,
                    self.admin_site,
                    db=kwargs.get("using"),
                )
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if isinstance(form_field.widget, SelectMultiple) and not isinstance(
            form_field.widget,
            RelatedSearchSelectMultiple,
        ):
            msg = _("Hold down “Control”, or “Command” on a Mac, to select more than one.")
            help_text = form_field.help_text
            form_field.help_text = format_lazy("{} {}", help_text, msg) if help_text else msg
        return form_field

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path(
                "related_search/<path:field_name>/",
                wrap(self.related_search_view),
                name="%s_%s_related_search" % info,
            ),
        ] + super().get_urls()

    def related_search_view(self, request, field_name):
        related_field = self.model._meta.get_field(field_name)
        related_model = related_field.remote_field.model
        model_admin = self.admin_site._registry[related_model]
        search_fields = self.get_related_search_fields(request)[field_name]
        if not search_fields and model_admin is not None:
            search_fields = model_admin.get_search_fields(request)
        return RelatedSearchJsonView.as_view(model_admin=model_admin, search_fields=search_fields)(
            request,
            related_field.name,
        )


class ModelAdmin(RelatedSearchMixin, NestedModelAdmin):
    pass


class StackedInline(RelatedSearchMixin, NestedStackedInline):
    pass


class TabularInline(RelatedSearchMixin, NestedTabularInline):
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
