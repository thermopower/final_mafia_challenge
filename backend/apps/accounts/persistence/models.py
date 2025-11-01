"""
사용자 프로필 ORM 모델 (Persistence Layer)

이 모델은 데이터베이스 스키마를 정의하며, Django ORM을 사용합니다.
"""

import uuid
from django.db import models


class UserProfile(models.Model):
    """사용자 프로필 ORM 모델

    Attributes:
        id: 사용자 고유 ID (UUID) - Supabase Auth의 user_id와 동일
        email: 이메일 주소 (고유)
        full_name: 전체 이름
        department: 부서명
        role: 역할 (admin 또는 user)
        profile_picture_url: 프로필 사진 URL
        is_active: 계정 활성화 여부
        created_at: 생성 일시
        updated_at: 수정 일시
    """

    ROLE_CHOICES = [
        ('admin', '관리자'),
        ('user', '일반 사용자'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    profile_picture_url = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필들'

    def __str__(self):
        """문자열 표현

        Returns:
            str: 이메일 (역할) 형식
        """
        return f"{self.email} ({self.get_role_display()})"
