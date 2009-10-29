==========
Decorators
==========

Some useful decorators for views.

``ajax_required``
=================

.. function:: fluo.views.decorators.ajax_required(func)

**Description:**

If the request is not ajax, throws an :class:`~django.http.HttpResponseBadRequest`

**Example:**

.. sourcecode:: python

    @ajax_required
    def ajax_view(request, *args, **kwargs):
        pass

``login_required``
==================

.. function:: fluo.views.decorators.login_required(function, required, redirect_field_name)

**Description:**

Select to protect the view based on `required` parameter.
If the view needs to be protected from anonyomous view, redirect to `redirect_field_name` view.

**Example:**

.. sourcecode:: python

    @login_required(settings.SHOULD_PROTECT)
    def upload_view(request, *args, **kwargs):
        pass

