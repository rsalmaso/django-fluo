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

# taken and adapted from django-cms
# Copyright (c) 2008, Batiste Bieler

"this is the locale selecting middleware that will look at accept headers"

from __future__ import absolute_import, print_function, unicode_literals
import re
from django.utils.cache import patch_vary_headers
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from fluo.settings import NO_LOCALE_PATTERNS

SUB = re.compile(ur'<a([^>]+)href="/(?!(%s|%s|%s))([^"]*)"([^>]*)>' % (
    "|".join(map(lambda l: l[0] + "/" , settings.LANGUAGES)),
    settings.MEDIA_URL[1:],
    settings.STATIC_URL[1:]
))
SUB2 = re.compile(ur'<form([^>]+)action="/(?!(%s|%s|%s))([^"]*)"([^>]*)>' % (
    "|".join(map(lambda l: l[0] + "/" , settings.LANGUAGES)),
     settings.MEDIA_URL[1:],
     settings.STATIC_URL[1:]
))
SUPPORTED = dict(settings.LANGUAGES)
START_SUB = re.compile(r"^/(%s)/(.*)" % "|".join(map(lambda l: l[0], settings.LANGUAGES)))
NO_LOCALE_SUB = re.compile(r"^(%s|%s)(.*)" % ("|".join(NO_LOCALE_PATTERNS), settings.STATIC_URL))
LANGUAGE_COOKIE_NAME = settings.LANGUAGE_COOKIE_NAME

def has_lang_prefix(path):
    check = START_SUB.match(path)
    if check is not None:
        return check.group(1)
    else:
        return False

def skip_translation(path):
    check = NO_LOCALE_SUB.match(path)
    if check is not None:
        return check.group(1)
    else:
        return False

def get_default_language(language_code=None):
    """
    Returns default language depending on settings.LANGUAGE_CODE merged with
    best match from settings.LANGUAGES

    Returns: language_code

    Raises ImproperlyConfigured if no match found
    """

    if not language_code:
        language_code = settings.LANGUAGE_CODE

    languages = dict(settings.LANGUAGES).keys()

    # first try if there is an exact language
    if language_code in languages:
        return language_code

    # otherwise split the language code if possible, so iso3
    language_code = language_code.split("-")[0]

    if not language_code in languages:
        raise ImproperlyConfigured("No match in LANGUAGES for LANGUAGE_CODE %s" % settings.LANGUAGE_CODE)

    return language_code

def get_language_from_request(request):
    language = request.REQUEST.get('language', None)

    if language:
        if not language in dict(settings.LANGUAGES).keys():
            language = None

    if language is None:
        language = getattr(request, 'LANGUAGE_CODE', None)

    if language:
        if not language in dict(settings.LANGUAGES).keys():
            language = None

    if language is None:
        language = get_default_language()

    return language

class LocaleMiddleware(object):
    def get_language_from_request(self, request):
        changed = False
        prefix = has_lang_prefix(request.path_info)
        if prefix:
            request.path = "/" + "/".join(request.path.split("/")[2:])
            request.path_info = "/" + "/".join(request.path_info.split("/")[2:])
            t = prefix
            if t in SUPPORTED:
                lang = t
                if hasattr(request, "session"):
                    request.session["django_language"] = lang
                else:
                    request.set_cookie(LANGUAGE_COOKIE_NAME, lang)
                changed = True
        else:
            lang = translation.get_language_from_request(request)
        if not changed:
            if hasattr(request, "session"):
                lang = request.session.get("django_language", None)
                if lang in SUPPORTED and lang is not None:
                    return lang
            elif LANGUAGE_COOKIE_NAME in request.COOKIES.keys():
                lang = request.COOKIES.get(LANGUAGE_COOKIE_NAME, None)
                if lang in SUPPORTED and lang is not None:
                    return lang
            if not lang:
                lang = translation.get_language_from_request(request)
        lang = get_default_language(lang)
        return lang

    def process_request(self, request):
        path = unicode(request.path)
        if skip_translation(path):
            return

        prefix = has_lang_prefix(request.path_info)
        if not prefix:
            return HttpResponseRedirect('/%s%s' % (settings.LANGUAGE_CODE[:2], request.get_full_path()))
        language = self.get_language_from_request(request)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        path = unicode(request.path)
        if skip_translation(path):
            return response

        patch_vary_headers(response, ("Accept-Language",))
        translation.deactivate()

        if not skip_translation(path) and response.status_code == 200 and response._headers['content-type'][1].split(';')[0] == "text/html":
            response.content = SUB.sub(ur'<a\1href="/%s/\3"\4>' % request.LANGUAGE_CODE, response.content.decode('utf-8'))
            response.content = SUB2.sub(ur'<form\1action="/%s/\3"\4>' % request.LANGUAGE_CODE, response.content.decode('utf-8'))
        if (response.status_code == 301 or response.status_code == 302 ):
            if 'Content-Language' not in response:
                response['Content-Language'] = translation.get_language()
            location = response._headers['location']
            prefix = has_lang_prefix(location[1])
            if not prefix and location[1].startswith("/") and not skip_translation(location[1]):
                response._headers['location'] = (location[0], "/%s%s" % (request.LANGUAGE_CODE, location[1]))
        return response

