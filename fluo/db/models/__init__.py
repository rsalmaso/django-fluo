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

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.db.models import *  # noqa: F401,F403
from django.db.models import __all__ as django_all

from .fields import *  # noqa: F401,F403
from .fields import __all__ as fields_all
from .models import *  # noqa: F401,F403
from .models import __all__ as models_all
from .postgresql import *  # noqa: F401,F403
from .postgresql import __all__ as postgresql_all

__all__ = [
    *[model for model in django_all if model not in ["EmailField", "SlugField", "URLField"]],
    *fields_all,
    *models_all,
    *postgresql_all,
    "GenericForeignKey",
    "GenericRelation",
    "ContentType",
    "ContentTypeManager",
]
