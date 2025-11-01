# -*- coding: utf-8 -*-
"""
Data API URL Configuration
"""

from django.urls import path
from apps.data.presentation.views import DataListView, DataDetailView, ExportView

app_name = 'data'

urlpatterns = [
    path('', DataListView.as_view(), name='data-list'),
    path('export/', ExportView.as_view(), name='data-export'),
    path('<str:data_type>/<int:pk>/', DataDetailView.as_view(), name='data-detail'),
]
