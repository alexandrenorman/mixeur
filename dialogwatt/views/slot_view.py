# -*- coding: utf-8 -*-
# from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from helpers.views import ApiView, ModelView

from dialogwatt.models import Slot, Reason
from dialogwatt.forms import SlotForm
from dialogwatt.serializers import SlotForSchedulerSerializer
from django.core.exceptions import ValidationError
from accounts.models import User

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


class SlotView(ModelView, ApiView):
    """
    SlotView requires authenticated user

    get :model:`dialogwatt.Slot`

    """

    model = Slot
    form = SlotForm
    serializer = SlotForSchedulerSerializer
    perm_module = "dialogwatt/slot"

    def filter(self, request, queryset):
        active_reasons = Reason.objects.filter(is_active=True)
        queryset = Slot.active.filter(reasons__in=active_reasons).distinct()

        if "from" in request.GET:
            queryset = queryset.filter(start_date__gte=request.GET["from"])
        if "to" in request.GET:
            queryset = queryset.filter(end_date__lt=request.GET["to"])
        if "for_a_week_from" in request.GET:
            start = parse(request.GET["for_a_week_from"])
            end = start + relativedelta(days=7)
            queryset = queryset.filter(start_date__gte=start, end_date__lt=end)
        if "place" in request.GET:
            queryset = queryset.filter(place__exact=request.GET["place"])

        queryset = queryset.select_related("group", "place").prefetch_related(
            "catchment_area", "advisors"
        )

        return queryset

    # def get_serializer(self, request, call):
    #     if "from" in request.GET:
    #         return SlotForSchedulerSerializer
    #
    #     return self.serializer

    def post_save(self, request, slot, slot_data, created):
        """
        Save advisors as M2M field
        """
        # advisors_id = [x["pk"] for x in slot_data["advisors"]]
        advisors_id = slot_data["advisors"]
        for pk in advisors_id:
            try:
                advisor = User.advisors.get(pk=pk)  # NOQA:F841
            except Exception:
                raise ValidationError(f"Le conseiller {pk} n'existe pas.")

        slot.advisors.clear()
        slot.advisors.add(*advisors_id)

        # reasons_id = [x["pk"] for x in slot_data["reasons"]]
        reasons_id = slot_data["reasons"]
        if len(reasons_id) == 0:
            raise ValidationError(
                "Un créneau doit être associé à au moins un motif de rendez-vous"
            )

        for pk in reasons_id:
            try:
                reason = Reason.objects.get(pk=pk)  # NOQA:F841
            except Exception:
                raise ValidationError(f"Le motif de rdv {pk} n'existe pas.")

        slot.reasons.clear()
        slot.reasons.add(*reasons_id)

    def delete(self, request, *args, **kwargs):
        """
        Do not delete model but set status to "cancelled"
        """
        try:
            key = kwargs["pk"]
        except KeyError:
            return JsonResponse(
                {"Error": "Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        pk = key
        obj = get_object_or_404(self.model, pk=pk)

        perm = self.get_perm_module(request, "DELETE")
        if perm:
            if not request.user.has_perm(f"{perm}.delete", obj):
                return JsonResponse(
                    {"error": "delete not permitted"}, status=status.HTTP_403_FORBIDDEN
                )

        with transaction.atomic():
            obj.status = "cancelled"
            obj.save()

        return JsonResponse({"ok": "Deleted"})
