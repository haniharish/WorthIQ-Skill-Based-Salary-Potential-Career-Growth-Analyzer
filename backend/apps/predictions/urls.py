"""
URL routing for predictions endpoints.
"""

from django.urls import path
from .views import (
    SalaryPredictionView,
    PredictionHistoryListView,
    PredictionHistoryDetailView,
    ModelInfoView
)

urlpatterns = [
    path('salary/', SalaryPredictionView.as_view(), name='predict-salary'),
    path('history/', PredictionHistoryListView.as_view(), name='prediction-history'),
    path('history/<int:pk>/', PredictionHistoryDetailView.as_view(), name='prediction-detail'),
    path('model-info/', ModelInfoView.as_view(), name='model-info'),
]
