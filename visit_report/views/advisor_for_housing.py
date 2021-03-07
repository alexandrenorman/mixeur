# -*- coding: utf-8 -*-

from django.http import JsonResponse

from rest_framework import status

from accounts.serializers import UserWithMinimalGroupSerializer

from helpers.views import (
    AdvisorRequiredApiView,
    ModelReadOnlyView,
    PreventListViewMixin,
)

from visit_report.models import Housing


class AdvisorForHousingView(
    PreventListViewMixin, AdvisorRequiredApiView, ModelReadOnlyView
):
    """"""

    def detail(self, request, *args, **kwargs):
        """
        Get :model:`visit_report.Housing` by [pk]
        """
        pk = kwargs["pk"]
        housing = Housing.objects.get(pk=pk)

        if not request.user.has_perm("visit_report/housing.view", housing):
            return JsonResponse(
                {"error": "operation not permitted"}, status=status.HTTP_403_FORBIDDEN
            )

        users = []
        for group in housing.groups.filter(is_active=True):
            users.append(group.users)

        users = [y for x in users for y in x if y.is_active]

        serializer = UserWithMinimalGroupSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
