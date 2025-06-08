from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve
from django.contrib import messages

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path starts with /admin/ 
        if request.path.startswith('/admin/'):
            # if the user is not authenticated, redirect to index
            if not request.user.is_authenticated:
                return redirect('index')
            
            # If authenticated but not superuser, deny access
            if not request.user.is_superuser :
                return redirect('index')

        response = self.get_response(request)
        return response