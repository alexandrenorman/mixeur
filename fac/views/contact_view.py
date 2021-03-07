# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import JsonResponse

import phonenumbers

from accounts.models import User
from accounts.serializers import UserNameSerializer

from core.forms import SearchForm

from fac.forms import ContactForm, ProjectSearchForm, ReferentsSearchForm
from fac.models import Contact, Project, Tag
from fac.serializers import (
    ContactCSVSerializer,
    ContactDropdownListSerializer,
    ContactEditSerializer,
    ContactIconSerializer,
    ContactMapSerializer,
    ContactNewsletterSerializer,
    ProjectNameSerializer,
)

from helpers.views import ExpertRequiredApiView, ModelView


class ContactView(ModelView, ExpertRequiredApiView):
    """
    ContactView requires authenticated user

    get :model:`fac.Contact`

    """

    model = Contact
    form = ContactForm
    perm_module = "fac/contact"

    def _is_request_for_csv(self, request):
        return request.GET.get("csv") == "1"

    def _is_request_for_map(self, request):
        return request.GET.get("map") == "1"

    def _is_request_for_dropdown_list(self, request):
        return request.GET.get("dropdown") == "1"

    def _is_request_for_newsletter(self, request):
        return request.GET.get("newsletter") == "1"

    def get_serializer(self, request, call):
        """
        :returns :
          - full contact serializer for viewing/editing
          - simple contact serializer for listing
          - csv contact serializer for exporting contacts
          - map serializer for map display
        """
        if self._is_request_for_csv(request):
            return ContactCSVSerializer

        if self._is_request_for_map(request):
            return ContactMapSerializer

        if self._is_request_for_dropdown_list(request):
            return ContactDropdownListSerializer

        if self._is_request_for_newsletter(request):
            return ContactNewsletterSerializer

        if call == "LIST":
            return ContactIconSerializer

        return ContactEditSerializer

    def _filter_on_project(self, request, contacts):
        if self._is_get_parameter_is_valid(request, "project"):
            project_form = ProjectSearchForm(request.GET)
            if project_form.is_valid():
                project = project_form.cleaned_data["project"]
                contacts = contacts.filter(folders__model__project__pk=project.pk)

        return contacts

    def _filter_on_referents(self, request, contacts):
        if self._is_get_parameter_is_valid(request, "referents"):
            referents_list = [int(x) for x in request.GET["referents"].split(",")]
            data = {
                "referents": referents_list,
            }
            referents_form = ReferentsSearchForm(data)
            if referents_form.is_valid():
                referents = referents_form.cleaned_data["referents"]
                contacts = contacts.filter(referents__in=referents)

        return contacts

    def _get_phone(self, value):
        try:
            phone_number = phonenumbers.parse(value, "FR")  # NOQA: F841
        except phonenumbers.NumberParseException:
            return None

        return phone_number.national_number

    def _filter_on_search_query(self, request, contacts):
        if self._is_get_parameter_is_valid(request, "q"):
            query_form = SearchForm(request.GET)
            if query_form.is_valid():
                query = query_form.cleaned_data["q"]

                for word in query.split():
                    if self._get_phone(word):
                        phone = f"0{self._get_phone(word)}"
                        contacts = contacts.filter(
                            Q(phone_cache__icontains=phone)
                            | Q(mobile_phone_cache__icontains=phone)
                            | Q(fax_cache__icontains=phone)
                        )
                    else:
                        contacts = contacts.filter(
                            Q(last_name__icontains=word)
                            | Q(first_name__icontains=word)
                            | Q(email__icontains=word)
                            | Q(address__icontains=word)
                            | Q(town__icontains=word)
                            | Q(zipcode__icontains=word)
                            | Q(phone_cache__icontains=word)
                            | Q(mobile_phone_cache__icontains=word)
                            | Q(fax_cache__icontains=word)
                        )

        return contacts

    def filter(self, request, queryset):  # NOQA: A003
        contacts = queryset
        contacts = self._filter_on_project(request, contacts)
        contacts = self._filter_on_referents(request, contacts)
        contacts = self._filter_on_search_query(request, contacts)

        contacts = contacts.distinct()

        return contacts

    def list(self, request, *args, **kwargs):  # NOQA: A003
        objects = self.model.objects.all().accessible_by(request.user)

        if self._is_request_for_dropdown_list(request):
            objects = objects.order_by("first_name", "last_name")
            serializer = self.get_serializer(request, "LIST")(objects, many=True)
            json_return = serializer.data
            return JsonResponse(json_return, safe=False)

        referents = User.objects.filter(
            pk__in={
                x["referents"]
                for x in objects.exclude(referents=None).values("referents")
                if x["referents"]
            }
        )

        projects = Project.objects.filter(
            pk__in={
                x["folders__model__project"]
                for x in objects.exclude(folders=None).values("folders__model__project")
                if x["folders__model__project"]
            }
        )

        objects = self.filter(request=request, queryset=objects)

        if self._is_request_for_map(request):
            objects = objects.exclude(lat=0, lon=0)
        else:
            objects = self._sort_objects(request, objects)

        total_records = objects.count()

        if self._is_request_for_pagination(request):
            objects = self._limit_objects_according_to_pagination(request, objects)

        objects = objects.prefetch_related(
            "tags",
            "owning_group",
            "client_account",
            "memberoforganization_set__organization",
            "referents",
            "folders__model__project",
            "folders__model__statuses__action_models",
            "folders__actions__model",
        )

        serializer = self.get_serializer(request, "LIST")(objects, many=True)

        if self._is_request_for_pagination(request):
            referents_serializer = UserNameSerializer(referents, many=True)
            projects_serializer = ProjectNameSerializer(projects, many=True)

            json_return = {
                "total_records": total_records,
                "records": serializer.data,
                "projects": projects_serializer.data,
                "referents": referents_serializer.data,
            }
        else:
            json_return = serializer.data

        return JsonResponse(json_return, safe=False)

    def post_save(self, request, instance, contact_data, created):
        """
        Save contact's M2M fields
        """
        self._save_m2m_from_select(
            instance=instance,
            attribute="tags",
            model_queryset=Tag.objects,
            data=contact_data.get("tags", []),
        )
        self._save_m2m_from_select(
            instance=instance,
            attribute="referents",
            model_queryset=User.advisors,
            data=contact_data.get("referents", []),
        )
