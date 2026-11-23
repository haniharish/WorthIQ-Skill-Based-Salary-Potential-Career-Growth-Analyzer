"""
Secure CSV export services with formula-injection sanitization.
"""

import csv
import io
from typing import List, Any
from django.http import HttpResponse

DANGEROUS_PREFIXES = ('=', '+', '-', '@', '\t', '\r')

def sanitize_csv_cell(value: Any) -> str:
    """
    Sanitizes string cells to prevent CSV / Formula Injection attacks
    when opened in Excel, Google Sheets, or LibreOffice.
    """
    if value is None:
        return ""
    val_str = str(value).strip()
    if val_str.startswith(DANGEROUS_PREFIXES):
        return f"'{val_str}"
    return val_str


def export_predictions_to_csv_response(predictions: List[Any], filename: str = "worthiq_salary_evaluations.csv") -> HttpResponse:
    """
    Serializes a queryset or list of predictions into a secure CSV HttpResponse.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)

    # Header
    writer.writerow([
        "Evaluation ID",
        "Created At",
        "Job Role",
        "Years of Experience",
        "Location",
        "Education",
        "Skills Count",
        "Skills Evaluated",
        "Conservative P10 (INR)",
        "Median P50 (INR)",
        "Top-Tier P90 (INR)",
        "Median (LPA)",
        "Confidence Tier",
        "Model Version"
    ])

    for p in predictions:
        p_id = getattr(p, 'id', '')
        created = getattr(p, 'created_at', '')
        if hasattr(created, 'strftime'):
            created = created.strftime('%Y-%m-%d %H:%M:%S')

        skills_list = getattr(p, 'skills', [])
        skills_str = "; ".join(skills_list) if isinstance(skills_list, list) else str(skills_list)

        low = float(getattr(p, 'predicted_low_salary', 0) or 0)
        median = float(getattr(p, 'predicted_median_salary', 0) or 0)
        high = float(getattr(p, 'predicted_high_salary', 0) or 0)
        median_lpa = round(median / 100_000.0, 2) if median > 0 else 0.0

        writer.writerow([
            sanitize_csv_cell(p_id),
            sanitize_csv_cell(created),
            sanitize_csv_cell(getattr(p, 'job_role', '')),
            sanitize_csv_cell(getattr(p, 'years_of_experience', '')),
            sanitize_csv_cell(getattr(p, 'location', '')),
            sanitize_csv_cell(getattr(p, 'education', '')),
            sanitize_csv_cell(len(skills_list) if isinstance(skills_list, list) else 0),
            sanitize_csv_cell(skills_str),
            sanitize_csv_cell(low),
            sanitize_csv_cell(median),
            sanitize_csv_cell(high),
            sanitize_csv_cell(median_lpa),
            sanitize_csv_cell(getattr(p, 'confidence', '')),
            sanitize_csv_cell(getattr(p, 'model_version', '2.0.0'))
        ])

    response = HttpResponse(buffer.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_scenarios_to_csv_response(scenarios: List[Any], filename: str = "worthiq_scenarios.csv") -> HttpResponse:
    """
    Serializes a queryset or list of SalaryScenario records into a secure CSV HttpResponse.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)

    writer.writerow([
        "Scenario ID",
        "Scenario Name",
        "Created At",
        "Updated At",
        "Job Role",
        "Years of Experience",
        "Location",
        "Education",
        "Skills Count",
        "Skills",
        "P10 Floor (LPA)",
        "P50 Median (LPA)",
        "P90 Ceiling (LPA)",
        "Confidence Tier"
    ])

    for sc in scenarios:
        snapshot = getattr(sc, 'prediction_snapshot', {}) or {}
        sr = snapshot.get('salary_range', {})

        writer.writerow([
            sanitize_csv_cell(sc.id),
            sanitize_csv_cell(sc.name),
            sanitize_csv_cell(sc.created_at.strftime('%Y-%m-%d %H:%M:%S')),
            sanitize_csv_cell(sc.updated_at.strftime('%Y-%m-%d %H:%M:%S')),
            sanitize_csv_cell(sc.job_role),
            sanitize_csv_cell(sc.years_of_experience),
            sanitize_csv_cell(sc.location),
            sanitize_csv_cell(sc.education),
            sanitize_csv_cell(len(sc.skills)),
            sanitize_csv_cell("; ".join(sc.skills)),
            sanitize_csv_cell(sr.get('p10_lpa', '—')),
            sanitize_csv_cell(sr.get('p50_lpa', '—')),
            sanitize_csv_cell(sr.get('p90_lpa', '—')),
            sanitize_csv_cell(snapshot.get('confidence', '—'))
        ])

    response = HttpResponse(buffer.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
