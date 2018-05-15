from .signals import object_viewed_signal

# Custom View Mixin (for Class Based Views)
class ObjectViewMixin(object):
    # Dispatch method might run .get_object() twice since some class view will be calling .get_object
    # def dispatch(self, request, *args,**kwargs):
    #     try:
    #         instance = self.get_object()
    #     except DoesNotExist:
    #         instance = None
    #     if instance is not None:
    #         object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    #     return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return context