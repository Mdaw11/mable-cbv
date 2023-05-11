from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.account_type == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper_func

def developer_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.account_type == 'developer':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper_func

def project_manager_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.account_type == 'project_manager':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper_func