from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def length_lt(value, lt):
    print(value)
    return value


register.filter('length_lt', length_lt)
