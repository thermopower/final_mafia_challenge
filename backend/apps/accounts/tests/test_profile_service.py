"""ProfileService 단위 테스트 (TDD Red Phase)"""

import pytest
from unittest.mock import Mock
from apps.accounts.services.profile_service import ProfileService
from apps.accounts.domain.models import User
from apps.core.exceptions import ResourceNotFoundError, ValidationError


class TestProfileServiceGetProfile:
    """프로필 조회 테스트"""

    def test_get_profile_returns_user_data(self):
        """프로필 조회 시 사용자 데이터를 반환한다"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        service = ProfileService(user_repository=mock_repo)

        # Act
        profile = service.get_profile('uuid-123')

        # Assert
        assert profile.full_name == '홍길동'
        assert profile.email == 'user@university.ac.kr'
        assert profile.department == '컴퓨터공학과'
        mock_repo.get_by_id.assert_called_once_with('uuid-123')


class TestProfileServiceUpdateProfile:
    """프로필 업데이트 테스트"""

    def test_update_profile_with_valid_data(self):
        """유효한 데이터로 프로필을 업데이트한다"""
        # Arrange
        existing_user = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        mock_repo = Mock()
        mock_repo.get_by_id.return_value = existing_user
        mock_repo.update.return_value = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='김철수',
            department='전자공학과',
            role='user',
            is_active=True
        )

        service = ProfileService(user_repository=mock_repo)

        profile_data = {
            'full_name': '김철수',
            'department': '전자공학과'
        }

        # Act
        updated_user = service.update_profile('uuid-123', profile_data)

        # Assert
        assert updated_user.full_name == '김철수'
        assert updated_user.department == '전자공학과'
        mock_repo.update.assert_called_once()

    def test_update_profile_user_not_found(self):
        """존재하지 않는 사용자 프로필 업데이트 시 에러를 발생시킨다"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        service = ProfileService(user_repository=mock_repo)

        profile_data = {
            'full_name': '김철수',
            'department': '전자공학과'
        }

        # Act & Assert
        with pytest.raises(ResourceNotFoundError, match='사용자를 찾을 수 없습니다'):
            service.update_profile('invalid-id', profile_data)

    def test_update_profile_validates_full_name_length(self):
        """full_name이 2자 미만이거나 50자 초과 시 에러를 발생시킨다"""
        # Arrange
        existing_user = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        mock_repo = Mock()
        mock_repo.get_by_id.return_value = existing_user

        service = ProfileService(user_repository=mock_repo)

        # Act & Assert - 2자 미만
        with pytest.raises(ValidationError, match='이름은 2자 이상 50자 이하여야 합니다'):
            service.update_profile('uuid-123', {'full_name': '김'})

        # Act & Assert - 50자 초과
        with pytest.raises(ValidationError, match='이름은 2자 이상 50자 이하여야 합니다'):
            service.update_profile('uuid-123', {'full_name': 'a' * 51})

    def test_update_profile_readonly_fields_not_changed(self):
        """이메일, 역할 등 읽기 전용 필드는 업데이트하지 않는다"""
        # Arrange
        existing_user = User(
            id='uuid-123',
            email='user@university.ac.kr',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        mock_repo = Mock()
        mock_repo.get_by_id.return_value = existing_user
        mock_repo.update.return_value = User(
            id='uuid-123',
            email='user@university.ac.kr',  # 변경되지 않음
            full_name='김철수',
            department='전자공학과',
            role='user',  # 변경되지 않음
            is_active=True
        )

        service = ProfileService(user_repository=mock_repo)

        # 공격: 이메일과 역할 변경 시도
        profile_data = {
            'full_name': '김철수',
            'department': '전자공학과',
            'email': 'hacker@evil.com',  # 무시되어야 함
            'role': 'admin'  # 무시되어야 함
        }

        # Act
        updated_user = service.update_profile('uuid-123', profile_data)

        # Assert - 이메일과 역할은 변경되지 않음
        assert updated_user.email == 'user@university.ac.kr'
        assert updated_user.role == 'user'
