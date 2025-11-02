"""
Django production settings.

프로덕션 환경(Railway)에서 사용되는 설정입니다.
"""
from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Railway provides RAILWAY_STATIC_URL which we use as our domain
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# CORS settings for production
cors_origins_raw = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000')
cors_origins = []
for origin in cors_origins_raw.split(','):
    origin = origin.strip()
    # Skip empty or internal Railway domains without scheme
    if origin and not origin.endswith('.railway.internal'):
        # Add https:// if no scheme provided (except localhost)
        if not origin.startswith(('http://', 'https://')):
            if 'localhost' in origin or '127.0.0.1' in origin:
                origin = f'http://{origin}'
            else:
                origin = f'https://{origin}'
        cors_origins.append(origin)

CORS_ALLOWED_ORIGINS = cors_origins
CORS_ALLOW_CREDENTIALS = True

# Database - Railway PostgreSQL (auto-configured via DATABASE_URL)
# Railway automatically sets DATABASE_URL environment variable
database_url = config('DATABASE_URL', default=None)
if database_url:
    DATABASES['default'] = dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
else:
    # Fallback to individual DB settings if DATABASE_URL not provided
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# WhiteNoise - Static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# React 빌드 파일을 Django static에 포함 (통합 배포)
import os
frontend_dist = BASE_DIR.parent / 'frontend' / 'dist'
if os.path.exists(frontend_dist):
    STATICFILES_DIRS = [frontend_dist]
else:
    STATICFILES_DIRS = []

# SPA (Single Page Application) 라우팅 지원
# React Router를 위한 fallback: 모든 URL이 매칭되지 않으면 index.html로 서빙
WHITENOISE_INDEX_FILE = True

# Logging - Send errors to Sentry in production (optional)
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# Use less verbose logging in production
LOGGING['root']['level'] = 'WARNING'
