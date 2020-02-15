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

# taken and adapted from django-cms
# Copyright (c) 2008, Batiste Bieler

from django import template
from fluo.middleware.locale import get_language_from_request

register = template.Library()


@register.inclusion_tag('fluo/tags/languages.html', takes_context=True)
def languages_as_li(context, template='fluo/tags/languages_as_li.html'):
    request = context['request']
    context['current_language'] = get_language_from_request(request)
    context['template'] = template
    return context


@register.inclusion_tag('fluo/tags/content.html', takes_context=True)
def page_language_url(context, lang):
    request = context['request']
    return {'content': r'/%s%s' % (lang, request.get_full_path())}
