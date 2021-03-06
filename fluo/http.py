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

import json

from django.http import *  # noqa: F401,F403
from django.http import __all__ as http_all

from .utils.json import JSONEncoder

__all__ = [
    *http_all,
    "JsonResponse",
]


class JsonResponse(HttpResponse):  # noqa: F405
    def __init__(
        self,
        content=None,
        content_type="application/json; charset=utf-8",
        status=200,
        indent=2,
    ):
        """
        return JsonResponse(content={'status': 200, 'message': '', 'data': [] })
        """
        if content is None:
            content = {}
        data = json.dumps(content, indent=indent, cls=JSONEncoder)
        super().__init__(content=data, content_type=content_type, status=status)
        self["Content-Length"] = len(data)
