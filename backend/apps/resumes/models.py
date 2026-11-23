"""
Models for Resume Documents and Information Extraction.
"""

from django.db import models
from django.conf import settings

class ResumeDocument(models.Model):
    """
    Uploaded resume file record stored privately per user.
    """
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('parsing', 'Parsing'),
        ('extracted', 'Extracted'),
        ('failed', 'Processing Failed'),
        ('applied', 'Applied to Profile'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    original_filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/%Y/%m/')
    file_size = models.IntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=20, help_text="pdf or docx")
    processing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='uploaded')
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'worthiq_resume_documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.original_filename} ({self.processing_status})"


class ResumeExtraction(models.Model):
    """
    Structured information extracted from a resume document.
    """
    resume_document = models.OneToOneField(
        ResumeDocument,
        on_delete=models.CASCADE,
        related_name='extraction'
    )
    extracted_skills = models.JSONField(
        default=list,
        help_text="Extracted skills with canonical mapping, category, confidence, and snippet"
    )
    candidate_info = models.JSONField(
        default=dict,
        help_text="Detected candidate metadata: name, email, phone, experience, education, job titles"
    )
    raw_text_length = models.IntegerField(default=0)
    warnings = models.JSONField(default=list, help_text="Extraction warnings or unreadable sections")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worthiq_resume_extractions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Extraction for {self.resume_document.original_filename}"
