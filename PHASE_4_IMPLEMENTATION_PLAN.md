# WorthIQ — Phase 4 Implementation Plan
## Complete Frontend Dashboard, UI/UX Integration, Responsive Design & Application-Wide Polish

---

## 1. Plan Overview & Objectives

Phase 4 transforms WorthIQ into a production-grade, connected, accessible, responsive SaaS platform. The plan establishes a unified design system, overhauls the dashboard with live API data, polishes all existing application pages, and validates end-to-end user journeys without breaking Phase 1–3 functionality.

---

## 2. Sequence of Tasks & Dependencies

```
[Task 1: Design System Primitives]
        │
        ├── StatCard, MetricCard, ConfidenceIndicator, LoadingSkeleton
        ├── EmptyState, ErrorState, Modal, Toast Notification System
        └── SelectInput, SkillTagInput, Breadcrumbs, Tabs
        │
        ▼
[Task 2: Layout & Navigation Overhaul]
        │
        ├── Desktop Categorized Sidebar (Main, Intelligence, Account)
        ├── Topbar with Breadcrumbs, Search, User Avatar & Menu
        └── Mobile Drawer Navigation with backdrop and accessible controls
        │
        ▼
[Task 3: Dashboard Central Overhaul (/dashboard)]
        │
        ├── Profile completion progress & personalized welcome header
        ├── Live Salary Prediction KPIs (P10, P50, P90, Confidence)
        ├── Salary range visualization & historical trend chart
        ├── Skill Intelligence & Gap Overview (Phase 3 APIs)
        ├── Matched Job Roles shortlist & Career Roadmap progress
        └── Recent evaluations table & Quick Action buttons
        │
        ▼
[Task 4: Polish & Connect Application Pages]
        │
        ├── Landing Page (SaaS hero, 5 features, How it Works, trust/methodology)
        ├── Login & Register Pages (password toggle, validation, error handling)
        ├── Profile & Profile Setup (canonical skill selector, autofill)
        ├── Salary Analysis (annual/monthly toggle, direct SHAP link, range chart)
        ├── Saved Reports (search, filter, sort, pagination, detail modal with SHAP)
        ├── Prediction Explanation (TreeSHAP waterfall, metric cards, narrative)
        ├── Skill Intelligence (portfolio valuation, co-occurrence, What-If sandbox)
        ├── Job Role Matching (9 roles, composite scoring, gap analysis, roadmap CTA)
        ├── Career Roadmap (DAG milestones, project briefs, interactive checkboxes)
        ├── What-If Simulator (connect to POST /api/intelligence/skills/compare/)
        └── Settings (account information, session metadata, SaaS layout)
        │
        ▼
[Task 5: End-to-End Verification & Regression Testing]
        │
        ├── Verify 6 user journeys against live backend
        ├── Execute Django backend test suite (45 tests)
        ├── Execute ML pytest test suite (13 tests)
        └── Execute Vite production build (npm run build)
        │
        ▼
[Task 6: Documentation Suite & Git Commit]
        │
        └── Audit, Implementation, Test, API, UI/UX, Setup reports + Git push
```

---

## 3. Files to Be Created or Modified

### 3.1 Files to Create:
- `frontend/src/context/ToastContext.jsx` (Global notification context)
- `frontend/src/components/ui/StatCard.jsx` (Reusable KPI metric display)
- `frontend/src/components/ui/EmptyState.jsx` (Informative empty state with CTA)
- `frontend/src/components/ui/ErrorState.jsx` (Graceful error boundary and retry card)
- `frontend/src/components/ui/LoadingSkeleton.jsx` (Shimmer skeletons for cards, tables, charts)
- `frontend/src/components/ui/Modal.jsx` (Accessible dialog with focus trap & Esc key)
- `frontend/src/components/ui/ConfidenceIndicator.jsx` (Calibrated badge and meter)
- `frontend/src/components/ui/Breadcrumbs.jsx` (Hierarchical route breadcrumbs)
- `frontend/src/components/ui/Tabs.jsx` (Underline and pill styled tab controls)
- `frontend/src/components/ui/SelectInput.jsx` (Styled custom select input)
- `frontend/src/components/ui/SkillTagInput.jsx` (Tag manager with canonical skill search)
- `frontend/src/services/dashboardService.js` (Centralized dashboard data aggregator)

### 3.2 Files to Modify / Polish:
- `frontend/src/App.jsx` (Add route aliases, ToastProvider integration)
- `frontend/src/components/layout/DashboardLayout.jsx` (Sidebar categories, mobile drawer, breadcrumbs)
- `frontend/src/pages/DashboardPage.jsx` (Full overhaul with real backend API integration)
- `frontend/src/pages/LandingPage.jsx` (Complete SaaS marketing copy, feature breakdown, preview)
- `frontend/src/pages/LoginPage.jsx` (Password visibility toggle, error handling)
- `frontend/src/pages/RegisterPage.jsx` (Password visibility toggle, validation)
- `frontend/src/pages/ProfilePage.jsx` & `ProfileSetupPage.jsx` (Canonical skills integration)
- `frontend/src/pages/SalaryAnalysisPage.jsx` (Autofill, annual/monthly toggle, direct SHAP link)
- `frontend/src/pages/SavedReportsPage.jsx` (Search, filter, sorting, pagination, modal)
- `frontend/src/pages/PredictionExplanationPage.jsx` (Waterfall chart, attribution metrics)
- `frontend/src/pages/SkillImpactPage.jsx` (Portfolio valuation, co-occurrence highlights)
- `frontend/src/pages/JobMatchingPage.jsx` (9 roles, composite scoring, gap analysis)
- `frontend/src/pages/CareerRoadmapPage.jsx` (DAG milestones, interactive checkboxes)
- `frontend/src/pages/WhatIfSimulatorPage.jsx` (Real counterfactual simulation sandbox)
- `frontend/src/pages/SettingsPage.jsx` (Account details, preferences, session status)

---

## 4. Testing & Verification Strategy

1. **Unit & Component Testing**: Verify UI components render cleanly with proper default and edge-case props.
2. **Backend Regression Testing**: Run `manage.py test apps.accounts apps.profiles apps.predictions apps.intelligence` (target: 45/45 passing).
3. **ML Pipeline Regression**: Run `pytest ml/tests/` (target: 13/13 passing).
4. **Production Build Compilation**: Run `npm run build` in `frontend` (target: 0 errors, clean bundle).
5. **End-to-End User Journeys**: Verify New User, Salary Analysis, Skill Intelligence, Role Matching, Career Growth, and Returning User flows with real PostgreSQL records.

---

## 5. Acceptance Criteria

- [ ] All 14 pages polished, responsive, and using the unified design system.
- [ ] No hardcoded heuristic calculations on the dashboard; all metrics drawn from live APIs.
- [ ] Accessible navigation with categorized sidebar, mobile drawer, and breadcrumbs.
- [ ] Every page handles Loading, Error, Empty, and Success states.
- [ ] What-If Simulator connected to `POST /api/intelligence/skills/compare/`.
- [ ] 0 build errors in Vite and 0 test regressions in Django and pytest.
- [ ] Comprehensive documentation suite authored.
