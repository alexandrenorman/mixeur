# -*- coding: utf-8 -*-
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from dialogwatt.models import Appointment

from fac.models import Contact, File, Folder, Note, Organization
from fac.tasks.background_check_incomplete_model import (
    background_check_incomplete_model,
)


@receiver(post_save, sender=Contact)
def check_incomplete_fields_for_contact(sender, instance, **kwargs):
    background_check_incomplete_model(
        app_label="fac", model_name="Contact", pk=instance.pk
    )


@receiver(post_save, sender=Folder)
def check_incomplete_fields_for_folder(sender, instance, **kwargs):
    background_check_incomplete_model(
        app_label="fac", model_name="Folder", pk=instance.pk
    )


@receiver(post_save, sender=Organization)
def check_incomplete_fields_for_organization(sender, instance, **kwargs):
    background_check_incomplete_model(
        app_label="fac", model_name="Organization", pk=instance.pk
    )


@receiver(post_save, sender=File)
@receiver(post_save, sender=Folder)
@receiver(post_save, sender=Note)
def update_linked_object_from_folder(sender, instance, **kwargs):
    if instance.linked_object:
        instance.linked_object.updated_at = datetime.datetime.now()
        instance.linked_object.save()


@receiver(post_save, sender=Appointment)
def update_linked_object_from_appointment(sender, instance, **kwargs):
    if instance.client_or_contact:
        instance.client_or_contact.updated_at = datetime.datetime.now()
        instance.client_or_contact.save()
