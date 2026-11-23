# WORTHIQ — PHASE 5 SETUP & RUN GUIDE

---

### 1. Prerequisites

- Python 3.10+ (Current: Python 3.14.7 in `backend/venv`)
- Node.js 18+ (Current: Node.js 20+ with Vite 6)
- Docker Desktop with PostgreSQL 16 active (`worthiq_postgres` on port 5432)

---

### 2. Environment Verification

1. **Verify PostgreSQL Container:**
   ```bash
   docker ps
   # Container 'worthiq_postgres' running on port 5432
   ```

2. **Verify Python Virtual Environment & Dependencies:**
   ```bash
   backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
   ```

3. **Verify Frontend Dependencies:**
   ```bash
   npm --prefix frontend install
   ```

---

### 3. Database Migrations

Apply database migrations:
```bash
backend\venv\Scripts\python.exe backend\manage.py migrate
```

---

### 4. Running the Application

1. **Backend Server (Django REST Framework):**
   ```bash
   backend\venv\Scripts\python.exe backend\manage.py runserver 0.0.0.0:8000
   ```
   Backend active at: `http://localhost:8000/`

2. **Frontend Dev Server (Vite / React):**
   ```bash
   npm --prefix frontend run dev
   ```
   Frontend active at: `http://localhost:5180/`

---

### 5. Running the Complete Test Suite

```bash
# Backend Phase 1-5 tests (33 tests)
backend\venv\Scripts\python.exe backend\manage.py test apps.accounts apps.profiles apps.predictions apps.scenarios apps.resumes apps.reports

# Intelligence tests (19 tests)
backend\venv\Scripts\python.exe backend\manage.py test apps.intelligence.tests

# ML Pipeline tests (13 tests)
backend\venv\Scripts\pytest.exe ml\tests\

# Frontend Build
npm --prefix frontend run build
```
Total: 65 automated tests passing with zero errors.
