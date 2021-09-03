"""
Module with permission validation functions for users
"""
from django.http import HttpResponseForbidden


def is_moderator(request):
    """
    Checks if user have moderator rights
    """
    if request.user.groups.filter(name='moderator').exists() or request.user.is_superuser:
        return True
    return False


class ModeratorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if user have moderator rights and if not raises 403
        """
        if is_moderator(request):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Moderator account required')


class OwnerOrModeratorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if user have moderator or owner rights and if not raises 403
        """
        if is_moderator(request) or self.get_object().owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden('Owner or moderator account required')
