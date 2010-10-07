from django.db import models
from ojii.utils.slug import auto_slug


class AutoSlugField(models.SlugField):
    def __init__(self, source_field=None, *args, **kwargs):
        if source_field is None:
            raise Exception
        self.source_field = source_field
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(AutoSlugField, self).contribute_to_class(cls, name)
        auto_slug(self.model, self.name, self.source_field)

    def south_field_triple(self):
        """
        South compatibility.
        """
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.SlugField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)