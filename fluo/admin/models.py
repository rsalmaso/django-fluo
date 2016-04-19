# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
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

from __future__ import absolute_import, division, print_function, unicode_literals
import operator
from functools import update_wrapper
from django.apps import apps
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.six.moves import reduce
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.utils.text import get_text_list
from django.utils import six
from django.contrib import admin
from ..db import models
from ..forms import ForeignKeySearchInput
from ..shortcuts import reverse

__all__ = [
    'ModelAdmin',
    'OrderedModelAdmin',
    'TreeOrderedModelAdmin',
    'CategoryModelAdmin',
    'StackedInline',
    'TabularInline',
    'ReadOnlyMixin',
    'ReadOnlyModelAdmin',
    'ReadOnlyInlineMixin',
    'ReadOnlyStackedInline',
    'ReadOnlyTabularInline',
]

# begin admin customization
# set this field for all models
admin.ModelAdmin.save_on_top = True
admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS.update({
    models.OrderField: {'required': False},
})
# end admin customization


class AutocompleteMixin(object):
    """Admin class for models using the autocomplete feature.

    There are two additional fields:
       - related_search_fields: defines fields of managed model that
         have to be represented by autocomplete input, together with
         a list of target model fields that are searched for
         input string, e.g.:

         related_search_fields = {
            'author': ('first_name', 'email'),
         }

       - related_string_functions: contains optional functions which
         take target model instance as only argument and return string
         representation. By default __unicode__() method of target
         object is used.
    """
    class Media:
        js = [
            'admin/js/jquery.min.js',
        ]
        css = {
            'all': ['fluo/jquery-autocomplete/jquery.autocomplete.css'],
        }

    related_search_fields = {}
    related_string_functions = {}
    autocomplete_limit = getattr(settings, 'FOREIGNKEY_AUTOCOMPLETE_LIMIT', None)

    def get_help_text(self, field_name, model_name):
        searchable_fields = self.related_search_fields.get(field_name, None)
        if searchable_fields:
            help_kwargs = {
                'model_name': model_name,
                'field_list': get_text_list(searchable_fields, _('and')),
            }
            return _('Use the left field to do %(model_name)s lookups in the fields %(field_list)s.') % help_kwargs
        return ''

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.related_search_fields:
            model_name = db_field.rel.to._meta.object_name
            help_text = self.get_help_text(db_field.name, model_name)
            if kwargs.get('help_text'):
                help_text = '{} {}'.format(kwargs['help_text'], help_text)
            kwargs['widget'] = ForeignKeySearchInput(db_field.rel, self.related_search_fields[db_field.name])
            kwargs['help_text'] = help_text
        return super(AutocompleteMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ModelAdmin(AutocompleteMixin, admin.ModelAdmin):
    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            url(r'autocomplete/$', wrap(self.autocomplete_view), name='%s_%s_autocomplete' % info),
        ] + super(AutocompleteMixin, self).get_urls()

    def autocomplete_view(self, request):
        """
        Searches in the fields of the given related model and returns the
        result as a simple string to be used by the jQuery Autocomplete plugin
        """
        query = request.GET.get('q', None)
        app_label = request.GET.get('app_label', None)
        model_name = request.GET.get('model_name', None)
        search_fields = request.GET.get('search_fields', None)
        object_pk = request.GET.get('object_pk', None)

        try:
            to_string_function = self.related_string_functions[model_name]
        except KeyError:
            to_string_function = lambda x: six.text_type(x)

        if search_fields and app_label and model_name and (query or object_pk):

            def construct_search(field_name):
                # use different lookup methods depending on the notation
                if field_name.startswith('^'):
                    fmt, name = "{}__istartswith", field_name[1:]
                elif field_name.startswith('='):
                    fmt, name = "{}__iexact", field_name[1:]
                elif field_name.startswith('@'):
                    fmt, name = "{}__search", field_name[1:]
                else:
                    fmt, name = "{}__icontains", field_name
                return fmt.format(name)

            model = apps.get_model(app_label, model_name)
            queryset = model._default_manager.all()
            data = ''
            if query:
                for bit in query.split():
                    or_queries = [
                        models.Q(**{construct_search(smart_str(field_name)): smart_str(bit)})
                        for field_name
                        in search_fields.split(',')
                    ]
                    other_qs = QuerySet(model)
                    other_qs.query.select_related = queryset.query.select_related
                    other_qs = other_qs.filter(reduce(operator.or_, or_queries))
                    queryset = queryset & other_qs

                if self.autocomplete_limit:
                    queryset = queryset[:self.autocomplete_limit]

                data = ''.join([
                    '{}|{}\n'.format(to_string_function(f), f.pk)
                    for f
                    in queryset
                ])
            elif object_pk:
                try:
                    obj = queryset.get(pk=object_pk)
                except:
                    pass
                else:
                    data = to_string_function(obj)
            return HttpResponse(data)
        return HttpResponseNotFound()


class StackedInline(AutocompleteMixin, admin.StackedInline):
    pass


class TabularInline(AutocompleteMixin, admin.TabularInline):
    pass


class OrderedModelAdmin(ModelAdmin):
    ordering = ['ordering']

    def get_queryset(self, request):
        return super(OrderedModelAdmin, self).get_queryset(request).order_by('ordering')

    def get_urls(self):
        from django.conf.urls import url

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            url(r'^(?P<id>\d+)/up/$', self.admin_site.admin_view(self.up), name='%s_%s_up' % info),
            url(r'^(?P<id>\d+)/down/$', self.admin_site.admin_view(self.down), name='%s_%s_down' % info),
        ] + super(OrderedModelAdmin, self).get_urls()

    def up(self, request, id):
        node = self.model._default_manager.get(pk=id)
        node.up()
        try:
            redirect_to = request.META['HTTP_REFERER']
        except:
            redirect_to = '../../'
        return HttpResponseRedirect(redirect_to)

    def down(self, request, id):
        node = self.model._default_manager.get(pk=id)
        node.down()
        try:
            redirect_to = request.META['HTTP_REFERER']
        except:
            redirect_to = '../../'
        return HttpResponseRedirect(redirect_to)

    def move_actions(self, node):
        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.model_name
        data = []
        if not node.is_first(): # up node
            data.append(u'<a href="%s" class="nodes-up">%s</a>' % (
                reverse('%sadmin_%s_%s_up' % info, node.id), _('up'),
            ))
        if not node.is_last() and not node.is_first():
            data.append(u'<span style="font-weight:normal"> | </span>')
        if not node.is_last(): # down node
            data.append(u'<a href="%s" class="nodes-down">%s</a>' % (
                reverse('%sadmin_%s_%s_down' % info, node.id), _('down'),
            ))
        return u''.join(data)
    move_actions.short_description = _('move')
    move_actions.allow_tags = True


class TreeOrderedModelAdmin(OrderedModelAdmin):
    def get_queryset(self, request):
        return super(TreeOrderedModelAdmin, self).get_queryset(request).filter(parent__isnull=True)


class CategoryModelAdmin(OrderedModelAdmin):
    search_fields = ['status', 'name']
    ordering = ['ordering', 'name']
    fieldsets = [
        (_('visualization admin'), {'fields': ('ordering',), 'classes': ('collapse',)}),
        (_('general admin'), {'fields': ('status', 'default')}),
        (None, {"fields": ("name",)}),
    ]


class ReadOnlyMixin(object):
    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(ReadOnlyMixin, self).has_change_permission(request, obj)

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
