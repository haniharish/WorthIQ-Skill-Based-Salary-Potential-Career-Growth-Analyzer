"""
Serializers for Resume Document Uploads and Extraction Results.
"""

from rest_framework import serializers
from .models import ResumeDocument, ResumeExtraction

class ResumeDocumentSerializer(serializers.ModelSerializer):
    has_extraction = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()
    extracted_skills_count = serializers.SerializerMethodField()
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = ResumeDocument
        fields = [
            'id',
            'original_filename',
            'file_size',
            'file_size_formatted',
            'file_type',
            'processing_status',
            'error_message',
            'created_at',
            'uploaded_at',
            'processed_at',
            'has_extraction',
            'extracted_skills_count',
        ]
        read_only_fields = fields

    def get_has_extraction(self, obj):
        return hasattr(obj, 'extraction')

    def get_file_size_formatted(self, obj):
        size_kb = obj.file_size / 1024.0
        if size_kb >= 1024:
            return f"{round(size_kb / 1024.0, 2)} MB"
        return f"{round(size_kb, 1)} KB"

    def get_extracted_skills_count(self, obj):
        if hasattr(obj, 'extraction') and obj.extraction and obj.extraction.extracted_skills:
            return len(obj.extraction.extracted_skills)
        return 0


class ResumeExtractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeExtraction
        fields = [
            'id',
            'extracted_skills',
            'candidate_info',
            'raw_text_length',
            'warnings',
            'created_at',
        ]
        read_only_fields = fields


class ApplyToProfileInputSerializer(serializers.Serializer):
    confirmed_skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list
    )
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list
    )
    apply_job_role = serializers.BooleanField(default=False)
    apply_experience = serializers.BooleanField(default=False)
    apply_education = serializers.BooleanField(default=False)

    def validate(self, attrs):
        confirmed = attrs.get('confirmed_skills') or attrs.get('skills') or []
        if not confirmed:
            raise serializers.ValidationError({"confirmed_skills": "At least one skill must be confirmed to sync with profile."})
        attrs['confirmed_skills'] = confirmed
        return attrs
