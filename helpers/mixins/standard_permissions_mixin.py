# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class StandardPermissionsMixin:
    """
    Apply standard permissions to view :
    - standard_permission_class.view
    - standard_permission_class.add
    - standard_permission_class.change

    This include the DrfNoCache mecanism which
    force re-evaluation of self.queryset because DRF is caching
    """

    def list(self, request):
        # Force re-evaluation of self.queryset because DRF is caching
        filtered_queryset = self.get_queryset()
        for obj in self.get_queryset():
            if not self.request.user.has_perm(
                f"{self.standard_permission_class}.view", obj
            ):
                filtered_queryset = filtered_queryset.exclude(pk=obj.pk)

        # serializer = self.serializer_class(filtered_queryset, many=True)
        serializer = self.get_serializer(
            filtered_queryset, context={"request": request}, many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        if not request.user.has_perm(f"{self.standard_permission_class}.view", obj):
            raise PermissionDenied

        return super().retrieve(request, pk)

    def create(self, request):
        if not request.user.has_perm(f"{self.standard_permission_class}.add"):
            raise PermissionDenied

        return super().create(request)

    def update(self, request, pk=None, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        if not request.user.has_perm(f"{self.standard_permission_class}.change", obj):
            raise PermissionDenied

        return super().update(request, pk, args, kwargs)

    def destroy(self, request, pk=None):
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        if not request.user.has_perm(f"{self.standard_permission_class}.change", obj):
            raise PermissionDenied

        return super().destroy(request, pk)
