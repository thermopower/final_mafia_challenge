# -*- coding: utf-8 -*-
"""
Core Models

공통 베이스 모델 정의
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    타임스탬프 추상 베이스 모델

    모든 모델에 created_at, updated_at 필드를 자동으로 추가합니다.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")

    class Meta:
        abstract = True
