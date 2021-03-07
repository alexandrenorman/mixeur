# -*- coding: utf-8 -*-
from nested_admin import NestedStackedInline
from nested_admin.forms import SortableHiddenMixin

from .action_model_inline_admin import ActionModelInlineAdmin
from ..models import CategoryModel


class CategoryModelInlineAdmin(SortableHiddenMixin, NestedStackedInline):
    model = CategoryModel
    inlines = [ActionModelInlineAdmin]
    sortable_field_name = "order"
    extra = 0
