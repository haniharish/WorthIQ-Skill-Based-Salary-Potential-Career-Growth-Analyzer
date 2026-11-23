# WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer

> **Final-Year B.Tech Project** &middot; **Phase 1, Phase 2, Phase 3, Phase 4 & Phase 5: Complete Implementation**

WorthIQ is a full-stack, data-driven web application designed to help students, freshers, and working professionals understand their estimated market salary, analyze the valuation and ROI of their skill stack, discover matching roles, simulate counterfactual career moves, extract skills from resumes, and generate comprehensive career reports.

---

## 1. Project Overview & Development Phases

WorthIQ is engineered across strategic development phases:

1. **Phase 1: Foundation** *(Fully Implemented)*:
   - Full-stack project structure, React + Vite frontend, Tailwind CSS design system.
   - Django REST Framework backend with custom user authentication.
   - SimpleJWT authentication with refresh token blacklisting and token rotation.
   - Normalized PostgreSQL database containerized via Docker on port `5432`.
   - Complete User Profile & Skills management endpoints with full frontend integration.
   - DBeaver visual database administration setup.

2. **Phase 2: Salary Potential Prediction Engine** *(Fully Implemented)*:
   - **Part 1: Data Engineering & Feature Pipeline**:
     - Acquisition of 3 authentic Indian tech compensation datasets (25,332 records).
     - Cleaning, deduplication, monthly stipend annualization, and outlier filtering (₹1.2L to ₹80L).
     - Scikit-learn ColumnTransformer feature pipeline outputting 55 engineered features.
     - Automated test suite with 6 passing unit/integration tests in `ml/tests/`.
   - **Part 2: Model Training, Comparison, Django API & UI Integration**:
     - Benchmark of 3 regression models (Linear Regression, Random Forest, XGBoost).
     - Random Forest selected as winning engine (CV MAE: ₹3.35L, Test $R^2$: 0.36, MedAE: ₹2.15L).
     - Quantile regression models ($P10, P50, P90$) with empirical coverage calibration (10.2%, 48.1%, 89.3%).
     - Django ML service app `backend/apps/predictions` with REST endpoints and PostgreSQL history tracking.
     - Empirical 4-factor confidence scoring engine (High, Medium, Low).
     - React frontend integration in `SalaryAnalysisPage.jsx` and `SavedReportsPage.jsx` with Recharts distribution charts.

3. **Phase 3: AI Intelligence Engine** *(Fully Implemented)*:
   - **Module A: Explainable AI with SHAP**: TreeExplainer on Random Forest, baseline log value $13.368$ (₹6.39L), local waterfall decomposition into additive Rupee impacts, and Recharts waterfall visualizer in `PredictionExplanationPage.jsx`.
   - **Module B: Skill Intelligence & Co-occurrence**: Canonical skill taxonomy (35 skills, 81 aliases), empirical co-occurrence matrix mined from 25,332 records, marginal single-skill ablation valuation, and interactive What-If simulation sandbox in `SkillImpactPage.jsx`.
   - **Module C: AI Job Role Matching**: Curated technology roles, composite scoring (40% mandatory coverage, 15% preferred coverage, 25% TF-IDF cosine similarity, 20% experience tenure compatibility), match tiers, and gap analysis in `JobMatchingPage.jsx`.
   - **Module D: Personalized Career Growth Roadmaps**: Non-circular DAG prerequisite milestones, practical software capstone project briefs, PostgreSQL relational persistence, and interactive completion tracking in `CareerRoadmapPage.jsx`.

4. **Phase 4: Complete Frontend Dashboard, UI/UX Integration & Design System** *(Fully Implemented)*:
   - **Centralized Dashboard Overhaul**: Live data aggregations from `dashboardService.js`, Welcome Banner with profile completeness %, real KPI StatCards (P50 Salary, P10–P90 Range, Role Matches, Roadmap Progress), Salary Valuation Distribution Chart (Recharts), Evaluation History Timeline, Compatible Roles Shortlist with gap badges, and Active Career Roadmap Progress.
   - **Production Design System**: Comprehensive UI component primitives in `frontend/src/components/ui/` (`StatCard`, `EmptyState`, `ErrorState`, `LoadingSkeleton`, `Modal`, `ConfidenceIndicator`, `Breadcrumbs`, `Tabs`, `SelectInput`, `SkillTagInput`) and accessible global `ToastContext` (`useToast`).
   - **Application Layout & Navigation**: Categorized sidebar navigation in `DashboardLayout.jsx` (Main, Intelligence Engine, Account & Settings), topbar with dynamic route breadcrumbs, quick action CTA, user profile summary pill with logout dropdown, and mobile navigation drawer with backdrop overlay.
   - **Accessibility & Responsive Polish**: WCAG 2.1 AA compliant color contrast, ARIA landmarks, mobile collapse, and clean SaaS aesthetics.

5. **Phase 5: Advanced Features, What-If Simulator, Resume Intelligence & Advanced Reports** *(Fully Implemented)*:
   - **What-If Salary Simulator (`apps.scenarios`)**: Multi-variable scenario creation, saving, updating, duplication, and comparative matrix evaluation. Compares baseline profile against up to 3 scenarios with P10/P50/P90 quantile bounds, pairwise deltas, and non-causality disclaimers in `WhatIfSimulatorPage.jsx`.
   - **Resume Intelligence & Skill Extractor (`apps.resumes`)**: Parsing pipeline for PDF (`pypdf`) and DOCX (`python-docx`), extracting candidate metadata and technical skills with token boundary regex, taxonomy alias resolution, context snippets, and confidence scores. Strict privacy guarantee with zero automatic profile overwrites without explicit user confirmation in `ResumeAnalysisPage.jsx`.
   - **Advanced Career Reports & Export (`apps.reports`)**: Publication-grade PDF document generation via ReportLab Platypus across 7 evaluation types with two-pass running page counters and non-causality notices. Sanitized streaming CSV export for predictions and scenarios in `SavedReportsPage.jsx`.

6. **Extended Phase 5: Pre-Deployment QA, Complete Testing, Security Audit & Release Readiness** *(Fully Implemented)*:
   - **Backend Test Suite & Code Coverage**: 57 tests executed under `coverage.py` achieving **86% coverage** across all applications (exceeding >80% threshold).
   - **ML Pipeline & Quantile Calibration**: Verified on held-out test set ($N = 5,067$). Point model MAE = ₹3.51 LPA, MedAE = ₹2.15 LPA, $R^2$ = 0.3597. Empirical quantile coverage: P10 = 10.20%, P50 = 48.10%, P90 = 89.30%, with strictly monotonic confidence bounds ($P10 \le P50 \le P90$) and 0 crossing violations.
   - **API Latency & Performance Benchmarks**: 115 live HTTP requests across 11 key endpoints achieving **0.0% error rate**. Point prediction P50 = 2,259 ms, Role matching P50 = 2,329 ms, What-If compare P50 = 2,443 ms.
   - **Security Audit (OWASP Top 10)**: 8/8 automated security checks passed: JWT signature tampering rejected (401), missing auth rejected (401), multi-tenant BOLA/IDOR isolation strictly enforced (404), SQL injection resilience verified, stored XSS neutralized, CSV formula injection neutralized (`sanitize_csv_cell`), executable files rejected (400).
   - **Disaster Recovery Rehearsal**: Successful `pg_dump` and test restore drill into `worthiq_test_restore` with 100% row-for-row parity across all database tables.

7. **Phase 6**: Enterprise Architecture & Production Cloud Deployment *(Upcoming)*.

---

## 2. Technology Stack

### Frontend
- **Framework**: React 18
- **Build Tool / Bundler**: Vite 6.4 (Configured strictly on port **5180**)
- **Language**: JavaScript (ES Modules)
- **Styling**: Tailwind CSS (SaaS theme, dark slate aesthetic)
- **Data Visualization**: Recharts 2.x
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios with automatic JWT interceptors & token rotation
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.14 & Django 5.2
- **API Engine**: Django REST Framework (DRF) 3.18
- **Authentication**: DRF SimpleJWT with token blacklist support
- **CORS Handling**: `django-cors-headers` (configured for `http://localhost:5180`)
- **Database Driver**: `psycopg` 3.3 (PostgreSQL adapter)
- **Machine Learning**: Scikit-Learn, LightGBM, XGBoost, SHAP, Joblib

### Database
- **Database**: PostgreSQL 16 Alpine
- **Containerization**: Docker & Docker Compose (Port **5432**)
- **Storage**: Named Docker volume `worthiq_pgdata` for persistent data storage
- **GUI Management**: DBeaver Community Edition

---

## 3. Fixed Port Configuration

| Service | Technology | Port | Access URL | Strict Port |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | React + Vite | `5180` | `http://localhost:5180` | `strictPort: true` |
| **Backend** | Django + DRF | `8000` | `http://localhost:8000` | Host: `0.0.0.0:8000` |
| **Database** | PostgreSQL Docker | `5432` | `localhost:5432` | Mapped from container |

---

## 4. Project Directory Structure

```text
WorthIQ/
│
├── frontend/                     # React + Vite application
│   ├── public/                   # Static assets & favicon
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/           # ProtectedRoute, PublicRoute, BrandLogo
│   │   │   ├── layout/           # DashboardLayout, Navbar, Topbar
│   │   │   └── ui/               # StatCard, EmptyState, ErrorState, LoadingSkeleton, Modal,
│   │   │                         # ConfidenceIndicator, Breadcrumbs, Tabs, SelectInput, SkillTagInput
│   │   ├── context/              # AuthContext, ToastContext
│   │   ├── hooks/                # useAuth, useToast
│   │   ├── pages/                # DashboardPage, SalaryAnalysisPage, PredictionExplanationPage,
│   │   │                         # SkillImpactPage, WhatIfSimulatorPage, JobMatchingPage,
│   │   │                         # CareerRoadmapPage, SavedReportsPage, SettingsPage, LandingPage
│   │   ├── services/             # api.js, authService, profileService, predictionService,
│   │   │                         # intelligenceService, dashboardService
│   │   ├── utils/                # formatting, math helpers
│   │   ├── App.jsx               # Routes & Providers
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Tailwind CSS & design tokens
│   ├── vite.config.js            # Port 5180 strict configuration
│   └── package.json
│
├── backend/                      # Django REST Framework application
│   ├── config/                   # Project settings, root URLs, WSGI, ASGI
│   ├── apps/
│   │   ├── accounts/             # Custom User model, JWT views, serializers
│   │   ├── profiles/             # User Profile & normalized Skills
│   │   ├── predictions/          # Salary prediction engine, quantiles & history
│   │   └── intelligence/         # SHAP, Skill Intelligence, Role Matching, Roadmaps
│   ├── manage.py
│   └── requirements.txt
│
├── ml/                           # Machine Learning Pipeline & Artifacts
│   ├── data/                     # Raw, interim, and processed compensation data
│   ├── models/                   # Serialized models (.joblib), metadata, preprocessors
│   ├── src/                      # Acquisition, cleaning, features, training scripts
│   ├── reports/                  # EDA figures and statistical tables
│   └── tests/                    # 13 pytest tests for data, models, quantiles, SHAP
│
├── database/                     # Docker PostgreSQL orchestration
│   ├── docker-compose.yml        # PostgreSQL 16 container definition & healthcheck
│   └── .env                      # Database credentials
│
├── docs/                         # Comprehensive project documentation
│   ├── API_DOCUMENTATION.md      # Phase 1 REST endpoint documentation
│   ├── DBEAVER_SETUP.md          # Visual DB configuration guide
│   ├── DATASET_SOURCES.md        # Authentic dataset provenance
│   ├── DATA_CLEANING_REPORT.md   # Data sanitization methodology
│   ├── EDA_REPORT.md             # Exploratory Data Analysis findings
│   ├── FEATURE_ENGINEERING.md    # 55-feature pipeline documentation
│   ├── ML_MODEL_REPORT.md        # Regression model comparison & benchmark
│   ├── SHAP_EXPLAINABILITY_GUIDE.md # TreeSHAP mathematical formulation & waterfall
│   ├── SKILL_INTELLIGENCE_METHODOLOGY.md # Skill taxonomy & ablation valuation
│   ├── ROLE_MATCHING_METHODOLOGY.md # Composite scoring & gap analysis
│   ├── CAREER_ROADMAP_METHODOLOGY.md # Directed acyclic graphs & learning paths
│   ├── PHASE_3_TEST_REPORT.md    # Phase 3 test verification report
│   ├── PHASE_4_TEST_REPORT.md    # Phase 4 test execution & regression report
│   ├── PHASE_4_API_INTEGRATION_REPORT.md # Frontend-backend service contracts
│   ├── PHASE_4_UI_UX_GUIDE.md    # Design system, components & accessibility
│   └── PHASE_4_SETUP_GUIDE.md    # Developer environment & orchestration guide
│
├── PHASE_4_AUDIT_REPORT.md       # Phase 4 gap analysis & initial audit
├── PHASE_4_IMPLEMENTATION_PLAN.md # Phase 4 6-checkpoint execution plan
├── PHASE_4_IMPLEMENTATION_REPORT.md # Comprehensive Phase 4 deliverables report
├── test_complete_integration.py  # 12-step end-to-end integration test runner
└── README.md
```

---

## 5. Prerequisites & Local Setup

### Step 1: Start PostgreSQL via Docker
```powershell
docker start worthiq_postgres
```
*Port: `5432` | DB: `worthiq_db` | User: `postgres`*

### Step 2: Start Django REST Framework Backend
```powershell
# Activate Python Virtual Environment
.\backend\venv\Scripts\Activate.ps1

# Run Migrations
python backend\manage.py migrate

# Start Server
python backend\manage.py runserver --noreload 0.0.0.0:8000
```
*Backend is accessible at: `http://127.0.0.1:8000/`*

### Step 3: Start React Frontend
```powershell
cd frontend
npm install
npm run dev
```
*Frontend is accessible at: `http://localhost:5180/`*

---

## 6. Running Automated Verification Suites

### Frontend Production Build
```powershell
npm --prefix frontend run build
```
*Result: 2,086 modules transformed, 0 errors, production bundle generated in `frontend/dist/`.*

### Full Backend Django Test Suite & Code Coverage (57 Tests)
```powershell
backend\venv\Scripts\python.exe -m coverage run --source=backend/apps backend/manage.py test apps.accounts apps.profiles apps.predictions apps.intelligence.tests apps.scenarios apps.resumes apps.reports
backend\venv\Scripts\python.exe -m coverage report -m
```
*Result: 57 passed in 56.81s (100% pass rate). Overall backend code coverage: **86%**.*

### Machine Learning Test Suite (13 Tests)
```powershell
backend\venv\Scripts\python.exe -m pytest ml/tests/ -v
```
*Result: 13 passed in 12.45s, 0 failures.*

### Machine Learning Empirical Validation (Held-Out Test Set $N = 5,067$)
```powershell
backend\venv\Scripts\python.exe testing/scripts/validate_ml_model.py
```
*Result: MAE = ₹3.51 LPA, MedAE = ₹2.15 LPA, $R^2$ = 0.3597. P10 = 10.20%, P50 = 48.10%, P90 = 89.30%, Monotonic violations = 0.*

### Live API Performance & Latency Benchmark
```powershell
backend\venv\Scripts\python.exe testing/scripts/benchmark_api.py
```
*Result: 115 live HTTP requests across 11 key endpoints with **0.0% error rate**.*

### Automated Security & OWASP Top 10 Audit
```powershell
backend\venv\Scripts\python.exe testing/scripts/security_audit.py
```
*Result: 8 / 8 checks passed (JWT signature tampering, unauthenticated route rejection, BOLA/IDOR isolation, SQL injection, XSS, CSV formula injection, file upload controls).*

---

## 7. Key Application URLs

- **Landing Page**: `http://localhost:5180/`
- **Dashboard**: `http://localhost:5180/dashboard`
- **Salary Valuation**: `http://localhost:5180/salary-analysis`
- **What-If Simulator**: `http://localhost:5180/what-if`
- **Skill Intelligence**: `http://localhost:5180/skill-intelligence`
- **Role Matching**: `http://localhost:5180/role-matching`
- **Career Roadmaps**: `http://localhost:5180/roadmaps`
- **Saved Reports**: `http://localhost:5180/reports`
- **Settings**: `http://localhost:5180/settings`
- **Backend API Root**: `http://127.0.0.1:8000/api/`

---

## 8. Phase 4 Implementation Checklist

- [x] Comprehensive Phase 4 UI/UX and API audit (`PHASE_4_AUDIT_REPORT.md`).
- [x] 6-checkpoint execution plan (`PHASE_4_IMPLEMENTATION_PLAN.md`).
- [x] Design system UI primitives (`StatCard`, `EmptyState`, `ErrorState`, `LoadingSkeleton`, `Modal`, `ConfidenceIndicator`, `Breadcrumbs`, `Tabs`, `SelectInput`, `SkillTagInput`).
- [x] Global accessible Toast provider (`ToastContext.jsx`).
- [x] Categorized sidebar layout with topbar breadcrumbs and profile dropdown (`DashboardLayout.jsx`).
- [x] Live aggregated dashboard replacing mock data (`dashboardService.js`, `DashboardPage.jsx`).
- [x] What-If Counterfactual simulation lab connected to live comparison API (`WhatIfSimulatorPage.jsx`).
- [x] Seamless SHAP explainability transitions from predictions and saved reports (`/explanations/:id`).
- [x] Filterable and searchable saved reports catalog with modal detail breakdown (`SavedReportsPage.jsx`).
- [x] High-converting SaaS landing page with feature cards, trust metrics, and workflow (`LandingPage.jsx`).
- [x] User settings page with profile management, security indicators, and system status (`SettingsPage.jsx`).
- [x] Responsive layout optimization across mobile (<640px), tablet, and desktop viewports.
- [x] 45 backend Django unit/integration tests passing (100%).
- [x] 13 ML pipeline pytest tests passing (100%).
- [x] Production Vite build passing cleanly with zero errors.
- [x] Complete documentation suite (`PHASE_4_TEST_REPORT.md`, `PHASE_4_API_INTEGRATION_REPORT.md`, `PHASE_4_UI_UX_GUIDE.md`, `PHASE_4_SETUP_GUIDE.md`).
