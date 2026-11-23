# WORTHIQ — PHASE 5 API DOCUMENTATION
## REST API Endpoints Specification for Scenarios, Resumes, and Reports

All endpoints require JWT Bearer Authentication header:
`Authorization: Bearer <access_token>`

---

### 1. What-If Scenarios Endpoints (`/api/scenarios/`)

#### 1.1 List & Create Scenarios
- **`GET /api/scenarios/`**
  - **Description:** Retrieve all saved scenarios belonging to the authenticated user.
  - **Response (200 OK):**
    ```json
    [
      {
        "id": 1,
        "name": "Senior Cloud Architect",
        "job_role": "Cloud Architect",
        "years_of_experience": "5.0",
        "location": "Bengaluru",
        "education": "Bachelor's Degree",
        "skills": ["AWS", "Docker", "Kubernetes", "Python"],
        "prediction_snapshot": {
          "p10_lpa": 12.5,
          "p50_lpa": 21.0,
          "p90_lpa": 28.5
        },
        "salary_lpa": 21.0,
        "notes": "Transition goal",
        "created_at": "2026-11-23T12:00:00Z"
      }
    ]
    ```

- **`POST /api/scenarios/`**
  - **Description:** Create and persist a new salary scenario, automatically computing its prediction snapshot.
  - **Request Body:**
    ```json
    {
      "name": "DevOps Lead Scenario",
      "job_role": "DevOps Engineer",
      "years_of_experience": 4.5,
      "location": "Hyderabad",
      "education": "Bachelor's Degree",
      "skills": ["Docker", "Kubernetes", "CI/CD", "Linux"],
      "notes": "Target for Q4"
    }
    ```
  - **Response (201 Created):** Serialized `SalaryScenario`.

#### 1.2 Scenario Operations
- **`GET /api/scenarios/<id>/`** (200 OK)
- **`PUT /api/scenarios/<id>/`** (200 OK)
- **`DELETE /api/scenarios/<id>/`** (204 No Content)
- **`POST /api/scenarios/<id>/duplicate/`** (201 Created)
- **`POST /api/scenarios/compare/`**
  - **Description:** Multi-scenario comparative evaluation engine.
  - **Request Body:**
    ```json
    {
      "baseline": {
        "job_role": "Full Stack Developer",
        "years_of_experience": 2.0,
        "location": "Delhi NCR",
        "education": "Bachelor's Degree",
        "skills": ["Python", "React.js", "PostgreSQL"]
      },
      "scenarios": [
        {
          "name": "Acquire Docker & AWS",
          "job_role": "Full Stack Developer",
          "years_of_experience": 3.0,
          "location": "Bengaluru",
          "education": "Bachelor's Degree",
          "skills": ["Python", "React.js", "PostgreSQL", "Docker", "AWS"]
        }
      ],
      "scenario_ids": [1]
    }
    ```
  - **Response (200 OK):** Comparative matrix with pairwise deltas and non-causality disclaimer.

---

### 2. Resume Intelligence Endpoints (`/api/resumes/`)

#### 2.1 Upload & Parse Document
- **`POST /api/resumes/upload/`**
  - **Content-Type:** `multipart/form-data`
  - **Payload:** `file` (PDF or DOCX, max 5MB).
  - **Response (201 Created):**
    ```json
    {
      "resume": { "id": 1, "original_filename": "resume.pdf", "processing_status": "completed" },
      "extraction": {
        "raw_text_length": 2540,
        "candidate_info": { "name": "Harish Sharma", "email": "harish@example.com", "years_of_experience": 3.0 },
        "extracted_skills": [
          { "name": "Python", "confidence": 98, "snippet": "...proficient in Python and Django..." }
        ]
      }
    }
    ```

#### 2.2 Extraction Results & Profile Sync
- **`GET /api/resumes/<id>/results/`**
  - **Response (200 OK):** Extraction details with comparison against user profile (`new_skills` vs `existing_skills`).
- **`POST /api/resumes/<id>/apply-to-profile/`**
  - **Description:** Explicit user-confirmed profile sync.
  - **Request Body:**
    ```json
    {
      "skills": ["Docker", "AWS"],
      "apply_experience": true,
      "apply_education": false
    }
    ```
  - **Response (200 OK):**
    ```json
    { "message": "Successfully synchronized 2 skills to your profile.", "added_skills": ["Docker", "AWS"] }
    ```

---

### 3. Advanced Reports & Export Endpoints (`/api/reports/`)

#### 3.1 Report Archive & PDF
- **`GET /api/reports/?type=<optional_type>`** (200 OK)
- **`POST /api/reports/generate/`** (201 Created)
- **`GET /api/reports/<id>/download/`**
  - **Response (200 OK):** Binary PDF stream (`Content-Type: application/pdf`).

#### 3.2 CSV Export
- **`GET /api/reports/export/csv/?type=predictions|scenarios`**
  - **Response (200 OK):** Streaming CSV file (`Content-Type: text/csv; charset=utf-8`).
