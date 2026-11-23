"""
URL routing for Advanced Career Reports & Export.
"""

from django.urls import path
from .views import (
    ReportListCreateView,
    ReportDetailView,
    ReportDownloadPDFView,
    ReportExportCSVView,
)

urlpatterns = [
    path('', ReportListCreateView.as_view(), name='report-list'),
    path('generate/', ReportListCreateView.as_view(), name='report-generate'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('<int:pk>/download/', ReportDownloadPDFView.as_view(), name='report-download-pdf'),
    path('export/csv/', ReportExportCSVView.as_view(), name='report-export-csv'),
]
