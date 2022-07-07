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

from django import template
from django.templatetags.static import static
from django.utils.encoding import iri_to_uri
from django.utils.safestring import mark_safe

from fluo.settings import MEDIA_URL

register = template.Library()


class MediaNode(template.Node):
    def __init__(self, filename, args):
        self.filename = filename
        self.args = args

    def render(self, context):
        filename = self.filename.resolve(context)
        args = " %s" % " ".join(self.args) if self.args else ""
        script = filename if filename.startswith(("https://", "http://", "//")) else static(iri_to_uri(filename))
        return mark_safe(self.fmt % {"script": script, "args": args})


def media_tag(parser, token, node_class):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument, the name of the script." % bits[0])

    filename = parser.compile_filter(bits[1])
    args = [bit for bit in bits[2:]]

    return node_class(filename, args)


class CssNode(MediaNode):
    fmt = '<link rel="stylesheet" type="text/css" href="%(script)s"%(args)s/>'


@register.tag
def css(parser, token):
    return media_tag(parser, token, CssNode)


class JsNode(MediaNode):
    fmt = '<script src="%(script)s"%(args)s></script>'


@register.tag
def js(parser, token):
    return media_tag(parser, token, JsNode)


@register.simple_tag
def static_url():
    """ Returns the string contained in the setting STATIC_URL. """
    return static("")


@register.simple_tag
def media_url():
    """ Returns the string contained in the setting MEDIA_URL. """
    return MEDIA_URL
