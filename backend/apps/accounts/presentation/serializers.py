"""사용자 프로필 Serializer"""

from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    """사용자 프로필 Serializer"""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField(allow_null=True)
    department = serializers.CharField(allow_null=True)
    role = serializers.CharField()
    profile_picture_url = serializers.CharField(allow_null=True)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)


class ProfileUpdateSerializer(serializers.Serializer):
    """프로필 업데이트 Serializer"""

    full_name = serializers.CharField(min_length=2, max_length=50, required=False)
    department = serializers.CharField(max_length=100, required=False, allow_null=True)
    profile_picture_url = serializers.URLField(required=False, allow_null=True)


class ChangePasswordSerializer(serializers.Serializer):
    """비밀번호 변경 Serializer"""

    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
