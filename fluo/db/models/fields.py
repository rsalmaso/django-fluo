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

# Original code for taken and adapted from
# - django-extensions
#   - CreationDateTimeField
#   - ModificationDateTimeField

from django.core import checks, validators
from django.db import connection, models
from django.db.models import lookups
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import gettext_lazy as _

from fluo import forms

from .postgresql import *  # noqa: F401,F403
from .postgresql import __all__ as postgresql_all

__all__ = [
    *postgresql_all,
    "StatusField",
    "STATUS_ACTIVE",
    "STATUS_INACTIVE",
    "STATUS_CHOICES",
    "CreationDateTimeField",
    "ModificationDateTimeField",
    "OrderField",
    "TimeDeltaField",
    "SlugField",
    "StringField",
    "EmailField",
    "URLField",
    "CISlugField",
    "CIStringField",
    "CIEmailField",
    "CIURLField",
]


STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_CHOICES = (
    (STATUS_ACTIVE, _("Active")),
    (STATUS_INACTIVE, _("Inactive")),
)


class CreationDateTimeField(models.DateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", timezone.now)
        super().__init__(*args, **kwargs)

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


class OrderField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", 0)
        models.Field.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.OrderField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class TimeDeltaField(models.DecimalField):
    description = _("TimeDelta field")

    def __init__(self, milliseconds=False, *args, **kwargs):
        self.milliseconds = milliseconds
        kwargs.setdefault("default", 0)
        kwargs.setdefault("decimal_places", 3)
        kwargs.setdefault("max_digits", 12)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TimeDeltaField,
            "milliseconds": self.milliseconds,
        }
        defaults.update(kwargs)
        # skip DecimalField.formfield
        # which injects decimal_places and max_digits
        return models.Field.formfield(self, **defaults)


class StringField(models.Field):
    description = _("String")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.max_length, int) and self.max_length > 0:
            self.validators.append(validators.MaxLengthValidator(self.max_length))

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_max_length_attribute(**kwargs),
        ]

    def formfield(self, **kwargs):
        defaults = {"max_length": self.max_length, "form_class": forms.StringField}
        # see django CharField comment
        if self.null and not connection.features.interprets_empty_strings_as_nulls:
            defaults["empty_value"] = None
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_internal_type(self):
        return "CharField" if self.max_length else "TextField"

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return smart_text(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["max_length"] = self.max_length
        return name, path, args, kwargs

    def _check_max_length_attribute(self, **kwargs):
        is_integer = isinstance(self.max_length, int)
        is_negative = is_integer and self.max_length <= 0
        is_none = self.max_length is None
        if (is_integer and is_negative) or (not is_integer and not is_none):
            errors = [
                checks.Error(
                    "StringField must define a 'max_length' attribute (can be None, 0 or a positive integer).",
                    hint=None,
                    obj=self,
                    id="fluo.E1",
                ),
            ]
        else:
            errors = []
        return errors


class URLField(StringField):
    default_validators = [validators.URLValidator()]
    description = _("URL")

    def formfield(self, **kwargs):
        # As with StringField, this will cause URL validation to be performed twice.
        defaults = {
            "form_class": forms.URLField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class SlugField(StringField):
    default_validators = [validators.validate_slug]
    description = _("Slug")

    def __init__(self, *args, db_index=True, allow_unicode=False, **kwargs):
        self.allow_unicode = allow_unicode
        if self.allow_unicode:
            self.default_validators = [validators.validate_unicode_slug]
        super().__init__(*args, db_index=db_index, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SlugField, self).deconstruct()
        if self.db_index is False:
            kwargs["db_index"] = False
        else:
            del kwargs["db_index"]
        if self.allow_unicode is not False:
            kwargs["allow_unicode"] = self.allow_unicode
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.SlugField, "allow_unicode": self.allow_unicode}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class EmailField(StringField):
    default_validators = [validators.validate_email]
    description = _("Email address")

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.EmailField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class StatusField(StringField):
    def __init__(
        self,
        choices=STATUS_CHOICES,
        max_length=None,
        default=STATUS_ACTIVE,
        blank=False,
        null=False,
        verbose_name=_("status"),
        help_text=_("Is active?"),
    ):
        super().__init__(
            choices=choices,
            max_length=max_length,
            default=default,
            blank=blank,
            null=null,
            verbose_name=verbose_name,
            help_text=help_text,
        )


class CIStringField(CIText, StringField):  # noqa: F405
    pass


class CIURLField(CIText, URLField):  # noqa: F405
    pass


class CISlugField(CIText, SlugField):  # noqa: F405
    pass


class CIEmailField(CIText, EmailField):  # noqa: F405
    pass


for field in [CIStringField, CIURLField, CISlugField, CIEmailField]:
    field.register_lookup(lookups.IExact, lookup_name="exact")
    field.register_lookup(lookups.IContains, lookup_name="contains")
    field.register_lookup(lookups.IStartsWith, lookup_name="startswith")
    field.register_lookup(lookups.IEndsWith, lookup_name="endswith")
    field.register_lookup(lookups.IRegex, lookup_name="regex")
