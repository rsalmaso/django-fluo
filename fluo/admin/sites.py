# Copyright (C) 2007-2022, Raffaele Salmaso <raffaele@salmaso.org>
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

from functools import update_wrapper

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import gettext as _

__all__ = [
    "AdminSite",
]


class AdminSite(admin.AdminSite):
    def get_urls(self):
        from django.urls import path

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        return [
            path("r/<int:content_type_id>/<path:object_id>/", wrap(self.view_on_site), name="view_on_site"),
        ] + super().get_urls()

    def view_on_site(self, request, content_type_id, object_id):
        """
        Redirect to an object's page based on a content-type ID and an object ID.
        """
        # Look up the object, making sure it's got a get_absolute_url() function.
        try:
            content_type = ContentType.objects.get(pk=content_type_id)
            if not content_type.model_class():
                raise Http404(_("Content type %(ct_id)s object has no associated model") % {"ct_id": content_type_id})
            obj = content_type.get_object_for_this_type(pk=object_id)
        except (ObjectDoesNotExist, ValueError):
            raise Http404(
                _("Content type %(ct_id)s object %(obj_id)s doesn't exist")
                % {"ct_id": content_type_id, "obj_id": object_id},
            )

        try:
            get_absolute_url = obj.get_absolute_url
        except AttributeError:
            raise Http404(
                _("%(ct_name)s objects don't have a get_absolute_url() method") % {"ct_name": content_type.name},
            )
        absurl = get_absolute_url()

        return HttpResponseRedirect(absurl)
