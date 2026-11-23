"""
Serializers for Resume Document Uploads and Extraction Results.
"""

from rest_framework import serializers
from .models import ResumeDocument, ResumeExtraction

class ResumeDocumentSerializer(serializers.ModelSerializer):
    has_extraction = serializers.SerializerMethodField()
    file_size_formatted = serializers.SerializerMethodField()

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
            'processed_at',
            'has_extraction',
        ]
        read_only_fields = fields

    def get_has_extraction(self, obj):
        return hasattr(obj, 'extraction')

    def get_file_size_formatted(self, obj):
        size_kb = obj.file_size / 1024.0
        if size_kb >= 1024:
            return f"{round(size_kb / 1024.0, 2)} MB"
        return f"{round(size_kb, 1)} KB"


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
        required=True,
        min_length=1,
        error_messages={"min_length": "At least one skill must be confirmed to sync with profile."}
    )
    apply_job_role = serializers.BooleanField(default=False)
    apply_experience = serializers.BooleanField(default=False)
    apply_education = serializers.BooleanField(default=False)
