"""사용자 프로필 API View"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from infrastructure.authentication.supabase_auth import SupabaseAuthentication
from apps.accounts.services.profile_service import ProfileService
from apps.accounts.presentation.serializers import (
    UserProfileSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer
)
from apps.core.exceptions import ResourceNotFoundError, ValidationError


class ProfileView(APIView):
    """사용자 프로필 API View"""

    authentication_classes = [SupabaseAuthentication]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.profile_service = ProfileService()

    def get(self, request):
        """사용자 프로필 조회"""
        try:
            user_id = request.user
            user = self.profile_service.get_profile(user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResourceNotFoundError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        """사용자 프로필 업데이트"""
        try:
            user_id = request.user
            serializer = ProfileUpdateSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_user = self.profile_service.update_profile(user_id, serializer.validated_data)
            response_serializer = UserProfileSerializer(updated_user)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ResourceNotFoundError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@authentication_classes([SupabaseAuthentication])
def change_password(request):
    """비밀번호 변경 API

    현재 프론트엔드에서 Supabase Auth를 직접 호출하여 비밀번호를 변경합니다.
    백엔드 API는 선택사항입니다.

    Supabase Auth API 사용 예시 (프론트엔드):
    - supabase.auth.updateUser({ password: new_password })
    """
    serializer = ChangePasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 비밀번호 변경은 프론트엔드에서 Supabase Auth API를 직접 호출하는 것을 권장합니다.
    # 백엔드 API 구현이 필요한 경우, Supabase Admin API를 사용하여 구현할 수 있습니다.
    return Response(
        {
            'message': '비밀번호 변경은 프론트엔드에서 Supabase Auth API를 직접 호출해주세요.',
            'guide': 'supabase.auth.updateUser({ password: new_password })'
        },
        status=status.HTTP_501_NOT_IMPLEMENTED
    )
