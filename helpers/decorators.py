from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def anonymousRequired(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirect to home page if user is authenticated
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def contactLoginRequired(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return HttpResponseForbidden("staff members are not allowed to access this page.")
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to login page if not authenticated
    return wrapper