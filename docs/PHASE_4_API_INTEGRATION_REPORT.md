# WorthIQ Phase 4 API Integration Report
## Frontend Services, Backend Endpoints, Data Contracts & Error Handling

---

## 1. Overview

Phase 4 establishes complete, unified full-stack integration between the React frontend and Django REST Framework backend. **All mock/fake data has been eliminated from production views.** Every widget, table, KPI card, and chart is powered by authenticated REST endpoints.

---

## 2. Frontend Service Layer Architecture

The frontend service layer is centralized under `frontend/src/services/` using Axios with an automated JWT interceptor:

```
frontend/src/services/
├── api.js                   # Axios base client, auth header injection, 401 token refresh interceptor
├── authService.js           # Authentication (login, register, token refresh, logout)
├── profileService.js        # User profile, skills array, education, experience
├── predictionService.js     # Salary prediction, evaluation history, report detail, delete
├── intelligenceService.js   # SHAP explainability, skills taxonomy, impact, role matching, roadmaps
└── dashboardService.js      # Aggregator service fetching unified dashboard data concurrently
```

---

## 3. Endpoints Integration Matrix

| Service | Target Endpoint | HTTP Method | Auth Required | Purpose in Phase 4 |
|:---|:---|:---:|:---:|:---|
| **authService** | `/api/accounts/login/` | `POST` | No | User authentication, JWT acquisition |
| | `/api/accounts/register/` | `POST` | No | New user onboarding |
| | `/api/accounts/token/refresh/` | `POST` | No | Silent access token refresh on 401 |
| **profileService** | `/api/accounts/profile/` | `GET` | Yes | Retrieves user info, skills list, job title |
| | `/api/accounts/profile/` | `PUT` | Yes | Updates skills, experience, and profile details |
| **predictionService** | `/api/predictions/salary/` | `POST` | Yes | Real-time salary prediction & quantile estimation |
| | `/api/predictions/history/` | `GET` | Yes | Historical salary predictions for timeline & reports |
| | `/api/predictions/history/{id}/` | `GET` | Yes | Detailed single evaluation breakdown with features |
| | `/api/predictions/history/{id}/` | `DELETE`| Yes | Deletes historical report record |
| **intelligenceService** | `/api/intelligence/skills/` | `GET` | Yes | Fetches canonical taxonomy of 35 skills |
| | `/api/intelligence/skills/compare/` | `POST` | Yes | Counterfactual simulation for What-If Simulator |
| | `/api/intelligence/skills/impact/` | `GET` | Yes | Marginal Rupee delta and portfolio skill impact |
| | `/api/intelligence/roles/match/` | `GET` | Yes | Profile-to-role matching and skill gap calculation |
| | `/api/intelligence/roadmaps/` | `GET` | Yes | Fetches saved learning roadmaps |
| | `/api/intelligence/roadmaps/` | `POST` | Yes | Generates custom multi-phase learning roadmap |
| | `/api/intelligence/roadmaps/{id}/` | `PATCH`| Yes | Checks off roadmap milestone progress |
| | `/api/intelligence/explanations/{id}/` | `GET` | Yes | Fetches TreeSHAP waterfall values and feature rank |
| **dashboardService** | Multi-endpoint parallel fetch | `GET` | Yes | Concurrent Promise.allSettled fetching all KPIs |

---

## 4. Key Request and Response Contracts

### 4.1 Salary Prediction (`POST /api/predictions/salary/`)
**Request Payload:**
```json
{
  "job_role": "Data Scientist",
  "years_of_experience": 4.5,
  "location": "Bengaluru",
  "education": "Master's Degree",
  "skills": ["Python", "Machine Learning", "SQL", "Pandas", "Scikit-Learn"]
}
```

**Response Payload:**
```json
{
  "prediction_id": "9a12c45e-b5f7-41e2-9b24-81d3fca91092",
  "predicted_salary": 1425000.0,
  "p10": 1150000.0,
  "p50": 1425000.0,
  "p90": 1780000.0,
  "confidence_score": 86.4,
  "currency": "INR",
  "created_at": "2026-11-23T12:00:00Z"
}
```

### 4.2 Counterfactual What-If Simulation (`POST /api/intelligence/skills/compare/`)
**Request Payload:**
```json
{
  "job_role": "Software Engineer",
  "years_of_experience": 3.0,
  "location": "Hyderabad",
  "education": "Bachelor's Degree",
  "base_skills": ["Python", "Django", "SQL"],
  "target_skills": ["Python", "Django", "SQL", "Docker", "Kubernetes", "AWS"]
}
```

**Response Payload:**
```json
{
  "base_salary": 920000.0,
  "counterfactual_salary": 1280000.0,
  "salary_difference": 360000.0,
  "percentage_change": 39.13,
  "skills_added": ["Docker", "Kubernetes", "AWS"],
  "skills_removed": [],
  "per_skill_impact": [
    {"skill": "Kubernetes", "marginal_delta": 150000.0},
    {"skill": "AWS", "marginal_delta": 130000.0},
    {"skill": "Docker", "marginal_delta": 80000.0}
  ]
}
```

### 4.3 SHAP Explanation (`GET /api/intelligence/explanations/{prediction_id}/`)
**Response Payload:**
```json
{
  "prediction_id": "9a12c45e-b5f7-41e2-9b24-81d3fca91092",
  "base_value_inr": 850000.0,
  "predicted_salary_inr": 1425000.0,
  "top_positive_features": [
    {"feature": "Machine Learning", "impact_inr": 210000.0, "category": "skill"},
    {"feature": "years_of_experience", "impact_inr": 185000.0, "category": "experience"},
    {"feature": "location_Bengaluru", "impact_inr": 120000.0, "category": "location"}
  ],
  "top_negative_features": [
    {"feature": "missing_Cloud_Computing", "impact_inr": -45000.0, "category": "missing_skill"}
  ]
}
```

---

## 5. Centralized Dashboard Aggregator (`dashboardService.js`)

To prevent blocking sequential network requests, `dashboardService.getDashboardData()` invokes 4 core requests concurrently using `Promise.allSettled`:

```javascript
const [profileResult, predictionsResult, rolesResult, roadmapsResult] = await Promise.allSettled([
  profileService.getProfile(),
  predictionService.getPredictionHistory({ limit: 1 }),
  intelligenceService.getRoleMatches(),
  intelligenceService.getSavedRoadmaps()
]);
```

### Benefits:
- **Resilient Degraded Loading:** If roadmaps fail or are empty, profile and salary prediction cards still render immediately.
- **Fast First Meaningful Paint:** Network round-trips happen in parallel over HTTP/1.1 keep-alive.
- **Unified Loading State:** Clean shimmer skeleton across all dashboard cards simultaneously.

---

## 6. Authentication & Error Handling Pipeline

1. **Automatic Authorization Header Injection:**
   All outgoing requests include `Authorization: Bearer <access_token>`.
2. **Silent 401 Refresh Cycle:**
   If access token expires, Axios interceptor pauses queued requests, invokes `/api/accounts/token/refresh/`, updates `localStorage`, and retries the original request.
3. **Graceful Error UI State:**
   API errors trigger `<ErrorState onRetry={...} />` or a global `<Toast />` alert notification rather than breaking component render trees.
