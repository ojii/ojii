from classytags.arguments import MultiValueArgument, Argument, Flag
from classytags.core import Options
from classytags.helpers import AsTag
from django import template
from django.template.defaulttags import cycle
from django.utils.safestring import mark_safe
import itertools

register = template.Library()

class SaneCycleNode(template.Node):
    def __init__(self, realnode):
        self.realnode = realnode
        
    def render(self, context):
        ret = self.realnode.render(context)
        if self.realnode.variable_name:
            return ""
        return ret


@register.tag
def sanecycle(*args, **kwargs):
    """
    {% cycle 1 2 3 a myvar %} => ""
    {{ myvar }} => 1
    {{ myvar }} => 2
    {{ myvar }} => 3
    {{ myvar }} => 1
    """
    realnode = cycle(*args, **kwargs)
    return SaneCycleNode(realnode)


class InsaneCycleObject(object):
    def __init__(self, pairs, using, safe):
        self.pairs = dict([(int(x), y) for x,y in pairs])
        self.using = using
        top = max(self.pairs.keys())
        iterable = []
        for i in xrange(1, top + 1):
            if i in self.pairs:
                iterable.append(self.pairs[i])
            else:
                iterable.append(None)
        self.cycle = itertools.cycle(iterable)
        self.mark = mark_safe if safe else lambda x: x
    
    def render(self):
        next = self.cycle.next()
        if next is None:
            return ''
        out = self.using % {'value': next}
        return self.mark(out)


class InsaneCycle(AsTag):
    """
    {% insane cycle 1 'first' 3 'last' using ' class="%(value)"' as cycler %}
    {% for obj in sequence %}
        <div{{ cycler.render }}>{{ obj }}</div>
    {% endfor %}
    
    With sequence=[1,2,3,4]:
    
    <div class="first">1</div>
    <div>2</div>
    <div class="last">3</div>
    <div class="first">4</div>
    """
    options = Options(
        MultiValueArgument('pairs'),
        'using',
        Argument('using', resolve=False, required=False),
        'as',
        Argument('varname', resolve=False),
        'mark',
        Flag('safe', default=False, true_values=['safe']),
    )
    
    def get_value(self, context, pairs, using, safe):
        return InsaneCycleObject(pairs, using, safe)
register.tag(InsaneCycle)