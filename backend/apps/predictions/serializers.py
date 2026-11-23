"""
Serializers for Salary Prediction and History Endpoints.
"""

from rest_framework import serializers
from .models import Prediction

class SalaryPredictionInputSerializer(serializers.Serializer):
    """Input payload validation for salary prediction requests."""
    job_role = serializers.CharField(
        max_length=150,
        required=True,
        error_messages={"required": "Job role is required.", "blank": "Job role cannot be blank."}
    )
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True,
        min_length=1,
        error_messages={
            "required": "Skills list is required.",
            "min_length": "At least one skill must be provided."
        }
    )
    years_of_experience = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        min_value=0,
        max_value=60,
        required=True,
        error_messages={
            "required": "Years of experience is required.",
            "min_value": "Experience cannot be negative.",
            "max_value": "Experience cannot exceed 60 years."
        }
    )
    location = serializers.CharField(
        max_length=150,
        required=True,
        error_messages={"required": "Location is required.", "blank": "Location cannot be blank."}
    )
    education = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        default="Bachelor's Degree"
    )

class PredictionHistorySerializer(serializers.ModelSerializer):
    """Serializer for user prediction history records."""
    salary_range = serializers.SerializerMethodField()
    salary_lpa = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            'id',
            'job_role',
            'skills',
            'years_of_experience',
            'location',
            'education',
            'predicted_low_salary',
            'predicted_median_salary',
            'predicted_high_salary',
            'salary_range',
            'salary_lpa',
            'confidence',
            'model_version',
            'created_at'
        ]
        read_only_fields = fields

    def get_salary_range(self, obj):
        return {
            "low": float(obj.predicted_low_salary),
            "median": float(obj.predicted_median_salary),
            "high": float(obj.predicted_high_salary)
        }

    def get_salary_lpa(self, obj):
        return round(float(obj.predicted_median_salary) / 100_000.0, 2)
