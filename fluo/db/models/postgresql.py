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

from django.apps import apps


if not apps.get_containing_app_config("django.contrib.postgres"):
    __all__ = []
else:
    __all__ = [
        'ArrayField',
        'CICharField', 'CIEmailField', 'CIText', 'CITextField',
        'DateTimeRangeField', 'DateRangeField',
        'IntegerRangeField', 'BigIntegerRangeField', 'FloatRangeField',
        'JSONField',
        'HStoreField',
        'RangeField',
    ]

    from django.contrib.postgres.fields import *  # noqa
    try:
        CIText  # noqa: F405
    except NameError as ex:
        from django.db.models import CharField, EmailField, TextField

        class CIText:
            def db_type(self, connection):
                return 'citext'

        class CICharField(CIText, CharField):
            pass

        class CIEmailField(CIText, EmailField):
            pass

        class CITextField(CIText, TextField):
            pass
