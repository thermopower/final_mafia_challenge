"""
Supabase JWT 인증 클래스

책임:
- HTTP 요청에서 JWT 토큰 추출
- Supabase JWT Secret으로 토큰 서명 검증
- 토큰 만료 여부 확인
- 사용자 ID 및 역할 추출
- 요청 객체에 사용자 정보 첨부
"""
import jwt
from typing import Optional, Tuple
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class SupabaseAuthentication(BaseAuthentication):
    """
    Supabase JWT 토큰 기반 인증 클래스
    """

    def authenticate(self, request) -> Optional[Tuple[str, str]]:
        """
        JWT 토큰을 검증하고 사용자 ID를 반환

        Args:
            request: Django HTTP 요청 객체

        Returns:
            (user_id, token) 튜플 또는 None (익명 사용자)

        Raises:
            AuthenticationFailed: 토큰이 유효하지 않은 경우
        """
        # Authorization 헤더 추출
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            # Authorization 헤더가 없으면 익명 사용자로 처리
            return None

        # Bearer 형식 검증
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Bearer 형식이 아닙니다')

        token = parts[1]

        try:
            # JWT 토큰 디코드 및 검증
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256']
            )

            # 사용자 ID 추출 (Supabase는 'sub' 필드에 user_id 저장)
            user_id = payload.get('sub')

            if not user_id:
                raise AuthenticationFailed('토큰에 사용자 ID가 없습니다')

            # (user_id, token) 튜플 반환
            return (user_id, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('토큰이 만료되었습니다')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('유효하지 않은 토큰입니다')

        except Exception as e:
            raise AuthenticationFailed(f'인증 처리 중 오류가 발생했습니다: {str(e)}')

    def authenticate_header(self, request):
        """
        401 응답 시 WWW-Authenticate 헤더 값 반환

        Args:
            request: Django HTTP 요청 객체

        Returns:
            WWW-Authenticate 헤더 값
        """
        return 'Bearer realm="api"'
