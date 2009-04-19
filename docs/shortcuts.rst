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

    * ``content_type``: an alias for ``mimetype`` that corresponds more closely to the HTTP
            header Content-Type.

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

``render_from_string``
======================

.. function:: fluo.shortcuts.render_from_string(template_string, request=None, \*\*kwargs)

**Description:**

A simple to use function to render a string template with a context.

**Required aruments:**

    * ``template_string``: the name of the template to render

**Optional arguments:**

    * ``request``: an :class:`~django.http.HttpRequest` object, it creates a RequestContext

    * ``kwargs``: a named keyword list, passed as  context to the template renderer

**Example:**

Render a mail boby message filled with only a :class:`~django.http.Context`::

    TEMPLATE = """
    From: {{ from }}

    {{ body }}
    """

    mail = render_from_string(
        TEMPLATE,
        from='webmaster@example.com',
        body='Welcome to example.com',
    )

And the same filled with a :class:`~django.http.RequestContext` created from the ``request``::

    TEMPLATE = """
    From: {{ from }}

    {{ body }}
    """

    mail = render_from_string(
        TEMPLATE,
        request=request,
        from='webmaster@example.com',
        body='Welcome to example.com',
    )

``reverse``
===========

.. function:: fluo.shortcuts.reverse(viewname, \*args, \*\*kwargs)

**Description:**

A simpler ``reverse`` function which wraps the :function:`django.core.urlresolvers.reverse` functionality
for common use. For more complex use to use function to render a template with a context.

**Required aruments:**

    * ``viewname``: the name of the template to render

**Optional arguments:**

    * ``args``: a positional arguments list, used for URL matching

    * ``kwargs``: a named keyword list, used for URL matching

**Example:**

Retrieve the URL for `summary` view::

    # in urls.py

    url(r'(?P<year>\d{4})/(?P<month>\d{1,2})/((?P<day>\d{1,2}))/', summary_view, name='summary')

    # in views.py

    from fluo.shortcuts import reverse

    def myview(request):
        return HttpResponseRedirect(reverse('summary', 1945, day=8, month=9))

