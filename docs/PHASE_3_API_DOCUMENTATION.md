# WorthIQ Phase 3 API Documentation
## AI Intelligence Engine REST API Specifications

---

## 1. Overview & Authentication

All endpoints in Phase 3 reside under the `/api/intelligence/` prefix.

- **Base URL**: `http://localhost:8000/api/intelligence/`
- **Authentication**: JWT Bearer token required for user-specific endpoints (`Authorization: Bearer <access_token>`).
- **Content Type**: `application/json`

---

## 2. Module A: SHAP Explainability Endpoints

### 2.1 Get Local SHAP Explanation for Prediction
- **URL**: `GET /api/intelligence/explanations/{prediction_id}/`
- **Auth**: Required (`IsAuthenticated`). User must be the owner of the prediction.
- **Status Codes**: `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

#### Response Example (`200 OK`)
```json
{
  "id": 1,
  "prediction_id": 104,
  "job_role": "Backend Developer",
  "location": "Bengaluru",
  "years_of_experience": "4.0",
  "base_value_log": 13.368,
  "base_value_inr": "639242.00",
  "predicted_value_log": 13.653,
  "predicted_value_inr": "850000.00",
  "total_delta_inr": "210758.00",
  "feature_attributions": [
    {
      "feature": "Location: Bengaluru",
      "shap_log_value": 0.088,
      "impact_percentage": 9.2,
      "inr_marginal_impact": 68420.0,
      "direction": "positive"
    },
    {
      "feature": "Years of Experience (4.0 yrs)",
      "shap_log_value": 0.067,
      "impact_percentage": 6.9,
      "inr_marginal_impact": 52190.0,
      "direction": "positive"
    },
    {
      "feature": "Skill: Docker",
      "shap_log_value": 0.041,
      "impact_percentage": 4.2,
      "inr_marginal_impact": 31450.0,
      "direction": "positive"
    }
  ],
  "positive_contributors": [
    { "feature": "Location: Bengaluru", "inr_impact": 68420.0, "pct_impact": 9.2 }
  ],
  "negative_contributors": [
    { "feature": "Education: Bachelor's Degree", "inr_impact": -8450.0, "pct_impact": -1.3 }
  ],
  "skills_impact": [
    { "skill": "Docker", "inr_marginal_impact": 31450.0 }
  ],
  "summary_narrative": "Your predicted compensation of ₹8,50,000 represents a +₹2,10,758 variance from the baseline expectation (₹6,39,242)...",
  "model_version": "2.0.0",
  "created_at": "2026-11-23T14:30:00Z"
}
```

### 2.2 Get Global Feature Importance Rankings
- **URL**: `GET /api/intelligence/explanations/global/`
- **Auth**: Public (`AllowAny`).

#### Response Example (`200 OK`)
```json
{
  "model_version": "2.0.0",
  "base_log_expected_value": 13.368,
  "base_expected_salary_inr": 639242.0,
  "top_global_features": [
    { "feature": "years_of_experience", "mean_abs_shap": 0.2418 },
    { "feature": "job_role", "mean_abs_shap": 0.1874 },
    { "feature": "location", "mean_abs_shap": 0.1295 },
    { "feature": "skill: Docker", "mean_abs_shap": 0.0612 }
  ]
}
```

---

## 3. Module B: Skill Intelligence Endpoints

### 3.1 Get Canonical Skill Taxonomy
- **URL**: `GET /api/intelligence/skills/`
- **Auth**: Public (`AllowAny`).

#### Response Example (`200 OK`)
```json
{
  "total_count": 35,
  "categories": {
    "Programming Languages": [...],
    "Frontend Frameworks": [...],
    "Backend & APIs": [...],
    "Databases & Storage": [...],
    "Cloud & DevOps": [...],
    "Data & AI": [...]
  },
  "skills": [...]
}
```

### 3.2 Evaluate Portfolio Marginal Skill Impact
- **URL**: `GET /api/intelligence/skills/impact/`
- **Auth**: Required (`IsAuthenticated`).
- **Query Parameters**: `job_role`, `years_of_experience`, `location`, `education`, `skills` (comma-separated).

#### Response Example (`200 OK`)
```json
{
  "evaluated_profile": {
    "job_role": "Backend Developer",
    "years_of_experience": 4.0,
    "location": "Bengaluru",
    "education": "Bachelor's Degree",
    "skills": ["Python", "PostgreSQL", "Docker", "Git"]
  },
  "skill_impacts": [
    {
      "skill": "Docker",
      "marginal_delta_inr": 72000.0,
      "marginal_delta_lpa": 0.72,
      "percentage_impact": 9.5
    },
    {
      "skill": "PostgreSQL",
      "marginal_delta_inr": 54000.0,
      "marginal_delta_lpa": 0.54,
      "percentage_impact": 7.1
    }
  ],
  "bundle_synergy": {
    "synergy_score": 1.48,
    "tier": "High Synergy",
    "description": "Your skills represent a cohesive and complementary technology stack."
  }
}
```

### 3.3 Get Skill Co-Occurrence Statistics
- **URL**: `GET /api/intelligence/skills/co-occurrence/`
- **Auth**: Public (`AllowAny`).
- **Query Parameters**: `skill` (optional), `limit` (default: 25).

#### Response Example (`200 OK`)
```json
{
  "skill_filter": "Python",
  "pair_count": 10,
  "co_occurrences": [
    {
      "skill_a": "Python",
      "skill_b": "SQL",
      "pair_count": 13950,
      "jaccard_similarity": 0.589,
      "median_salary": 765000.0
    },
    {
      "skill_a": "Python",
      "skill_b": "Git",
      "pair_count": 14892,
      "jaccard_similarity": 0.621,
      "median_salary": 780000.0
    }
  ]
}
```

### 3.4 What-If Counterfactual Comparison
- **URL**: `POST /api/intelligence/skills/compare/`
- **Auth**: Required (`IsAuthenticated`).

#### Request Body
```json
{
  "job_role": "Full Stack Developer",
  "years_of_experience": 3.0,
  "location": "Bengaluru",
  "education": "Bachelor's Degree",
  "skills": ["JavaScript", "React.js", "SQL", "Git"],
  "add_skills": ["Docker", "AWS", "TypeScript"],
  "remove_skills": []
}
```

#### Response Example (`200 OK`)
```json
{
  "original_salary_annual": 640000.0,
  "original_salary_lpa": 6.4,
  "counterfactual_salary_annual": 815000.0,
  "counterfactual_salary_lpa": 8.15,
  "delta_annual": 175000.0,
  "delta_lpa": 1.75,
  "percentage_change": 27.34,
  "added_skills": ["Docker", "AWS", "TypeScript"],
  "removed_skills": [],
  "resulting_skill_count": 7
}
```

---

## 4. Module C: Job Role Matching Endpoints

### 4.1 List Role Catalog
- **URL**: `GET /api/intelligence/roles/`
- **Auth**: Public (`AllowAny`).

### 4.2 Get Role Detail
- **URL**: `GET /api/intelligence/roles/{role_id}/`
- **Auth**: Public (`AllowAny`).

### 4.3 Match Roles for Candidate
- **URL**: `POST /api/intelligence/roles/match/`
- **Auth**: Public / Authenticated.

#### Request Body
```json
{
  "skills": ["Python", "PostgreSQL", "Docker", "Git", "REST APIs"],
  "experience": 3.5
}
```

#### Response Example (`200 OK`)
```json
{
  "total_roles_evaluated": 9,
  "matches": [
    {
      "id": 2,
      "title": "Backend Developer",
      "description": "Designs robust distributed microservices...",
      "match_score": 82.5,
      "match_category": "Strong Match",
      "badge_color": "emerald",
      "matched_required_skills": ["Python", "PostgreSQL", "REST APIs", "Git", "SQL"],
      "missing_required_skills": [],
      "missing_preferred_skills": ["Django", "FastAPI", "Kubernetes", "Linux", "Microservices", "Redis"],
      "required_coverage_pct": 100.0,
      "experience_compatibility_pct": 100.0,
      "median_salary_inr": 750000.0,
      "median_salary_lpa": 7.5,
      "factors": {
        "required_skills_weight": "40%",
        "preferred_skills_weight": "15%",
        "text_similarity_weight": "25%",
        "experience_fit_weight": "20%"
      }
    }
  ]
}
```

---

## 5. Module D: Career Growth Roadmap Endpoints

### 5.1 List Saved Roadmaps
- **URL**: `GET /api/intelligence/roadmaps/`
- **Auth**: Required (`IsAuthenticated`).

### 5.2 Generate New Career Roadmap
- **URL**: `POST /api/intelligence/roadmaps/generate/`
- **Auth**: Required (`IsAuthenticated`).

#### Request Body
```json
{
  "target_role_id": 4,
  "current_role": "Backend Developer",
  "current_experience": 2.5,
  "current_skills": ["Python", "Django", "PostgreSQL", "Git"]
}
```

#### Response Example (`201 Created`)
```json
{
  "id": 12,
  "title": "Career Roadmap: Backend Developer -> DevOps Engineer",
  "current_role": "Backend Developer",
  "target_role": 4,
  "target_role_title": "DevOps Engineer",
  "target_role_description": "Automates software delivery pipelines...",
  "overall_progress_pct": 0.0,
  "is_saved": true,
  "stages": [
    {
      "id": 34,
      "stage_number": 1,
      "title": "Stage 1: Core Technical Foundations",
      "objective": "Build solid mastery of foundational Linux and basic containerization concepts.",
      "project_suggestion": "Build and containerize a multi-stage Docker build microservice with automated unit tests.",
      "is_completed": false,
      "skills_progress": [
        {
          "id": 101,
          "skill_name": "Linux",
          "category": "Cloud & DevOps",
          "importance": "Mandatory",
          "is_completed": false
        },
        {
          "id": 102,
          "skill_name": "Docker",
          "category": "Cloud & DevOps",
          "importance": "Mandatory",
          "is_completed": false
        }
      ]
    }
  ]
}
```

### 5.3 Toggle Skill Progress
- **URL**: `PATCH /api/intelligence/roadmaps/{roadmap_id}/progress/`
- **Auth**: Required (`IsAuthenticated`). Must be owner.

#### Request Body
```json
{
  "skill_progress_id": 101,
  "is_completed": true
}
```

#### Response Example (`200 OK`)
```json
{
  "detail": "Roadmap progress updated successfully.",
  "overall_progress_pct": 25.0,
  "roadmap": { ... }
}
```

### 5.4 Delete Saved Roadmap
- **URL**: `DELETE /api/intelligence/roadmaps/{roadmap_id}/`
- **Auth**: Required (`IsAuthenticated`). Must be owner.
- **Status Code**: `204 No Content`.
