# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import get_object_or_404


from fac.models import List, Tag, Contact, Organization, MemberOfOrganization
from fac.forms import ListForm
from fac.serializers import ListSerializer, ListCSVSerializer

from helpers.views import ExpertRequiredApiView, ModelView


class ListView(ModelView, ExpertRequiredApiView):
    """
    List View
    """

    model = List
    form = ListForm
    serializer = ListSerializer
    perm_module = "list"

    def get_serializer(self, request, call):
        if request.GET.get("csv") == "1":
            return ListCSVSerializer

        return ListSerializer

    def post_save(self, request, instance, list_data, created):
        """
        Save object's M2M fields
        """

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="tags",
            model_queryset=Tag.objects,
            data=list_data.get("tags", []),
        )

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="contacts",
            model_queryset=Contact.objects,
            data=list_data.get("contacts", []),
        )

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="organizations",
            model_queryset=Organization.objects,
            data=list_data.get("organizations", []),
        )

        self._save_m2m_from_double_list_select(
            instance=instance,
            attribute="lists",
            model_queryset=List.objects,
            data=list_data.get("lists", []),
        )

    def filter(self, request, queryset):
        # If we have these two parameter, we filter lists to get only
        # those which have the object inside the list of contacts
        type_of_object = request.GET.get("type")
        object_id = request.GET.get("object_id")

        if type_of_object and object_id:
            if type_of_object == "contact":
                contact = get_object_or_404(Contact, pk=object_id)
                organizations_of_contact = MemberOfOrganization.objects.filter(
                    contact=contact
                ).values_list("organization", flat=True)
                list_pks_where_contact_is_present = List.objects.filter(
                    Q(tags__in=contact.tags.all())
                    | Q(
                        use_organizations_as_contacts=False,
                        organizations__in=organizations_of_contact,
                    )
                    | Q(contacts__pk=contact.pk)
                ).values_list("pk", flat=True)
                queryset = queryset.filter(
                    Q(pk__in=[list_pks_where_contact_is_present])
                    | Q(lists__pk__in=[list_pks_where_contact_is_present])
                )

            elif type_of_object == "organization":
                organization = get_object_or_404(Organization, pk=object_id)
                queryset = queryset.filter(
                    Q(tags__in=organization.tags.all())
                    | Q(
                        use_organizations_as_contacts=True,
                        organizations__pk=organization.pk,
                    )
                )

        return queryset.distinct("pk")
