"""
Production Health & Readiness Check Views for WorthIQ Backend.
Used by Render, Docker orchestrators, and monitoring services.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from django.utils import timezone
import logging

logger = logging.getLogger("config.health")

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Liveness probe.
    Returns HTTP 200 if the WSGI/ASGI application worker is running.
    """
    return Response({
        "status": "healthy",
        "service": "worthiq-backend",
        "timestamp": timezone.now().isoformat(),
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def readiness_check(request):
    """
    Readiness probe.
    Validates PostgreSQL database connectivity and ML model loading state.
    Returns HTTP 200 if ready to serve traffic, or HTTP 503 Service Unavailable.
    """
    checks = {
        "database": False,
        "ml_registry": False,
    }
    details = {}

    # 1. Database Connectivity Check
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if row and row[0] == 1:
                checks["database"] = True
                details["database"] = "connected"
    except Exception as e:
        logger.warning(f"Health check database failure: {e}")
        details["database"] = "disconnected"

    # 2. ML Model Registry Check
    try:
        from apps.predictions.services.model_loader import MLModelRegistry
        registry = MLModelRegistry()
        if not registry.is_ready():
            # Attempt to lazy-load artifacts
            registry.load_artifacts()
        if registry.is_ready():
            checks["ml_registry"] = True
            details["ml_registry"] = "loaded"
        else:
            details["ml_registry"] = "uninitialized"
    except Exception as e:
        logger.warning(f"Health check ML registry failure: {e}")
        details["ml_registry"] = f"error: {str(e)}"

    all_ready = all(checks.values())
    http_status = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    return Response({
        "status": "ready" if all_ready else "not_ready",
        "service": "worthiq-backend",
        "checks": checks,
        "details": details,
        "timestamp": timezone.now().isoformat(),
    }, status=http_status)
