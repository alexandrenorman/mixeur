# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register

from dialogwatt.models import Appointment

from helpers.mixins import BasicPermissionLogicMixin


class AppointmentPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, appointment, *args):
        """
        Permissions for viewing Appointment
        """
        if user.is_anonymous:
            return False

        if user.is_client and appointment.client_or_contact == user:
            return True

        if user.is_administrator:
            return True

        if user.is_manager:
            return False

        if user.is_advisor and user.group == appointment.group:
            return True

        return self.admin_permission(user, appointment, *args)

    def change_waiting(self, user, appointment, *args):
        """
        Permissions for changing Appointment

        It allow a client to change an appointment if it's status is "waiting"
        """
        if (
            user.is_client
            and appointment.client_or_contact is None
            and appointment.status == Appointment.WAITING
        ):
            return True

        return False

    change = view
    delete = view
    create = view


register("dialogwatt/appointment", AppointmentPermissionLogic)
