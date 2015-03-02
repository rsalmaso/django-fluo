# -*- coding: utf-8 -*-

# Copyright (C) 2007-2015, Raffaele Salmaso <raffaele@salmaso.org>
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
from django import template
from django.utils.translation import get_language
from django.utils.encoding import iri_to_uri
from fluo.settings import STATIC_URL, FLUO_STATIC_URL, JQUERY_STATIC_URL, JQUERY_MINIFIED


register = template.Library()


@register.simple_tag
def css(script, static="all"):
    return '<link rel="stylesheet" type="text/css" href="%(static_url)s%(script)s" static="%(static)s"/>' % {
        'static_url': STATIC_URL,
        'script': iri_to_uri(script),
        'static': iri_to_uri(static),
    }


@register.simple_tag
def css_print(script):
    return css(script, media="print")


@register.simple_tag
def css_ie(script, media="all"):
    return """<!--[if IE]>%s<![endif]-->""" % css(script, media)


@register.simple_tag
def css_ie6(script, media="all"):
    return """<!--[if IE 6]>%s<![endif]-->""" % css(script, media)


@register.simple_tag
def css_ie7(script, media="all"):
    return """<!--[if IE 7]>%s<![endif]-->""" % css(script, media)


@register.simple_tag
def js(script):
    return '<script type="text/javascript" src="%(static)s%(script)s"></script>' % {
        'static': STATIC_URL,
        'script': iri_to_uri(script),
    }


@register.simple_tag
def jquery():
    return '<script type="text/javascript" src="%(static)s%(jquery)s"></script>' % {
        'static': JQUERY_STATIC_URL,
        'jquery': {True: 'jquery.min.js', False: 'jquery.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jqueryui():
    return '''<script type="text/javascript" src="%(static)s%(jqueryui)s"></script><script type="text/javascript" src="%(static)si18n/%(i18n)s"></script>''' % { # NOQA
        'static': JQUERY_STATIC_URL,
        'jqueryui': {True: 'jquery.ui.min.js', False: 'jquery.ui.js'}[JQUERY_MINIFIED],
        'i18n': {
            True: 'jquery.ui.datepicker-%s.min.js',
            False: 'jquery.ui.datepicker-%s.js',
        }[JQUERY_MINIFIED] % get_language()[:2],
    }


@register.simple_tag
def jqueryui_default_theme():
    return '<link rel="stylesheet" type="text/css" href="%(media_url)stheme/jquery.ui.css" media="all"/>' % {
        'media_url': JQUERY_STATIC_URL,
    }


@register.simple_tag
def thickbox():
    return """<link rel="stylesheet" type="text/css" href="%(static)sthickbox/css/thickbox.css" />
<script type="text/javascript">var tb_pathToImage = "%(static)sfluo/thickbox/images/loadingAnimation.gif";</script>
<script type="text/javascript" src="%(static)sfluo/thickbox/js/%(thickbox)s"></script>""" % {
        'static': FLUO_STATIC_URL,
        'thickbox': {True: 'thickbox.min.js', False: 'thickbox.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_ajaxqueue():
    return '<script type="text/javascript" src="%(static)sjquery-ajaxqueue/%(js)s"></script>' % {
        'static': FLUO_STATIC_URL,
        'js': {True: 'jquery.ajaxqueue.min.js', False: 'jquery.ajaxqueue.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_autocomplete():
    return '<script type="text/javascript" src="%(static)sjquery-autocomplete/%(js)s"></script>' % {
        'static': FLUO_STATIC_URL,
        'js': {True: 'jquery.autocomplete.min.js', False: 'jquery.autocomplete.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_listreorder():
    return '<script type="text/javascript" src="%(static)sjquery-listreorder/%(js)s"></script>' % {
        'static': FLUO_STATIC_URL,
        'js': {True: 'jquery.listreorder.min.js', False: 'jquery.listreorder.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_tablednd():
    return '<script type="text/javascript" src="%(static)sjquery-tablednd/%(js)s"></script>' % {
        'static': FLUO_STATIC_URL,
        'js': {True: 'jquery.tablednd.min.js', False: 'jquery.tablednd.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_bgiframe():
    return '<script type="text/javascript" src="%(static)sjquery-bgiframe/%(js)s"></script>' % {
        'static': FLUO_STATIC_URL,
        'js': {True: 'jquery.bgiframe.min.js', False: 'jquery.bgiframe.js'}[JQUERY_MINIFIED],
    }


@register.simple_tag
def jquery_disable_text_select():
    return '<script type="text/javascript" src="%(static)sjquery-disable-text-select/jquery.disable.text.select.pack.js"></script>' % { # NOQA
        'static': FLUO_STATIC_URL,
    }


@register.simple_tag
def media_url():
    """ Returns the string contained in the setting STATIC_URL. """
    return STATIC_URL
