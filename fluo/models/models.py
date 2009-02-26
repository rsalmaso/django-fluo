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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from fluo.models import fields

class OrderedModel(models.Model):
    ordering = fields.OrderField(
        default=0,
        blank=True,
        verbose_name=_('ordering'),
        help_text=_('Ordered'),
    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False):
        ordering = False
        if not self.ordering:
            self.ordering = 1
            ordering = True
        super(OrderedModel, self).save(force_insert=force_insert, force_update=force_update)
        if ordering:
            self._set_default_ordering()
            super(OrderedModel, self).save(force_insert=force_insert, force_update=force_update)
    def brothers_and_me(self):
        return self._default_manager.all()
    def brothers(self):
        return self.brothers_and_me().exclude(pk=self.id)
    def is_first(self):
        return self.brothers_and_me().order_by('ordering')[0:1][0] == self
    def is_last(self):
        return self.brothers_and_me().order_by('-ordering')[0:1][0] == self
    def _switch_node(self, other):
        self.ordering, other.ordering = other.ordering, self.ordering
        self.save()
        other.save()
    def up(self):
        brothers = self.brothers().order_by('-ordering').filter(ordering__lt=self.ordering+1)[0:1]
        if not brothers.count():
            return False
        if brothers[0].ordering == self.ordering:
            self._set_default_order()
            self.save()
        self._switch_node(brothers[0])
        return True
    def down(self):
        brothers = self.brothers().order_by('ordering').filter(ordering__gt=self.ordering-1)[0:1]
        if not brothers.count():
            return False
        brother = brothers[0]
        if brother.ordering == self.ordering:
            brother._set_default_ordering()
            brother.save()
        self._switch_node(brother)
        return True
    def _set_default_ordering(self):
        max = 0
        brothers = self.brothers()
        if brothers.count():
            for brother in brothers:
                if brother.ordering >= max:
                    max = brother.ordering
        self.ordering = max + 1

