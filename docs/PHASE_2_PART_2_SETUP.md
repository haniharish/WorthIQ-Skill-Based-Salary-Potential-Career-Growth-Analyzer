# WorthIQ — Phase 2 Part 2 Setup & Operational Guide
## Machine Learning Model Engine & Full-Stack Service Integration

**Project:** WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer  
**Milestone:** Phase 2 Part 2 Complete  

---

## 1. System Requirements & Port Allocation

- **Frontend:** React + Vite on `http://localhost:5180`
- **Backend:** Django 5.2 + DRF on `http://localhost:8000`
- **Database:** PostgreSQL 16 on `localhost:5432` (`worthiq_db`)
- **Python Environment:** Python 3.14+ with packages: `scikit-learn`, `xgboost`, `pandas`, `numpy`, `joblib`, `django`, `djangorestframework`, `django-cors-headers`, `djangorestframework-simplejwt`, `psycopg2-binary`.

---

## 2. Setting Up the Database

Ensure PostgreSQL is running via Docker Compose:
```bash
docker compose -f database/docker-compose.yml up -d
```

Verify container status:
```bash
docker ps --filter "name=worthiq_postgres"
```

Apply database migrations:
```bash
backend\venv\Scripts\python.exe backend\manage.py migrate
```

---

## 3. Verifying Machine Learning Artifacts

The ML artifacts reside in `ml/models/`:
- `salary_model.joblib`: Production Random Forest regressor.
- `preprocessing_pipeline.joblib`: One-Hot and Multi-Label Skills feature transformer.
- `quantile_models/quantile_p10.joblib`: 10th percentile model.
- `quantile_models/quantile_p50.joblib`: 50th percentile model.
- `quantile_models/quantile_p90.joblib`: 90th percentile model.
- `model_metadata.json`: Feature vectors and validation metrics.

To verify model loading in Django:
```bash
backend\venv\Scripts\python.exe -c "from apps.predictions.services.model_loader import ModelRegistry; reg = ModelRegistry.get_instance(); print('Model status:', reg.is_loaded(), 'Algorithm:', reg.metadata['algorithm'])"
```

---

## 4. Running Automated Tests

Run the complete test suite across ML pipelines and Django services:

### 4.1 ML Pipeline Tests (13 tests)
```bash
backend\venv\Scripts\pytest.exe ml/tests/
```

### 4.2 Django Service Tests (26 tests)
```bash
backend\venv\Scripts\python.exe backend\manage.py test apps.accounts apps.profiles apps.predictions
```

### 4.3 Frontend Production Build
```bash
cd frontend
npm run build
```

---

## 5. Starting the Development Servers

In terminal 1 (Backend):
```bash
backend\venv\Scripts\python.exe backend\manage.py runserver 8000
```

In terminal 2 (Frontend):
```bash
cd frontend
npm run dev -- --port 5180
```

Navigate to `http://localhost:5180/salary-analysis` to test real-time salary predictions!
