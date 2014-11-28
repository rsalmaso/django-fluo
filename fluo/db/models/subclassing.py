# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
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

# taken and adapted from https://github.com/bradjasper/django-jsonfield.git
# Copyright (c) 2012 Brad Jasper

## This file was copied from django.db.models.fields.subclassing so that we could
## change the Creator.__set__ behavior. Read the comment below for full details.

"""
Convenience routines for creating non-trivial Field subclasses, as well as
backwards compatibility utilities.

Add SubfieldBase as the __metaclass__ for your Field subclass, implement
to_python() and the other necessary methods and everything will work seamlessly.
"""


class Creator(object):
    """
    A placeholder class that provides a way to set the attribute on the model.
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        # Usually this would call to_python, but we've changed it to pre_init
        # so that we can tell which state we're in. By passing an obj,
        # we can definitively tell if a value has already been deserialized
        # More: https://github.com/bradjasper/django-jsonfield/issues/33
        obj.__dict__[self.field.name] = self.field.pre_init(value, obj)


def make_contrib(superclass, func=None):
    """
    Returns a suitable contribute_to_class() method for the Field subclass.

    If 'func' is passed in, it is the existing contribute_to_class() method on
    the subclass and it is called before anything else. It is assumed in this
    case that the existing contribute_to_class() calls all the necessary
    superclass methods.
    """
    def contribute_to_class(self, cls, name):
        if func:
            func(self, cls, name)
        else:
            super(superclass, self).contribute_to_class(cls, name)
        setattr(cls, self.name, Creator(self))

    return contribute_to_class


class SubfieldBase(type):
    """
    A metaclass for custom Field subclasses. This ensures the model's attribute
    has the descriptor protocol attached to it.
    """
    def __new__(cls, name, bases, attrs):
        new_class = super(SubfieldBase, cls).__new__(cls, name, bases, attrs)
        new_class.contribute_to_class = make_contrib(
            new_class, attrs.get('contribute_to_class')
        )
        return new_class
