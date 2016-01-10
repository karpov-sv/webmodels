from django import template

register = template.Library()

@register.filter
def GET_remove(value, key):
    value = value.copy()

    if key in value:
        value.pop(key)

    return value

@register.filter
def GET_append(value, key, new=1):
    value = value.copy()

    if key in value:
        value.pop(key)

    if '=' in key:
        s = key.split('=')
        value.appendlist(s[0], s[1])
    else:
        value.appendlist(key, new)

    return value

@register.filter
def GET_urlencode(value):
    return value.urlencode()
