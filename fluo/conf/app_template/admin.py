# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from django.utils.translation import ugettext_lazy as _
from fluo import admin
from fluo import forms
from .models import X

#import logging
#log = logging.getLogger('{{ app_name }}')

class XAdminForm(forms.ModelForm):
    class Meta:
        model = X
class XAdmin(forms.ModelAdmin):
    model = X
    form = XAdminForm
admin.site.register(X, XAdmin)

