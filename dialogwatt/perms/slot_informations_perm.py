# -*- coding: utf-8 -*-
from simple_perms import PermissionLogic, register
from helpers.mixins import BasicPermissionLogicMixin


class SlotInformationsPermissionLogic(BasicPermissionLogicMixin, PermissionLogic):
    def view(self, user, slot, *args):
        """
        Permissions for viewing extensive informations about Slots
        """
        return True


register("dialogwatt/slot_informations", SlotInformationsPermissionLogic)
