# WorthIQ Phase 5 Implementation Plan
## Execution Blueprint, Module Breakdown, Database Schema, and Acceptance Criteria

---

## 1. Architectural Strategy

Phase 5 introduces three cohesive Django applications to house the new domain capabilities, keeping business logic clean and isolated while reusing existing Phase 1–4 foundational services:

```
backend/apps/
├── scenarios/     # What-If Scenario persistence, comparison & predictive simulation
├── resumes/       # Resume document upload, text parsing (PDF/DOCX), skill extraction & review
└── reports/       # Advanced Multi-Type Career Reports, ReportLab PDF generation, CSV exports
```

---

## 2. Checkpoint Breakdown

### Checkpoint 1: Database Entities & Migrations
- **`SalaryScenario`**: User, name, role, experience, location, education, skills (JSON), prediction snapshot (JSON), timestamps.
- **`ResumeDocument`**: User, original filename, file reference, file size, MIME type, status, timestamps.
- **`ResumeExtraction`**: ResumeDocument, extracted skills (JSON), candidate metadata, warnings, timestamps.
- **`AdvancedReport`**: User, title, report_type, source_id, metadata (JSON), timestamps.
- Register apps in `backend/config/settings.py` (`apps.scenarios`, `apps.resumes`, `apps.reports`).
- Generate and apply Django migrations safely against `worthiq_db` on PostgreSQL.

### Checkpoint 2: What-If Salary Simulator Engine (`apps.scenarios`)
- **Backend Services & Serializers:**
  - `ScenarioSerializer`, `ScenarioCompareSerializer`.
  - Service linking directly to `backend.apps.predictions.services.salary_prediction.predict_salary_profile`.
  - Multi-scenario comparative delta calculation (P10/P50/P90 differences, percentage change, per-variable change detection).
- **Backend REST API Endpoints:**
  - `POST /api/scenarios/` (Create scenario).
  - `GET /api/scenarios/` (List user scenarios).
  - `GET /api/scenarios/{id}/` (Retrieve single scenario).
  - `PATCH /api/scenarios/{id}/` (Update scenario).
  - `DELETE /api/scenarios/{id}/` (Delete scenario).
  - `POST /api/scenarios/{id}/duplicate/` (Duplicate scenario).
  - `POST /api/scenarios/compare/` (Multi-scenario comparative evaluation up to 4 scenarios).
- **Frontend Implementation:**
  - `frontend/src/services/scenarioService.js`.
  - Overhaul [WhatIfSimulatorPage.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/pages/WhatIfSimulatorPage.jsx):
    - Baseline Profile Panel (auto-populated from active profile).
    - Multi-scenario editor (role, experience, city, education, dynamic skill tags).
    - Recharts multi-scenario bar chart comparing P10, P50, and P90 across up to 4 profiles.
    - Side-by-side delta cards with non-causality disclaimer.
    - Scenario save, rename, and load actions.

### Checkpoint 3: Resume Intelligence & Skill Extraction (`apps.resumes`)
- **Backend Document Parsing & Skill Extraction:**
  - `PDFParser`: Uses `pypdf` to extract raw text, detect empty or scanned documents.
  - `DOCXParser`: Uses `python-docx` to extract text from paragraphs and tables.
  - `ResumeSkillExtractor`: Uses Phase 3 canonical skill dictionary (35 skills, 81 aliases) with token boundary matching, extraction confidence, and snippet evidence.
  - Candidate metadata extractor (name, email, phone, detected years of experience, highest qualification).
- **Backend REST API Endpoints:**
  - `POST /api/resumes/upload/` (Upload document, validate MIME and 5MB size limit).
  - `GET /api/resumes/` (List uploaded resumes).
  - `GET /api/resumes/{id}/` (Get document status).
  - `POST /api/resumes/{id}/extract/` (Trigger extraction pipeline).
  - `GET /api/resumes/{id}/results/` (Get extracted skills and metadata).
  - `POST /api/resumes/{id}/apply-to-profile/` (Apply user-approved skills to profile).
  - `DELETE /api/resumes/{id}/` (Delete resume file and record).
- **Frontend Implementation:**
  - `frontend/src/services/resumeService.js`.
  - Create [ResumeAnalysisPage.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/pages/ResumeAnalysisPage.jsx):
    - Drag-and-drop upload zone with progress indicator.
    - Review screen showing Extracted Skills (with confidence and snippet), Existing Profile Skills, and Newly Detected Skills.
    - Add/remove/confirm interface before profile update.
    - Explicit confirmation dialog updating user profile with toast feedback.

### Checkpoint 4: Advanced Reports, PDF & CSV Export (`apps.reports`)
- **Backend Report Engine & PDF Compilation:**
  - Report types: `salary_prediction`, `shap_explanation`, `skill_intelligence`, `role_matching`, `career_roadmap`, `scenario_comparison`, `resume_analysis`.
  - PDF Generator using `reportlab`:
    - Clean WorthIQ branding, primary indigo palette, professional typography.
    - Dynamic data tables for salary bounds, skill breakdowns, and career milestones.
    - Numbered pages, generation timestamp, and statistical disclaimer.
  - CSV Generator: Formula-injection-safe tabular CSV downloads for historical predictions and scenario benchmarks.
- **Backend REST API Endpoints:**
  - `GET /api/reports/` (List user reports).
  - `GET /api/reports/{id}/` (Report detail).
  - `POST /api/reports/generate/` (Generate report snapshot).
  - `GET /api/reports/{id}/download/pdf/` (Stream authenticated PDF).
  - `GET /api/reports/export/csv/` (Download safe CSV).
  - `DELETE /api/reports/{id}/` (Delete report).
- **Frontend Implementation:**
  - `frontend/src/services/reportService.js`.
  - Upgrade [SavedReportsPage.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/pages/SavedReportsPage.jsx):
    - Multi-tab filter by report type.
    - Detail modal previewing complete snapshot data.
    - Direct "Download PDF" and "Export CSV" buttons.

### Checkpoint 5: Dashboard & Full Application Integration
- Update [DashboardPage.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/pages/DashboardPage.jsx) with What-If Scenario and Resume Analysis quick-actions.
- Update [DashboardLayout.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/components/layout/DashboardLayout.jsx) with navigation routes for Resume Analysis (`/resume-analysis`) and What-If Simulator (`/what-if-simulator`).
- Update [App.jsx](file:///c:/Users/Lenovo/Desktop/WorthIQ/frontend/src/App.jsx) with all new routes.

### Checkpoint 6: Verification & Complete Documentation Suite
- Run full automated test suite:
  - Phase 1–4 regression tests (45 Django tests + 13 ML pytest tests).
  - New Phase 5 unit and API tests (`apps.scenarios`, `apps.resumes`, `apps.reports`).
- Frontend production build verification (`npm run build`).
- End-to-end user journeys verification.
- Author all 11 required documentation files in repository.
- Stage, commit, and push to GitHub.
