# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class KeepModelHistoryQuerySet(models.QuerySet):
    """
    Queryset for using with KeepModelHistoryMixin

    WARNING: It overides the queryset all
    """

    def get_history_for_object(self, obj):
        """
        Get historic states of an object

        Parameters:
        obj -- object for whitch history will be returned
        """
        return (
            self.filter(keep_history_value=True)
            .filter(keep_history_relates_to=obj)
            .order_by("pk")
        )

    def all(self):
        """
        Returns all objects except those who are history
        """
        return self.filter(keep_history_value=False)

    def all_including_history(self):
        """
        Returns all objects including history
        """
        return super(KeepModelHistoryQuerySet, self).all()


class KeepModelHistoryManager(models.Manager):
    """
    Manager for using KeepModelHistoryManager
    """

    def get_queryset(self):
        return KeepModelHistoryQuerySet(self.model, using=self._db)

    def history_for_object(self, obj):
        return self.get_queryset().get_history_for_object(obj)

    def all(self):
        return self.get_queryset().all()

    def all_including_history(self):
        return self.get_queryset().all_including_history()


class KeepModelHistoryMixin(models.Model):
    """
    Abstract mixin for keeping history of an object

    it adds keep_history_value, keep_history_relates_to and keep_history_date
    fields to the model.

    Warning :
    It uses a specific model manager for filterring historic values
    from the returned quesryset :

    Object.objects.all() -- returns all objects except those who are history
    Object.objects.history_for_object(obj) -- get historic states of an object
    Object.objects.all_including_history() -- returns all objects including history
    """

    class Meta:
        abstract = True

    objects = KeepModelHistoryManager()

    keep_history_date = models.DateTimeField(
        verbose_name=_("Datetime of modificaiton"),
        null=True,
        blank=True,
        auto_now_add=True,
    )
    keep_history_value = models.BooleanField(
        verbose_name=_("This is an historic value"), default=False
    )
    keep_history_relates_to = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Historic value of this"),
    )

    def save(self, *args, **kwargs):
        """
        Save object and keep an historic version
        """
        super(KeepModelHistoryMixin, self).save(*args, **kwargs)
        if not self.keep_history_value:
            nh = self.__class__()
            for prop in self.__dict__:
                if prop not in {
                    "_state",
                    "id",
                    "keep_history_value",
                    "keep_history_relates_to",
                    "keep_history_date",
                }:
                    value = getattr(self, prop)
                    nh.__setattr__(prop, value)

            nh.keep_history_value = True
            nh.keep_history_relates_to = self
            nh.save()
