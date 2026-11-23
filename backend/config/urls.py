from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/profile/', include('apps.profiles.urls')),
    path('api/predictions/', include('apps.predictions.urls')),
    path('api/intelligence/', include('apps.intelligence.urls')),
]
