import datetime
from django import template

register = template.Library()


@register.filter
def get_value(dictionary, key):
    if isinstance(dictionary, list):
        dictionary = dict(dictionary)
    if key is not None and key in dictionary:
        return dictionary[key]
    else:
        return None
