from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Prediction(models.Model):
    """
    Salary Prediction History Record.
    Stores user inputs, model predictions (P10, P50, P90), confidence,
    and model version metadata with strict user isolation.
    """
    CONFIDENCE_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions',
        db_index=True
    )
    job_role = models.CharField(
        max_length=150,
        help_text="Standardized or input job role"
    )
    skills = models.JSONField(
        default=list,
        help_text="List of technical skills evaluated"
    )
    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text="Years of professional experience"
    )
    location = models.CharField(
        max_length=150,
        help_text="Geographic location or tech hub"
    )
    education = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Highest level of education"
    )
    predicted_low_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="P10 (10th percentile) estimated annual salary in INR"
    )
    predicted_median_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="P50 (Median) estimated annual salary in INR"
    )
    predicted_high_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="P90 (90th percentile) estimated annual salary in INR"
    )
    confidence = models.CharField(
        max_length=20,
        choices=CONFIDENCE_CHOICES,
        default='Medium',
        help_text="Confidence tier based on data representation and interval ratio"
    )
    model_version = models.CharField(
        max_length=50,
        default='2.0.0',
        help_text="Version of ML model bundle generating the prediction"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Salary Prediction'
        verbose_name_plural = 'Salary Predictions'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['job_role']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.job_role} (Median: ₹{self.predicted_median_salary:,.0f})"
