"""
API URL patterns for the accounts application.
"""

from django.urls import path
from . import api

app_name = 'api_auth'

urlpatterns = [
    path('login/', api.api_login, name='login'),
    path('logout/', api.api_logout, name='logout'),
    path('register/', api.api_register, name='register'),
    path('me/', api.api_me, name='me'),
]
