"""
관리자 권한 클래스
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """관리자 권한 확인"""

    def has_permission(self, request, view):
        """
        관리자 권한 확인

        Args:
            request: HTTP 요청
            view: View

        Returns:
            bool: 관리자 여부
        """
        # request.user가 있고, role 속성이 'admin'인지 확인
        return (
            request.user
            and hasattr(request.user, "role")
            and request.user.role == "admin"
        )
