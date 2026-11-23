# WorthIQ Career Roadmap Methodology
## DAG Prerequisite Sequencing, Milestone Stages, Project Briefs, and Progress Tracking

---

## 1. Executive Summary

Acquiring technical skills randomly or without dependency awareness leads to learner fatigue and high abandonment rates. A frontend developer cannot effectively master Kubernetes without first learning Docker and Linux basics.

**WorthIQ Phase 3 Module D** introduces an automated Career Growth Roadmap engine:
1. **DAG Prerequisite Modeling**: Enforces non-circular dependency trees across 35 technology competencies.
2. **Three-Tier Milestone Progression**: Structures missing skills into:
   - **Stage 1: Core Foundations** (Immediate blocker skills)
   - **Stage 2: Core Specialization** (Role-specific tooling & frameworks)
   - **Stage 3: Advanced Architecture & Production Scale** (High-throughput & distributed systems)
3. **Capstone Project Synthesis**: Synthesizes a real-world software engineering capstone brief per stage to ground conceptual learning in tangible code.
4. **Interactive Progress Persistence**: Tracks granular skill completion in PostgreSQL and computes dynamic roadmap completion percentages.

---

## 2. Directed Acyclic Graph (DAG) Prerequisite Model

### 2.1 Dependency Hierarchy

The roadmap engine validates skills against an explicit Directed Acyclic Graph (DAG) ensuring no circular dependencies exist:

```
[Linux] ───────────────► [Docker] ───────────────► [Kubernetes]
   │                         │
   ▼                         ▼
[CI/CD]                  [Microservices]

[Python / Java / JS] ──► [REST APIs / Django] ──► [PostgreSQL / Redis] ──► [System Design]

[HTML5 / CSS3] ────────► [JavaScript / React.js] ─► [Next.js / TypeScript]
```

### 2.2 Dependency Resolution Algorithm

When a user selects a target role:
1. Target role skills (both mandatory and preferred) are extracted.
2. Candidate's existing skills are subtracted, leaving the set of missing competencies $G = \{g_1, g_2, \dots, g_m\}$.
3. Topological sorting is performed over $G$ using the prerequisite mapping:
   $$\text{Prereq}(g_i) \cap G \implies \text{scheduled in earlier stages than } g_i$$
4. Gaps are partitioned into three chronological stages:
   - **Stage 1 (Weeks 1–4)**: Foundational prerequisites (languages, VCS, basic APIs, fundamentals).
   - **Stage 2 (Weeks 5–8)**: Primary frameworks, databases, and core application development.
   - **Stage 3 (Weeks 9–14)**: Container orchestration, caching, cloud provisioning, and architectural patterns.

---

## 3. Real-World Capstone Project Briefs

Each generated stage includes an end-to-end practical project assignment to ensure skills are demonstrated in code:

| Stage Domain | Sample Project Title | Architectural Deliverables |
|:---|:---|:---|
| **Backend Foundations** | RESTful E-Commerce Micro-Service | Clean layered architecture, JWT authentication, PostgreSQL schema, Dockerfile containerization. |
| **Frontend Architecture** | Real-Time SaaS Dashboard | React.js / Next.js SPA, Tailwind CSS responsive design, WebSockets, state management, accessibility (a11y). |
| **DevOps & Cloud** | Multi-Tier GitOps Kubernetes Deployment | Terraform IaC, Dockerized microservice, Helm chart, CI/CD pipeline with automated testing and staging rollout. |
| **Data & AI Systems** | End-to-End MLOps Prediction API | Feature engineering pipeline, Scikit-learn / XGBoost training, FastAPI inference service, Dockerized deployment. |

---

## 4. PostgreSQL Relational Persistence Architecture

Roadmaps are stored with strict user-level isolation across three normalized models:

```
+--------------------+           +--------------------+           +------------------------+
|   CareerRoadmap    | 1       N |    RoadmapStage    | 1       N |  RoadmapSkillProgress  |
+--------------------+           +--------------------+           +------------------------+
| id (PK)            |───────────| id (PK)            |───────────| id (PK)                |
| user (FK)          |           | roadmap (FK)       |           | stage (FK)             |
| target_role (FK)   |           | stage_number (1..3)|           | skill (FK)             |
| overall_progress_pct           | title              |           | is_completed (Boolean) |
| current_skills     |           | objective          |           | completed_at (DateTime)|
| created_at         |           | project_suggestion |           | importance (Mandatory) |
+--------------------+           +--------------------+           +------------------------+
```

### 4.1 Granular Progress Calculation

When a user toggles a skill as completed (`PATCH /api/intelligence/roadmaps/{id}/progress/`):

$$\text{Progress} = \left( \frac{\sum_{i=1}^M \mathbb{I}(\text{skill}_i = \text{completed})}{M} \right) \times 100\%$$

- Updates `RoadmapSkillProgress.is_completed` and `completed_at`.
- Evaluates whether all skills in the stage are now completed; if so, sets `RoadmapStage.is_completed = True`.
- Updates `CareerRoadmap.overall_progress_pct` atomically in PostgreSQL.

---

## 5. Frontend Interactive Roadmap Experience

In `frontend/src/pages/CareerRoadmapPage.jsx`:
- **Interactive Checkboxes**: Users click checkboxes to toggle skill mastery in real time.
- **Stage Progression Visualizer**: Shows completed stages, in-progress stages, and locked future stages.
- **Project Brief Accordions**: Expandable project specs detailing deliverables and recommended tech stack.
- **Role Switching**: Users can generate and manage multiple roadmaps across different aspirational roles.
