from django import template

register = template.Library()

@register.filter(name="multiply")
def multiply(val1, val2):
    return val1 * val2
