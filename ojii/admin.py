from django.contrib.admin.options import ModelAdmin


class ModifiedByAdmin(ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            field = 'modified_by'
        else:
            field = 'created_by'
        setattr(obj, field, request.user)
        obj.save()