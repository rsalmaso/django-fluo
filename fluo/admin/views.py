import operator
from functools import reduce

from django.contrib.admin.utils import lookup_needs_distinct
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.http import Http404, JsonResponse


class RelatedSearchJsonView(AutocompleteJsonView):
    search_fields = []

    def get_queryset(self):
        qs = self.model_admin.get_queryset(self.request)
        qs, search_use_distinct = self.get_search_results(self.request, qs, self.search_fields, self.term)
        if search_use_distinct:
            qs = qs.distinct()
        return qs

    def get_search_results(self, request, queryset, search_fields, search_term):
        """
        Return a tuple containing a queryset to implement the search
        and a boolean indicating if the results may contain duplicates.
        """
        # override ModelAdmin.get_search_results to use a custom search_fields

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith("^"):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith("="):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith("@"):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "get_path_info"):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        use_distinct = False
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field)) for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            use_distinct |= any(lookup_needs_distinct(queryset.model._meta, search_spec) for search_spec in orm_lookups)

        return queryset, use_distinct

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """
        if not self.search_fields:
            raise Http404("%s must have search_fields for the related_search_view." % type(self.model_admin).__name__)
        if not self.has_perm(request):
            return JsonResponse({"error": "403 Forbidden"}, status=403)

        self.term = request.GET.get("term", "")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [{"id": str(obj.pk), "text": str(obj)} for obj in context["object_list"]],
                "pagination": {"more": context["page_obj"].has_next()},
            },
        )
