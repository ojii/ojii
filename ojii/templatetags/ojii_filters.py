from django import template

register = template.Library()


@register.filter
def truncatechars(text, length):
    if len(text) <= length:
        return text
    return u'%s...' % text