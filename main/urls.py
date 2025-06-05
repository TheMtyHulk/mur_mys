from django.contrib import admin
from django.urls import path,include
from .views import index,registerView,loginView,logoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name='index'),  # Home page
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]
