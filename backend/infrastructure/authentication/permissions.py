# -*- coding: utf-8 -*-
"""
권한 체크 데코레이터

책임:
- View 레벨에서 사용자 권한 검증
- 관리자 전용 기능 보호
- 권한 부족 시 403 Forbidden 응답
"""
from functools import wraps
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


def require_admin(view_func):
    """
    관리자 권한 필수 데코레이터

    Usage:
        @require_admin
        def upload_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 인증 확인
        if not request.user or not hasattr(request.user, '__iter__'):
            raise PermissionDenied('로그인이 필요합니다')

        # JWT에서 역할 추출 (user_id, token)
        user_id, token = request.user

        # JWT 토큰 디코드
        import jwt
        from django.conf import settings

        try:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256']
            )

            role = payload.get('role', 'user')

            if role != 'admin':
                raise PermissionDenied('관리자 권한이 필요합니다')

        except jwt.InvalidTokenError:
            raise PermissionDenied('유효하지 않은 토큰입니다')

        return view_func(request, *args, **kwargs)

    return wrapper


def require_authenticated(view_func):
    """
    로그인 필수 데코레이터

    Usage:
        @require_authenticated
        def dashboard_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 인증 확인
        if not request.user or not hasattr(request.user, '__iter__'):
            raise PermissionDenied('로그인이 필요합니다')

        return view_func(request, *args, **kwargs)

    return wrapper
