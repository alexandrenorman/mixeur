from types import SimpleNamespace

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.http import JsonResponse

from accounts.models import User

from fac.models import Contact, Organization, Tag
from fac.serializers import GlobalSearchSerializer

from helpers.views import AdvisorRequiredApiView


class GlobalSearchView(AdvisorRequiredApiView):
    """
    Search contacts, organizations and tags
    """

    def get(self, request, *args, **kwargs):
        query_param = request.GET.get("q", None)
        selected_type = request.GET.get("type", None)
        try:
            threshold = float(request.GET["threshold"])
        except (ValueError, KeyError):
            threshold = 0.5

        results = SimpleNamespace()

        if not selected_type or selected_type == "contacts":
            results.contacts = self._get_and_filter_contacts(
                user=request.user, query_param=query_param, threshold=threshold
            )

        if not selected_type or selected_type == "clients":
            results.clients = self._get_and_filter_client_users(
                user=request.user, query_param=query_param, threshold=threshold
            )

        if not selected_type or selected_type == "organizations":
            results.organizations = self._get_and_filter_organizations(
                user=request.user, query_param=query_param, threshold=threshold
            )

        if not selected_type or selected_type == "tags":
            results.tags = self._get_and_filter_tags(
                user=request.user, query_param=query_param, threshold=threshold
            )

        return JsonResponse(GlobalSearchSerializer(results).data)

    def _exec_query(self, user, searched_object, query_fields, query, threshold):
        all_objects = {}
        similarity_list = [TrigramSimilarity(x, query) for x in query_fields]
        similarity = Greatest(*similarity_list)
        if user:
            objects = (
                searched_object.objects.annotate(similarity=similarity)
                .accessible_by(user)
                .filter(similarity__gte=threshold)
                .order_by("-similarity")
                .values("pk", "similarity")
            )
        else:
            objects = (
                searched_object.objects.annotate(similarity=similarity)
                .filter(similarity__gte=threshold)
                .order_by("-similarity")
                .values("pk", "similarity")
            )

        for c in objects:
            all_objects[c["pk"]] = c["similarity"]

        return all_objects

    def _parse_query(self, user, searched_object, query_fields, query_param, threshold):
        all_objects = {}
        full_query_all_objects = {}
        first_pass = True

        # Full query
        full_query_all_objects = self._exec_query(
            user, searched_object, query_fields, query_param, threshold
        )

        # word by word
        for word in query_param.split():
            objects = self._exec_query(
                user, searched_object, query_fields, word, threshold
            )

            if first_pass:
                first_pass = False
                for c in objects:
                    all_objects[c] = objects[c]
            else:
                new_list = {}
                for c in objects:
                    if c in all_objects:
                        new_list[c] = all_objects[c] + objects[c]

                all_objects = new_list

        list_all_objects = []
        for c in full_query_all_objects:
            list_all_objects.append({"pk": c, "similarity": full_query_all_objects[c]})
        for c in all_objects:
            list_all_objects.append({"pk": c, "similarity": all_objects[c]})

        ordered_objects = sorted(
            list_all_objects, key=lambda contact: -contact["similarity"]
        )
        objects_pk = [x["pk"] for x in ordered_objects]

        objects = []
        for pk in objects_pk:
            objects.append(searched_object.objects.get(pk=pk))

        return remove_duplicates(objects)

    def _get_and_filter_contacts(self, user, query_param, threshold):
        return self._parse_query(
            user=user,
            searched_object=Contact,
            query_fields=[
                "first_name",
                "last_name",
                "email",
                "tags__name",
                "town",
                "zipcode",
                "address",
                "phone_cache",
                "mobile_phone_cache",
                "fax_cache",
            ],
            query_param=query_param,
            threshold=threshold,
        )

    def _get_and_filter_client_users(self, user, query_param, threshold):
        return self._parse_query(
            user=None,
            searched_object=User,
            query_fields=[
                "first_name",
                "last_name",
                "email",
                "phone_cache",
            ],
            query_param=query_param,
            threshold=threshold,
        )

    def _get_and_filter_organizations(self, user, query_param, threshold):
        return self._parse_query(
            user=user,
            searched_object=Organization,
            query_fields=[
                "type_of_organization",
                "name",
                "tags__name",
                "email",
                "reference",
                "website",
                "town",
                "zipcode",
                "address",
                "phone_cache",
                "fax_cache",
            ],
            query_param=query_param,
            threshold=threshold,
        )

    def _get_and_filter_tags(self, user, query_param, threshold):
        return self._parse_query(
            user=user,
            searched_object=Tag,
            query_fields=[
                "name",
                "name",  # Not a bug : Greatest takes at least 2 parameters !
            ],
            query_param=query_param,
            threshold=threshold,
        )


def remove_duplicates(values):
    seen = set()
    # cache add function to speed things up, cf. https://stackoverflow.com/a/480227
    seen_add = seen.add
    return [value for value in values if not (value.pk in seen or seen_add(value.pk))]
