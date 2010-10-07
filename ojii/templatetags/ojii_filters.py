from django import template
from django.utils.encoding import force_unicode
import re

register = template.Library()


@register.filter
def truncatechars(text, length):
    """
    with myval = "lorem ipsum dolor sit amet"
    {{ myval|truncatechars:13 }} => "lorem ipsum d..."
    """
    if len(text) <= length:
        return text
    return u'%s...' % text

def smartintsep(value, sep="'"):
    """
    with myval=10000:
    {{ myval|smartintsep:"'" }} => 10'000
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>%s\g<2>' % sep, orig)
    if orig == new:
        return new
    else:
        return smartintsep(new)
smartintsep.is_safe = True
register.filter(smartintsep)