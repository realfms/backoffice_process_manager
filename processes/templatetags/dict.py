from django import template

register = template.Library()


@register.filter
def keyvalue(dict, key):
    return dict[key]


@register.filter
def index(list, elem):
    return list.index(elem)
