from django import template

register = template.Library()


@register.simple_tag()
def apply_discount(value, discount):
    return round(float(value) * 0.01 * (100 - discount), 2)
