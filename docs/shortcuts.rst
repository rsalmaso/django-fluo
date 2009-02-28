=========
Shortcuts
=========

Some useful shortcuts.

``render_to_string``
====================

.. function:: fluo.shortcuts.render_to_string(template_name, request=None, \*\*kwargs)

**Description:**

A simple to use function to render a template with a context.

**Required aruments:**

    * ``template_name``: the name of the template to render

**Optional arguments:**

    * ``request``: an :class:`~django.http.HttpRequest` object, it creates a RequestContext

    * ``kwargs``: a named keyword list, passed as  context to the template renderer

**Example:**

Render a mail boby message filled with only a :class:`~django.http.Context`::

    mail = render_to_string(
        'mail-template.txt',
        title='Welcome to example.com',
        from='webmaster@example.com',
    )

And the same filled with a :class:`~django.http.RequestContext` created from the ``request``::

    mail = render_to_string(
        'mail-template.txt',
        request=request,
        title='Welcome to example.com',
        from='webmaster@example.com',
    )

``render_to_response``
======================

.. function:: fluo.shortcuts.render_to_response(template_name, request=None, mimetype=None, \*\*kwargs)

**Description:**

A simple to use function to return an :class:`~HttpResponse` object.

**Required aruments:**

    * ``template_name``: the name of the template to render

**Optional arguments:**

    * ``request``: an :class:`~django.http.HttpRequest` object, it creates a RequestContext

    * ``mimetype``: the MIME type to use for the resulting document. Defaults
            to the value of the ``DEFAULT_CONTENT_TYPE`` setting.

    * ``kwargs``: a named keyword list, passed as  context to the template renderer

**Example:**

Return a :class:`~django.http.HttpResponse` filled with only a :class:`~Context` object list::

    return render_to_response(
        'template.html',
        title='User list',
        users=User.objects.all(),
    )

And the same filled with a :class:`~django.http.RequestContext` created from the ``request``::

    return render_to_response(
        'template.html',
        request=request,
        title='User list',
        users=User.objects.all(),
    )

