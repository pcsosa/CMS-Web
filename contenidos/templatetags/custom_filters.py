# contenidos/templatetags/custom_filters.py
from django import template
from django.template.defaultfilters import truncatewords_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def safe_truncate(value, arg):
    safe_value = mark_safe(value)
    return truncatewords_html(safe_value, arg)
