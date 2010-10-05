from django.shortcuts import render_to_response
from django.template.context import RequestContext
from ojii.utils.datastructures import NULL

def cachedproperty(func):
    """
    class MyClass(object):
        @cachedproperty
        def myproperty(self):
            return heave_calculation()
    """
    key = '_cached_property_of_%s' % func.__name__
    def _wrapped(self):
        cached = getattr(self, key, NULL)
        if cached is not NULL:
            return cached
        value = func(self)
        setattr(self, key, value)
        return value
    _wrapped.__name__ = func.__name__
    return property(_wrapped)

def renderable_request(func):
    """
    @renderable_request
    def my_view(request):
        return request.render_to_response("my_template.html")
    """
    def _wrapped(request, *args, **kwargs):
        def render(tpl, data=None):
            return render_to_response(tpl, data, RequestContext(request))
        request.render_to_response = render(request)
        return func(request, *args, **kwargs)
    _wrapped.__name__ = func.__name__
    return _wrapped