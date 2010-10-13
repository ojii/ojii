from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class CachedModelChoiceIterator(object):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset
        self.model = field.queryset.model

    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.model not in CachedModelChoiceField.__cache__:
            CachedModelChoiceField.__cache__[self.model] = [
                self.choice(obj) for obj in self.queryset.all()
            ]
        for choice in CachedModelChoiceField.__cache__[self.model]:
            yield choice

    def __len__(self):
        return len(self.queryset)

    def choice(self, obj):
        return (self.field.prepare_value(obj), self.field.label_from_instance(obj))


class CachedModelChoiceField(ModelChoiceField):
    __cache__ = {}
    
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CachedModelChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)
    
    
class CachedModelMultipleChoiceField(CachedModelChoiceField , ModelMultipleChoiceField): pass