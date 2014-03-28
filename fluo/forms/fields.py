# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
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

from __future__ import absolute_import, division, print_function, unicode_literals
from operator import add, mul
from django import forms
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from fluo.forms.widgets import GroupedSelect, DurationWidget

__all__ = (
    'OrderField',
    'TextField',
    'GroupedChoiceField',
    'DurationField',
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
        value = smart_text(value)
        if value == u'':
            return value
        valid_values = []
        for group_label, group in self.choices:
            valid_values += [str(k) for k, v in group]
        if value not in valid_values:
            raise ValidationError(ugettext(u'Select a valid choice. That choice is not one of the available choices.'))
        return value

class DurationField(forms.MultiValueField):
    """Input accurate timing. Interface with models.DurationField."""

    LABELS  = [_('Hours'), _('Minutes'), _('Seconds'), _('Milliseconds')]
    SECONDS = [ 60*60, 60, 1, 0.001]

    def __init__(self, milliseconds=True, *args, **kwargs):
        if not milliseconds:
            self.LABELS = self.LABELS[:3]
            self.SECONDS = self.SECONDS[:3]
        self.widget = DurationWidget(milliseconds=milliseconds)
        fields = [ forms.CharField(label=label) for label in self.LABELS ]
        super(DurationField, self).__init__(fields, *args, **kwargs)

    def compress(self, value):
        if value:
            return str(reduce(add, map(lambda x: mul(*x), zip(map(float, value), self.SECONDS))))
        return None
