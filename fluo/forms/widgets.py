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

# Copyright (C) 2007 Michael Trier
# ForeignKeySearchInput taken from django-extensions

import datetime
import re

from django import forms
from django.contrib.admin.widgets import (
    AdminDateWidget as DateWidget,
    AdminSplitDateTime as DateTimeWidget,
    AdminTimeWidget as TimeWidget,
)
from django.forms.utils import flatatt
from django.utils.dates import MONTHS
from django.utils.encoding import smart_text
from django.utils.html import escape
from django.utils.safestring import mark_safe

__all__ = [
    "DateWidget",
    "TimeWidget",
    "DateTimeWidget",
    "GroupedSelect",
    "SelectYearWidget",
    "SelectMonthYearWidget",
    "TimeDeltaWidget",
]


RE_DATE = re.compile(r"(\d{4})-(\d\d?)-(\d\d?)$")


# taken and adapted from http://djangosnippets.org/snippets/200/
class GroupedSelect(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, name=name)
        output = ["<select%s>" % flatatt(final_attrs)]
        str_value = smart_text(value)
        for group_label, group in self.choices:
            if group_label:  # should belong to an optgroup
                group_label = smart_text(group_label)
                output.append('<optgroup label="%s">' % escape(group_label))
            for k, v in group:
                option_value = smart_text(k)
                option_label = smart_text(v)
                selected_html = (option_value == str_value) and ' selected="selected"' or ""
                output.append(
                    '<option value="%s"%s>%s</option>' % (escape(option_value), selected_html, escape(option_label))
                )
            if group_label:
                output.append("</optgroup>")
        output.append("</select>")
        return mark_safe("\n".join(output))


class SelectYearWidget(forms.Widget):
    none_value = (0, "---")
    year_field = "%s_year"

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

    def render(self, name, value, attrs=None):
        try:
            year_val = value.year
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, str):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if "id" in self.attrs:
            id_ = self.attrs["id"]
        else:
            id_ = "id_%s" % name

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=self.year_field % id_)
        s = forms.Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe("\n".join(output))

    def id_for_label(self, id_):
        return "%s_year" % id_

    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        if y == "0":
            return None
        if y:
            return "%s-%s-%s" % (y, 1, 1)
        return data.get(name, None)


class SelectMonthYearWidget(forms.Widget):
    none_value = (0, "---")
    month_field = "%s_month"
    year_field = "%s_year"

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, str):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if "id" in self.attrs:
            id_ = self.attrs["id"]
        else:
            id_ = "id_%s" % name

        month_choices = MONTHS.items()
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = forms.Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs["id"] = self.year_field % id_
        s = forms.Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe("\n".join(output))

    def id_for_label(self, id_):
        return "%s_month" % id_

    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m == "0":
            return "%s-%s-%s" % (y, 1, 1)
        if y and m:
            return "%s-%s-%s" % (y, m, 1)
        return data.get(name, None)


class TimeDeltaWidget(forms.MultiWidget):
    """Input accurate timing. IntegerFields for hours, minutes, seconds and milliseconds."""

    def __init__(self, milliseconds=False, attrs=None):
        attrs = attrs if attrs is not None else {"size": 2, "maxlength": 2, "style": "width:auto;"}
        self.show_milliseconds = milliseconds
        self.NUM_FIELDS = 4 if milliseconds else 3
        widgets = [forms.TextInput(attrs=attrs)] * self.NUM_FIELDS
        super().__init__(widgets, attrs)

    def format_output(self, widgets):
        widgets.insert(1, " : ")
        widgets.insert(3, " : ")
        if self.show_milliseconds:
            widgets.insert(5, " . ")
        return mark_safe("".join(widgets))

    def decompress(self, value):
        if value:
            return [
                "%02d" % (value / 3600),
                "%02d" % (value % 3600 / 60),
                "%02d" % (value % 3600 % 60),
                "%03d" % (value % 1 * 1000),
            ][: self.NUM_FIELDS]
        return [None] * self.NUM_FIELDS
