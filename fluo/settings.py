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

from django.conf import settings
from django.utils.encoding import iri_to_uri

DATABASES = getattr(settings, 'DATABASES')
DEBUG = getattr(settings, 'DEBUG')

MEDIA_URL = iri_to_uri(getattr(settings, 'MEDIA_URL'))
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
FLUO_MEDIA_URL = getattr(settings, 'FLUO_MEDIA_URL', MEDIA_URL + 'fluo/')
JQUERY_MEDIA_URL = FLUO_MEDIA_URL + 'jquery/'

STATIC_URL = iri_to_uri(getattr(settings, 'STATIC_URL'))
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
FLUO_STATIC_URL = getattr(settings, 'FLUO_STATIC_URL', STATIC_URL + 'fluo/')
JQUERY_STATIC_URL = FLUO_STATIC_URL + 'jquery/'

SERVE_MEDIA_FILES = getattr(settings, 'SERVE_MEDIA_FILES', True)

JQUERY_MINIFIED = getattr(settings, 'JQUERY_MINIFIED', True)
LANGUAGES = getattr(settings, 'LANGUAGES')
LOGGING_FORMAT = getattr(settings, 'LOGGING_FORMAT', '%(asctime)s %(levelname)s %(message)s')
LOGGING_FILENAME = getattr(settings, 'LOGGING_FILENAME', '/tmp/fluo.log')

DEFAULT_PERMISSIONS = ('list', 'view',)
try:
    DEFAULT_PERMISSIONS += list(getattr(settings, 'DEFAULT_PERMISSIONS'))
except:
    pass

NO_LOCALE_PATTERNS = (MEDIA_URL,)
try:
    NO_LOCALE_PATTERNS += getattr(settings, 'NO_LOCALE_PATTERNS',)
except:
    pass
