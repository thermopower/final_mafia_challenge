"""
Supabase Authentication 테스트

TDD Red 단계: 테스트 먼저 작성
"""
import pytest
from unittest.mock import Mock, patch
import jwt
from datetime import datetime, timedelta

from infrastructure.authentication.supabase_auth import SupabaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TestSupabaseAuthentication:
    """SupabaseAuthentication 단위 테스트"""

    @pytest.fixture
    def auth(self):
        """SupabaseAuthentication 인스턴스 생성"""
        return SupabaseAuthentication()

    @pytest.fixture
    def valid_jwt_token(self):
        """유효한 JWT 토큰 생성"""
        secret = "test-secret-key"
        payload = {
            'sub': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'email': 'test@example.com',
            'role': 'user',
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token

    @pytest.fixture
    def expired_jwt_token(self):
        """만료된 JWT 토큰 생성"""
        secret = "test-secret-key"
        payload = {
            'sub': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'email': 'test@example.com',
            'role': 'user',
            'exp': datetime.utcnow() - timedelta(hours=1)  # 1시간 전 만료
        }
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token

    def test_authenticate_returns_user_id_and_token_for_valid_jwt(self, auth, valid_jwt_token):
        """
        유효한 JWT 토큰 → 사용자 ID 추출 성공

        Arrange: 유효한 JWT 토큰을 가진 요청 생성
        Act: authenticate 메서드 호출
        Assert: (user_id, token) 튜플 반환
        """
        # Arrange
        request = Mock()
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {valid_jwt_token}'}

        # Act
        with patch('infrastructure.authentication.supabase_auth.settings.SUPABASE_JWT_SECRET', 'test-secret-key'):
            user_id, token = auth.authenticate(request)

        # Assert
        assert user_id == 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        assert token == valid_jwt_token

    def test_authenticate_raises_authentication_failed_for_expired_token(self, auth, expired_jwt_token):
        """
        만료된 토큰 → AuthenticationFailed 예외 발생

        Arrange: 만료된 JWT 토큰을 가진 요청 생성
        Act: authenticate 메서드 호출
        Assert: AuthenticationFailed 예외 발생
        """
        # Arrange
        request = Mock()
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {expired_jwt_token}'}

        # Act & Assert
        with patch('infrastructure.authentication.supabase_auth.settings.SUPABASE_JWT_SECRET', 'test-secret-key'):
            with pytest.raises(AuthenticationFailed, match='토큰이 만료되었습니다'):
                auth.authenticate(request)

    def test_authenticate_raises_authentication_failed_for_invalid_signature(self, auth, valid_jwt_token):
        """
        잘못된 서명 → AuthenticationFailed 예외 발생

        Arrange: 유효한 JWT 토큰이지만 잘못된 시크릿으로 검증
        Act: authenticate 메서드 호출
        Assert: AuthenticationFailed 예외 발생
        """
        # Arrange
        request = Mock()
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {valid_jwt_token}'}

        # Act & Assert
        with patch('infrastructure.authentication.supabase_auth.settings.SUPABASE_JWT_SECRET', 'wrong-secret-key'):
            with pytest.raises(AuthenticationFailed, match='유효하지 않은 토큰입니다'):
                auth.authenticate(request)

    def test_authenticate_returns_none_for_missing_authorization_header(self, auth):
        """
        Authorization 헤더 없음 → None 반환 (익명 사용자)

        Arrange: Authorization 헤더가 없는 요청 생성
        Act: authenticate 메서드 호출
        Assert: None 반환
        """
        # Arrange
        request = Mock()
        request.META = {}

        # Act
        result = auth.authenticate(request)

        # Assert
        assert result is None

    def test_authenticate_raises_authentication_failed_for_invalid_bearer_format(self, auth):
        """
        Bearer 형식 아님 → AuthenticationFailed 예외 발생

        Arrange: Bearer 형식이 아닌 Authorization 헤더를 가진 요청 생성
        Act: authenticate 메서드 호출
        Assert: AuthenticationFailed 예외 발생
        """
        # Arrange
        request = Mock()
        request.META = {'HTTP_AUTHORIZATION': 'Token abc123'}

        # Act & Assert
        with pytest.raises(AuthenticationFailed, match='Bearer 형식이 아닙니다'):
            auth.authenticate(request)

    def test_authenticate_extracts_user_role_from_jwt(self, auth, valid_jwt_token):
        """
        JWT 토큰에서 사용자 역할 추출 성공

        Arrange: 역할 정보를 포함한 JWT 토큰을 가진 요청 생성
        Act: authenticate 메서드 호출
        Assert: 사용자 역할 추출 확인
        """
        # Arrange
        request = Mock()
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {valid_jwt_token}'}

        # Act
        with patch('infrastructure.authentication.supabase_auth.settings.SUPABASE_JWT_SECRET', 'test-secret-key'):
            user_id, token = auth.authenticate(request)
            # JWT 디코드하여 역할 확인
            decoded = jwt.decode(token, 'test-secret-key', algorithms=['HS256'])

        # Assert
        assert decoded['role'] == 'user'
        assert decoded['email'] == 'test@example.com'
