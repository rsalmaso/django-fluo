=====
Admin
=====

Fluo include a customized ``admin`` application, which inherits all `django.contrib.admin`,
so you can use `fluo.admin` instead of `django.contrib.admin`.

Customization
=============

`templates/admin/filter.html`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The admin filter interface is implemented as a select choices instead of a flatten list. It save
a lot of space when you have a lot of filters.

``ModelAdmin.save_on_top``
~~~~~~~~~~~~~~~~~~~~~~~~~~

It's set to ``True`` for all :class:`~django.contrib.admin.ModelAdmin` s.

:class:`~OrderedModelAdmin`
===========================

Useful for :class:`~fluo.db.models.OrderedModel` subclasses: it implements an interface
to simplify the ordering change of the model.

:class:`~TreeOrderedModelAdmin`
===============================

Useful for :class:`~fluo.db.models.TreeOrderedModel` subclasses.

