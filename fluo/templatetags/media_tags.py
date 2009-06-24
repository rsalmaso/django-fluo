# -*- coding: utf-8 -*-

# Copyright (C) 2007-2009, Salmaso Raffaele <raffaele@salmaso.org>
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

from django import template
from fluo import settings

register = template.Library()

@register.simple_tag
def css(script, media="all"):
    return '<link rel="stylesheet" type="text/css" href="%(media_url)s%(script)s" media="%(media)s"/>' % {
        'media_url': settings.MEDIA_URL,
        'script': script,
        'media': media,
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
    return '<script type="text/javascript" src="%(media)s%(script)s"></script>' % {
        'media': settings.MEDIA_URL,
        'script': script,
    }

@register.simple_tag
def media_url():
    return settings.MEDIA_URL

@register.simple_tag
def admin_media_prefix():
    return settings.ADMIN_MEDIA_PREFIX

