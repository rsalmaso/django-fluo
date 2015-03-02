# -*- coding: utf-8 -*-

# Copyright (C) 2007-2015, Raffaele Salmaso <raffaele@salmaso.org>
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
import copy
from django.utils.translation import ugettext_lazy as _


class CopyObject(object):
    short_description = _("Duplicate as new")

    def __init__(self, *args, **kwargs):
        super(CopyObject, self).__init__(*args, **kwargs)
        self.__name__ = self.__class__.__name__

    def __call__(self, modeladmin, request, queryset):
        for original in queryset:
            instance = copy.copy(original)
            instance.id = None
            self.update(request, instance, original)
            instance.save()
            self.update_m2m(request, instance, original)
            instance.save()

            translations = getattr(original, "translations", None)
            if translations:
                for translation in translations.all():
                    tr = copy.copy(translation)
                    tr.id = None
                    tr.parent = instance
                    self.update_translation(request, tr, translation)
                    tr.save()

    def update(self, request, instance, original):
        pass

    def update_m2m(self, request, instance, original):
        pass

    def update_translation(self, request, instance, original):
        pass
