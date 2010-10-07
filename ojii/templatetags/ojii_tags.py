from classytags.arguments import MultiValueArgument, Argument, Flag
from classytags.core import Options, Tag
from classytags.helpers import AsTag
from django import template
from django.template.defaulttags import cycle, url
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


class FootnoteHolder(object):
    def __init__(self):
        self.data = {}
        self.order = []
        
    def push(self, id, content):
        if id not in self.order:
            self.order.append(id)
            self.data[id] = content
            return len(self.order)
        return self.order.index(id) + 1
    
    def __iter__(self):
        for index, id in enumerate(self.order):
            yield index + 1, self.data[id]


class Footnote(Tag):
    """
    {% for obj in queryset %}
        {% if obj.footnote %}
            <sup>{% footnote obj.pk obj.footnote into "firstfootnote" %}</sup>
        {% endif %}
    {% endfor %}
    
    {% for number,footnote in firstfootnote %}
        {{ number }}: {{ footnote }}
    {% endfor %}
    """
    options = Options(
        Argument('id'),
        Argument('content'),
        'into',
        Argument('namespace', resolve=False),
    )
    def render_tag(self, context, id, content, namespace):
        footnote = context.dicts[0].get(namespace, FootnoteHolder())
        context.dicts[0][namespace] = footnote
        return footnote.push(id, content)
register.tag(Footnote)


class SaneURLNode(template.Node):
    def __init__(self, real):
        self.real = real
        self.view_name = template.Variable(self.real.view_name)
        
    def render(self, context):
        self.real.view_name = self.view_name.resolve(context)
        return self.real.render(context)


@register.tag
def saneurl(parser, token):
    """
    Allows variable/filters as view names in url tag.
    
    {% saneurl some_variable %}
    """
    return SaneURLNode(url(parser, token))