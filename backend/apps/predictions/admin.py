from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'job_role', 'years_of_experience', 'location',
        'predicted_median_salary', 'confidence', 'model_version', 'created_at'
    )
    list_filter = ('job_role', 'location', 'confidence', 'model_version', 'created_at')
    search_fields = ('user__email', 'job_role', 'location')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
