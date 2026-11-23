"""
Serializers for Salary Scenarios and What-If Simulations.
"""

from rest_framework import serializers
from .models import SalaryScenario

class SalaryScenarioSerializer(serializers.ModelSerializer):
    """Full detail serializer for SalaryScenario records."""
    salary_range = serializers.SerializerMethodField()
    salary_lpa = serializers.SerializerMethodField()

    class Meta:
        model = SalaryScenario
        fields = [
            'id',
            'name',
            'job_role',
            'years_of_experience',
            'location',
            'education',
            'skills',
            'prediction_snapshot',
            'salary_range',
            'salary_lpa',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'salary_range', 'salary_lpa']

    def get_salary_range(self, obj):
        if obj.prediction_snapshot and 'salary_range' in obj.prediction_snapshot:
            return obj.prediction_snapshot['salary_range']
        return None

    def get_salary_lpa(self, obj):
        if obj.prediction_snapshot and 'salary_lpa' in obj.prediction_snapshot:
            return obj.prediction_snapshot['salary_lpa']
        return None


class ScenarioCreateUpdateSerializer(serializers.Serializer):
    """Validation serializer for creating and updating scenarios."""
    name = serializers.CharField(max_length=150, required=True)
    job_role = serializers.CharField(max_length=150, required=True)
    years_of_experience = serializers.DecimalField(max_digits=4, decimal_places=1, min_value=0, max_value=60, required=True)
    location = serializers.CharField(max_length=150, required=True)
    education = serializers.CharField(max_length=150, required=False, default="Bachelor's Degree")
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True,
        min_length=1,
        error_messages={"min_length": "At least one skill must be provided for the scenario."}
    )
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class ScenarioCompareInputSerializer(serializers.Serializer):
    """Validation serializer for comparing multiple scenarios."""
    baseline = serializers.DictField(
        required=False,
        default=None,
        help_text="Optional custom baseline profile"
    )
    scenario_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
        help_text="IDs of saved scenarios to include in comparison"
    )
    new_scenarios = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text="Optional unsaved scenario payloads to include in comparison"
    )
    scenarios = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text="Alias for new_scenarios"
    )
    include_baseline = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether to include user's active profile as baseline"
    )

    def validate(self, attrs):
        scenarios_list = attrs.get('scenarios', [])
        new_scenarios_list = attrs.get('new_scenarios', [])
        combined_scenarios = new_scenarios_list or scenarios_list
        attrs['new_scenarios'] = combined_scenarios

        has_baseline = bool(attrs.get('baseline')) or attrs.get('include_baseline', True)
        total_count = len(attrs.get('scenario_ids', [])) + len(combined_scenarios)
        if has_baseline:
            total_count += 1

        if total_count < 2:
            raise serializers.ValidationError("At least 2 profiles (including baseline) are required for comparison.")
        if total_count > 5:
            raise serializers.ValidationError("A maximum of 4 scenarios can be compared simultaneously with baseline.")
        return attrs
