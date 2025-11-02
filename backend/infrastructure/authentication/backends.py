"""
Django REST Framework 인증 백엔드
"""
from .supabase_auth import SupabaseAuthentication, SupabaseUser

__all__ = ['SupabaseAuthentication', 'SupabaseUser']
