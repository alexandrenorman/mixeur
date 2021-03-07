# -*- coding: utf-8 -*-
from nested_admin import NestedStackedInline
from nested_admin.forms import SortableHiddenMixin

from ..models import Status


class StatusInlineAdmin(SortableHiddenMixin, NestedStackedInline):
    model = Status
    verbose_name_plural = "Statuts"
    sortable_field_name = "order"
    extra = 0
