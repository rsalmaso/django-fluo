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

import django
from django.apps import apps

if apps.get_containing_app_config("django.contrib.postgres"):
    from django.contrib.postgres.fields.array import *  # noqa
    from django.contrib.postgres.fields.array import __all__ as array_all
    from django.contrib.postgres.fields.citext import *  # noqa
    from django.contrib.postgres.fields.citext import __all__ as citext_all
    from django.contrib.postgres.fields.hstore import *  # noqa
    from django.contrib.postgres.fields.hstore import __all__ as hstore_all

    if django.VERSION >= (3, 1):
        jsonb_all = []
    else:
        from django.contrib.postgres.fields.jsonb import *  # noqa
        from django.contrib.postgres.fields.jsonb import __all__ as jsonb_all
    from django.contrib.postgres.fields.ranges import *  # noqa
    from django.contrib.postgres.fields.ranges import __all__ as ranges_all

    postgres__all__ = [
        *array_all,
        *[k for k in citext_all if k not in ["CIEmailField"]],
        *hstore_all,
        *jsonb_all,
        *ranges_all,
    ]
else:
    from django.db import models

    postgres__all__ = ["CIText", "CICharField", "CITextField"]

    class CIText:
        pass

    class CICharField(models.CharField):
        pass

    class CITextField(models.TextField):
        pass


__all__ = postgres__all__
