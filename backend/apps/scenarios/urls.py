"""
URL routing for Salary Scenarios & What-If Simulation.
"""

from django.urls import path
from .views import (
    ScenarioListCreateView,
    ScenarioDetailView,
    ScenarioDuplicateView,
    ScenarioPredictView,
    ScenarioCompareView,
)

urlpatterns = [
    path('', ScenarioListCreateView.as_view(), name='scenario-list-create'),
    path('<int:pk>/', ScenarioDetailView.as_view(), name='scenario-detail'),
    path('<int:pk>/duplicate/', ScenarioDuplicateView.as_view(), name='scenario-duplicate'),
    path('<int:pk>/predict/', ScenarioPredictView.as_view(), name='scenario-predict'),
    path('compare/', ScenarioCompareView.as_view(), name='scenario-compare'),
]
