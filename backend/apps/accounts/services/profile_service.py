"""프로필 관리 서비스"""

from typing import Dict, Any
from apps.core.exceptions import ResourceNotFoundError, ValidationError
from apps.accounts.domain.models import User
from apps.accounts.repositories.user_repository import UserRepository


class ProfileService:
    """프로필 관리 서비스"""

    def __init__(self, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()

    def get_profile(self, user_id: str) -> User:
        """사용자 프로필 조회"""
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise ResourceNotFoundError("사용자를 찾을 수 없습니다")

        return user

    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> User:
        """사용자 프로필 업데이트

        Args:
            user_id: 사용자 ID
            profile_data: 업데이트할 프로필 데이터
                - full_name: 이름 (2-50자)
                - department: 부서명
                - profile_picture_url: 프로필 사진 URL (선택)

        Returns:
            User: 업데이트된 사용자 도메인 모델

        Raises:
            ResourceNotFoundError: 사용자를 찾을 수 없는 경우
            ValidationError: 입력 데이터가 유효하지 않은 경우
        """
        # 사용자 존재 확인
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundError("사용자를 찾을 수 없습니다")

        # 수정 가능한 필드만 추출 (읽기 전용 필드 제거)
        allowed_fields = {'full_name', 'department', 'profile_picture_url'}
        update_data = {k: v for k, v in profile_data.items() if k in allowed_fields}

        # 유효성 검증
        if 'full_name' in update_data:
            full_name = update_data['full_name']
            if len(full_name) < 2 or len(full_name) > 50:
                raise ValidationError("이름은 2자 이상 50자 이하여야 합니다")

        # 업데이트 실행
        updated_user = self.user_repository.update(user_id, update_data)
        return updated_user
