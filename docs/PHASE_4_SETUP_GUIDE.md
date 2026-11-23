# WorthIQ Phase 4 Setup & Developer Guide
## Local Environment, Docker Container, Services Orchestration & Verification

---

## 1. System Requirements & Ports

| Service | Technology | Port | Binding | Configuration |
|:---|:---|:---:|:---:|:---|
| **PostgreSQL Database** | PostgreSQL 16 on Docker | `5432` | `localhost:5432` | DB: `worthiq_db`, User: `postgres`, Pass: `postgres` |
| **Backend REST API** | Python 3.14.7 / Django 5.x | `8000` | `0.0.0.0:8000` | DRF with JWT Authentication |
| **Frontend Web App** | React 18 / Vite 6.4.6 | `5180` | `http://localhost:5180` | Tailwind CSS, Recharts, strictPort: true |

> [!IMPORTANT]
> The frontend dev server is configured with `strictPort: true` on port **5180**. Do not change this port as it is referenced in CORS headers and authentication callbacks.

---

## 2. Quick Start (Windows PowerShell)

### Step 1: Start PostgreSQL Database Container
Ensure Docker Desktop is running:
```powershell
docker start worthiq_postgres
```
*If setting up a fresh container:*
```powershell
docker run --name worthiq_postgres -e POSTGRES_DB=worthiq_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
```

### Step 2: Configure & Start Backend Server
From the project root:
```powershell
# Activate Python Virtual Environment
.\backend\venv\Scripts\Activate.ps1

# Run Database Migrations
python backend\manage.py migrate

# Start Django Development Server (noreload mode recommended on Windows)
python backend\manage.py runserver --noreload 0.0.0.0:8000
```
Backend will be live at `http://127.0.0.1:8000/`.

### Step 3: Configure & Start Frontend Server
In a separate terminal window from the project root:
```powershell
# Navigate to frontend directory and install dependencies (if not installed)
cd frontend
npm install

# Start Vite Development Server
npm run dev
```
Frontend will be live at `http://localhost:5180/`.

---

## 3. Test Account Credentials

For development and grading evaluations, the following seeded account can be used:
- **Email:** `harish@worthiq.dev`
- **Password:** `Admin@12345`

*Or register a new test user via the web registration screen at `http://localhost:5180/register`.*

---

## 4. Running the Complete Verification Suite

### 4.1 Frontend Production Build Check
```powershell
npm --prefix frontend run build
```
Expected output: `✓ built in ~18s`, `0 errors`.

### 4.2 Full Backend Django Test Suite (45 Tests)
```powershell
backend\venv\Scripts\python.exe backend\manage.py test apps.accounts apps.profiles apps.predictions apps.intelligence
```
Expected output: `Ran 45 tests in ~100s. OK.`

### 4.3 Machine Learning Pipeline Tests (13 Tests)
```powershell
backend\venv\Scripts\python.exe -m pytest ml/tests/ -v
```
Expected output: `13 passed in ~33s.`

---

## 5. Key Frontend Routes

| Route | View Name | Description |
|:---|:---|:---|
| `/` | Landing Page | High-converting SaaS landing page with features and methodology |
| `/login` | Login | JWT authentication screen |
| `/register` | Register | User registration |
| `/dashboard` | Live Dashboard | Central operational dashboard with real metrics & widgets |
| `/salary-analysis` | Salary Valuation | Salary prediction form with quantile breakdown & SHAP link |
| `/explanations/:id` | Explainability | Interactive TreeSHAP waterfall and attribution analysis |
| `/skill-intelligence` | Skill Intelligence | Canonical skill taxonomy, co-occurrence, and marginal impact |
| `/what-if` | What-If Simulator | Counterfactual simulation lab comparing salary scenarios |
| `/role-matching` | Role Matching | Multi-dimensional skill match scores & missing skill gaps |
| `/roadmaps` | Career Roadmaps | Interactive multi-phase learning roadmaps with progress tracking |
| `/reports` | Saved Reports | Historical prediction catalog with search, filter, and detail modal |
| `/settings` | Settings | Profile attributes, appearance settings, and infrastructure status |

---

## 6. Troubleshooting

- **IPv4 vs IPv6 Binding on Windows:**
  When making automated HTTP requests or curl calls, use `http://127.0.0.1:8000/` instead of `localhost:8000` to avoid Windows IPv6 resolution latency.
- **Port Conflict on 5180:**
  If port 5180 is in use, terminate any lingering node processes:
  ```powershell
  Get-Process -Name node | Stop-Process -Force
  ```
- **Database Connection Error:**
  Ensure the Docker container is active:
  ```powershell
  docker ps -f name=worthiq_postgres
  ```
