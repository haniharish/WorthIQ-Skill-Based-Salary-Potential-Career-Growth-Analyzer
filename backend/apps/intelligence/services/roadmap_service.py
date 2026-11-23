"""
Career Growth Roadmap Service
Generates structured milestone learning stages, DAG skill sequences,
and practical real-world project recommendations tailored to target roles.
"""

from decimal import Decimal
from django.utils import timezone
from apps.intelligence.models import (
    CareerRoadmap,
    RoadmapStage,
    RoadmapSkillProgress,
    JobRole
)
from apps.intelligence.services.skill_gap_service import (
    analyze_skill_gap,
    SKILL_DEPENDENCY_GRAPH
)
from apps.intelligence.services.skill_normalization_service import (
    normalize_skill_list,
    SKILL_TAXONOMY
)

STAGE_PROJECT_CATALOG = {
    "Full Stack Developer": [
        {
            "stage": 1,
            "title": "Foundational Component Design & Clean Code",
            "objective": "Build solid fundamentals in modern JavaScript, HTML5 semantic structures, and Git branching workflows.",
            "project": {
                "title": "Interactive Task & Sprint Management Dashboard",
                "stack": "HTML5, CSS3/Tailwind, Modern JavaScript (ES6+), Git",
                "deliverables": "Responsive kanban board with drag-and-drop, persistent local storage, and structured git commits.",
                "completion_criteria": "Fully responsive on mobile/desktop, zero console warnings, passing linting rules."
            }
        },
        {
            "stage": 2,
            "title": "Frontend State Management & Component Ecosystem",
            "objective": "Master React.js declarative component design, hooks, custom state, and API consumption.",
            "project": {
                "title": "Multi-Tenant E-Commerce Product Catalog with Cart",
                "stack": "React.js, Tailwind CSS, REST APIs, Context/Redux",
                "deliverables": "Catalog with live search, category filtering, cart state persistence, and responsive checkout UI.",
                "completion_criteria": "Fast render performance, reusable design system components, clean error boundaries."
            }
        },
        {
            "stage": 3,
            "title": "Backend Services, Relational Schemas & Auth",
            "objective": "Design robust Node.js/Express.js backend services, PostgreSQL relational tables, and JWT authentication.",
            "project": {
                "title": "RESTful SaaS Backend with PostgreSQL & JWT",
                "stack": "Node.js, Express.js, PostgreSQL, SQL, JWT",
                "deliverables": "Secure user signup/login with bcrypt, protected CRUD resources, transactional DB migrations.",
                "completion_criteria": "All endpoints documented, parameterized SQL queries preventing injection, >85% test coverage."
            }
        },
        {
            "stage": 4,
            "title": "Full-Stack Integration, Containers & Production Deployment",
            "objective": "Dockerize the full-stack system, configure Docker Compose, and deploy with CI/CD automation.",
            "project": {
                "title": "Containerized Full-Stack Enterprise Portal",
                "stack": "React.js, Node.js, PostgreSQL, Docker, CI/CD, AWS",
                "deliverables": "Multi-container Docker Compose setup, GitHub Actions automated build pipeline, live cloud deployment.",
                "completion_criteria": "Single-command local bringup (docker compose up), automated tests passing on PRs."
            }
        }
    ],
    "Backend Developer": [
        {
            "stage": 1,
            "title": "Core Backend Languages, Data Structures & Git",
            "objective": "Master server-side Python/Java fundamentals, data structures, and algorithmic complexity.",
            "project": {
                "title": "High-Throughput File Processing & Log Analytics Utility",
                "stack": "Python, Linux, Git",
                "deliverables": "CLI tool parsing multi-gigabyte server logs, extracting error metrics, and exporting structured CSV.",
                "completion_criteria": "Memory-efficient streaming, proper exception hierarchies, modular unit tests."
            }
        },
        {
            "stage": 2,
            "title": "RESTful Architecture, Frameworks & Relational Modeling",
            "objective": "Design clean API contracts with Django/FastAPI and normalize PostgreSQL databases.",
            "project": {
                "title": "Multi-Role Banking & Wallet Transaction API",
                "stack": "Django / FastAPI, PostgreSQL, REST APIs",
                "deliverables": "ACID compliant ledger, atomic transactions, OpenAPI/Swagger interactive docs, JWT token auth.",
                "completion_criteria": "Zero race conditions under concurrent requests, verified via database lock tests."
            }
        },
        {
            "stage": 3,
            "title": "Caching, Asynchronous Queues & Microservices",
            "objective": "Implement distributed Redis caching, message brokers, and service boundaries.",
            "project": {
                "title": "Real-Time Event Streamer & Cache-Aside Service",
                "stack": "FastAPI/Django, Redis, Docker, Microservices",
                "deliverables": "Sub-millisecond cached lookups, rate limiting middleware, pub/sub notification workers.",
                "completion_criteria": "P99 latency < 15ms under 500 RPS load test using Locust."
            }
        },
        {
            "stage": 4,
            "title": "Production Deployment, Containerization & Orchestration",
            "objective": "Deploy backend microservices onto Docker, configure Kubernetes pods, and set up CI/CD.",
            "project": {
                "title": "Production Kubernetes Microservices Cluster",
                "stack": "Docker, Kubernetes, CI/CD, AWS, Linux",
                "deliverables": "Multi-replica deployment with health probes, ingress routing, secret management, automated rollouts.",
                "completion_criteria": "Zero-downtime rolling updates verified during simulated traffic spikes."
            }
        }
    ],
    "DevOps Engineer": [
        {
            "stage": 1,
            "title": "Linux Systems Administration & Shell Scripting",
            "objective": "Deep-dive into Linux permissions, processes, networking (TCP/IP, DNS), and automated shell workflows.",
            "project": {
                "title": "Automated Linux Server Provisioner & Hardener",
                "stack": "Linux (Ubuntu), Bash, Git, SSH",
                "deliverables": "Idempotent script configuring firewalls, rotating logs, creating isolated users, and auditing ports.",
                "completion_criteria": "Passes Lynis security audit benchmark with a hardened score."
            }
        },
        {
            "stage": 2,
            "title": "Containerization & Multi-Stage Builds",
            "objective": "Master Docker container internals, layer caching, security scanning, and Compose networks.",
            "project": {
                "title": "Optimized Multi-Service Container Architecture",
                "stack": "Docker, Docker Compose, Linux",
                "deliverables": "Minimal alpine/distroless images (<50MB), non-root execution, multi-stage compilation.",
                "completion_criteria": "Zero critical CVE vulnerabilities detected by Docker Scout / Trivy."
            }
        },
        {
            "stage": 3,
            "title": "Continuous Integration & Deployment Pipelines",
            "objective": "Construct declarative CI/CD pipelines automating linting, testing, image building, and staging deploys.",
            "project": {
                "title": "Enterprise GitOps CI/CD Deployment Pipeline",
                "stack": "GitHub Actions / GitLab CI, Docker, Linux",
                "deliverables": "Matrix unit test runs, semantic versioning, container registry publishing, automated staging push.",
                "completion_criteria": "End-to-end pipeline executes in <4 minutes with automated slack notification hooks."
            }
        },
        {
            "stage": 4,
            "title": "Kubernetes Orchestration & Cloud Infrastructure",
            "objective": "Manage production workloads with Kubernetes, Helm charts, and AWS cloud resources.",
            "project": {
                "title": "High-Availability Kubernetes Cluster with Monitoring",
                "stack": "Kubernetes, AWS, Helm, Docker, Linux",
                "deliverables": "Deployments with Horizontal Pod Autoscalers (HPA), persistent volumes, Prometheus/Grafana monitors.",
                "completion_criteria": "Demonstrated auto-scaling from 2 to 10 pods under synthetic stress test."
            }
        }
    ],
    "Data Scientist": [
        {
            "stage": 1,
            "title": "Python Scientific Foundations & Statistical Analysis",
            "objective": "Master Pandas, NumPy, and exploratory data analysis (EDA) techniques.",
            "project": {
                "title": "Comprehensive Exploratory Data Analysis & Hypothesis Testing",
                "stack": "Python, Pandas, NumPy, Matplotlib",
                "deliverables": "Jupyter analysis notebook cleaning raw dirty data, testing parametric hypotheses, visualizing distributions.",
                "completion_criteria": "Zero missing values unaddressed, documented statistical p-values and correlations."
            }
        },
        {
            "stage": 2,
            "title": "Supervised & Unsupervised Machine Learning",
            "objective": "Implement regression, classification, clustering, and cross-validation pipelines with Scikit-learn.",
            "project": {
                "title": "End-to-End Predictive Machine Learning Pipeline",
                "stack": "Python, Scikit-learn, Pandas, NumPy",
                "deliverables": "Feature scaling, hyperparameter tuning via GridSearchCV, model evaluation (ROC-AUC, F1, MAE).",
                "completion_criteria": "No data leakage across folds, validated against stratified test baseline."
            }
        },
        {
            "stage": 3,
            "title": "Model Serving, APIs & Containerization",
            "objective": "Serve machine learning models as high-speed RESTful microservices packaged in Docker.",
            "project": {
                "title": "Production ML Inference API with FastAPI & Docker",
                "stack": "FastAPI, Docker, Scikit-learn, Python",
                "deliverables": "Asynchronous REST endpoint receiving feature payloads, validating schemas via Pydantic, returning predictions.",
                "completion_criteria": "P95 response latency < 35ms, fully dockerized container."
            }
        }
    ]
}

def generate_roadmap_for_user(user, target_role_id, current_role=None, current_experience=None, current_skills=None):
    """
    Generates and persists a personalized CareerRoadmap instance.
    """
    target_role = JobRole.objects.filter(id=target_role_id).first()
    if not target_role:
        # Fallback to first role
        target_role = JobRole.objects.first()

    # Prefill from user profile if not passed
    profile = getattr(user, 'profile', None)
    if current_role is None and profile:
        current_role = profile.job_role or "Software Engineer"
    elif current_role is None:
        current_role = "Software Engineer"

    if current_experience is None and profile:
        current_experience = float(profile.years_of_experience)
    elif current_experience is None:
        current_experience = 2.0

    if current_skills is None and profile:
        raw_s = profile.skills.all()
        current_skills = [s.name for s in raw_s]
    elif current_skills is None:
        current_skills = []

    norm_skills = normalize_skill_list(current_skills)

    # 1. Compute gap
    gap = analyze_skill_gap(norm_skills, target_role.id)

    # 2. Create CareerRoadmap
    roadmap = CareerRoadmap.objects.create(
        user=user,
        target_role=target_role,
        current_role=current_role,
        current_experience=Decimal(str(current_experience)),
        current_skills=norm_skills,
        title=f"Path to {target_role.title}",
        overall_progress_pct=0,
        is_saved=True
    )

    # 3. Create Stages
    template_stages = STAGE_PROJECT_CATALOG.get(target_role.title, STAGE_PROJECT_CATALOG["Full Stack Developer"])

    missing_req = list(gap["missing_required"])
    missing_pref = list(gap["missing_preferred"])

    total_stages = len(template_stages)
    for idx, t_stage in enumerate(template_stages):
        stage_num = idx + 1
        
        stage_obj = RoadmapStage.objects.create(
            roadmap=roadmap,
            stage_number=stage_num,
            title=t_stage["title"],
            objective=t_stage["objective"],
            prerequisites=f"Stage {stage_num - 1}" if stage_num > 1 else "None",
            project_suggestion=t_stage["project"],
            is_completed=False
        )

        # Distribute missing skills across stages
        stage_skills = []
        if stage_num == 1:
            # Stage 1: Fundamentals
            stage_skills = [s for s in missing_req if s in ["HTML5", "CSS3", "JavaScript", "Python", "Java", "SQL", "Git", "Linux"]]
        elif stage_num == 2:
            # Stage 2: Frameworks & Stores
            stage_skills = [s for s in missing_req if s in ["React.js", "Django", "FastAPI", "Node.js", "Spring Boot", "PostgreSQL", "REST APIs", "Pandas", "NumPy"]]
        elif stage_num == 3:
            # Stage 3: Architecture & Systems
            stage_skills = [s for s in (missing_req + missing_pref) if s in ["Docker", "Redis", "Microservices", "Scikit-learn", "Machine Learning", "GraphQL", "Tailwind CSS"]]
        else:
            # Stage 4+: Cloud, Orchestration, Production
            stage_skills = [s for s in (missing_req + missing_pref) if s in ["Kubernetes", "AWS", "CI/CD", "Next.js", "TypeScript", "Data Analysis", "Go"]]

        # If empty, assign remaining
        if not stage_skills and (missing_req or missing_pref):
            if missing_req:
                stage_skills = [missing_req.pop(0)]
            elif missing_pref:
                stage_skills = [missing_pref.pop(0)]

        for s_name in stage_skills:
            tax = SKILL_TAXONOMY.get(s_name, {})
            RoadmapSkillProgress.objects.create(
                stage=stage_obj,
                skill_name=s_name,
                category=tax.get("category", "Technical Skill"),
                importance="Mandatory" if s_name in gap["missing_required"] else "Preferred",
                is_completed=False
            )

    roadmap.update_progress()
    return roadmap
