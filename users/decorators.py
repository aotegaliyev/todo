import logging

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from tasks.models import Task

logger = logging.getLogger('django-info')


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                role = request.user.profile.role
                if role not in allowed_roles:
                    raise PermissionDenied
            except ObjectDoesNotExist:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator


def user_can_update_or_delete(function):
    def wrap(request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        if task.author == request.user or request.user.profile.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    return wrap
