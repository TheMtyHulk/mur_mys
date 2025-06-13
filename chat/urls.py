from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('support/chat/', views.admin_chat_dashboard, name='admin_chat'),
    path('ajax/get-new-messages/', views.get_new_messages, name='get_new_messages'),
    path('ajax/send-message/', views.send_message, name='send_message'),
    path('ajax/clear-chat/', views.clear_chat, name='clear_chat'),  # Add this line
    path('ajax/admin-get-new-messages/', views.admin_get_new_messages, name='admin_get_new_messages'),
    path('support/clear-chat/', views.admin_clear_chat, name='admin_clear_chat'),
    path('contact/', views.contactView, name='contact'),
]
