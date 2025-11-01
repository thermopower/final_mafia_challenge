# -*- coding: utf-8 -*-
"""메인 URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.presentation.urls')),
    path('api/', include('apps.dashboard.presentation.urls')),
    path('api/upload/', include('apps.uploads.presentation.urls')),
    path('api/data/', include('apps.data.presentation.urls')),
]
