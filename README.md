# WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer

> **Final-Year B.Tech Project** &middot; **Phase 1: Foundation Implementation**

WorthIQ is a full-stack, data-driven web application designed to help students, freshers, and working professionals understand their estimated market salary, analyze the valuation and ROI of their skill stack, discover matching roles, and plan their career trajectory.

---

## 1. Project Overview

WorthIQ is being engineered across six strategic development phases:

1. **Phase 1: Foundation** *(Current Phase — Fully Implemented)*:
   - Full-stack project structure, React + Vite frontend, Tailwind CSS design system.
   - Django REST Framework backend with custom user authentication.
   - SimpleJWT authentication with refresh token blacklisting and token rotation.
   - Normalized PostgreSQL database containerized via Docker on port `5432`.
   - Complete User Profile & Skills management endpoints with full frontend integration.
   - DBeaver visual database administration setup.
2. **Phase 2**: Salary Potential Prediction Engine (Supervised Regression, XGBoost, Random Forest).
3. **Phase 3**: Skill Impact & Valuation Analysis (Marginal skill attribution, SHAP explainability).
4. **Phase 4**: Job Role Matching & Gap Analysis (TF-IDF & Cosine Similarity).
5. **Phase 5**: Dynamic Career Growth Roadmap (Sequential DAG learning paths).
6. **Phase 6**: What-If Salary Simulation Lab (Real-time interactive career sandboxing).

---

## 2. Technology Stack

### Frontend
- **Framework**: React 18
- **Build Tool / Bundler**: Vite 6 (Configured strictly on port **5180**)
- **Language**: JavaScript (ES Modules)
- **Styling**: Tailwind CSS v4 (SaaS theme, light-mode first)
- **Routing**: React Router DOM v6
- **HTTP Client**: Axios with automatic JWT interceptors & token rotation
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.14 & Django 5.2
- **API Engine**: Django REST Framework (DRF) 3.18
- **Authentication**: DRF SimpleJWT with token blacklist support
- **CORS Handling**: `django-cors-headers` (allowing `http://localhost:5180`)
- **Database Driver**: `psycopg` 3.3 (PostgreSQL adapter)
- **Configuration**: `python-dotenv`

### Database
- **Database**: PostgreSQL 16 Alpine
- **Containerization**: Docker & Docker Compose (Port **5432**)
- **Storage**: Named Docker volume `worthiq_pgdata` for persistent data storage
- **GUI Management**: DBeaver Community Edition

---

## 3. Fixed Port Configuration

| Service | Technology | Port | Access URL | Strict Port |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | React + Vite | `5180` | `http://localhost:5180` | `strictPort: true` |
| **Backend** | Django + DRF | `8000` | `http://localhost:8000` | Host: `0.0.0.0:8000` |
| **Database** | PostgreSQL Docker | `5432` | `localhost:5432` | Mapped from container |

---

## 4. Project Folder Structure

```text
WorthIQ/
│
├── frontend/                     # React + Vite application
│   ├── public/                   # Static assets & favicon
│   ├── src/
│   │   ├── assets/               # Local icons and branding
│   │   ├── components/
│   │   │   ├── common/           # Logo, ProtectedRoute, PublicRoute
│   │   │   ├── layout/           # DashboardLayout, Navbar
│   │   │   └── ui/               # Button, Input, Card, Badge
│   │   ├── context/              # AuthContext (state & session management)
│   │   ├── hooks/                # useAuth hook
│   │   ├── pages/                # Landing, Login, Register, ProfileSetup, Dashboard, FeaturePlaceholders
│   │   ├── services/             # Axios API client, authService, profileService
│   │   ├── utils/                # Helper utilities
│   │   ├── App.jsx               # Route definitions
│   │   ├── main.jsx              # React DOM entry point
│   │   └── index.css             # Tailwind CSS & typography
│   ├── vite.config.js            # Port 5180 & strictPort configuration
│   ├── package.json              # Frontend dependencies
│   ├── .env                      # Local environment configuration
│   └── .env.example              # Safe placeholder template
│
├── backend/                      # Django REST Framework application
│   ├── config/                   # Project settings, root URLs, WSGI, ASGI
│   │   ├── settings.py           # CORS, JWT, PostgreSQL settings
│   │   └── urls.py               # Main routing table
│   ├── apps/
│   │   ├── accounts/             # Custom User model, JWT views, serializers
│   │   │   ├── models.py         # Email-based User model
│   │   │   ├── serializers.py    # Registration, Login, User details
│   │   │   ├── views.py          # Auth endpoints
│   │   │   ├── urls.py           # /api/auth/ routes
│   │   │   └── tests.py          # Auth unit tests (8 tests)
│   │   └── profiles/             # User Profile & normalized Skills
│   │       ├── models.py         # UserProfile & Skill models (M2M)
│   │       ├── serializers.py    # Profile serializers with skill syncing
│   │       ├── views.py          # Profile CRUD & Skills catalog
│   │       ├── urls.py           # /api/profile/ routes
│   │       └── tests.py          # Profile unit tests (8 tests)
│   ├── manage.py
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Local environment configuration
│   └── .env.example              # Safe placeholder template
│
├── database/                     # Docker PostgreSQL orchestration
│   ├── docker-compose.yml        # PostgreSQL 16 container definition & healthcheck
│   ├── .env                      # Database credentials
│   └── .env.example              # Safe placeholder template
│
├── docs/                         # Detailed documentation
│   ├── API_DOCUMENTATION.md      # Full REST endpoint schemas
│   └── DBEAVER_SETUP.md          # Visual DB configuration guide
│
├── test_complete_integration.py  # 12-step end-to-end integration test runner
├── .gitignore
├── README.md
└── PHASE_1_REPORT.md
```

---

## 5. Prerequisites

Before running the application, ensure the following are installed on your Windows machine:

1. **Docker Desktop**:
   - Download & install: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Ensure WSL 2 backend is enabled.
2. **Python**: Python 3.11+ (Python 3.14 verified).
3. **Node.js**: Node 18+ (v22.13 verified) with `npm`.
4. **DBeaver** (Optional for visual DB inspection): [https://dbeaver.io/download/](https://dbeaver.io/download/)

---

## 6. Getting Started — Step-by-Step Instructions

Execute the following commands in **Windows PowerShell**:

### Step 1: Start PostgreSQL via Docker

```powershell
cd C:\Users\Lenovo\Desktop\WorthIQ\database
docker compose up -d
docker compose ps
```
*Expected status: `worthiq_postgres` container is `Up (healthy)` on port `0.0.0.0:5432`.*

---

### Step 2: Configure and Start Django Backend

In a PowerShell terminal:

```powershell
cd C:\Users\Lenovo\Desktop\WorthIQ\backend

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run database migrations
python manage.py migrate

# (Optional) Run automated test suite (16 tests)
python manage.py test

# Start the Django development server on port 8000
python manage.py runserver 0.0.0.0:8000
```
*Backend is accessible at: `http://localhost:8000/`*

---

### Step 3: Configure and Start React Frontend

In a second PowerShell terminal:

```powershell
cd C:\Users\Lenovo\Desktop\WorthIQ\frontend

# Start Vite dev server on strict port 5180
npm run dev
```
*Frontend is accessible at: `http://localhost:5180/`*

---

## 7. Connecting DBeaver to PostgreSQL

1. Open **DBeaver**.
2. Click **Database** &rarr; **New Database Connection** &rarr; select **PostgreSQL**.
3. Enter connection parameters:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `worthiq_db`
   - **Username**: `worthiq_user`
   - **Password**: `worthiq_password`
4. Click **Test Connection ...** to confirm, then click **Finish**.
5. Detailed guidance on viewing tables, querying records, and inspecting relationships is provided in [`docs/DBEAVER_SETUP.md`](file:///c:/Users/Lenovo/Desktop/WorthIQ/docs/DBEAVER_SETUP.md).

---

## 8. Automated Integration Testing

To run the automated 12-suite end-to-end integration test against live running services:

```powershell
cd C:\Users\Lenovo\Desktop\WorthIQ
.\backend\venv\Scripts\python.exe test_complete_integration.py
```

This script verifies:
1. Frontend HTTP response on port 5180 (Status 200).
2. User Registration (`POST /api/auth/register/`).
3. User Authentication (`POST /api/auth/login/`).
4. Authenticated identity check (`GET /api/auth/me/`).
5. Profile 404 detection for unconfigured profiles.
6. Profile creation with normalized M2M skills (`POST /api/profile/`).
7. Profile retrieval (`GET /api/profile/`).
8. Profile partial update (`PATCH /api/profile/`).
9. JWT token refresh & rotation (`POST /api/auth/token/refresh/`).
10. Logout and refresh token blacklisting (`POST /api/auth/logout/`).
11. Rejection of blacklisted refresh tokens (Status 401).
12. Denial of unauthorized access to protected routes (Status 401).

---

## 9. API Endpoints Overview

Full schemas are documented in [`docs/API_DOCUMENTATION.md`](file:///c:/Users/Lenovo/Desktop/WorthIQ/docs/API_DOCUMENTATION.md).

| Method | Endpoint | Description | Permissions |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register new user account | AllowAny |
| `POST` | `/api/auth/login/` | Authenticate user & return JWT tokens | AllowAny |
| `POST` | `/api/auth/token/refresh/` | Refresh expired access token | AllowAny |
| `POST` | `/api/auth/logout/` | Blacklist refresh token & terminate session | IsAuthenticated |
| `GET` | `/api/auth/me/` | Retrieve current user profile status | IsAuthenticated |
| `GET` | `/api/profile/` | Retrieve logged-in user's profile & skills | IsAuthenticated |
| `POST` | `/api/profile/` | Create profile with skills array | IsAuthenticated |
| `PUT` | `/api/profile/` | Full update of profile | IsAuthenticated |
| `PATCH` | `/api/profile/` | Partial update of profile | IsAuthenticated |
| `GET` | `/api/profile/skills/` | Search and retrieve skills catalog | AllowAny |

---

## 10. Phase 1 Verification Checklist

- [x] React + Vite configured strictly on port `5180`.
- [x] Django REST Framework configured on port `8000`.
- [x] PostgreSQL 16 running inside Docker container on port `5432`.
- [x] Named persistent volume `worthiq_pgdata` preserves database records across container restarts.
- [x] DBeaver connection enabled and verified on `localhost:5432`.
- [x] Custom User model using email as unique identifier.
- [x] User Profile and Skill models with normalized Many-to-Many relationship.
- [x] Real JWT authentication with rotation and token blacklisting.
- [x] Axios client configured with automatic token refresh interceptor.
- [x] Responsive SaaS dashboard with KPI cards, salary distribution charts, skill matrix, and role compatibility.
- [x] 16 Django backend unit tests passing (100%).
- [x] 12 end-to-end integration tests passing (100%).
- [x] Production build (`npm run build`) passing with zero errors.
