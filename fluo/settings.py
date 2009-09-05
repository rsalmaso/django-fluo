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

from django.conf import settings

MEDIA_URL = getattr(settings, 'MEDIA_URL')
JQUERY_MINIFIED = getattr(settings, 'JQUERY_MINIFIED', True)
ADMIN_MEDIA_PREFIX = getattr(settings, 'ADMIN_MEDIA_PREFIX')
LANGUAGES = getattr(settings, 'LANGUAGES')
LOGGING_FORMAT = getattr(settings, 'LOGGING_FORMAT', '%(asctime)s %(levelname)s %(message)s')
LOGGING_FILENAME = getattr(settings, 'LOGGING_FILENAME', '/tmp/fluo.log')
DEFAULT_PERMISSIONS = ('list', 'view',)
try:
    DEFAULT_PERMISSIONS += list(getattr(settings, 'DEFAULT_PERMISSIONS'))
except:
    pass

