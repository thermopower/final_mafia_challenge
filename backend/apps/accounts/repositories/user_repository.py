"""사용자 데이터 접근 Repository"""

from typing import Optional, Dict, Any
from apps.accounts.domain.models import User
from apps.accounts.persistence.models import UserProfile


class UserRepository:
    """사용자 데이터 접근 Repository"""

    def get_by_id(self, user_id: str) -> Optional[User]:
        """ID로 사용자 조회"""
        try:
            user_orm = UserProfile.objects.get(id=user_id, is_active=True)
            return self._to_domain(user_orm)
        except UserProfile.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        try:
            user_orm = UserProfile.objects.get(email=email, is_active=True)
            return self._to_domain(user_orm)
        except UserProfile.DoesNotExist:
            return None

    def update(self, user_id: str, update_data: Dict[str, Any]) -> User:
        """사용자 정보 업데이트"""
        user_orm = UserProfile.objects.get(id=user_id, is_active=True)

        # 업데이트 가능한 필드만 수정
        if 'full_name' in update_data:
            user_orm.full_name = update_data['full_name']
        if 'department' in update_data:
            user_orm.department = update_data['department']
        if 'profile_picture_url' in update_data:
            user_orm.profile_picture_url = update_data['profile_picture_url']

        user_orm.save()
        return self._to_domain(user_orm)

    def _to_domain(self, user_orm: UserProfile) -> User:
        """ORM 모델을 도메인 모델로 변환"""
        return User(
            id=str(user_orm.id),
            email=user_orm.email,
            full_name=user_orm.full_name or '',
            department=user_orm.department,
            role=user_orm.role,
            is_active=user_orm.is_active,
            profile_picture_url=user_orm.profile_picture_url,
            created_at=user_orm.created_at,
            updated_at=user_orm.updated_at
        )
