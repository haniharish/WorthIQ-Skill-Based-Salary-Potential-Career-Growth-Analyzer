"""
WorthIQ AI Intelligence Serializers
DRF serializers for SHAP explainability, skills, role matching, and roadmaps.
"""

from rest_framework import serializers
from apps.intelligence.models import (
    CanonicalSkill,
    JobRole,
    RoleSkillRequirement,
    PredictionExplanation,
    CareerRoadmap,
    RoadmapStage,
    RoadmapSkillProgress
)

class CanonicalSkillSerializer(serializers.ModelSerializer):
    aliases = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='alias'
    )

    class Meta:
        model = CanonicalSkill
        fields = ('id', 'name', 'category', 'description', 'market_importance_tier', 'aliases')


class RoleSkillRequirementSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = RoleSkillRequirement
        fields = ('id', 'skill_name', 'category', 'is_mandatory', 'importance_weight')


class JobRoleSerializer(serializers.ModelSerializer):
    skill_requirements = RoleSkillRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = JobRole
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'min_exp',
            'max_exp',
            'median_salary',
            'p10_salary',
            'p90_salary',
            'dataset_coverage_count',
            'skill_requirements'
        )


class PredictionExplanationSerializer(serializers.ModelSerializer):
    prediction_id = serializers.IntegerField(source='prediction.id', read_only=True)
    job_role = serializers.CharField(source='prediction.job_role', read_only=True)
    location = serializers.CharField(source='prediction.location', read_only=True)
    years_of_experience = serializers.DecimalField(
        source='prediction.years_of_experience',
        max_digits=4,
        decimal_places=1,
        read_only=True
    )

    class Meta:
        model = PredictionExplanation
        fields = (
            'id',
            'prediction_id',
            'job_role',
            'location',
            'years_of_experience',
            'base_value_log',
            'base_value_inr',
            'predicted_value_log',
            'predicted_value_inr',
            'total_delta_inr',
            'feature_attributions',
            'positive_contributors',
            'negative_contributors',
            'skills_impact',
            'summary_narrative',
            'model_version',
            'created_at'
        )


class RoadmapSkillProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapSkillProgress
        fields = (
            'id',
            'skill_name',
            'category',
            'importance',
            'is_completed',
            'completed_at'
        )


class RoadmapStageSerializer(serializers.ModelSerializer):
    skills_progress = RoadmapSkillProgressSerializer(many=True, read_only=True)

    class Meta:
        model = RoadmapStage
        fields = (
            'id',
            'stage_number',
            'title',
            'objective',
            'prerequisites',
            'project_suggestion',
            'is_completed',
            'completed_at',
            'skills_progress'
        )


class CareerRoadmapListSerializer(serializers.ModelSerializer):
    target_role_title = serializers.CharField(source='target_role.title', read_only=True)
    stages_count = serializers.IntegerField(source='stages.count', read_only=True)

    class Meta:
        model = CareerRoadmap
        fields = (
            'id',
            'title',
            'current_role',
            'target_role',
            'target_role_title',
            'overall_progress_pct',
            'stages_count',
            'is_saved',
            'created_at',
            'updated_at'
        )


class CareerRoadmapDetailSerializer(serializers.ModelSerializer):
    target_role_title = serializers.CharField(source='target_role.title', read_only=True)
    target_role_description = serializers.CharField(source='target_role.description', read_only=True)
    stages = RoadmapStageSerializer(many=True, read_only=True)

    class Meta:
        model = CareerRoadmap
        fields = (
            'id',
            'title',
            'current_role',
            'current_experience',
            'current_skills',
            'target_role',
            'target_role_title',
            'target_role_description',
            'overall_progress_pct',
            'is_saved',
            'stages',
            'created_at',
            'updated_at'
        )


# Request Input Serializers

class CounterfactualCompareSerializer(serializers.Serializer):
    job_role = serializers.CharField(max_length=150, default='Software Developer')
    years_of_experience = serializers.FloatField(min_value=0.0, max_value=60.0, default=3.0)
    location = serializers.CharField(max_length=150, default='Bengaluru')
    education = serializers.CharField(max_length=150, default="Bachelor's Degree")
    skills = serializers.ListField(child=serializers.CharField(), default=list)
    add_skills = serializers.ListField(child=serializers.CharField(), default=list)
    remove_skills = serializers.ListField(child=serializers.CharField(), default=list)


class RoleMatchInputSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    experience = serializers.FloatField(min_value=0.0, max_value=60.0, required=False, default=0.0)


class GenerateRoadmapInputSerializer(serializers.Serializer):
    target_role_id = serializers.IntegerField(required=True)
    current_role = serializers.CharField(max_length=150, required=False, allow_blank=True)
    current_experience = serializers.FloatField(min_value=0.0, max_value=60.0, required=False)
    current_skills = serializers.ListField(child=serializers.CharField(), required=False)


class UpdateProgressSerializer(serializers.Serializer):
    skill_progress_id = serializers.IntegerField(required=False)
    stage_id = serializers.IntegerField(required=False)
    is_completed = serializers.BooleanField(required=True)
