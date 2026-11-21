from django.contrib import admin
from .models import UserProfile, Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_role', 'years_of_experience', 'location', 'education', 'current_salary', 'created_at')
    list_filter = ('job_role', 'education', 'created_at')
    search_fields = ('user__email', 'user__full_name', 'job_role', 'location')
    filter_horizontal = ('skills',)
    ordering = ('-updated_at',)
