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

from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.template import Template, Context, RequestContext
from django.template import loader
from fluo.http import JsonResponse

__all__ = [
    'View',
    'TemplateView',
    'TemplateViewMixin',
    'JsonViewMixin',
    'RedirectView',
]

METHODS = ('head', 'get', 'post', 'put', 'delete', 'trace', 'options', 'connect',)

class View(object):
    #template_name = None
    mimetype = None
    content_type = None
    urlprefix = ''
    renderer = None
    extra_context = {}

    def __init__(self, **kwargs):
        #self.template_name = kwargs.pop('template_name', kwargs.pop('template', self.template_name))
        self.mimetype = kwargs.pop('mimetype', self.mimetype)
        self.content_type = kwargs.pop('content_type', self.content_type)
        self.urlprefix = kwargs.pop('urlprefix', self.urlprefix)
        self.renderer = kwargs.pop('renderer', self.renderer)
        self.extra_context = kwargs.pop('extra_context', self.extra_context)
        try:
            self.render = self.renderer(self)
        except TypeError:
            pass

        self.allowed_methods = []
        self.methods = {}
        for item in METHODS:
            method = getattr(self, item, None)
            if method is not None:
                self.allowed_methods.append(item)
                self.methods[item] = method

    def __call__(self, request, *args, **kwargs):
        try:
            method = self.methods[request.method.lower()]
        except KeyError:
            method = self.http_method_not_allowed
        return method(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.allowed_methods)

    def options(self, request, *args, **kwargs):
        return HttpResponse(self.allowed)

    #def render(self, *args, **kwargs):
        #raise NotImplemented

class TemplateViewMixin(object):
    mimetype = None
    content_type = None

    def render(self, request, template_name=None, context=None, mimetype=None, content_type=None):
        dictionary = {}
        dictionary.update(self.extra_context)
        dictionary.update(context)
        return HttpResponse(
            loader.render_to_string(
                template_name=template_name or self.template_name,
                dictionary=dictionary,
                context_instance=RequestContext(request)
            ),
            mimetype=mimetype or self.mimetype,
            content_type=content_type or self.content_type,
        )

class JsonViewMixin(object):
    def render(self, request, context=None, mimetype="text/javascript", status=200, indent=None):
        return JsonResponse(context=context, mimetype=mimetype, status=status, indent=indent)

class TemplateView(TemplateViewMixin, View):
    template_name = None
    def __init__(self, **kwargs):
        self.template_name = kwargs.pop('template_name', kwargs.pop('template', self.template_name))
        super(TemplateView, self).__init__(**kwargs)
    """
    A view that renders a template.
    """
    def get_context_data(self, **kwargs):
        return {
            'params': kwargs,
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render(
            request=request,
            template_name=self.template_name,
            context=context,
        )

class RedirectView(View):
    permanent = True
    url = None
    query_string = False

    def __init__(self, **kwargs):
        self.permanent = kwargs.pop('permanent', self.permanent)
        self.url = kwargs.pop('url', self.url)
        self.query_string = kwargs.pop('query_string', self.query_string)
        super(RedirectView, self).__init__(**kwargs)

    def get_redirect_url(self, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.url:
            args = self.request.META["QUERY_STRING"]
            if args and self.query_string:
                url = "%s?%s" % (self.url, args)
            else:
                url = self.url
            return url % kwargs
        else:
            return None

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(**kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            return HttpResponseGone()

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

