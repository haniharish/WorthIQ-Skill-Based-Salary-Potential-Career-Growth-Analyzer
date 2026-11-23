"""
WorthIQ AI Intelligence URL Configuration
Maps all endpoints for SHAP explanations, skills, role matching, and roadmaps.
"""

from django.urls import path
from apps.intelligence.views.explanations import (
    PredictionExplanationDetailView,
    GlobalExplanationView
)
from apps.intelligence.views.skills import (
    SkillListView,
    SkillImpactView,
    SkillCoOccurrenceView,
    SkillCompareView
)
from apps.intelligence.views.roles import (
    JobRoleListView,
    JobRoleDetailView,
    RoleMatchView,
    RoleRecommendationsView
)
from apps.intelligence.views.roadmaps import (
    RoadmapListCreateView,
    RoadmapDetailView,
    RoadmapProgressUpdateView
)

app_name = 'intelligence'

urlpatterns = [
    # Module A: SHAP Explainability
    path('explanations/global/', GlobalExplanationView.as_view(), name='explanation-global'),
    path('explanations/<int:prediction_id>/', PredictionExplanationDetailView.as_view(), name='explanation-detail'),

    # Module B: Skill Intelligence & Co-occurrence
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('skills/impact/', SkillImpactView.as_view(), name='skill-impact'),
    path('skills/co-occurrence/', SkillCoOccurrenceView.as_view(), name='skill-cooccurrence'),
    path('skills/compare/', SkillCompareView.as_view(), name='skill-compare'),

    # Module C: Job Role Matching
    path('roles/', JobRoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/', JobRoleDetailView.as_view(), name='role-detail'),
    path('roles/match/', RoleMatchView.as_view(), name='role-match'),
    path('roles/recommendations/', RoleRecommendationsView.as_view(), name='role-recommendations'),

    # Module D: Career Growth Roadmaps
    path('roadmaps/', RoadmapListCreateView.as_view(), name='roadmap-list'),
    path('roadmaps/generate/', RoadmapListCreateView.as_view(), name='roadmap-generate'),
    path('roadmaps/<int:pk>/', RoadmapDetailView.as_view(), name='roadmap-detail'),
    path('roadmaps/<int:pk>/progress/', RoadmapProgressUpdateView.as_view(), name='roadmap-progress'),
]
