class QuerysetUpdater(object):
    """
    class MyAdmin(ModelAdmin):
        actions = [QuerysetUpdater('Publish selected items', published=True)]
    """
    def __init__(self, name, **kwargs):
        self.short_description = name
        self.kwargs = kwargs
        
    def __call__(self, modeladmin, request, queryset):
        queryset.update(**self.kwargs)