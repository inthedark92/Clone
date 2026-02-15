from django import template

register = template.Library()

@register.filter
def attr(obj, arg):
    return getattr(obj, arg, None)
