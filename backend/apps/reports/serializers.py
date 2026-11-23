"""
Serializers for Advanced Career Reports.
"""

from rest_framework import serializers
from .models import AdvancedReport

class AdvancedReportSerializer(serializers.ModelSerializer):
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)

    class Meta:
        model = AdvancedReport
        fields = [
            'id',
            'title',
            'report_type',
            'report_type_display',
            'source_id',
            'summary',
            'data_snapshot',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'report_type_display']


class GenerateReportInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    report_type = serializers.ChoiceField(choices=AdvancedReport.REPORT_TYPES, required=True)
    source_id = serializers.CharField(max_length=100, required=False, allow_blank=True, default="")
    summary = serializers.CharField(required=False, allow_blank=True, default="")
    data_snapshot = serializers.DictField(required=False, default=dict)
