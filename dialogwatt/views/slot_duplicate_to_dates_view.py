# -*- coding: utf-8 -*-
import json
import uuid
import pytz

from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from helpers.views import AdvisorRequiredApiView
from django.http import JsonResponse
from rest_framework import status


from dialogwatt.forms import SlotDuplicateToDatesForm


class SlotDuplicateToDatesView(AdvisorRequiredApiView):
    def post(self, request, *args, **kwargs):
        """
        """
        object_data = json.loads(request.body)
        form = SlotDuplicateToDatesForm(object_data)

        if form.is_valid():
            slot = form.cleaned_data["slot"]

            if not request.user.has_perm("dialogwatt/slot.create", slot):
                return JsonResponse(
                    {"error": "creation not permitted"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            dates = form.cleaned_data["dates"]

            tz_europe = pytz.timezone("Europe/Paris")

            start_date = slot.start_date.astimezone(tz_europe)
            end_date = slot.end_date.astimezone(tz_europe)
            advisors = slot.advisors.all()
            reasons = slot.reasons.all()

            pklist = []

            with transaction.atomic():
                for date in dates:
                    slot.pk = None
                    slot.created_at = timezone.now()
                    slot.updated_at = timezone.now()
                    slot.uuid = uuid.uuid4()

                    slot.start_date = dst_stabilize(
                        start_date,
                        (
                            start_date
                            + relativedelta(year=date.year)
                            + relativedelta(month=date.month)
                            + relativedelta(day=date.day)
                        ).astimezone(tz_europe),
                    )
                    slot.end_date = dst_stabilize(
                        end_date,
                        (
                            end_date
                            + relativedelta(year=date.year)
                            + relativedelta(month=date.month)
                            + relativedelta(day=date.day)
                        ).astimezone(tz_europe),
                    )

                    slot.save()
                    for advisor in advisors:
                        slot.advisors.add(advisor)
                    for reason in reasons:
                        slot.reasons.add(reason)

                    pklist.append(slot.pk)

                return JsonResponse({"CREATED": pklist})

        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)


def dst_stabilize(from_datetime, to_datetime):
    return to_datetime + from_datetime.dst() - to_datetime.dst()
