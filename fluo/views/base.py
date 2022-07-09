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

from __future__ import annotations

import logging

from django.core.exceptions import ImproperlyConfigured
from django.http import (
    HttpResponse,
    HttpResponseGone,
    HttpResponseNotAllowed,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

log = logging.getLogger("fluo")


class View:
    METHODS = (
        "head",
        "get",
        "post",
        "put",
        "delete",
        "trace",
        "options",
        "connect",
        "trace",
        "patch",
    )
    content_type = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.METHODS:
                raise TypeError(
                    "You tried to pass in the %s method name as a keyword argument to %s(). Don't do that."
                    % (key, self.__class__.__name__),
                )
            if not hasattr(self, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. only accepts arguments that are already attributes of the class."  # noqa: E501
                    % (self.__class__.__name__, key),
                )
            else:
                setattr(self, key, value)

        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get

        self.allowed_methods = []
        self.methods = {}
        for item in View.METHODS:
            method = getattr(self, item, None)
            if method is not None:
                self.allowed_methods.append(item.upper())
                self.methods[item] = method

    def __call__(self, request, *args, **kwargs):
        try:
            method = self.methods[request.method.lower()]
        except KeyError:
            method = self.http_method_not_allowed
        return method(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        log.warning(
            "Method Not Allowed (%s): %s",
            request.method,
            request.path,
            extra={"status_code": 405, "request": request},
        )
        return HttpResponseNotAllowed(self.allowed_methods)

    def options(self, request, *args, **kwargs):
        """
        Handles responding to requests for the OPTIONS HTTP verb
        """
        response = HttpResponse()
        response["Allow"] = ", ".join(self.allowed_methods)
        response["Content-Length"] = 0
        return response


class TemplateView(View):
    """
    A view that renders a template.
    """

    template_name = None
    content_type = None

    def get_context_data(self, **kwargs):
        return {
            "params": kwargs,
        }

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]
        msg = _("%s must either define 'template_name' or override 'get_template_names()'")
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def render(self, request, template_name, context=None, content_type=None, status=None):
        return TemplateResponse(
            request=request,
            template=template_name,
            context=context,
            content_type=self.content_type if content_type is None else content_type,
            status=status,
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render(request=request, template_name=self.get_template_names(), context=context)


class RedirectView(View):
    permanent = True
    url = None
    query_string = True

    def __init__(self, **kwargs):
        self.permanent = kwargs.pop("permanent", self.permanent)
        self.url = kwargs.pop("url", self.url)
        self.query_string = kwargs.pop("query_string", self.query_string)
        super().__init__(**kwargs)

    def get_redirect_url(self, request, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.url:
            url = self.url % kwargs
            args = request.META.get("QUERY_STRING", "")
            if args and self.query_string:
                url = "%s?%s" % (url, args)
            return url
        else:
            return None

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(request, **kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            log.warning(
                "Gone: %s",
                self.request.path,
                extra={"status_code": 410, "request": self.request},
            )
            return HttpResponseGone()

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
