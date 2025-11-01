"""ProfileView API 테스트 (TDD Red Phase)"""

import pytest
import uuid
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.persistence.models import UserProfile


@pytest.mark.django_db
class TestProfileViewGET:
    """프로필 조회 API 테스트"""

    def test_get_profile_returns_200(self):
        """인증된 사용자가 프로필 조회 시 200 OK를 반환한다"""
        # Arrange
        user_id = str(uuid.uuid4())
        user = UserProfile.objects.create(
            id=user_id,
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        client = APIClient()
        # Supabase JWT 인증 시뮬레이션
        client.force_authenticate(user=user_id)

        # Act
        response = client.get('/api/account/profile/')

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'user@university.ac.kr'
        assert response.data['full_name'] == '홍길동'
        assert response.data['department'] == '컴퓨터공학과'

    def test_get_profile_without_auth_returns_401(self):
        """인증 없이 프로필 조회 시 401 Unauthorized를 반환한다"""
        # Arrange
        client = APIClient()

        # Act
        response = client.get('/api/account/profile/')

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfileViewPUT:
    """프로필 업데이트 API 테스트"""

    def test_update_profile_returns_200(self):
        """유효한 데이터로 프로필 업데이트 시 200 OK를 반환한다"""
        # Arrange
        user_id = str(uuid.uuid4())
        user = UserProfile.objects.create(
            id=user_id,
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        client = APIClient()
        client.force_authenticate(user=user_id)

        # Act
        response = client.put(
            '/api/account/profile/',
            {
                'full_name': '김철수',
                'department': '전자공학과'
            },
            format='json'
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == '김철수'
        assert response.data['department'] == '전자공학과'
        # 이메일과 역할은 변경되지 않음
        assert response.data['email'] == 'user@university.ac.kr'
        assert response.data['role'] == 'user'

    def test_update_profile_invalid_name_returns_400(self):
        """이름이 2자 미만이면 400 Bad Request를 반환한다"""
        # Arrange
        user_id = str(uuid.uuid4())
        user = UserProfile.objects.create(
            id=user_id,
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        client = APIClient()
        client.force_authenticate(user=user_id)

        # Act
        response = client.put(
            '/api/account/profile/',
            {
                'full_name': '김'
            },
            format='json'
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert '이름은 2자 이상 50자 이하여야 합니다' in str(response.data)

    def test_update_profile_without_auth_returns_401(self):
        """인증 없이 프로필 업데이트 시 401 Unauthorized를 반환한다"""
        # Arrange
        client = APIClient()

        # Act
        response = client.put(
            '/api/account/profile/',
            {
                'full_name': '김철수'
            },
            format='json'
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestChangePasswordView:
    """비밀번호 변경 API 테스트"""

    def test_change_password_endpoint_exists(self):
        """비밀번호 변경 엔드포인트가 존재한다"""
        # Arrange
        user_id = str(uuid.uuid4())
        user = UserProfile.objects.create(
            id=user_id,
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        client = APIClient()
        client.force_authenticate(user=user_id)

        # Act
        response = client.post(
            '/api/account/profile/change-password/',
            {
                'current_password': 'OldPassword123!',
                'new_password': 'NewPassword456@'
            },
            format='json'
        )

        # Assert
        # 엔드포인트가 존재하고, Supabase 연동이 필요하므로 400 또는 500이 아닌 다른 응답 확인
        assert response.status_code != status.HTTP_404_NOT_FOUND
