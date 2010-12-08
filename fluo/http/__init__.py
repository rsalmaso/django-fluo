# -*- coding: utf-8 -*-

# Copyright (C) 2007-2010, Salmaso Raffaele <raffaele@salmaso.org>
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

from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings

__all__ = [
    'JsonResponse',
]

class JsonResponse(HttpResponse):
    def __init__(self, content=None, mimetype="text/javascript", status=200, indent=None):
        """
        return JsonResponse(content={'status': 200, 'message': '', 'data': [] })
        """
        if content is None:
            content = {}
        if settings.DEBUG and indent is None:
            indent = 4
        json = content=simplejson.dumps(content, indent=indent)
        super(JsonResponse, self).__init__(content=json, mimetype=mimetype, status=status)

