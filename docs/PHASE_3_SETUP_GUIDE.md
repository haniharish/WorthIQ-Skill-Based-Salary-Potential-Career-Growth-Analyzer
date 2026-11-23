# WorthIQ Phase 3 Setup Guide
## AI Intelligence Engine Deployment, Seeding & Execution

---

## 1. Prerequisites

Before running WorthIQ Phase 3, ensure the following components are active:
- **Python**: 3.10+ (Current deployment: Python 3.14.7)
- **Node.js**: 18+ (Current deployment: Node.js 22+)
- **PostgreSQL**: 16 (Running in Docker container `worthiq_postgres` on port `5432`)
- **Git**: Working copy on branch `main`

---

## 2. PostgreSQL Infrastructure

Ensure the PostgreSQL container is running:
```bash
docker compose up -d postgres
```
Verify container health:
```bash
docker ps --filter "name=worthiq_postgres"
```

Connection parameters configured in `backend/config/settings.py`:
- **Database**: `worthiq_db`
- **User**: `worthiq_user`
- **Password**: `worthiq_secure_pass_2026`
- **Host**: `localhost`
- **Port**: `5432`

---

## 3. Backend Setup & Seeding

### 3.1 Activate Virtual Environment & Install Dependencies

On Windows PowerShell:
```powershell
cd c:\Users\Lenovo\Desktop\WorthIQ
.\backend\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Verify `shap` is installed:
```powershell
python -c "import shap; print('SHAP version:', shap.__version__)"
# Output: SHAP version: 0.54.1
```

### 3.2 Apply Database Migrations

Apply database schema changes for Phase 3 models (`apps.intelligence`):
```powershell
python backend\manage.py migrate
```

### 3.3 Seed Skill Taxonomy and Job Roles

WorthIQ includes automated database seeders for the canonical skill taxonomy (35 skills, 81 aliases) and job roles (9 curated roles):

```powershell
python backend\manage.py shell -c "from apps.intelligence.services.skill_normalization_service import seed_skills_in_db; from apps.intelligence.services.role_matching_service import seed_roles_in_db; seed_skills_in_db(); seed_roles_in_db(); print('Seeding complete!')"
```

### 3.4 Start Backend Server

```powershell
python backend\manage.py runserver 8000
```
Backend API will be live at `http://127.0.0.1:8000/`.

---

## 4. Frontend Setup & Execution

### 4.1 Install Packages

```powershell
cd c:\Users\Lenovo\Desktop\WorthIQ\frontend
npm install
```

### 4.2 Start Vite Development Server

```powershell
npm run dev
```
Frontend will be live at `http://localhost:5180/`.

---

## 5. Verification & Test Execution

### 5.1 Run Django Intelligence & Full Backend Tests

To run the intelligence app test suite:
```powershell
python backend\manage.py test apps.intelligence
# Output: Ran 19 tests in 37s ... OK
```

To run all backend tests across all apps:
```powershell
python backend\manage.py test apps.accounts apps.profiles apps.predictions apps.intelligence
# Output: Ran 45 tests in 51s ... OK
```

### 5.2 Run Machine Learning Test Suite

```powershell
pytest ml/tests/
# Output: 13 passed in 10.23s
```

### 5.3 Verify Frontend Production Build

```powershell
cd frontend
npm run build
# Output: ✓ built in ~12s (dist/ generated successfully)
```
