"""
User 도메인 모델 테스트 (TDD - RED 단계)
"""

from datetime import datetime
from apps.accounts.domain.models import User


class TestUserDomainModel:
    """User 도메인 모델 테스트"""

    def test_create_user_domain_model_with_valid_data(self):
        """유효한 데이터로 User 도메인 모델 생성"""
        # Arrange & Act
        user = User(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        # Assert
        assert user.id == 'uuid-123'
        assert user.email == 'test@example.com'
        assert user.full_name == '홍길동'
        assert user.department == '컴퓨터공학과'
        assert user.role == 'user'
        assert user.is_active is True
        assert user.is_admin() is False

    def test_is_admin_returns_true_for_admin_role(self):
        """관리자 역할일 때 is_admin() True 반환"""
        # Arrange
        admin_user = User(
            id='uuid-123',
            email='admin@example.com',
            full_name='관리자',
            department='전산팀',
            role='admin',
            is_active=True
        )

        # Act & Assert
        assert admin_user.is_admin() is True

    def test_is_admin_returns_false_for_user_role(self):
        """일반 사용자 역할일 때 is_admin() False 반환"""
        # Arrange
        user = User(
            id='uuid-123',
            email='user@example.com',
            full_name='일반사용자',
            department='컴퓨터공학과',
            role='user',
            is_active=True
        )

        # Act & Assert
        assert user.is_admin() is False

    def test_is_active_user_when_is_active_true(self):
        """활성화된 사용자일 때 is_active True"""
        # Arrange
        user = User(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user',
            is_active=True
        )

        # Act & Assert
        assert user.is_active is True

    def test_user_repr_returns_correct_format(self):
        """__repr__ 메서드가 올바른 형식 반환"""
        # Arrange
        user = User(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user',
            is_active=True
        )

        # Act
        repr_str = repr(user)

        # Assert
        assert 'uuid-123' in repr_str
        assert 'test@example.com' in repr_str
        assert 'user' in repr_str

    def test_create_user_with_optional_fields_none(self):
        """선택적 필드가 None일 때 User 생성"""
        # Arrange & Act
        user = User(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user',
            is_active=True,
            department=None,
            profile_picture_url=None,
            created_at=None,
            updated_at=None
        )

        # Assert
        assert user.department is None
        assert user.profile_picture_url is None
        assert user.created_at is None
        assert user.updated_at is None

    def test_create_user_with_timestamps(self):
        """타임스탬프를 포함하여 User 생성"""
        # Arrange
        now = datetime.now()

        # Act
        user = User(
            id='uuid-123',
            email='test@example.com',
            full_name='홍길동',
            role='user',
            is_active=True,
            created_at=now,
            updated_at=now
        )

        # Assert
        assert user.created_at == now
        assert user.updated_at == now
