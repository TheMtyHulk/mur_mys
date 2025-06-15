from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
    
    path('solve/<int:murder_id>/', views.solveMurderView, name='solve_murder'),
    path('suspectsprofile/<int:murder_id>/', views.suspectsProfileView, name='suspects_profile'),
    path('investigatorsprofile/<int:murder_id>/', views.investigatorsProfileView, name='investigators_profile'),
    path('interviews/<int:murder_id>/', views.interviewsView, name='interview'),
       
    # Ajax URLs
    path('ajax/get-suspects/', views.get_suspects_by_murder, name='get_suspects_by_murder'),
    path('ajax/get-investigators/', views.get_investigators_by_murder, name='get_investigators_by_murder'),
    path('ajax/get-suspect-details/<int:suspect_id>/', views.get_suspect_details, name='get_suspect_details'),
    path('ajax/get-investigator-details/<int:investigator_id>/', views.get_investigator_details, name='get_investigator_details'),
    path('ajax/get-interview-details/<int:interview_id>/', views.get_interview_details, name='get_interview_details'),
    path('profile/', views.profileView, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='main/password_change.html',
        success_url='/profile/?changed=true'
    ), name='password_change'),
   
]

urlpatterns+=[
    path('password-reset/', views.passwordReset, name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', views.passwordResetConfirm, name='password_reset_confirm'),
    
    ]