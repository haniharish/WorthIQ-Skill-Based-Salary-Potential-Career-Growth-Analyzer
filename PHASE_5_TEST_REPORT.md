# WORTHIQ — PHASE 5 TEST REPORT
## Automated Verification, Regression Testing & Build Validation

**Test Run Date:** November 23, 2026  
**Environment:** Python 3.14.7, Django 5.2.11, PostgreSQL 16 (Docker `worthiq_postgres`), Node.js / Vite 6.4.6  
**Status:** ALL TESTS PASSING (65 / 65 Tests)  

---

### 1. Test Summary Overview

| Test Module | Test Harness | Total Tests | Passed | Failed | Errors | Execution Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **apps.scenarios** | Django TestCase | 3 | 3 | 0 | 0 | 1.8s |
| **apps.resumes** | Django TestCase | 2 | 2 | 0 | 0 | 1.1s |
| **apps.reports** | Django TestCase | 2 | 2 | 0 | 0 | 0.8s |
| **apps.accounts** | Django TestCase | 8 | 8 | 0 | 0 | 4.2s |
| **apps.profiles** | Django TestCase | 7 | 7 | 0 | 0 | 3.9s |
| **apps.predictions** | Django TestCase | 11 | 11 | 0 | 0 | 10.1s |
| **apps.intelligence** | Django TestCase | 19 | 19 | 0 | 0 | 47.1s |
| **ml.tests** (Pipelines) | Pytest 9.2.0 | 13 | 13 | 0 | 0 | 16.4s |
| **Total Automated** | | **65** | **65** | **0** | **0** | **85.3s** |

---

### 2. Frontend Build Verification

```
> worthiq-frontend@1.0.0 build
> vite build

vite v6.4.6 building for production...
transforming...
✓ 2086 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.12 kB │ gzip:   0.63 kB
dist/assets/index-DQkFQ_pS.css   68.78 kB │ gzip:  11.12 kB
dist/assets/index-BQ4n32Y9.js   951.25 kB │ gzip: 267.06 kB
✓ built in 11.45s
```
- Zero JSX / TypeScript / React syntax errors.
- Clean bundle generation in `frontend/dist/`.

---

### 3. Verification of User Journeys

1. **Journey 1: What-If Salary Simulation:**
   - Baseline profile loaded automatically from `useAuth()`.
   - Adjusted role from Full Stack Developer to Senior Cloud Architect, increased experience to 5 years, added Docker and AWS.
   - Clicked "Run Simulation": `/api/scenarios/compare/` executed with P10/P50/P90 quantile bounds.
   - Clicked "Save Scenario": Scenario persisted in PostgreSQL `worthiq_salary_scenarios` table.
   - Recharts comparative bar chart rendered baseline vs scenario with delta callouts.
   - Non-causality disclaimer displayed.

2. **Journey 2: Resume Intelligence & Skill Extraction:**
   - Uploaded PDF document: `/api/resumes/upload/` parsed text via `pypdf`.
   - Discovered candidate metadata (name, email, detected experience).
   - Extracted 9 skills mapped against canonical taxonomy with context snippets and match confidence.
   - Grouped into New Skills vs Already in Profile.
   - Checked 3 new skills and opened confirmation modal.
   - Clicked "Confirm & Update Profile": `/api/resumes/{id}/apply-to-profile/` synced skills to user's profile with zero auto-sync without confirmation.

3. **Journey 3: PDF Career Report Download:**
   - Triggered `/api/reports/{id}/download/`.
   - ReportLab Platypus generated formatted PDF document with branded header, candidate info table, P10/P50/P90 metrics table, and methodology disclaimer.
   - Blob downloaded directly in browser as `WorthIQ_Report_{id}.pdf`.

4. **Journey 4: CSV Export:**
   - Triggered `/api/reports/export/csv/?type=scenarios` and `?type=predictions`.
   - Streamed RFC 4180 CSV with UTF-8 encoding and sanitized formula injection prefixes (`=`, `+`, `-`, `@`).
