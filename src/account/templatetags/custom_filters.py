from django import template

register = template.Library()

@register.filter(name='mask_email')
def mask_email(email):
    parts = email.split('@')
    return f"{parts[0][:2]}{'*' * (len(parts[0]) - 2)}@{parts[1]}"

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})