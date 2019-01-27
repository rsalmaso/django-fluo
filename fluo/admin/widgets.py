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

from django import forms
from django.conf import settings
from django.contrib.admin.sites import site
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import Truncator, slugify
from django.utils.translation import gettext as _
from fluo.urls import reverse

__all__ = [
    'AdminImageFileWidget',
    'ForeignKeySearchInput',
]


class AdminImageFileWidget(forms.FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('''
<div>
    <div style="float: left; vertical-align: middle;">
        <a target="_blank" href="%(url)s"><img src="%(url)s" width="40px"/></a>
    </div>
    <div style="padding-left: 20px; float: left; vertical-align: middle;">
        %(text)s <a target="_blank" href="%(url)s">%(value)s</a>
        <br />
        %(change)s ''' % {
                'text': _('Currently:'),
                'url': value.url,
                'value': value,
                'change': _('Change:'),
            })
        output.append(super().render(name, value, attrs))
        output.append('</div>')
        if value and hasattr(value, "url"):
            output.append('</div>')
        return mark_safe(''.join(output))


class ForeignKeySearchInput(ForeignKeyRawIdWidget):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input
    instead in a <select> box.
    """
    # Set in subclass to render the widget with a different template
    widget_template = None
    # Set this to the patch of the search view
    search_path = '../foreignkey_autocomplete/'

    def _media(self):
        js_files = [
            'fluo/jquery-ajaxqueue/jquery.ajaxqueue.min.js',
            'fluo/jquery-autocomplete/jquery.autocomplete.min.js',
        ]
        return forms.Media(
            css={'all': ('fluo/jquery-autocomplete/jquery.autocomplete.css',)},
            js=js_files,
        )

    media = property(_media)

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.get(**{key: value})  # django <= 1.11
        except Exception:  # FIXME!!!
            obj = self.rel.remote_field._default_manager.get(**{key: value})  # django >= 2
        return Truncator(obj).words(14, truncate='...')

    def __init__(self, rel, search_fields, attrs=None):
        self.search_fields = search_fields
        super().__init__(rel, site, attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        # output = [super().render(name, value, attrs)]
        try:
            opts = self.rel.remote_field.model._meta  # django >= 2
        except Exception:  # FIXME!!!
            opts = self.rel.to.model._meta  # django <= 1.11
        app_label = opts.app_label
        model_name = opts.object_name.lower()
        related_url = reverse('admin:{}_{}_changelist'.format(app_label, model_name))
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if 'class' not in attrs:
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        # Call the TextInput render method directly to have more control
        output = [forms.TextInput.render(self, name, value, attrs)]
        label = self.label_for_value(value) if value else ''

        admin_media_prefix = settings.STATIC_URL + "admin/"

        context = {
            'url': url,
            'related_url': related_url,
            'admin_media_prefix': admin_media_prefix,
            'search_path': self.search_path,
            'search_fields': ','.join(self.search_fields),
            'model_name': model_name,
            'app_label': app_label,
            'label': label,
            'name': name,
            'slug': slugify(name).replace('-', '_'),
        }
        output.append(render_to_string(self.widget_template or (
            'fluo/widgets/%s/%s/foreignkey_searchinput.html' % (app_label, model_name),
            'fluo/widgets/%s/foreignkey_searchinput.html' % app_label,
            'fluo/widgets/foreignkey_searchinput.html',
        ), context))
        output.reverse()
        return mark_safe(''.join(output))
