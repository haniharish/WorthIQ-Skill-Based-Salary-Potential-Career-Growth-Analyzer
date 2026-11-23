"""
WorthIQ AI Intelligence Database Models
Entities for Explainable AI, Skill Normalization, Job Role Catalog, and Personalized Roadmaps.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class CanonicalSkill(models.Model):
    """Normalized technical skill entity."""
    CATEGORY_CHOICES = [
        ('Programming Languages', 'Programming Languages'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Databases', 'Databases'),
        ('Cloud & DevOps', 'Cloud & DevOps'),
        ('Data & AI', 'Data & AI'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    description = models.TextField(blank=True, default='')
    market_importance_tier = models.CharField(max_length=20, default='Tier-1')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Canonical Skill'
        verbose_name_plural = 'Canonical Skills'

    def __str__(self):
        return f"{self.name} ({self.category})"


class SkillAlias(models.Model):
    """Lookup table mapping aliases, abbreviations, and common typos to CanonicalSkill."""
    alias = models.CharField(max_length=100, unique=True, db_index=True)
    canonical_skill = models.ForeignKey(
        CanonicalSkill,
        on_delete=models.CASCADE,
        related_name='aliases'
    )

    class Meta:
        ordering = ['alias']
        verbose_name = 'Skill Alias'
        verbose_name_plural = 'Skill Aliases'

    def __str__(self):
        return f"{self.alias} -> {self.canonical_skill.name}"


class JobRole(models.Model):
    """Curated technology role catalog with empirical salary and experience benchmarks."""
    title = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField()
    min_exp = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(40)]
    )
    max_exp = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=15.0,
        validators=[MinValueValidator(0), MaxValueValidator(40)]
    )
    median_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0,
        help_text="Empirical median annual compensation in INR"
    )
    p10_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0,
        help_text="10th percentile annual compensation in INR"
    )
    p90_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.0,
        help_text="90th percentile annual compensation in INR"
    )
    dataset_coverage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Job Role'
        verbose_name_plural = 'Job Roles'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RoleSkillRequirement(models.Model):
    """Associates job roles with mandatory and preferred technical skills."""
    role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
        related_name='skill_requirements'
    )
    skill = models.ForeignKey(
        CanonicalSkill,
        on_delete=models.CASCADE,
        related_name='role_requirements'
    )
    is_mandatory = models.BooleanField(
        default=True,
        help_text="True for required core skills; False for preferred complementary skills"
    )
    importance_weight = models.FloatField(default=1.0)

    class Meta:
        unique_together = ('role', 'skill')
        ordering = ['-is_mandatory', 'skill__name']
        verbose_name = 'Role Skill Requirement'
        verbose_name_plural = 'Role Skill Requirements'

    def __str__(self):
        status = "Required" if self.is_mandatory else "Preferred"
        return f"{self.role.title} - {self.skill.name} ({status})"


class PredictionExplanation(models.Model):
    """
    Persisted SHAP explainability record linked 1-to-1 with a salary prediction.
    Caches calculated local SHAP values and narrative breakdowns.
    """
    prediction = models.OneToOneField(
        'predictions.Prediction',
        on_delete=models.CASCADE,
        related_name='explanation'
    )
    base_value_log = models.FloatField(help_text="Expected value E[f(x)] in log-space")
    base_value_inr = models.DecimalField(max_digits=12, decimal_places=2)
    predicted_value_log = models.FloatField(help_text="Final predicted value in log-space")
    predicted_value_inr = models.DecimalField(max_digits=12, decimal_places=2)
    total_delta_inr = models.DecimalField(max_digits=12, decimal_places=2)
    feature_attributions = models.JSONField(
        default=list,
        help_text="Ranked array of individual feature SHAP contributions"
    )
    positive_contributors = models.JSONField(
        default=list,
        help_text="Top positive drivers boosting salary"
    )
    negative_contributors = models.JSONField(
        default=list,
        help_text="Top limiting or dragging factors"
    )
    skills_impact = models.JSONField(
        default=list,
        help_text="Specific SHAP attributions for evaluated skills"
    )
    summary_narrative = models.TextField(help_text="Human-readable explanation of salary drivers")
    model_version = models.CharField(max_length=50, default='2.0.0')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prediction Explanation'
        verbose_name_plural = 'Prediction Explanations'

    def __str__(self):
        return f"Explanation for Prediction #{self.prediction_id} (Delta: ₹{self.total_delta_inr:,.0f})"


class CareerRoadmap(models.Model):
    """
    Personalized career roadmap entity tracking a candidate's journey from their
    current skill profile to a target technology role.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='career_roadmaps',
        db_index=True
    )
    target_role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE,
        related_name='roadmaps'
    )
    current_role = models.CharField(max_length=150, blank=True, default='')
    current_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(60)]
    )
    current_skills = models.JSONField(
        default=list,
        help_text="Snapshot of candidate's starting technical skills"
    )
    title = models.CharField(max_length=200)
    overall_progress_pct = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_saved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Career Roadmap'
        verbose_name_plural = 'Career Roadmaps'

    def update_progress(self):
        """Recomputes overall completion percentage from all stage skills."""
        stages = self.stages.all()
        if not stages.exists():
            self.overall_progress_pct = 0
            self.save(update_fields=['overall_progress_pct', 'updated_at'])
            return 0

        total_skills = RoadmapSkillProgress.objects.filter(stage__in=stages).count()
        if total_skills == 0:
            completed_stages = stages.filter(is_completed=True).count()
            self.overall_progress_pct = int((completed_stages / stages.count()) * 100)
        else:
            completed_skills = RoadmapSkillProgress.objects.filter(
                stage__in=stages,
                is_completed=True
            ).count()
            self.overall_progress_pct = int((completed_skills / total_skills) * 100)

        self.save(update_fields=['overall_progress_pct', 'updated_at'])
        return self.overall_progress_pct

    def __str__(self):
        return f"{self.user.email} -> {self.target_role.title} ({self.overall_progress_pct}%)"


class RoadmapStage(models.Model):
    """A milestone stage within a personalized career roadmap."""
    roadmap = models.ForeignKey(
        CareerRoadmap,
        on_delete=models.CASCADE,
        related_name='stages'
    )
    stage_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    objective = models.TextField()
    prerequisites = models.CharField(max_length=255, blank=True, default='')
    project_suggestion = models.JSONField(
        default=dict,
        help_text="Practical project title, stack, deliverables, and completion criteria"
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['stage_number']
        unique_together = ('roadmap', 'stage_number')
        verbose_name = 'Roadmap Stage'
        verbose_name_plural = 'Roadmap Stages'

    def __str__(self):
        return f"Stage {self.stage_number}: {self.title}"


class RoadmapSkillProgress(models.Model):
    """Tracks completion of a specific skill within a roadmap stage."""
    stage = models.ForeignKey(
        RoadmapStage,
        on_delete=models.CASCADE,
        related_name='skills_progress'
    )
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, default='Technical Skill')
    importance = models.CharField(max_length=20, default='Mandatory')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['is_completed', 'skill_name']
        unique_together = ('stage', 'skill_name')
        verbose_name = 'Roadmap Skill Progress'
        verbose_name_plural = 'Roadmap Skill Progresses'

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"{self.skill_name} ({status})"
