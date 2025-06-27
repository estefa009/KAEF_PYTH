from django import template
from django.template.defaultfilters import intcomma

register = template.Library()

@register.filter
def moneda_cop(value):
    try:
        value = float(value)
        value = int(value) if value.is_integer() else round(value, 0)
        return f"${intcomma(int(value))}"
    except:
        return value
