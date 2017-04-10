# Copyright (C) 2007-2017, Raffaele Salmaso <raffaele@salmaso.org>
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

import re

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from . import fields
from ... import settings

__all__ = [
    'StatusModel',
    'OrderedModel', 'TreeOrderedModel',
    'TimestampModel',
    'I18NProxy', 'I18NModel', 'TranslationModel',
    'CategoryModelManager', 'CategoryModel', 'CategoryTranslationModel',
    'GenericModel',
    'AbstractUser', 'BaseUserManager', 'UserManager',
]


class StatusModel(models.Model):
    status = fields.StatusField()

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    ordering = fields.OrderField(
        default=0,
        blank=True,
        db_index=True,
        verbose_name=_('ordering'),
        help_text=_('Ordered'),
    )

    class Meta:
        abstract = True
        ordering = ("-ordering",)

    def save(self, *args, **kwargs):
        if not self.ordering:
            self.ordering = self.get_max_ordering() + 1
        super().save(*args, **kwargs)

    @property
    def brothers_and_me(self):
        return self.__class__._default_manager.all()

    @property
    def brothers(self):
        return self.brothers_and_me.exclude(pk=self.id)

    def get_max_ordering(self):
        ordering = self.brothers.aggregate(max=Max("ordering"))["max"]
        return 0 if ordering is None else ordering


class TreeOrderedModel(OrderedModel):
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_('Parent node'),
        help_text=_('The parent node of this field.'),
    )

    class Meta:
        abstract = True

    @property
    def brothers_and_me(self):
        if self.parent:
            return self.__class__._default_manager.filter(parent=self.parent)
        else:
            return self.__class__._default_manager.filter(parent__isnull=True)


class TimestampModel(models.Model):
    created_at = fields.CreationDateTimeField(
        verbose_name=_('created'),
    )
    last_modified_at = fields.ModificationDateTimeField(
        verbose_name=_('modified'),
    )

    class Meta:
        abstract = True


class I18NProxy:
    def __init__(self, tr, original):
        self._tr = tr
        self._original = original

    def __getattr__(self, name):
        attr = getattr(self._tr, name, None)
        if not attr or (attr and (attr == '' or attr == '')):
            attr = getattr(self._original, name)
        return attr


class I18NModel(models.Model):
    def translate(self, language=None):
        try:
            language = language or get_language()[:2]
            return I18NProxy(self.translations.get(language__startswith=language), self)
        except (models.ObjectDoesNotExist, AttributeError, TypeError):
            return self

    class Meta:
        abstract = True


class TranslationModel(models.Model):
    language = models.CharField(
        max_length=5,
        choices=settings.LANGUAGES,
        db_index=True,
        verbose_name=_('language'),
    )

    class Meta:
        abstract = True
        ordering = ['language']


class CategoryModelQuerySet(models.QuerySet):
    def default(self):
        return self.get(default=True)

    def active(self):
        return self.filter(status=fields.STATUS_ACTIVE)

    def inactive(self):
        return self.filter(status=fields.STATUS_INACTIVE)


class CategoryModelManager(models.Manager.from_queryset(CategoryModelQuerySet)):
    use_for_related_fields = True
    silence_use_for_related_fields_deprecation = True


class CategoryModel(StatusModel, OrderedModel):
    objects = CategoryModelManager()

    name = models.CharField(
        unique=True,
        max_length=255,
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name=_('slug'),
        help_text=_('A "slug" is a unique URL-friendly title for the object automatically generated from the "name" field.'),  # noqa: E501
    )
    default = models.BooleanField(
        default=False,
        verbose_name=_('default'),
        help_text=_('Is the default one?'),
    )

    class Meta:
        abstract = True
        base_manager_name = "objects"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        if self.default:
            for c in self.__class__._default_manager.exclude(pk=self.id):
                c.default = False
                c.save(*args, **kwargs)
        try:
            c = self.__class__._default_manager.get(default=True)
        except models.ObjectDoesNotExist:
            self.default = True
            super().save(*args, **kwargs)


class CategoryTranslationModel(TranslationModel):
    name = models.CharField(
        max_length=255,
    )

    class Meta:
        abstract = True


class GenericModel(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Object Type'),
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID'),
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        abstract = True


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    objects = UserManager()

    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'),
                'invalid',
            ),
        ],
        verbose_name=_('username'),
        help_text=_('Required. 255 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('first name'),
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('last name'),
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name=_('email address'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('staff status'),
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),  # noqa: E501
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date joined'),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_display_name(self):
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.username
