from django.contrib import admin
from django.urls import path,include
from .views import index,register

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name='index'),  # Home page
    path('register/', register, name='register'),
]
