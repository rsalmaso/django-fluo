# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
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
from django.template import Template, Context, RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render as render_to_response
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse as django_reverse


__all__ = [
    'get_object_or_404', 'get_list_or_404', 'redirect',
    'render_to_string', 'render_to_response', 'render_from_string',
    'reverse',
]


def render_from_string(template_string, request=None, **kwargs):
    t = Template(template_string)
    if request:
        context_instance = RequestContext(request, kwargs)
    else:
        context_instance = Context(kwargs)
    return t.render(context_instance)


def reverse(viewname, *args, **kwargs):
    return django_reverse(viewname, args=args, kwargs=kwargs)
