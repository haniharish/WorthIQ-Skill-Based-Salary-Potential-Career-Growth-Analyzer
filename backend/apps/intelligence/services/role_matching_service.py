"""
Job Role Matching Service
Computes multi-dimensional matching scores between candidate skill profiles
and the curated technology role catalog using TF-IDF, Cosine Similarity,
and empirical experience-tenure compatibility.
"""

from decimal import Decimal
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.intelligence.models import JobRole, RoleSkillRequirement, CanonicalSkill
from apps.intelligence.services.skill_normalization_service import normalize_skill, normalize_skill_list

DEFAULT_ROLES_DATA = [
    {
        "title": "Full Stack Developer",
        "description": "Architects, develops, and maintains end-to-end web applications across reactive frontend interfaces, scalable backend APIs, and relational/document databases.",
        "min_exp": 1.0,
        "max_exp": 12.0,
        "median_salary": 720000.0,
        "p10_salary": 380000.0,
        "p90_salary": 1800000.0,
        "required_skills": ["JavaScript", "React.js", "Node.js", "SQL", "Git"],
        "preferred_skills": ["TypeScript", "Docker", "PostgreSQL", "REST APIs", "Next.js", "Tailwind CSS"]
    },
    {
        "title": "Backend Developer",
        "description": "Designs robust distributed microservices, RESTful and GraphQL APIs, database schemas, and caching layers prioritizing high concurrency, security, and low latency.",
        "min_exp": 1.0,
        "max_exp": 15.0,
        "median_salary": 750000.0,
        "p10_salary": 400000.0,
        "p90_salary": 1950000.0,
        "required_skills": ["Python", "PostgreSQL", "REST APIs", "Git", "SQL"],
        "preferred_skills": ["Django", "FastAPI", "Docker", "Redis", "Microservices", "Kubernetes", "Linux"]
    },
    {
        "title": "Frontend Developer",
        "description": "Crafts accessible, high-performance web user interfaces, component systems, state management flows, and responsive client experiences.",
        "min_exp": 0.5,
        "max_exp": 10.0,
        "median_salary": 650000.0,
        "p10_salary": 350000.0,
        "p90_salary": 1600000.0,
        "required_skills": ["JavaScript", "React.js", "HTML5", "CSS3", "Git"],
        "preferred_skills": ["TypeScript", "Next.js", "Tailwind CSS", "REST APIs", "Flutter"]
    },
    {
        "title": "DevOps Engineer",
        "description": "Automates software delivery pipelines, manages Kubernetes clusters, provisions infrastructure as code, and guarantees 99.99% system reliability.",
        "min_exp": 2.0,
        "max_exp": 15.0,
        "median_salary": 850000.0,
        "p10_salary": 450000.0,
        "p90_salary": 2200000.0,
        "required_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "Git"],
        "preferred_skills": ["AWS", "Python", "Go", "Microservices", "Redis"]
    },
    {
        "title": "Data Scientist",
        "description": "Develops predictive machine learning models, discovers statistical insights from complex data, and deploys intelligence pipelines into production.",
        "min_exp": 1.5,
        "max_exp": 12.0,
        "median_salary": 800000.0,
        "p10_salary": 420000.0,
        "p90_salary": 2100000.0,
        "required_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL"],
        "preferred_skills": ["Scikit-learn", "Data Analysis", "Docker", "FastAPI", "PostgreSQL"]
    },
    {
        "title": "Machine Learning Engineer",
        "description": "Bridges the gap between data science and software engineering by scaling, containerizing, optimizing, and deploying deep learning and ML systems.",
        "min_exp": 2.0,
        "max_exp": 14.0,
        "median_salary": 900000.0,
        "p10_salary": 480000.0,
        "p90_salary": 2400000.0,
        "required_skills": ["Python", "Machine Learning", "Scikit-learn", "Docker", "Pandas"],
        "preferred_skills": ["Kubernetes", "FastAPI", "REST APIs", "AWS", "Linux", "SQL"]
    },
    {
        "title": "Data Analyst",
        "description": "Transforms business data into actionable dashboards, KPIs, and reports using advanced SQL queries, data wrangling, and statistical storytelling.",
        "min_exp": 0.5,
        "max_exp": 8.0,
        "median_salary": 550000.0,
        "p10_salary": 320000.0,
        "p90_salary": 1350000.0,
        "required_skills": ["SQL", "Data Analysis", "Pandas", "Python"],
        "preferred_skills": ["NumPy", "PostgreSQL", "Git"]
    },
    {
        "title": "Software Developer",
        "description": "Builds, tests, and deploys core software modules, object-oriented applications, and services adhering to clean architecture and design patterns.",
        "min_exp": 0.0,
        "max_exp": 12.0,
        "median_salary": 600000.0,
        "p10_salary": 300000.0,
        "p90_salary": 1600000.0,
        "required_skills": ["Java", "SQL", "Git", "REST APIs"],
        "preferred_skills": ["Spring Boot", "Docker", "Linux", "PostgreSQL", "Microservices", "C++"]
    },
    {
        "title": "Cloud Engineer",
        "description": "Architects, secures, and operates cloud computing environments, VPC networking, serverless infrastructure, and high-availability storage.",
        "min_exp": 2.0,
        "max_exp": 14.0,
        "median_salary": 820000.0,
        "p10_salary": 440000.0,
        "p90_salary": 2150000.0,
        "required_skills": ["AWS", "Linux", "Docker", "Kubernetes", "CI/CD"],
        "preferred_skills": ["Python", "Go", "Microservices", "Git", "Redis"]
    }
]

def seed_roles_in_db():
    """Seeds JobRole and RoleSkillRequirement records into the database."""
    roles_created = 0
    for r_data in DEFAULT_ROLES_DATA:
        role_obj, created = JobRole.objects.get_or_create(
            title=r_data["title"],
            defaults={
                "description": r_data["description"],
                "min_exp": Decimal(str(r_data["min_exp"])),
                "max_exp": Decimal(str(r_data["max_exp"])),
                "median_salary": Decimal(str(r_data["median_salary"])),
                "p10_salary": Decimal(str(r_data["p10_salary"])),
                "p90_salary": Decimal(str(r_data["p90_salary"])),
                "dataset_coverage_count": 2800
            }
        )
        if created:
            roles_created += 1

        # Link required skills
        for s_name in r_data["required_skills"]:
            skill_obj = CanonicalSkill.objects.filter(name=s_name).first()
            if skill_obj:
                RoleSkillRequirement.objects.get_or_create(
                    role=role_obj,
                    skill=skill_obj,
                    defaults={"is_mandatory": True, "importance_weight": 1.2}
                )

        # Link preferred skills
        for s_name in r_data["preferred_skills"]:
            skill_obj = CanonicalSkill.objects.filter(name=s_name).first()
            if skill_obj:
                RoleSkillRequirement.objects.get_or_create(
                    role=role_obj,
                    skill=skill_obj,
                    defaults={"is_mandatory": False, "importance_weight": 0.8}
                )

    return roles_created


def match_candidate_roles(candidate_skills, experience=0.0):
    """
    Ranks technology roles against candidate's skills and experience tenure.

    Parameters:
        candidate_skills (list): Raw or canonical skills list.
        experience (float): Years of professional experience.

    Returns:
        list of role match dicts sorted by match_score descending.
    """
    norm_candidate = set(s.lower() for s in normalize_skill_list(candidate_skills))
    candidate_skills_text = " ".join(norm_candidate)

    # 1. Fetch all roles (from DB or fallback to defaults)
    roles = list(JobRole.objects.prefetch_related('skill_requirements__skill').all())
    if not roles:
        # If DB not yet migrated or empty, use DEFAULT_ROLES_DATA
        role_dicts = DEFAULT_ROLES_DATA
    else:
        role_dicts = []
        for r in roles:
            reqs = [sr.skill.name for sr in r.skill_requirements.filter(is_mandatory=True)]
            prefs = [sr.skill.name for sr in r.skill_requirements.filter(is_mandatory=False)]
            role_dicts.append({
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "min_exp": float(r.min_exp),
                "max_exp": float(r.max_exp),
                "median_salary": float(r.median_salary),
                "p10_salary": float(r.p10_salary),
                "p90_salary": float(r.p90_salary),
                "required_skills": reqs,
                "preferred_skills": prefs
            })

    # Prepare corpus for TF-IDF Cosine Similarity
    all_role_texts = [
        " ".join([s.lower() for s in (rd["required_skills"] + rd["preferred_skills"])])
        for rd in role_dicts
    ]
    corpus = [candidate_skills_text] + all_role_texts

    try:
        tfidf = TfidfVectorizer().fit_transform(corpus)
        user_vec = tfidf[0:1]
        cosine_sims = cosine_similarity(user_vec, tfidf[1:]).flatten()
    except Exception:
        cosine_sims = [0.0] * len(role_dicts)

    results = []
    exp_f = float(experience)

    for idx, rd in enumerate(role_dicts):
        req_set = set(s.lower() for s in rd["required_skills"])
        pref_set = set(s.lower() for s in rd["preferred_skills"])

        matched_req = [s for s in rd["required_skills"] if s.lower() in norm_candidate]
        missing_req = [s for s in rd["required_skills"] if s.lower() not in norm_candidate]

        matched_pref = [s for s in rd["preferred_skills"] if s.lower() in norm_candidate]
        missing_pref = [s for s in rd["preferred_skills"] if s.lower() not in norm_candidate]

        all_matched = matched_req + matched_pref

        # Metric 1: Required Skills Overlap (0.0 to 1.0)
        s_req = len(matched_req) / max(1, len(req_set))

        # Metric 2: Preferred Skills Overlap (0.0 to 1.0)
        s_pref = len(matched_pref) / max(1, len(pref_set))

        # Metric 3: TF-IDF Cosine Similarity (0.0 to 1.0)
        s_cos = float(cosine_sims[idx]) if idx < len(cosine_sims) else 0.0

        # Metric 4: Experience Compatibility (0.0 to 1.0)
        min_e = rd["min_exp"]
        max_e = rd["max_exp"]
        if min_e <= exp_f <= max_e:
            s_exp = 1.0
        elif exp_f < min_e:
            s_exp = max(0.2, 1.0 - 0.25 * (min_e - exp_f))
        else:
            s_exp = max(0.5, 1.0 - 0.08 * (exp_f - max_e))

        # Weighted composite score on 0-100 scale
        composite = (0.40 * s_req + 0.15 * s_pref + 0.25 * s_cos + 0.20 * s_exp) * 100.0
        match_score = round(min(100.0, max(0.0, composite)), 1)

        # Categorize match tier
        if match_score >= 80.0:
            category = "Strong Match"
            cat_badge = "emerald"
        elif match_score >= 65.0:
            category = "Good Match"
            cat_badge = "indigo"
        elif match_score >= 50.0:
            category = "Moderate Match"
            cat_badge = "sky"
        else:
            category = "Low Match"
            cat_badge = "amber"

        results.append({
            "id": rd.get("id"),
            "title": rd["title"],
            "description": rd["description"],
            "match_score": match_score,
            "match_category": category,
            "badge_color": cat_badge,
            "matched_skills": all_matched,
            "matched_required_skills": matched_req,
            "missing_required_skills": missing_req,
            "missing_preferred_skills": missing_pref,
            "required_coverage_pct": round(s_req * 100, 1),
            "experience_compatibility_pct": round(s_exp * 100, 1),
            "median_salary_inr": rd["median_salary"],
            "median_salary_lpa": round(rd["median_salary"] / 100000.0, 2),
            "p10_salary_lpa": round(rd["p10_salary"] / 100000.0, 2),
            "p90_salary_lpa": round(rd["p90_salary"] / 100000.0, 2),
            "min_exp": min_e,
            "max_exp": max_e,
            "factors": {
                "required_skills_weight": "40%",
                "preferred_skills_weight": "15%",
                "text_similarity_weight": "25%",
                "experience_fit_weight": "20%"
            }
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
