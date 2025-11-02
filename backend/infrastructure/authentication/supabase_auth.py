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


class SupabaseUser:
    """
    Supabase 사용자 객체

    Django User 모델을 사용하지 않고 JWT 토큰의 정보만으로 인증합니다.
    """

    def __init__(self, user_id: str, email: str = None, role: str = 'authenticated'):
        self.id = user_id
        self.email = email
        self.role = role
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def __str__(self):
        return f'SupabaseUser({self.id})'

    def __repr__(self):
        return self.__str__()


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
            print('[SupabaseAuth] Authorization 헤더가 없습니다')
            return None

        # Bearer 형식 검증
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print(f'[SupabaseAuth] Bearer 형식이 아닙니다: {auth_header[:50]}...')
            raise AuthenticationFailed('Bearer 형식이 아닙니다')

        token = parts[1]
        print(f'[SupabaseAuth] 토큰 검증 시작: {token[:20]}...')

        try:
            # JWT Secret 확인
            if not settings.SUPABASE_JWT_SECRET:
                print('[SupabaseAuth] SUPABASE_JWT_SECRET이 설정되지 않았습니다!')
                raise AuthenticationFailed('JWT Secret이 설정되지 않았습니다')

            # JWT 토큰 디코드 및 검증
            # Supabase JWT는 audience를 'authenticated'로 설정
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=['HS256'],
                audience='authenticated',
                options={"verify_aud": True}
            )

            # 사용자 정보 추출 (Supabase는 'sub' 필드에 user_id 저장)
            user_id = payload.get('sub')
            email = payload.get('email')
            role = payload.get('role', 'authenticated')

            print(f'[SupabaseAuth] 토큰 검증 성공. User ID: {user_id}, Email: {email}')

            if not user_id:
                raise AuthenticationFailed('토큰에 사용자 ID가 없습니다')

            # SupabaseUser 객체 생성 및 반환
            user = SupabaseUser(user_id=user_id, email=email, role=role)
            return (user, token)

        except jwt.ExpiredSignatureError:
            print('[SupabaseAuth] 토큰이 만료되었습니다')
            raise AuthenticationFailed('토큰이 만료되었습니다')

        except jwt.InvalidTokenError as e:
            print(f'[SupabaseAuth] 유효하지 않은 토큰입니다: {str(e)}')
            raise AuthenticationFailed('유효하지 않은 토큰입니다')

        except Exception as e:
            print(f'[SupabaseAuth] 인증 처리 중 오류: {str(e)}')
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
