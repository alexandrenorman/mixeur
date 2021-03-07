# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from core.models import MixeurBaseModel


class StoreDataWithDefaultValueByKey(MixeurBaseModel):
    """
    Mixin for storing value with a unique default value for all
    and a unique default value for each item associated by key
    """

    class Meta:
        abstract = True
        ordering = ("created_at",)

    is_default_value = models.BooleanField(
        _("est une valeur par défaut"), default=False
    )

    @classmethod
    def default_value(cls, key=None):
        """
        Return default value which is:
        - default value for the key if exists
        - else generic default value if exists
        - else None
        """
        if key:
            if cls.objects.filter(key=key).exists():
                return cls.objects.filter(key=key).first()

        if cls.objects.filter(key=None).exists():
            return cls.objects.filter(key=None).first()

        return None

    def clean(self):
        """
        verify that:
        - an unique value exists without a key
        - an unique value exists with a key
        """
        if self.is_default_value:
            if (
                self.key is None
                and self.__class__.objects.exclude(pk=self.pk)
                .filter(key=None, is_default_value=True)
                .exists()
            ):
                raise ValidationError(
                    "Une seule valeur par défaut générique est possible"
                )

            if (
                self.key is not None
                and self.__class__.objects.exclude(pk=self.pk)
                .filter(key=self.key, is_default_value=True)
                .exists()
            ):
                raise ValidationError(
                    "Une seule valeur par défaut par clef est possible"
                )

        else:
            if self.key is None:
                raise ValidationError(
                    "Une valeur non générique doit être associée à une clef"
                )
        return super().clean()
