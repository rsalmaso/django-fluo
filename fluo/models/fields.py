# -*- coding: utf-8 -*-

# Copyright (C) 2007-2009, Salmaso Raffaele <raffaele@salmaso.org>
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

# Original code for CreationDateTimeField and ModificationDateTimeField
# taken from django-extensions
# Copyright (c) 2007 Michael Trier

import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from fluo import forms

__all__ = (
    'StatusField', 'STATUS_CHOICES',
    'CreationDateTimeField', 'ModificationDateTimeField',
    'OrderField',
)

STATUS_CHOICES = (
    ('active', _('Active')),
    ('inactive', _('Inactive')),
)

class StatusField(models.CharField):
    def __init__(self,
                 choices=STATUS_CHOICES,
                 max_length=10,
                 default='active',
                 verbose_name=_('status'),
                 help_text=_('Is active?')):
        super(StatusField, self).__init__(
            choices=choices,
            max_length=max_length,
            default=default,
            verbose_name=verbose_name,
            help_text=help_text
        )

class CreationDateTimeField(models.DateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', datetime.datetime.now)
        super(CreationDateTimeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

class ModificationDateTimeField(CreationDateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now

    Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = datetime.datetime.now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"

class OrderField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0
        models.Field.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.OrderField}
        defaults.update(kwargs)
        return super(OrderField, self).formfield(**defaults)

