from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('contact/', views.contactView, name='contact'),
    path('solve/<int:murder_id>/', views.solveMurderView, name='solve_murder'),
    path('suspectsprofile/<int:murder_id>/', views.suspectsProfileView, name='suspects_profile'),
    path('investigatorsprofile/<int:murder_id>/', views.investigatorsProfileView, name='investigators_profile'),
    path('interviews/<int:murder_id>/', views.interviewsView, name='interview'),
    # Chat URLs
    path('contact/', views.contactView, name='contact'),
    path('ajax/get-new-messages/', views.get_new_messages, name='get_new_messages'),
    path('ajax/send-message/', views.send_message, name='send_message'),
    path('ajax/clear-chat/', views.clear_chat, name='clear_chat'),  # Add this line
    # Ajax URLs
    path('ajax/get-suspects/', views.get_suspects_by_murder, name='get_suspects_by_murder'),
    path('ajax/get-investigators/', views.get_investigators_by_murder, name='get_investigators_by_murder'),
    path('ajax/get-suspect-details/<int:suspect_id>/', views.get_suspect_details, name='get_suspect_details'),
    path('ajax/get-investigator-details/<int:investigator_id>/', views.get_investigator_details, name='get_investigator_details'),
    path('ajax/get-interview-details/<int:interview_id>/', views.get_interview_details, name='get_interview_details'),
]