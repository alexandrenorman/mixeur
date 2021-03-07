from core.models import MixeurBaseModel

from django.db import models
from django.utils.translation import ugettext_lazy as _


class TypeValorizationQueryset(models.QuerySet):
    def accessible_by(self, user):
        if user.is_administrator:
            return self

        return self.filter(groups=user.group)


class TypeValorizationManager(models.Manager.from_queryset(TypeValorizationQueryset)):
    def get_queryset(self):
        return super().get_queryset()


class TypeValorization(MixeurBaseModel):
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    groups = models.ManyToManyField("accounts.Group", related_name="type_valorizations")

    objects = TypeValorizationManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Type de valorisation")
        verbose_name_plural = _("Types de valorisation")
