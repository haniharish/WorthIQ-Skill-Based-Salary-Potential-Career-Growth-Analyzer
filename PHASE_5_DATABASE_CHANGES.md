# WORTHIQ — PHASE 5 DATABASE CHANGES
## PostgreSQL Schema Migrations, Tables & Indexes

**Database:** PostgreSQL 16 (`worthiq_db`)  
**Container:** `worthiq_postgres` on Port 5432  
**Migrations Applied:**
- `scenarios.0001_initial`
- `resumes.0001_initial`
- `reports.0001_initial`

---

### 1. New Tables Overview

#### 1.1 `worthiq_salary_scenarios` (`apps.scenarios`)
Stores user-created What-If salary simulation experiments.
- `id` (BigAutoField, PRIMARY KEY)
- `user_id` (ForeignKey -> `accounts_user.id`, ON DELETE CASCADE)
- `name` (VARCHAR 150)
- `job_role` (VARCHAR 150)
- `years_of_experience` (DECIMAL 4,1)
- `location` (VARCHAR 150)
- `education` (VARCHAR 150)
- `skills` (JSONB) — array of technical skills
- `prediction_snapshot` (JSONB) — cached salary prediction output (P10, P50, P90, confidence)
- `notes` (TEXT)
- `created_at` (TIMESTAMPTZ)
- `updated_at` (TIMESTAMPTZ)
- **Indexes:** `['user', '-created_at']`, `['user', 'job_role']`

#### 1.2 `worthiq_resume_documents` (`apps.resumes`)
Stores uploaded resume files and processing lifecycle status.
- `id` (BigAutoField, PRIMARY KEY)
- `user_id` (ForeignKey -> `accounts_user.id`, ON DELETE CASCADE)
- `file` (FileField -> `media/resumes/%Y/%m/`)
- `original_filename` (VARCHAR 255)
- `file_size` (INTEGER)
- `file_type` (VARCHAR 10: `'pdf'` or `'docx'`)
- `processing_status` (VARCHAR 20: `'pending'`, `'processing'`, `'completed'`, `'failed'`)
- `error_message` (TEXT)
- `uploaded_at` (TIMESTAMPTZ)
- **Indexes:** `['user', '-uploaded_at']`

#### 1.3 `worthiq_resume_extractions` (`apps.resumes`)
Stores parsed metadata and skill extractions linked 1-to-1 with a document.
- `id` (BigAutoField, PRIMARY KEY)
- `document_id` (OneToOneField -> `worthiq_resume_documents.id`, ON DELETE CASCADE)
- `extracted_skills` (JSONB) — array of `{ name, confidence, snippet }`
- `candidate_info` (JSONB) — `{ name, email, phone, years_of_experience, education }`
- `raw_text_length` (INTEGER)
- `warnings` (JSONB) — parsing warnings
- `created_at` (TIMESTAMPTZ)

#### 1.4 `worthiq_advanced_reports` (`apps.reports`)
Stores persistent assessment reports and data snapshots.
- `id` (BigAutoField, PRIMARY KEY)
- `user_id` (ForeignKey -> `accounts_user.id`, ON DELETE CASCADE)
- `title` (VARCHAR 255)
- `report_type` (VARCHAR 50: `salary_prediction`, `shap_explanation`, `job_role_matching`, `career_roadmap`, `scenario_comparison`, `resume_analysis`, `comprehensive_audit`)
- `source_id` (VARCHAR 100)
- `summary` (TEXT)
- `data_snapshot` (JSONB)
- `pdf_file` (FileField -> `media/reports/%Y/%m/`, optional)
- `created_at` (TIMESTAMPTZ)
- `updated_at` (TIMESTAMPTZ)
- **Indexes:** `['user', '-created_at']`, `['user', 'report_type']`

---

### 2. Constraints & Data Integrity

- User isolation enforced through foreign keys with cascading deletions.
- Zero orphaned extractions or reports upon user account deletion.
- JSONB columns utilized in PostgreSQL for high-performance indexing and querying.
