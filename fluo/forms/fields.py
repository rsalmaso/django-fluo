# -*- coding: utf-8 -*-

# Copyright (C) 2007-2012, Raffaele Salmaso <raffaele@salmaso.org>
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
from django.utils.translation import ugettext
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_unicode
from fluo.forms.widgets import GroupedSelect

__all__ = (
    'OrderField',
    'TextField',
    'GroupedChoiceField',
)

try:
    # new from django-admin-ui branch
    from django.forms import OrderField
except ImportError:
    class OrderField(forms.IntegerField):
        pass

class TextField(forms.CharField):
    widget = forms.Textarea

# taken and adapted from http://djangosnippets.org/snippets/200/
class GroupedChoiceField(forms.ChoiceField):
    widget = GroupedSelect

    def __init__(self, choices=(), required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):
        super(GroupedChoiceField, self).__init__(
            #choices=choices,
            required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            *args, **kwargs)
        self.choices = choices

    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        value = super(GroupedChoiceField, self).clean(value)
        if value in (None, ''):
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(ugettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value

