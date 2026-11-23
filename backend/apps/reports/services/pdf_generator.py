"""
Professional server-side PDF report generator for WorthIQ.
Uses ReportLab Platypus flowables with modern SaaS layout, custom branding,
tables, pagination, and statistical governance disclaimers.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

INDIGO_PRIMARY = colors.HexColor("#4f46e5")
INDIGO_DARK = colors.HexColor("#312e81")
SLATE_900 = colors.HexColor("#0f172a")
SLATE_700 = colors.HexColor("#334155")
SLATE_500 = colors.HexColor("#64748b")
SLATE_100 = colors.HexColor("#f1f5f9")
EMERALD_GREEN = colors.HexColor("#059669")
BORDER_COLOR = colors.HexColor("#e2e8f0")

DISCLAIMER_TEXT = (
    "Methodological Governance: WorthIQ reports are generated using historical Indian technology compensation "
    "datasets and machine learning estimators (Random Forest Regressor, TreeSHAP). Numerical projections represent "
    "empirical statistical expectations and market benchmarks. They do not constitute guaranteed compensation offers, "
    "binding agreements, or causal certainty."
)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic 'Page X of Y' numbering and running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(SLATE_500)
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "WorthIQ — Career & Compensation Intelligence")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Generated for personal career evaluation only.")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def generate_pdf_report(report) -> io.BytesIO:
    """
    Generates a complete PDF document for an AdvancedReport instance.
    Returns in-memory BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=SLATE_900
    )
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=SLATE_500
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=INDIGO_PRIMARY,
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=SLATE_700
    )
    bold_style = ParagraphStyle(
        'ReportBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=SLATE_500
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("Worth<b>IQ</b>", ParagraphStyle('Brand', fontName='Helvetica', fontSize=24, textColor=INDIGO_PRIMARY)))
    story.append(Paragraph(report.title, title_style))
    story.append(Spacer(1, 4))
    
    meta_info = f"Report Type: <b>{report.get_report_type_display()}</b> &nbsp;|&nbsp; Generated: <b>{report.created_at.strftime('%B %d, %Y')}</b> &nbsp;|&nbsp; User: <b>{report.user.email}</b>"
    story.append(Paragraph(meta_info, subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceBefore=4, spaceAfter=14))

    snapshot = report.data_snapshot or {}
    report_type = report.report_type

    # 2. Body based on report type
    if report_type == 'salary_prediction':
        story.append(Paragraph("Evaluation Profile & Inputs", heading_style))
        profile_data = [
            [Paragraph("Job Role", bold_style), Paragraph(str(snapshot.get("job_role", "—")), body_style),
             Paragraph("Experience", bold_style), Paragraph(f"{snapshot.get('years_of_experience', '—')} Years", body_style)],
            [Paragraph("Location", bold_style), Paragraph(str(snapshot.get("location", "—")), body_style),
             Paragraph("Education", bold_style), Paragraph(str(snapshot.get("education", "—")), body_style)],
        ]
        t_profile = Table(profile_data, colWidths=[100, 150, 100, 150])
        t_profile.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), SLATE_100),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_profile)
        story.append(Spacer(1, 10))

        story.append(Paragraph("Evaluated Technical Skills", heading_style))
        skills_str = ", ".join(snapshot.get("skills_evaluated", []) or snapshot.get("skills", [])) or "None specified"
        story.append(Paragraph(skills_str, body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("Market Salary Quantiles (Annual ₹ INR)", heading_style))
        salary_range = snapshot.get("salary_range", {})
        low = salary_range.get("low", 0)
        median = salary_range.get("median", 0)
        high = salary_range.get("high", 0)

        salary_table_data = [
            [Paragraph("Quantile Tier", bold_style), Paragraph("Annual Salary (INR)", bold_style), Paragraph("In Lakhs (LPA)", bold_style), Paragraph("Description", bold_style)],
            [Paragraph("Conservative (P10)", body_style), Paragraph(f"₹{int(low):,}", body_style), Paragraph(f"₹{round(low/100000, 2)}L", body_style), Paragraph("Baseline market threshold (90% earn above)", body_style)],
            [Paragraph("Median Market (P50)", bold_style), Paragraph(f"₹{int(median):,}", bold_style), Paragraph(f"₹{round(median/100000, 2)}L", bold_style), Paragraph("Central tendency benchmark expectation", body_style)],
            [Paragraph("Top Tier (P90)", body_style), Paragraph(f"₹{int(high):,}", body_style), Paragraph(f"₹{round(high/100000, 2)}L", body_style), Paragraph("Top-decile compensation ceiling", body_style)],
        ]
        t_sal = Table(salary_table_data, colWidths=[120, 110, 90, 180])
        t_sal.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), INDIGO_PRIMARY),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#e0e7ff")),
        ]))
        story.append(t_sal)

    elif report_type == 'scenario_comparison':
        story.append(Paragraph("Multi-Scenario Salary Simulation Comparison", heading_style))
        scenarios = snapshot.get("scenarios", [])
        if scenarios:
            comp_headers = [Paragraph("Scenario", bold_style), Paragraph("Role", bold_style), Paragraph("Exp", bold_style), Paragraph("Skills (Count)", bold_style), Paragraph("P50 Median", bold_style), Paragraph("Net Delta", bold_style)]
            comp_rows = [comp_headers]
            for sc in scenarios:
                pred = sc.get("prediction", {})
                sr = pred.get("salary_range", {})
                p50 = sr.get("p50_lpa", "—")
                delta_lpa = sc.get("comparison_to_baseline", {}).get("absolute_diff_lpa", 0.0)
                delta_str = f"+₹{delta_lpa}L" if delta_lpa > 0 else (f"-₹{abs(delta_lpa)}L" if delta_lpa < 0 else "Baseline")
                comp_rows.append([
                    Paragraph(sc.get("name", "Scenario"), bold_style if sc.get("is_baseline") else body_style),
                    Paragraph(sc.get("job_role", "—"), body_style),
                    Paragraph(f"{sc.get('years_of_experience', 0)}y", body_style),
                    Paragraph(f"{len(sc.get('skills', []))} skills", body_style),
                    Paragraph(f"₹{p50} LPA", bold_style),
                    Paragraph(delta_str, body_style),
                ])
            t_comp = Table(comp_rows, colWidths=[110, 100, 40, 80, 80, 90])
            t_comp.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), INDIGO_PRIMARY),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_comp)

    elif report_type == 'role_matching':
        story.append(Paragraph("Job Role Compatibility & Skill Gaps", heading_style))
        matches = snapshot.get("matches", [])[:5]
        if matches:
            role_headers = [Paragraph("Role", bold_style), Paragraph("Fit Score", bold_style), Paragraph("Category", bold_style), Paragraph("Missing Required Skills", bold_style)]
            role_rows = [role_headers]
            for rm in matches:
                role_rows.append([
                    Paragraph(rm.get("title", "—"), bold_style),
                    Paragraph(f"{rm.get('match_score', 0)}%", body_style),
                    Paragraph(rm.get("match_category", "—"), body_style),
                    Paragraph(", ".join(rm.get("missing_required_skills", [])[:3]) or "None (Full Match)", body_style),
                ])
            t_roles = Table(role_rows, colWidths=[120, 70, 100, 210])
            t_roles.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), INDIGO_PRIMARY),
                ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_roles)

    elif report_type == 'career_roadmap':
        story.append(Paragraph(f"Career Transition Roadmap — Target: {snapshot.get('target_role', 'Tech Track')}", heading_style))
        stages = snapshot.get("stages", [])
        for st in stages:
            story.append(Paragraph(f"Stage {st.get('stage_number', 1)}: {st.get('title', 'Milestone Stage')} ({st.get('estimated_weeks', 4)} Weeks)", bold_style))
            skills = ", ".join([m.get("skill_name", "") for m in st.get("milestones", [])])
            story.append(Paragraph(f"Skills to master: {skills}", body_style))
            if st.get("capstone_project"):
                story.append(Paragraph(f"Recommended Capstone: {st['capstone_project'].get('title', '')} — {st['capstone_project'].get('description', '')}", subtitle_style))
            story.append(Spacer(1, 6))

    else:
        # Generic summary block for any other report type
        story.append(Paragraph("Summary Data Snapshot", heading_style))
        story.append(Paragraph(str(report.summary or "Summary metrics captured from live evaluation."), body_style))
        story.append(Spacer(1, 8))

    # 3. Methodological Governance & Legal Disclaimer Block
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=8, spaceAfter=10))
    story.append(Paragraph(DISCLAIMER_TEXT, disclaimer_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer
