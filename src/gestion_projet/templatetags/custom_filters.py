# custom_filters.py
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def format_timestamp(value):
    now = timezone.now()
    if value.date() == now.date():
        return f"Aujourd'hui à {value.strftime('%H:%M')}"
    elif value.date() == (now - timezone.timedelta(days=1)).date():
        return f"Hier à {value.strftime('%H:%M')}"
    elif value.year == now.year:
        return value.strftime('%d %b à %H:%M')
    else:
        return value.strftime('%d %b %Y à %H:%M')
