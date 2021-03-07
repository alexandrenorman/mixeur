# -*- coding: utf-8 -*-
from django import template

from helpers.helpers import remove_diacritics as remove_diacritics_helper

register = template.Library()


@register.filter(name="remove_diacritics")
def remove_diacritics(value):
    """
    Return string without diacritics (Épice => Epice)
    """
    return remove_diacritics_helper(value)
