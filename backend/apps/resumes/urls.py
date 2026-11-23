"""
URL routing for Resume Intelligence & Skill Extraction.
"""

from django.urls import path
from .views import (
    ResumeUploadView,
    ResumeListView,
    ResumeDetailView,
    ResumeResultsView,
    ResumeApplyToProfileView,
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('', ResumeListView.as_view(), name='resume-list'),
    path('<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('<int:pk>/results/', ResumeResultsView.as_view(), name='resume-results'),
    path('<int:pk>/apply-to-profile/', ResumeApplyToProfileView.as_view(), name='resume-apply-to-profile'),
]
