# Copyright (C) 2007-2022, Raffaele Salmaso <raffaele@salmaso.org>
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

from django.conf.urls import handler400, handler403, handler404, handler500
from django.urls import (
    NoReverseMatch,
    Resolver404,
    ResolverMatch,
    get_script_prefix,
    resolve,
    reverse as django_reverse,
)
from django.utils.functional import lazy
from django.utils.http import urlencode

try:
    from django.urls import include
except ImportError:
    from django.conf.urls import include

try:
    from django.urls import path, re_path
except ImportError:
    path, re_path = None, None

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

try:
    from django.urls import URLPattern, URLResolver
except ImportError:
    from django.urls import RegexURLPattern as URLPattern, RegexURLResolver as URLResolver


__all__ = [
    "handler400",
    "handler403",
    "handler404",
    "handler500",
    "path",
    "re_path",
    "url",
    "include",
    "NoReverseMatch",
    "URLPattern",
    "URLResolver",
    "ResolverMatch",
    "Resolver404",
    "get_script_prefix",
    "reverse",
    "reverse_lazy",
    "resolve",
    "UrlsMixin",
]


class UrlsMixin:
    def get_urls(self):
        raise NotImplementedError

    @property
    def urls(self):
        return self.get_urls()


def reverse(viewname, *, args=None, kwargs=None, request=None, format=None, data=None, **extra):
    if format is not None:
        kwargs = kwargs or {}
        kwargs["format"] = format
    url = django_reverse(viewname, args=args, kwargs=kwargs, **extra)

    if data is not None:
        url += "?" + urlencode(data)

    if request:
        url = request.build_absolute_uri(url)

    return url


reverse_lazy = lazy(reverse, str)
