# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status


from helpers.views import LoginRequiredApiView

from visit_report.forms import HousingForm
from visit_report.models import Housing
from visit_report.serializers import HousingSerializer


class HousingView(LoginRequiredApiView):
    """
    HousingView requires authenticated user

    get :model:`visit_report.Housing`

    """

    def get(self, request, *args, **kwargs):
        """"""
        if "pk" in kwargs:
            return self.detail(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def detail(self, request, *args, **kwargs):
        """
        Get :model:`visit_report.Housing` by [pk]
        """
        pk = kwargs["pk"]
        housing = Housing.objects.get(pk=pk)

        if not request.user.has_perm("visit_report/housing.view", housing):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = HousingSerializer(housing)
        return JsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):  # NOQA: A003
        """
        List :model:`visit_report.Housing`
        """
        housings = Housing.objects.all()
        contact_type = request.GET.get("contact_type")
        contact_id = request.GET.get("contact_id")
        if contact_type and contact_id:
            content_type = ContentType.objects.get(app_label="fac", model=contact_type)
            housings = housings.filter(
                contact_or_organization_id=contact_id, content_type=content_type
            )

        allowed_housings = [
            x for x in housings if request.user.has_perm("visit_report/housing.view", x)
        ]

        serializer = HousingSerializer(allowed_housings, many=True)
        return JsonResponse(serializer.data, safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Delete :model:`visit_report.Housing` by [pk]

        Must have housing.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        pk = key
        housing = get_object_or_404(Housing, pk=pk)

        if not request.user.has_perm("visit_report/housing.change", housing):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        housing.delete()

        return JsonResponse({"ok": "Deleted"})

    def patch(self, request, *args, **kwargs):
        """
        Updtae :model:`visit_report.Housing` by [pk]

        Must have housing.change permission
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        housing_data = json.loads(request.body)

        pk = key
        housing = get_object_or_404(Housing, pk=pk)

        if not request.user.has_perm("visit_report/housing.change", housing):
            return JsonResponse(
                {"error": "change not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        form = HousingForm(housing_data, instance=housing)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=pk)

    def post(self, request, *args, **kwargs):
        """
        Create :model:`visit_report.Housing` by [pk]

        Must be an expert or a client which edit it's own housing
        """
        housing_data = json.loads(request.body)

        form = HousingForm(housing_data)
        if form.is_valid():
            housing = form.save()
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get(request, pk=housing.pk)
