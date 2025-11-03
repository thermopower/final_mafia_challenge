"""
URL configuration for university dashboard project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health_check(request):
    """Health check endpoint for Railway"""
    from django.views.decorators.csrf import csrf_exempt
    return JsonResponse({
        'status': 'healthy',
        'service': 'university-dashboard-api',
        'timestamp': '2025-11-03T12:00:00Z'
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/health/', health_check, name='health_check'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API endpoints
    path('api/dashboard/', include('apps.dashboard.presentation.urls')),
    path('api/uploads/', include('apps.uploads.presentation.urls')),
    path('api/data/', include('apps.data.presentation.urls')),
    path('api/accounts/', include('apps.accounts.presentation.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Django Debug Toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns = [
            path('__debug__/', include('debug_toolbar.urls')),
        ] + urlpatterns
