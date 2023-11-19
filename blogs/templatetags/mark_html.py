from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter(name="mark_safe")
def mark_safe_filter(value):
    return mark_safe(value)
