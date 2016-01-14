from django import template

import markdown

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

@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape')


@register.simple_tag
def markdown_file(filename):
    with open(filename) as ff:
        text = ff.read()

    return markdownify(text.decode('utf-8'))

@register.filter
def multiply(value, arg):
    return float(value)*float(arg)

@register.filter
def my_float(value, ndigits=1):
    format = '%.' + str(ndigits) + 'e'
    return format % value
