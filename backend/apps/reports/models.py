"""
Models for Advanced Career Reports and Data Snapshots.
"""

from django.db import models
from django.conf import settings

class AdvancedReport(models.Model):
    """
    Structured career intelligence report snapshot eligible for PDF/CSV generation.
    """
    REPORT_TYPES = [
        ('salary_prediction', 'Salary Prediction Report'),
        ('shap_explanation', 'Salary Explanation Report'),
        ('skill_intelligence', 'Skill Intelligence Report'),
        ('role_matching', 'Job Role Matching Report'),
        ('career_roadmap', 'Career Roadmap Report'),
        ('scenario_comparison', 'What-If Comparison Report'),
        ('resume_analysis', 'Resume Skill Analysis Report'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    source_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID of source prediction/scenario")
    summary = models.TextField(blank=True, default="")
    data_snapshot = models.JSONField(
        default=dict,
        help_text="Complete frozen snapshot of data evaluated at report creation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worthiq_advanced_reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'report_type']),
        ]

    def __str__(self):
        return f"{self.user.email} - [{self.get_report_type_display()}] {self.title}"
