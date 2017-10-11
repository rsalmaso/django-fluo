# Copyright (C) 2007-2017, Raffaele Salmaso <raffaele@salmaso.org>
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
from django.apps import apps
from django.utils.encoding import iri_to_uri
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from fluo.settings import JQUERY_MINIFIED, MEDIA_URL

if apps.is_installed('django.contrib.staticfiles'):
    from django.contrib.staticfiles.templatetags.staticfiles import static as _static
else:
    from django.templatetags.static import static as _static

register = template.Library()


@register.simple_tag
def static(path):
    return _static(path)


class MediaNode(template.Node):
    def __init__(self, filename, args):
        self.filename = filename
        self.args = args

    def render(self, context):
        filename = self.filename.resolve(context)
        args = ' %s' % ' '.join(self.args) if self.args else ''
        script = filename if filename.startswith(('https://', 'http://', '//')) else _static(iri_to_uri(filename))
        return mark_safe(self.fmt % {
            'script': script,
            'args': args,
        })


def media_tag(parser, token, node_class):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument, the name of the script." % bits[0])

    filename = parser.compile_filter(bits[1])
    args = [bit for bit in bits[2:]]

    return node_class(filename, args)


class CssNode(MediaNode):
    fmt = '<link rel="stylesheet" type="text/css" href="%(script)s"%(args)s/>'


@register.tag("css")
def css_tag(parser, token):
    return media_tag(parser, token, CssNode)


def css(script, media="all"):
    return mark_safe('<link rel="stylesheet" type="text/css" href="%(script)s" media="%(media)s"/>' % {
        'script': _static(iri_to_uri(script)),
        'media': media,
    })


@register.simple_tag
def css_print(script):
    return mark_safe(css(script, media="print"))


@register.simple_tag
def css_ie(script, media="all"):
    return mark_safe("""<!--[if IE]>%s<![endif]-->""" % css(script, media))


class JsNode(MediaNode):
    fmt = '<script src="%(script)s"%(args)s></script>'


@register.tag("js")
def js_tag(parser, token):
    return media_tag(parser, token, JsNode)


def js(script):
    return mark_safe('<script type="text/javascript" src="%(script)s"></script>' % {
        'script': _static(iri_to_uri(script)),
    })


@register.simple_tag
def jquery():
    return mark_safe(js("fluo/jquery/%(jquery)s" % {
        'jquery': {True: 'jquery.min.js', False: 'jquery.js'}[JQUERY_MINIFIED],
    }))


@register.simple_tag
def jqueryui():
    minified = ".min" if JQUERY_MINIFIED else ""
    return mark_safe('''
%(jqueryui)s
%(i18n)s
''' % { # NOQA
        'jqueryui': js("fluo/jquery/jquery.ui{minified}.js".format(minified=minified)),
        'i18n': js("fluo/jquery/i18n/jquery.ui.datepicker-{language}{minified}.js".format(
            minified=minified,
            language=get_language()[:2]
        )),
    })


@register.simple_tag
def jqueryui_default_theme():
    return mark_safe(css("fluo/jquery/theme/jquery.ui.css", media="all"))


@register.simple_tag
def thickbox():
    return mark_safe("""%(css)s
<script type="text/javascript">var tb_pathToImage = "%(img)s";</script>
%(js)s""" % {
        "css": css("fluo/thickbox/css/thickbox.css", media="all"),
        "img": _static("fluo/thickbox/images/loadingAnimation.gif"),
        "js": js("fluo/thickbox/js/%(thickbox)s" % {True: 'thickbox.min.js', False: 'thickbox.js'}[JQUERY_MINIFIED]),
    })


@register.simple_tag
def jquery_ajaxqueue():
    return mark_safe(js("fluo/jquery-ajaxqueue/%(js)s" % {
        'js': {True: 'jquery.ajaxqueue.min.js', False: 'jquery.ajaxqueue.js'}[JQUERY_MINIFIED],
    }))


@register.simple_tag
def jquery_autocomplete():
    return mark_safe(js("fluo/jquery-autocomplete/%(js)s" % {
        'js': {True: 'jquery.autocomplete.min.js', False: 'jquery.autocomplete.js'}[JQUERY_MINIFIED],
    }))


@register.simple_tag
def static_url():
    """ Returns the string contained in the setting STATIC_URL. """
    return _static("")


@register.simple_tag
def media_url():
    """ Returns the string contained in the setting MEDIA_URL. """
    return MEDIA_URL
