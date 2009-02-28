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

