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

from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf.urls import handler400, handler403, handler404, handler500, include, patterns, url
from django.core.urlresolvers import resolve
from django.core.urlresolvers import reverse as django_reverse
from django.utils import six
from django.utils.functional import lazy


__all__ = [
    'handler400', 'handler403', 'handler404', 'handler500',
    'url', 'include', 'patterns',
    'reverse', 'reverse_lazy', 'resolve',
    'Urls',
]


class Urls(object):
    def get_urls(self):
        raise NotImplemented

    def urls(self):
        return self.get_urls()
    urls = property(urls)


def reverse(viewname, args=None, kwargs=None, request=None, format=None, **extra):
    if format is not None:
        kwargs = kwargs or {}
        kwargs['format'] = format
    _url = django_reverse(viewname, args=args, kwargs=kwargs, **extra)
    if request:
        _url = request.build_absolute_uri(url)
    return _url


reverse_lazy = lazy(reverse, six.text_type)
