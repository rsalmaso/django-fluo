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
from django.utils.cache import cache
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.utils.decorators import wraps, method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

__all__ = [
    'ajax_required', 'ajax_required_m',
    'login_required', 'login_required_m',
    'throttle', 'throttle_m',
]

def ajax_required(func):
    # taken from djangosnippets.org
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return func(request, *args, **kwargs)
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
ajax_required_m = method_decorator(ajax_required)

def login_required(function=None, required=False, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that, if required, checks that the user is logged in and redirect
    to the log-in page if necessary.
    """
    if required:
        actual_decorator = user_passes_test(
            lambda u: u.is_authenticated(),
            redirect_field_name=redirect_field_name
        )
        if function:
            return actual_decorator(function)
        return actual_decorator
    # login not required
    def decorator(view_func):
        def _wrapper(request, *args, **kwargs):
            return function(request, *args, **kwargs)
        return wraps(function)(_wrapper)
    return method_decorator(decorator)
login_required_m = method_decorator(login_required)

def throttle(func, limit=3, duration=900, methods=('POST','GET', 'PUT', 'DELETE', 'OPTIONS')):
    def inner(request, *args, **kwargs):
        if request.method in methods:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            if cache.get(remote_addr) == limit:
                return HttpResponseForbidden('Try slowing down a little.')
            elif not cache.get(remote_addr):
                cache.set(remote_addr, 1, duration)
            else:
                cache.incr(remote_addr)
        return func(request, *args, **kwargs)
    return inner
throttle_m = method_decorator(throttle)

