"""Accounts URL 라우팅"""

from django.urls import path
from apps.accounts.presentation.views import ProfileView, change_password

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', change_password, name='change-password'),
]
