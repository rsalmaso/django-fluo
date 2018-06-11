# Copyright (C) 2007-2018, Raffaele Salmaso <raffaele@salmaso.org>
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

import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils.encoding import force_text
from django.utils.functional import Promise

__all__ = [
    'decoder', 'encoder', 'scanner',
    'dump', 'dumps',
    'load', 'loads',
]


class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):  # noqa
        if isinstance(obj, QuerySet):
            return tuple(obj)
        elif hasattr(obj, 'tolist'):
            # Numpy arrays and array scalars.
            return obj.tolist()
        elif hasattr(obj, '__getitem__'):
            try:
                return dict(obj)
            except:
                pass
        elif hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super().default(obj)


decoder = json.decoder
encoder = json.encoder
scanner = json.scanner


def dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, **kw): # NOQA
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the some chunks written to ``fp``
    may be ``unicode`` instances, subject to normal Python ``str`` to
    ``unicode`` coercion rules. Unless ``fp.write()`` explicitly
    understands ``unicode`` (as in ``codecs.getwriter()``) this is likely
    to cause an error.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)
    in strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If ``separators`` is an ``(item_separator, dict_separator)`` tuple
    then it will be used instead of the default ``(', ', ': ')`` separators.
    ``(',', ':')`` is the most compact JSON representation.

    ``encoding`` is the character encoding for str instances, default is UTF-8.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``DjangoJSONEncoder`` is used.

    """
    cls = cls or JSONEncoder
    kwargs = {
        "obj": obj,
        "fp": fp,
        "skipkeys": skipkeys,
        "ensure_ascii": ensure_ascii,
        "check_circular": check_circular,
        "allow_nan": allow_nan,
        "cls": cls,
        "indent": indent,
        "separators": separators,
        "default": default,
    }
    kwargs.update(kw)

    return json.dump(**kwargs)


def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, **kw): # NOQA
    """Serialize ``obj`` to a JSON formatted ``str``.

    If ``skipkeys`` is false then ``dict`` keys that are not basic types
    (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``)
    will be skipped instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the return value will be a
    ``unicode`` instance subject to normal Python ``str`` to ``unicode``
    coercion rules instead of being escaped to an ASCII ``str``.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
    strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    If ``separators`` is an ``(item_separator, dict_separator)`` tuple
    then it will be used instead of the default ``(', ', ': ')`` separators.
    ``(',', ':')`` is the most compact JSON representation.

    ``encoding`` is the character encoding for str instances, default is UTF-8.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``DjangoJSONEncoder`` is used.

    """
    cls = cls or JSONEncoder
    kwargs = {
        "obj": obj,
        "skipkeys": skipkeys,
        "ensure_ascii": ensure_ascii,
        "check_circular": check_circular,
        "allow_nan": allow_nan,
        "cls": cls,
        "indent": indent,
        "separators": separators,
        "default": default,
    }
    kwargs.update(kw)

    return json.dumps(**kwargs)


def load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw): # NOQA
    kwargs = {
        "fp": fp,
        "cls": cls,
        "object_hook": object_hook,
        "parse_float": parse_float,
        "parse_int": parse_int,
        "parse_constant": parse_constant,
        "object_pairs_hook": object_pairs_hook,
    }
    kwargs.update(kw)

    return json.load(**kwargs)
load.__doc__ = json.load.__doc__


def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw): # NOQA
    kwargs = {
        "s": s,
        "cls": cls,
        "object_hook": object_hook,
        "parse_float": parse_float,
        "parse_int": parse_int,
        "parse_constant": parse_constant,
        "object_pairs_hook": object_pairs_hook,
    }
    kwargs.update(kw)

    return json.loads(**kwargs)
loads.__doc__ = json.loads.__doc__
