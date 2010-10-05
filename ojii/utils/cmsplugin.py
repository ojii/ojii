from cms.plugin_base import CMSPluginBase


class BaseCMSPlugin(CMSPluginBase):
    admin_preview = False
    
    def render(self, context, instance, placeholder):
        data = {
            'instance': instance,
            'placeholder': placeholder
        }
        data.update(self.get_render_context(context, instance, placeholder))
        context.update(data)
        return context
    
    def get_render_context(self, context, instance, placeholder):
        return {}