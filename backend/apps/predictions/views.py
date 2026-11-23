"""
Views for Salary Predictions and Prediction History.
"""

import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Prediction
from .serializers import (
    SalaryPredictionInputSerializer,
    PredictionHistorySerializer
)
from .services.salary_prediction import predict_salary_profile
from .services.model_loader import get_model_registry, ModelLoadingError

logger = logging.getLogger("predictions.views")

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class SalaryPredictionView(APIView):
    """
    POST /api/predictions/salary/
    Generates real-time machine learning salary prediction and persists
    the prediction record to the user's history in PostgreSQL.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SalaryPredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        try:
            # 1. Run ML prediction pipeline
            result = predict_salary_profile(
                job_role=data["job_role"],
                years_of_experience=float(data["years_of_experience"]),
                location=data["location"],
                skills=data["skills"],
                education=data.get("education", "Bachelor's Degree")
            )

            # 2. Persist to Prediction model
            prediction_record = Prediction.objects.create(
                user=request.user,
                job_role=result["job_role"],
                skills=result["skills_evaluated"],
                years_of_experience=data["years_of_experience"],
                location=result["location"],
                education=result["education"],
                predicted_low_salary=result["salary_range"]["low"],
                predicted_median_salary=result["salary_range"]["median"],
                predicted_high_salary=result["salary_range"]["high"],
                confidence=result["confidence"],
                model_version=result["model_version"]
            )

            # 3. Construct API response
            response_payload = {
                "prediction_id": prediction_record.id,
                "currency": result["currency"],
                "salary_period": result["salary_period"],
                "job_role": result["job_role"],
                "location": result["location"],
                "years_of_experience": float(data["years_of_experience"]),
                "education": result["education"],
                "skills_evaluated": result["skills_evaluated"],
                "salary_range": result["salary_range"],
                "salary_lpa": result["salary_lpa"],
                "confidence": result["confidence"],
                "confidence_details": result["confidence_details"],
                "model_version": result["model_version"],
                "top_contributing_skills": result["top_contributing_skills"],
                "high_value_skills_to_learn": result["high_value_skills_to_learn"],
                "created_at": prediction_record.created_at.isoformat(),
                "message": result["message"]
            }

            return Response(response_payload, status=status.HTTP_201_CREATED)

        except ModelLoadingError as e:
            logger.error(f"Prediction service unavailable: {e}")
            return Response(
                {
                    "error": "Prediction Service Unavailable",
                    "detail": "Salary prediction model artifacts are currently loading or unavailable. Please try again shortly."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.exception(f"Unexpected prediction failure: {e}")
            return Response(
                {
                    "error": "Prediction Failed",
                    "detail": "An internal error occurred while processing salary prediction."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PredictionHistoryListView(APIView):
    """
    GET /api/predictions/history/
    Returns paginated prediction history belonging strictly to the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        queryset = Prediction.objects.filter(user=request.user).order_by('-created_at')
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = PredictionHistorySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
            
        serializer = PredictionHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PredictionHistoryDetailView(APIView):
    """
    GET /api/predictions/history/<int:pk>/
    Retrieves a single prediction record with strict user data isolation.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = Prediction.objects.get(pk=pk, user=request.user)
        except Prediction.DoesNotExist:
            return Response(
                {"detail": "Prediction report not found or does not belong to your account."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PredictionHistorySerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModelInfoView(APIView):
    """
    GET /api/predictions/model-info/
    Returns safe, non-sensitive model governance and evaluation metadata.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registry = get_model_registry()
        try:
            meta = registry.get_metadata()
            # Sanitize to expose only safe public metadata
            safe_info = {
                "model_name": meta.get("model_name", "Random Forest Regressor"),
                "model_version": meta.get("model_version", "2.0.0"),
                "training_timestamp": meta.get("training_timestamp"),
                "target_variable": meta.get("target_variable", "annual_salary_inr"),
                "target_currency": meta.get("target_currency", "INR"),
                "training_rows": meta.get("training_rows", 20265),
                "test_rows": meta.get("test_rows", 5067),
                "feature_count": meta.get("engineered_feature_count", 55),
                "evaluation_metrics": meta.get("evaluation_metrics", {}).get("test", {}),
                "supported_taxonomies": meta.get("supported_taxonomies", {
                    "job_roles": [
                        "Software Developer", "Full Stack Developer", "Frontend Developer",
                        "Backend Developer", "Data Analyst", "Data Scientist",
                        "Machine Learning Engineer", "DevOps Engineer"
                    ],
                    "locations": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi NCR", "Chennai"]
                })
            }
            return Response(safe_info, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Could not load model info: {e}")
            return Response(
                {"error": "Model metadata temporarily unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
