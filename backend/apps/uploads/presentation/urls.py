# -*- coding: utf-8 -*-
"""
Upload URL Configuration
"""
from django.urls import path
from apps.uploads.presentation.views import FileUploadView

app_name = 'uploads'

urlpatterns = [
    path('', FileUploadView.as_view(), name='file_upload'),
]
