# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
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
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class AdminImageFileWidget(forms.FileInput):
    def __init__(self, attrs=None):
        super(AdminImageFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('''
<div>
    <div style="float: left; vertical-align: middle;">
        <a target="_blank" href="%(url)s"><img src="%(url)s" width="40px"/></a>
    </div>
    <div style="padding-left: 20px; float: left; vertical-align: middle;">
        %(text)s <a target="_blank" href="%(url)s">%(value)s</a>
        <br />
        %(change)s ''' % {
                'text': _('Currently:'),
                'url': value.url,
                'value': value,
                'change': _('Change:'),
            })
        output.append(super(AdminImageFileWidget, self).render(name, value, attrs))
        output.append('</div>')
        if value and hasattr(value, "url"):
            output.append('</div>')
        return mark_safe(u''.join(output))
