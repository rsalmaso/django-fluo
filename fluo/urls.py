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

from __future__ import absolute_import, print_function, unicode_literals
import re
from django.conf.urls import url, include, patterns
from fluo import settings

__all__ = [
    'url', 'include', 'patterns',
    'Urls', 'MediaUrls',
]

class Urls(object):
    def get_urls(self):
        raise NotImplemented

    def urls(self):
        return self.get_urls()
    urls = property(urls)

class MediaUrls(Urls):
    def get_urls(self):
        if settings.DEBUG or settings.SERVE_MEDIA_FILES:
            urlpatterns = patterns('',
                url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
                url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT, }),
            )
        else:
            urlpatterns = []
        return urlpatterns

