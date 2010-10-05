from django.core.urlresolvers import get_resolver
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern


def _recurse_resolver(resolver, prefix=[]):
    patterns = []
    for obj in resolver.url_patterns:
        if isinstance(obj, RegexURLPattern):
            patterns.append(prefix + [obj.regex.pattern])
        elif isinstance(obj, RegexURLResolver):
            patterns += _recurse_resolver(obj, prefix + [obj.regex.pattern])
    return patterns
    

def get_all_url_patterns(url_conf=None):
    """
    Returns a list of lists of urlpatterns:
    [
        [prefix, prefix, pattern],
        ...
    ]
    """
    resolver = get_resolver(url_conf)
    return _recurse_resolver(resolver)