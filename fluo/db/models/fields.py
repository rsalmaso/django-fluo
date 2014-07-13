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

# Original code for taken and adapted from
# - django-extensions
#   - CreationDateTimeField
#   - ModificationDateTimeField
#   - AutoSlugField
#   - UUIDField

# JSONField taken and adapted from https://github.com/bradjasper/django-jsonfield.git
# Copyright (c) 2012 Brad Jasper

from __future__ import absolute_import, division, print_function, unicode_literals
import base64
import copy
import re
import uuid
from django.core import exceptions, validators
from django.utils import timezone
from django.utils import six
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from fluo import forms
from fluo.utils import json
from .subclassing import SubfieldBase

__all__ = (
    'StatusField', 'STATUS_CHOICES',
    'CreationDateTimeField', 'ModificationDateTimeField',
    'OrderField',
    'AutoSlugField',
    'UUIDField',
    'DurationField',
    'JSONField',
    'Base64Field',
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

class DurationField(models.DecimalField):
    description = _('Duration field')

    def __init__(self, milliseconds=True, verbose_name=None, name=None, default=0, *args, **kwargs):
        self.milliseconds = milliseconds
        kwargs.setdefault('decimal_places', 3)
        kwargs.setdefault('max_digits', 12)
        super(DurationField, self).__init__(
            verbose_name=verbose_name,
            name=name,
            **kwargs
        )

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.DurationField,
            'milliseconds': self.milliseconds,
        }
        defaults.update(kwargs)
        # skip DecimalField.formfield
        # which injects decimal_places and max_digits
        return models.Field.formfield(self, **defaults)

class JSONField(six.with_metaclass(SubfieldBase, models.TextField)):
    description = _("JSON object")
    form_class = forms.JSONField
    empty_values = ()

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})
        super(JSONField, self).__init__(*args, **kwargs)

    def pre_init(self, value, obj):
        """
        Convert a string value to JSON only if it needs to be deserialized.

        SubfieldBase metaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized
        """

        if obj._state.adding:
            # Make sure the primary key actually exists on the object before
            # checking if it's empty. This is a special case for South datamigrations
            # see: https://github.com/bradjasper/django-jsonfield/issues/52
            if hasattr(obj, "pk") and obj.pk is not None:
                if isinstance(value, six.string_types):
                    try:
                        return json.loads(value, **self.load_kwargs)
                    except ValueError:
                        raise exceptions.ValidationError(_("Enter valid JSON"))

        return value

    def to_python(self, value):
        """
        The SubfieldBase metaclass calls pre_init instead of to_python,
        however to_python is still necessary for Django's deserializer
        """
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """ Convert JSON object to a string """
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj):
        value = super(JSONField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value)

    def dumps_for_display(self, value):
        kwargs = { "indent": 2 }
        kwargs.update(self.dump_kwargs)
        return json.dumps(value, **kwargs)

    def formfield(self, **kwargs):
        if "form_class" not in kwargs:
            kwargs["form_class"] = self.form_class
        field = super(JSONField, self).formfield(**kwargs)
        if isinstance(field, forms.JSONField):
            field.load_kwargs = self.load_kwargs

        if not field.help_text:
            field.help_text = _("Enter valid JSON")

        return field

    def get_default(self):
        """
        Returns the default value for this field.

        The default implementation on models.Field calls force_unicode
        on the default, which means you can't set arbitrary Python
        objects as the default. To fix this, we just return the value
        without calling force_unicode on it. Note that if you set a
        callable as a default, the field will still call it. It will
        *not* try to pickle and encode it.
        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return copy.deepcopy(self.default)
        # If the field doesn't have a default, then we punt to models.Field.
        return super(JSONField, self).get_default()

    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90300:
            return 'json'
        else:
            return super(JSONField, self).db_type(connection)

class Base64Field(models.TextField):
    """ Stolen from http://djangosnippets.org/snippets/1669/ """
    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_base64'
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        return base64.decodestring(getattr(obj, self.field_name))

    def set_data(self, obj, data):
        setattr(obj, self.field_name, base64.encodestring(data))

from django.conf import settings
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    rules = [
        (
            (DurationField,),
            [],
            {
            },
        ),
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
        (
            (JSONField,),
            [],
            {
            },
        ),
        (
            (Base64Field,),
            [],
            {},
        ),
    ]
    add_introspection_rules(rules, ["^fluo\.db\.models\.fields",])
