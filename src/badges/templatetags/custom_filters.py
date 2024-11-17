from django import template

register = template.Library()

@register.filter(name='range')
def range_filter(value):
    """Retourne une liste d'entiers de 0 à value-1"""
    return range(value)
