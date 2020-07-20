from django import template

register = template.Library()

@register.filter()
def is_negative(value):
    return int(value) < 0

@register.filter()
def is_positive(value):
    return int(value) > 0

@register.filter()
def money_value(value):
    result = 0
    if value == None:
        result = "R0.00"
    elif value < 0:
        result = "-R" + str(-1*value)
    else:
        result = "R" + str(value)

    return result
