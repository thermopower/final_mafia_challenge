"""
Accounts app configuration
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Accounts 앱 설정"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = '계정 관리'
