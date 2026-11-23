# WorthIQ — Prediction Engine REST API Documentation
## Endpoints, Schemas, Authentication & Response Formats

**Base URL:** `http://localhost:8000/api/predictions`  
**Authentication:** Bearer JWT (`Authorization: Bearer <access_token>`)  

---

## 1. Overview of Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/predictions/salary/` | Submit candidate attributes and receive real-time ML salary predictions. | Yes |
| `GET` | `/api/predictions/history/` | Retrieve paginated historical predictions for the authenticated user. | Yes |
| `GET` | `/api/predictions/history/{id}/` | Retrieve detailed breakdown of a single historical prediction. | Yes |
| `GET` | `/api/predictions/model-info/` | Retrieve ML model version, architecture, and governance metrics. | No (Public) |

---

## 2. POST /api/predictions/salary/

Generates a machine learning compensation prediction and records it into the user's prediction history.

### Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### Request Body Schema
| Field | Type | Required | Range / Enum | Description |
|---|---|---|---|---|
| `job_role` | String | Yes | Max 150 chars | Target job title (e.g. `Full Stack Developer`). |
| `years_of_experience` | Decimal / Float | Yes | 0.0 to 60.0 | Full-time professional experience. |
| `location` | String | Yes | Max 150 chars | Primary metro hub or city (e.g. `Bengaluru`). |
| `education` | String | No | Max 150 chars | Highest degree (e.g. `Bachelor's Degree`). |
| `skills` | Array of Strings | No | Max 50 items | List of technical skills (e.g. `['React', 'Node.js']`). |

### Example Request
```json
{
  "job_role": "Full Stack Developer",
  "years_of_experience": 3.5,
  "location": "Bengaluru",
  "education": "Bachelor's Degree",
  "skills": ["JavaScript", "React.js", "Node.js", "PostgreSQL", "Docker", "Git"]
}
```

### Success Response (`201 Created`)
```json
{
  "id": 142,
  "job_role": "Full Stack Developer",
  "years_of_experience": 3.5,
  "location": "Bengaluru",
  "education": "Bachelor's Degree",
  "skills": ["JavaScript", "React.js", "Node.js", "PostgreSQL", "Docker", "Git"],
  "predicted_salary_annual": 1284500.0,
  "predicted_salary_lpa": "12.85",
  "predicted_salary_formatted": "₹12,84,500",
  "salary_range": {
    "p10_annual": 915200.0,
    "p10_lpa": "9.15",
    "p10_formatted": "₹9,15,200",
    "p50_annual": 1284500.0,
    "p50_lpa": "12.85",
    "p50_formatted": "₹12,84,500",
    "p90_annual": 1942000.0,
    "p90_lpa": "19.42",
    "p90_formatted": "₹19,42,000"
  },
  "confidence_score": 92.5,
  "confidence_level": "High",
  "confidence_factors": {
    "experience_factor": 100,
    "role_factor": 100,
    "location_factor": 100,
    "skills_factor": 100
  },
  "top_recommended_skills": ["AWS", "Kubernetes", "Redis", "TypeScript"],
  "model_version": "2.0.0",
  "created_at": "2026-11-23T07:45:12.184920Z"
}
```

---

## 3. GET /api/predictions/history/

Retrieves a paginated list of all salary predictions evaluated by the authenticated user, sorted in descending order of creation time (`-created_at`).

### Query Parameters
- `page` (Integer, default = 1): Target page index.

### Success Response (`200 OK`)
```json
{
  "count": 18,
  "next": "http://localhost:8000/api/predictions/history/?page=2",
  "previous": null,
  "results": [
    {
      "id": 142,
      "job_role": "Full Stack Developer",
      "years_of_experience": 3.5,
      "location": "Bengaluru",
      "education": "Bachelor's Degree",
      "skills": ["JavaScript", "React.js", "Node.js", "PostgreSQL", "Docker", "Git"],
      "predicted_salary_annual": 1284500.0,
      "predicted_salary_lpa": "12.85",
      "predicted_salary_formatted": "₹12,84,500",
      "salary_range": {
        "p10_annual": 915200.0,
        "p10_lpa": "9.15",
        "p10_formatted": "₹9,15,200",
        "p50_annual": 1284500.0,
        "p50_lpa": "12.85",
        "p50_formatted": "₹12,84,500",
        "p90_annual": 1942000.0,
        "p90_lpa": "19.42",
        "p90_formatted": "₹19,42,000"
      },
      "confidence_score": 92.5,
      "confidence_level": "High",
      "created_at": "2026-11-23T07:45:12.184920Z"
    }
  ]
}
```

---

## 4. GET /api/predictions/history/{id}/

Retrieves detailed record for a specific prediction ID. Enforces strict user isolation: attempting to access another user's report returns `404 Not Found`.

### Success Response (`200 OK`)
Returns the complete prediction object including `confidence_factors` and `top_recommended_skills`.

---

## 5. GET /api/predictions/model-info/

Returns governance and operational metrics about the active production model artifacts.

### Success Response (`200 OK`)
```json
{
  "model_name": "Random Forest",
  "model_version": "2.0.0",
  "algorithm": "RandomForestRegressor",
  "target_currency": "INR",
  "features_count": 55,
  "training_rows": 20265,
  "test_rows": 5067,
  "metrics": {
    "cv_5fold": {
      "mae": 335065.71,
      "rmse": 556272.73,
      "r2": 0.4109
    },
    "test": {
      "mae": 351026.62,
      "rmse": 607554.94,
      "r2": 0.3597,
      "medae": 215291.21
    }
  },
  "quantiles": {
    "p10_coverage_pct": 10.2,
    "p50_coverage_pct": 48.1,
    "p90_coverage_pct": 89.3
  }
}
```

---

## 6. Error Responses

### `400 Bad Request` (Invalid Inputs)
```json
{
  "years_of_experience": ["Ensure this value is greater than or equal to 0."]
}
```

### `401 Unauthorized` (Missing or Expired Token)
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

### `404 Not Found` (Non-existent or Unauthorized History ID)
```json
{
  "detail": "Not found."
}
```
