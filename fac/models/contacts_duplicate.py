# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helpers.models import representation_helper


from .contact import Contact


@representation_helper
class ContactsDuplicate(models.Model):
    """
    Store duplicates
    """

    class Meta:
        verbose_name = _("Doublons de contacts")
        verbose_name_plural = _("Doublons de contacts")

    owning_group = models.ForeignKey(
        "accounts.Group",
        verbose_name=_("Groupe propriétaire"),
        on_delete=models.CASCADE,
        null=False,
        related_name="contacts_duplicate",
    )

    contacts = models.ManyToManyField(Contact, blank=True, verbose_name=_("Contacts"))
    acknowledged = models.BooleanField(verbose_name=_("Acquitté"), default=False)
    created_at = models.DateTimeField(
        verbose_name=("Date de création"), auto_now_add=True
    )


def find_duplicated_contacts():
    duplicates = {}
    alls = Contact.objects.valid()
    start = 0
    for c in alls:
        start += 1
        for c2 in alls[start:]:
            if c == c2:
                continue

            percent = c.compare_with_another_contact(c2)

            if percent > 0.8:
                keys = [c, c2]
                sorted(keys, key=lambda c: c.pk)

                if keys[0] in duplicates:
                    duplicates[keys[0]].append(keys[1])

                elif keys[1] in duplicates:
                    duplicates[keys[1]].append(keys[0])

                else:
                    for k in duplicates:
                        v = duplicates[k]
                        if c in v:
                            duplicates[k].append(c2)
                            break
                        elif c2 in v:
                            duplicates[k].append(c)
                            break
                    else:
                        duplicates[keys[0]] = keys

    return duplicates


def find_and_save_duplicated_contacts():
    duplicates = find_duplicated_contacts()
    for k in duplicates:
        existing = ContactsDuplicate.objects.all()
        for contact in duplicates[k]:
            existing = existing.filter(contacts=contact)

        if existing:
            continue

        cd = ContactsDuplicate()
        cd.save()
        for contact in duplicates[k]:
            cd.contacts.add(contact)

        cd.save()
    return
