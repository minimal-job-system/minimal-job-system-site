import datetime
from django import template

register = template.Library()


@register.filter
def to_int(value):
    if value is not None:
        return int(value)
    else:
        return None
