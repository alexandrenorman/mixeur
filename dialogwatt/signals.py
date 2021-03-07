# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dialogwatt.models import Appointment


@receiver(post_save, sender=Appointment)
@receiver(post_delete, sender=Appointment)
def update_slot_when_appointment_change(sender, instance, **kwargs):
    if instance.slot:
        instance.slot.updated_at = None
        instance.slot.save()
