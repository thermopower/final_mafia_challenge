"""
UserProfile ORM 모델 테스트 (TDD - RED 단계)
"""

import pytest
from django.db import IntegrityError
from apps.accounts.persistence.models import UserProfile


@pytest.mark.django_db
class TestUserProfileORM:
    """UserProfile ORM 모델 테스트"""

    def test_create_user_profile_with_valid_data(self):
        """유효한 데이터로 UserProfile 생성"""
        # Arrange & Act
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user'
        )

        # Assert
        assert user.email == 'test@example.com'
        assert user.full_name == '홍길동'
        assert user.department == '컴퓨터공학과'
        assert user.role == 'user'
        assert user.is_active is True

    def test_email_field_is_unique(self):
        """이메일 필드가 유일해야 함"""
        # Arrange
        UserProfile.objects.create(
            id='uuid-1',
            email='duplicate@example.com',
            full_name='User1',
            role='user'
        )

        # Act & Assert
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(
                id='uuid-2',
                email='duplicate@example.com',
                full_name='User2',
                role='user'
            )

    def test_default_role_is_user(self):
        """기본 역할은 'user'"""
        # Arrange & Act
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동'
        )

        # Assert
        assert user.role == 'user'

    def test_default_is_active_is_true(self):
        """기본 is_active는 True"""
        # Arrange & Act
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user'
        )

        # Assert
        assert user.is_active is True

    def test_str_method_returns_email_and_role(self):
        """__str__ 메서드가 이메일과 역할 반환"""
        # Arrange
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='admin'
        )

        # Act
        str_repr = str(user)

        # Assert
        assert 'test@example.com' in str_repr
        assert '관리자' in str_repr  # get_role_display()

    def test_created_at_auto_set_on_creation(self):
        """created_at이 생성 시 자동 설정됨"""
        # Arrange & Act
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user'
        )

        # Assert
        assert user.created_at is not None

    def test_updated_at_auto_updated_on_save(self):
        """updated_at이 저장 시 자동 업데이트됨"""
        # Arrange
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user'
        )
        original_updated_at = user.updated_at

        # Act
        user.full_name = '김철수'
        user.save()

        # Assert
        assert user.updated_at > original_updated_at

    def test_optional_fields_can_be_null(self):
        """선택적 필드는 NULL 가능"""
        # Arrange & Act
        user = UserProfile.objects.create(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user',
            department=None,
            profile_picture_url=None
        )

        # Assert
        assert user.department is None
        assert user.profile_picture_url is None
