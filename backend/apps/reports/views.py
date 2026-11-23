"""
Views for Advanced Career Intelligence Reports, PDF generation, and CSV export.
"""

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import AdvancedReport
from .serializers import AdvancedReportSerializer, GenerateReportInputSerializer
from .services.pdf_generator import generate_pdf_report
from .services.csv_generator import export_predictions_to_csv_response, export_scenarios_to_csv_response
from apps.predictions.models import Prediction
from apps.scenarios.models import SalaryScenario

class ReportListCreateView(APIView):
    """
    GET /api/reports/ - Lists reports belonging to the authenticated user.
    Supports filtering by ?report_type=... and ?search=...
    POST /api/reports/generate/ - Creates a new frozen report snapshot.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = AdvancedReport.objects.filter(user=request.user)
        report_type = request.query_params.get('report_type')
        if report_type:
            qs = qs.filter(report_type=report_type)

        search = request.query_params.get('search')
        if search:
            qs = qs.filter(title__icontains=search)

        serializer = AdvancedReportSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GenerateReportInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        snapshot = data.get("data_snapshot", {})
        source_id = data.get("source_id")

        # Auto-populate snapshot if source_id is given and snapshot is empty
        if not snapshot and source_id:
            if data["report_type"] == 'salary_prediction':
                pred = Prediction.objects.filter(user=request.user, id=source_id).first()
                if pred:
                    snapshot = {
                        "job_role": pred.job_role,
                        "location": pred.location,
                        "years_of_experience": float(pred.years_of_experience),
                        "education": pred.education,
                        "skills_evaluated": pred.skills,
                        "salary_range": {
                            "low": float(pred.predicted_low_salary),
                            "median": float(pred.predicted_median_salary),
                            "high": float(pred.predicted_high_salary),
                        },
                        "salary_lpa": round(float(pred.predicted_median_salary) / 100_000.0, 2),
                        "confidence": pred.confidence,
                        "model_version": pred.model_version
                    }
            elif data["report_type"] == 'scenario_comparison':
                sc = SalaryScenario.objects.filter(user=request.user, id=source_id).first()
                if sc and sc.prediction_snapshot:
                    snapshot = {"scenarios": [sc.prediction_snapshot]}

        report = AdvancedReport.objects.create(
            user=request.user,
            title=data["title"],
            report_type=data["report_type"],
            source_id=source_id,
            summary=data.get("summary", ""),
            data_snapshot=snapshot
        )

        return Response(AdvancedReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ReportDetailView(APIView):
    """
    GET /api/reports/{id}/ - Retrieve a single report snapshot.
    DELETE /api/reports/{id}/ - Delete a report.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(AdvancedReport, pk=pk, user=user)

    def get(self, request, pk):
        report = self.get_object(pk, request.user)
        return Response(AdvancedReportSerializer(report).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        report = self.get_object(pk, request.user)
        report.delete()
        return Response({"message": "Report deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ReportDownloadPDFView(APIView):
    """
    GET /api/reports/{id}/download/
    Generates and streams a professional ReportLab PDF for the authenticated report owner.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        report = get_object_or_404(AdvancedReport, pk=pk, user=request.user)
        pdf_buffer = generate_pdf_report(report)

        sanitized_title = "".join(c for c in report.title if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        filename = f"WorthIQ_{report.report_type}_{sanitized_title}.pdf"

        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ReportExportCSVView(APIView):
    """
    GET /api/reports/export/csv/?source=predictions|scenarios
    Exports tabular user data to a formula-injection-safe CSV file.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        source = request.query_params.get('source', 'predictions')

        if source == 'scenarios':
            scenarios = SalaryScenario.objects.filter(user=request.user)
            return export_scenarios_to_csv_response(scenarios, filename="worthiq_salary_scenarios.csv")
        else:
            predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
            return export_predictions_to_csv_response(predictions, filename="worthiq_salary_evaluations.csv")
