# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013, Raffaele Salmaso <raffaele@salmaso.org>
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

from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from fluo.shortcuts import reverse
from fluo import models
from fluo.admin import widgets

# begin admin customization
# set this field for all models
admin.ModelAdmin.save_on_top = True
admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS.update({
    models.ImageField:   {'widget': widgets.AdminImageFileWidget},
    models.OrderField:   {'required': False},
})
# end admin customization

class OrderedModelAdmin(admin.ModelAdmin):
    ordering = ('ordering',)
    def queryset(self, request):
        return super(OrderedModelAdmin, self).queryset(request).order_by('ordering')
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        info = self.model._meta.app_label, self.model._meta.module_name

        return patterns('',
            url(r'^(?P<id>\d+)/up/$', self.admin_site.admin_view(self.up), name='%s_%s_up' % info),
            url(r'^(?P<id>\d+)/down/$', self.admin_site.admin_view(self.down), name='%s_%s_down' % info),
        ) + super(OrderedModelAdmin, self).get_urls()
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
        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.module_name
        args = [node.id]
        data = []
        if not node.is_first(): # up node
            data.append(u'<a href="%s" class="nodes-up">%s</a>' % (reverse('%sadmin_%s_%s_up' % info, node.id), _('up')))
        if not node.is_last() and not node.is_first():
            data.append(u'<span style="font-weight:normal"> | </span>')
        if not node.is_last(): # down node
            data.append(u'<a href="%s" class="nodes-down">%s</a>' % (reverse('%sadmin_%s_%s_down' % info, node.id), _('down')))
        return u''.join(data)
    move_actions.short_description = _('move')
    move_actions.allow_tags = True

class TreeOrderedModelAdmin(OrderedModelAdmin):
    def queryset(self, request):
        return super(TreeOrderedModelAdmin, self).queryset(request).filter(parent__isnull=True)

class CategoryModelAdmin(OrderedModelAdmin):
    search_fields = ('status', 'name',)
    ordering = ('ordering', 'name',)
    fieldsets = (
        (_('visualization admin'), {'fields': ('ordering',), 'classes': ('collapse',),}),
        (_('general admin'), {'fields': ('status', 'default'),}),
        (None, {"fields": ("name",),}),
    )

