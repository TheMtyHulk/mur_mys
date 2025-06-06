from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Home page
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('contact/', views.contactView, name='contact'),
    path('ajax/get-suspects/', views.get_suspects_by_murder, name='get_suspects_by_murder'),
    path('ajax/get-investigators/', views.get_investigators_by_murder, name='get_investigators_by_murder'),
]
