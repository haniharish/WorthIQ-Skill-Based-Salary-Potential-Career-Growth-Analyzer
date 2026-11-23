"""
SHAP Explainability Views
Serves local per-prediction SHAP explanations and global model importance.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from apps.intelligence.services.shap_service import (
    get_or_create_explanation,
    get_global_explanations
)
from apps.intelligence.serializers import PredictionExplanationSerializer

class PredictionExplanationDetailView(APIView):
    """
    GET /api/intelligence/explanations/{prediction_id}/
    Returns detailed SHAP feature attributions and narrative explanation
    for a specific prediction belonging to the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, prediction_id):
        try:
            explanation = get_or_create_explanation(
                prediction_id=prediction_id,
                user=request.user
            )
            serializer = PredictionExplanationSerializer(explanation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"detail": f"Failed to compute SHAP explanation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GlobalExplanationView(APIView):
    """
    GET /api/intelligence/explanations/global/
    Returns global feature importance rankings, top skills impact,
    and baseline expected values across the full training dataset.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            global_data = get_global_explanations()
            return Response(global_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": f"Failed to load global explanations: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
