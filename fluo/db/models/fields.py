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

# Original code for taken from django-extensions
# - CreationDateTimeField
# - ModificationDateTimeField
# - AutoSlugField
# - UUIDField

from __future__ import absolute_import, division, print_function, unicode_literals
import re
from django.core import validators
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
try:
    import uuid
except ImportError:
    from fluo.utils import uuid
from fluo import forms

__all__ = (
    'StatusField', 'STATUS_CHOICES',
    'CreationDateTimeField', 'ModificationDateTimeField',
    'OrderField',
    'AutoSlugField',
    'UUIDField',
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
                 blank=False,
                 null=False,
                 verbose_name=_('status'),
                 help_text=_('Is active?')):
        super(StatusField, self).__init__(
            choices=choices,
            max_length=max_length,
            default=default,
            blank=blank,
            null=null,
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
        kwargs.setdefault('default', timezone.now)
        super(CreationDateTimeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

class ModificationDateTimeField(CreationDateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now

    Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = timezone.now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"

class URIField(models.CharField):
    description = _("URL")

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 8196)
        models.CharField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(validators.URLValidator())

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        defaults = {
            'form_class': forms.URLField,
        }
        defaults.update(kwargs)
        return super(URIField, self).formfield(**defaults)

class AutoSlugField(models.SlugField):
    """
    By default, sets editable=False, blank=True.

    Required arguments:

    populate_from
        Specifies which field or list of fields the slug is populated from.

    Optional arguments:

    separator
        Defines the used separator (default: '-')

    overwrite
        If set to True, overwrites the slug on every save (default: False)

    Inspired by SmileyChris' Unique Slugify snippet:
    http://www.djangosnippets.org/snippets/690/
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        #kwargs.setdefault('editable', False)

        populate_from = kwargs.pop('populate_from', None)
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from
        self.separator = kwargs.pop('separator',  u'-')
        self.overwrite = kwargs.pop('overwrite', False)
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Cleans up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.

        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        re_sep = '(?:-|%s)' % re.escape(self.separator)
        value = re.sub('%s+' % re_sep, self.separator, value)
        return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

    def slugify_func(self, content):
        return slugify(content)

    def create_slug(self, model_instance, add):
        # get fields to populate from and slug field to set
        if not isinstance(self._populate_from, (list, tuple)):
            self._populate_from = (self._populate_from, )
        slug_field = model_instance._meta.get_field(self.attname)

        if add or self.overwrite:
            # slugify the original field content and set next step to 2
            slug_for_field = lambda field: self.slugify_func(getattr(model_instance, field))
            slug = self.separator.join(map(slug_for_field, self._populate_from))
            next = 2
        else:
            # get slug from the current model instance and calculate next
            # step from its number, clean-up
            slug = self._slug_strip(getattr(model_instance, self.attname))
            next = slug.split(self.separator)[-1]
            if next.isdigit():
                slug = self.separator.join(slug.split(self.separator)[:-1])
                next = int(next)
            else:
                next = 2

        # strip slug depending on max_length attribute of the slug field
        # and clean-up
        slug_len = slug_field.max_length
        if slug_len:
            slug = slug[:slug_len]
        slug = self._slug_strip(slug)
        original_slug = slug

        # exclude the current model instance from the queryset used in finding
        # the next valid slug
        queryset = model_instance.__class__._default_manager.all()
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # form a kwarg dict used to impliment any unique_together contraints
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)
        kwargs[self.attname] = slug

        # increases the number while searching for the next valid slug
        # depending on the given slug, clean-up
        while not slug or queryset.filter(**kwargs):
            slug = original_slug
            end = '%s%s' % (self.separator, next)
            end_len = len(end)
            if slug_len and len(slug)+end_len > slug_len:
                slug = slug[:slug_len-end_len]
                slug = self._slug_strip(slug)
            slug = '%s%s' % (slug, end)
            kwargs[self.attname] = slug
            next += 1
        return slug

    def pre_save(self, model_instance, add):
        value = unicode(self.create_slug(model_instance, add))
        setattr(model_instance, self.attname, value)
        return value

    def get_internal_type(self):
        return "SlugField"

class UUIDVersionError(Exception):
    pass

class UUIDField(models.CharField):
    """
    By default uses UUID version 1 (generate from host ID, sequence number and current time)

    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    """

    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 36
        if auto:
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto = auto
        self.version = version
        if version==1:
            self.node, self.clock_seq = node, clock_seq
        elif version==3 or version==5:
            self.namespace, self.name = namespace, name
        super(UUIDField, self).__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return models.CharField.__name__

    def create_uuid(self):
        if not self.version or self.version==4:
            return uuid.uuid4()
        elif self.version==1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version==2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version==3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version==5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError("UUID version %s is not valid." % self.version)

    def pre_save(self, model_instance, add):
        if self.auto and add:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(model_instance, add)
            if self.auto and not value:
                value = unicode(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value

class OrderField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0
        models.Field.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.OrderField}
        defaults.update(kwargs)
        return super(OrderField, self).formfield(**defaults)

from django.conf import settings
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    rules = [
        (
            (StatusField,),
            [],
            {
                "max_length": ["max_length", {"default": 10}],
                "default": ["default", {"default": "active"}],
            },
        ),
        (
            (CreationDateTimeField,),
            [],
            {
            },
        ),
        (
            (ModificationDateTimeField,),
            [],
            {
            },
        ),
        (
            (AutoSlugField,),
            [],
            {
            },
        ),
        (
            (UUIDField,),
            [],
            {
            },
        ),
        (
            (OrderField,),
            [],
            {
            },
        ),
    ]
    add_introspection_rules(rules, ["^fluo\.db\.models\.fields",])

