from django.db import models
from django.http import Http404


class ExtendedManager(models.Manager):
    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise Http404
        
    def flat_get_or_create(self, *args, **kwargs):
        return self.get_or_create(*args, **kwargs)[0]