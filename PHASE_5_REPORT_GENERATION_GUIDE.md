# WORTHIQ — ADVANCED REPORT GENERATION GUIDE

---

### 1. PDF Generation Architecture

WorthIQ utilizes **ReportLab Platypus** (Page Layout and Typography Using Scripts) to generate high-quality documents:
- **`NumberedCanvas`:** Custom two-pass canvas printing running page counts (`Page X of Y`), generation timestamps, and confidential footers.
- **Header & Branding:** Professional indigo header banner, WorthIQ logomark, report ID, and candidate details.
- **Section Modules:**
  1. Executive Summary box.
  2. Candidate Benchmark Profile table.
  3. Quantile Market Compensation table (P10 Conservative, P50 Median, P90 Top-Tier).
  4. Technical Stack Breakdown.
  5. Methodology & Non-Causality Legal Disclaimer.

---

### 2. Supported Report Types

1. `salary_prediction`: Official salary estimation snapshot.
2. `shap_explanation`: SHAP feature contribution breakdown in ₹ INR.
3. `job_role_matching`: Top matched roles and skill overlap scores.
4. `career_roadmap`: Structured stages, milestones, and capstone briefs.
5. `scenario_comparison`: Comparative matrix of What-If trajectories.
6. `resume_analysis`: Full transcript of extracted skills and candidate info.
7. `comprehensive_audit`: Full multi-page career portfolio audit.

---

### 3. CSV Export

Available via `/api/reports/export/csv/?type=predictions|scenarios`:
- Conforms to RFC 4180.
- UTF-8 BOM encoding for proper Microsoft Excel display.
- Sanitized against formula injection vulnerabilities.
