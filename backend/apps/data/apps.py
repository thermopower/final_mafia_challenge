# -*- coding: utf-8 -*-
from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.data"
    verbose_name = "데이터 조회"
