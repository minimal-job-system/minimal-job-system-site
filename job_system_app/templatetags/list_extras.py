from django import template

register = template.Library()


@register.filter
def to_list(value):
    return [value]


@register.simple_tag
def to_list(*args):
    return args


@register.simple_tag
def concat_list(list1, list2):
    return list1 + list2
