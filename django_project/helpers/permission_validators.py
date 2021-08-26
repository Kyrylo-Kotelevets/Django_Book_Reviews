from django.http import HttpResponseForbidden


def is_moderator(request):
    if request.user.groups.filter(name='moderator').exists() or request.user.is_superuser:
        return True
    return False


class ModeratorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if is_moderator(request):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Moderator account required')


class OwnerOrModeratorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if is_moderator(request) or self.get_object().owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Owner or moderator account required')


class DifferentUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if is_moderator(request) or self.get_object().owner != request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('You can`t comment your own reviews')