from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .health import health_check, readiness_check

urlpatterns = [
    # Health checks for Render, Docker, and uptime monitoring
    path('health/', health_check, name='health_check'),
    path('ready/', readiness_check, name='readiness_check'),
    path('api/health/', health_check, name='api_health_check'),
    path('api/ready/', readiness_check, name='api_readiness_check'),

    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/profile/', include('apps.profiles.urls')),
    path('api/predictions/', include('apps.predictions.urls')),
    path('api/intelligence/', include('apps.intelligence.urls')),
    path('api/scenarios/', include('apps.scenarios.urls')),
    path('api/resumes/', include('apps.resumes.urls')),
    path('api/reports/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

