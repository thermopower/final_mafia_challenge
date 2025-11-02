# -*- coding: utf-8 -*-
"""
인증 미들웨어

Supabase JWT 토큰 검증 및 사용자 정보 추가
"""
from django.utils.deprecation import MiddlewareMixin


class SupabaseAuthMiddleware(MiddlewareMixin):
    """
    Supabase 인증 미들웨어

    JWT 토큰을 검증하고 request 객체에 사용자 정보를 추가합니다.
    실제 인증은 DRF의 SupabaseAuthentication에서 처리됩니다.
    """

    def process_request(self, request):
        """
        요청 처리

        현재는 DRF authentication이 처리하므로 별도 로직 없음
        """
        return None
