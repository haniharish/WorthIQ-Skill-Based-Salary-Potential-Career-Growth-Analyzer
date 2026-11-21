from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Skill(models.Model):
    """Normalized Skill Model."""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """User Profile Model with normalized M2M skills relationship."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    job_role = models.CharField(
        max_length=150,
        help_text="Current or desired job role (e.g. Full Stack Developer, Data Scientist)"
    )
    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text="Years of professional experience (0 for freshers)"
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Current location or preferred city/country"
    )
    education = models.CharField(
        max_length=150,
        blank=True,
        default='',
        help_text="Highest level of education (e.g., B.Tech, M.S, MCA, Bachelor's)"
    )
    current_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Optional current annual salary (in currency or LPA)"
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='profiles',
        blank=True,
        help_text="Normalized Many-to-Many skills relationship"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.email} - {self.job_role} ({self.years_of_experience} yrs)"
