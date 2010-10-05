from django.db import models


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class ModifiedByModel(models.Model):
    """
    Should be used together with ojii.admin.ModifiedByAdmin
    
    Both fields are null=True because not all data comes from admin
    """
    created_by = models.ForeignKey('auth.User', null=True)
    modified_by = models.ForeignKey('auth.User', null=True)
    
    class Meta:
        abstract = True