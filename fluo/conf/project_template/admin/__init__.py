# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
#from django.utils.translation import ugettext_lazy as _

from fluo import admin
admin.autodiscover()

log = logging.getLogger(__name__)

