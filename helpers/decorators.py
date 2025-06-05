from django.http import HttpResponseForbidden

def anonymous_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            return view_func(request, *args, **kwargs)
    return wrapper