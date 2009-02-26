=========
Shortcuts
=========

Some useful shortcuts.

render_to_string
================

Differently from :func:`~django.template.loader.render_to_string` it accepts, after the template
to render, a request object and a named keyword list (instead of passing a dict)

.. function:: render_to_string(template_name, request=None, \*\*kwargs)

If request object is given, it adds the ContextRequest.

render_to_response
==================

Differently from :func:`~django.shortcuts.render_to_response`, after the template name 
it accepts a request object, used to add a ContextRequest, a mimetype and a named keyword list
(instead of passing a dict)

.. function:: render_to_response(template_name, request=None, mimetype=None, \*\*kwargs)

