=====
Admin
=====

Fluo include a customized ``admin`` application, which inherits all `django.contrib.admin`,
so you can use `fluo.admin` instead of `django.contrib.admin`.

Customization
=============

``ModelAdmin.save_on_top``
~~~~~~~~~~~~~~~~~~~~~~~~~~

It's set to ``True`` for all :class:`~django.contrib.admin.ModelAdmin` s.

:class:`~django.contrib.auth.models.User`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`~django.contrib.auth.models.User` admin interface is extended to display in `changelist` view
the `is_superuser` and `is_staff` flags.

``templates/admin/filter.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The admin filter interface is implemented as a select choices instead of a flatten list. It save
a lot of space when you have a lot of filters.

``templates/admin/custom_base.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``custom_base.html`` extends the `userlink` block from ``base.html`` template adding:

    * a `Back to site` link which redirect to `/`
    * a `languages` block, useful to change the site language

``templates/admin/base_site.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``base_site.html`` template inherit from the fluo custom ``custom_base.html`` template. It permits to
customise the `title` and the `branding` blocks.

``templates/admin/filter.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The admin filter interface is implemented as a select choices instead of a flatten list. It save
a lot of space when you have a lot of filters.

ModelAdmin extensions
=====================

:class:`~fluo..admin.OrderedModelAdmin`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful for :class:`~fluo.db.models.OrderedModel` subclasses: it implements an interface
to simplify the ordering change of the model.

:class:`~fluo.admin.TreeOrderedModelAdmin`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful for :class:`~fluo.db.models.TreeOrderedModel` subclasses.

Widgets
=======

:class:`~fluo.admin.widget.AdminImageFileWidget`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overwrite the standard ImageFileWidget and show the image in a little box, other than filename.

NOTE: actually it shows the original image, scaled to 40px. So beware of big images (this will
change in future with the creation of a small thumbnail).

