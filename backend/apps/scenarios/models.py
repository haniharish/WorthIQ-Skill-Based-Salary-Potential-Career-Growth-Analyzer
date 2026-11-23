"""
Models for What-If Salary Scenarios and Simulation.
"""

from django.db import models
from django.conf import settings

class SalaryScenario(models.Model):
    """
    Persisted user scenario representing an exploratory career profile
    and its machine learning salary evaluation snapshot.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenarios'
    )
    name = models.CharField(max_length=150, help_text="User-defined scenario title")
    job_role = models.CharField(max_length=150)
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1)
    location = models.CharField(max_length=150)
    education = models.CharField(max_length=150, default="Bachelor's Degree")
    skills = models.JSONField(default=list, help_text="List of candidate skills in scenario")
    prediction_snapshot = models.JSONField(
        null=True,
        blank=True,
        help_text="Cached prediction bounds (low, median, high) and confidence"
    )
    notes = models.TextField(blank=True, default="", help_text="Optional user notes on scenario goal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worthiq_salary_scenarios'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - Scenario '{self.name}' ({self.job_role})"
