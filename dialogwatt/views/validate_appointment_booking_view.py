from helpers.views import ModelReadOnlyView, ApiView, PreventListViewMixin
from django.http import JsonResponse
from rest_framework import status

# from dialogwatt.helpers.find_slots import FindSlots
from dialogwatt.models import Appointment
from dialogwatt.serializers import AppointmentBookInfoSerializer


class ValidateAppointmentBookingView(ModelReadOnlyView, PreventListViewMixin, ApiView):
    """
    Validate a pre-booked appointment and return the whole validated appointment
    """

    def patch(self, request, *args, **kwargs):
        """
        """
        try:
            uuid = kwargs["uuid"]
        except KeyError:
            return JsonResponse(
                {"Error": "Missing appointment uuid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment = Appointment.active.get(uuid=uuid)
        if request.user.pk != appointment.client_or_contact.pk:
            return JsonResponse(
                {
                    "error": "La réservation demandée n'a pas été effectuée avec votre compte."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if not appointment:
            return JsonResponse(
                {"message": "La réservation temporaire du rendez-vous est expirée."},
                status=status.HTTP_404_NOT_FOUND,
            )

        appointment.status = "validated"
        appointment.save()

        serializer = AppointmentBookInfoSerializer(appointment)
        return JsonResponse(serializer.data)
