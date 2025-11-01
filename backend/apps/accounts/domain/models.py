"""
사용자 도메인 모델 (Domain Layer)

이 모델은 순수 비즈니스 로직만 포함하며, Django ORM과 독립적입니다.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """사용자 도메인 모델

    Attributes:
        id: 사용자 고유 ID (UUID)
        email: 이메일 주소
        full_name: 전체 이름
        role: 역할 ('admin' 또는 'user')
        is_active: 계정 활성화 여부
        department: 부서명 (선택)
        profile_picture_url: 프로필 사진 URL (선택)
        created_at: 생성 일시 (선택)
        updated_at: 수정 일시 (선택)
    """
    id: str
    email: str
    full_name: str
    role: str  # 'admin' or 'user'
    is_active: bool
    department: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_admin(self) -> bool:
        """관리자 권한 여부 확인

        Returns:
            bool: 역할이 'admin'이면 True, 그렇지 않으면 False
        """
        return self.role == 'admin'

    def __repr__(self) -> str:
        """문자열 표현

        Returns:
            str: User 객체의 문자열 표현
        """
        return f"User(id={self.id}, email={self.email}, role={self.role})"
