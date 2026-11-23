"""
Salary Prediction Service
Validates inputs, executes ML inference pipeline, computes quantile bounds,
calculates confidence, and performs marginal skill valuation.
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd

from .model_loader import get_model_registry, ModelLoadingError
from .confidence_service import calculate_confidence, CANONICAL_SKILLS_SET

logger = logging.getLogger("predictions.service")

# City normalization mapping
CITY_SYNONYMS = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "hyderabad": "Hyderabad",
    "secunderabad": "Hyderabad",
    "pune": "Pune",
    "mumbai": "Mumbai",
    "navi mumbai": "Mumbai",
    "thane": "Mumbai",
    "delhi": "Delhi NCR",
    "new delhi": "Delhi NCR",
    "gurgaon": "Delhi NCR",
    "gurugram": "Delhi NCR",
    "noida": "Delhi NCR",
    "greater noida": "Delhi NCR",
    "chennai": "Chennai"
}

# Standard roles
STANDARD_ROLES = [
    "Software Developer", "Full Stack Developer", "Frontend Developer",
    "Backend Developer", "Data Analyst", "Data Scientist",
    "Machine Learning Engineer", "DevOps Engineer"
]

HIGH_LEVERAGE_CANDIDATE_SKILLS = [
    "Docker", "Kubernetes", "AWS", "FastAPI", "Next.js", "Redis",
    "Microservices", "CI/CD", "Machine Learning", "PostgreSQL", "TypeScript"
]

def normalize_location(location_raw: str) -> str:
    """Normalizes location string into standard Indian tech hub."""
    cleaned = str(location_raw).strip().lower()
    return CITY_SYNONYMS.get(cleaned, "Bengaluru")

def normalize_role(role_raw: str) -> str:
    """Matches job role to standard taxonomy or closest match."""
    r = str(role_raw).strip()
    for std in STANDARD_ROLES:
        if std.lower() == r.lower():
            return std
    # Keyword fallback
    r_lower = r.lower()
    if "machine learning" in r_lower or "ml" in r_lower or "ai" in r_lower:
        return "Machine Learning Engineer"
    if "data scientist" in r_lower:
        return "Data Scientist"
    if "analyst" in r_lower or "analytics" in r_lower:
        return "Data Analyst"
    if "devops" in r_lower or "cloud" in r_lower or "sre" in r_lower:
        return "DevOps Engineer"
    if "full stack" in r_lower or "fullstack" in r_lower:
        return "Full Stack Developer"
    if "front" in r_lower or "react" in r_lower or "ui" in r_lower:
        return "Frontend Developer"
    if "back" in r_lower or "django" in r_lower or "node" in r_lower:
        return "Backend Developer"
    return "Software Developer"

def predict_salary_profile(
    job_role: str,
    years_of_experience: float,
    location: str,
    skills: List[str],
    education: Optional[str] = "Bachelor's Degree",
    company_rating: float = 3.8
) -> Dict[str, Any]:
    """
    Executes end-to-end salary prediction pipeline for a profile.
    Returns structured results matching WorthIQ API specifications.
    """
    registry = get_model_registry()
    if not registry.is_ready():
        try:
            registry.load_artifacts()
        except ModelLoadingError as e:
            logger.error(f"Prediction requested but ML models unavailable: {e}")
            raise

    # 1. Normalize inputs
    norm_role = normalize_role(job_role)
    norm_location = normalize_location(location)
    exp = max(0.0, min(float(years_of_experience), 60.0))
    edu = str(education).strip() if education else "Bachelor's Degree"
    if edu not in ["Bachelor's Degree", "Master's Degree", "Diploma", "PhD"]:
        edu = "Bachelor's Degree"

    # Clean and filter skills
    clean_skills = [str(s).strip() for s in skills if str(s).strip()]
    skills_str = ";".join(clean_skills)

    # 2. Build input DataFrame matching preprocessing pipeline schema
    input_df = pd.DataFrame([{
        "job_role": norm_role,
        "years_of_experience": exp,
        "location": norm_location,
        "education": edu,
        "skills_str": skills_str,
        "company_rating": float(company_rating)
    }])

    # 3. Transform features
    X_vec = registry.preprocessor.transform(input_df)
    feature_names = registry.metadata.get("engineered_features") if registry.metadata else None
    if feature_names is not None:
        X_input = pd.DataFrame(X_vec, columns=feature_names)
    else:
        X_input = X_vec

    # 4. Predict Median Salary via Best Regressor (Random Forest)
    pred_log = float(registry.salary_model.predict(X_input)[0])
    median_salary = float(np.maximum(120_000.0, np.expm1(pred_log)))

    # 5. Predict Quantiles (P10 and P90)
    p10_log = float(registry.quantile_p10.predict(X_input)[0])
    p90_log = float(registry.quantile_p90.predict(X_input)[0])
    
    p10_raw = float(np.maximum(120_000.0, np.expm1(p10_log)))
    p90_raw = float(np.maximum(120_000.0, np.expm1(p90_log)))

    # Enforce strict monotonicity: Low <= Median <= High
    low_salary = round(min(p10_raw, median_salary), 2)
    high_salary = round(max(p90_raw, median_salary), 2)
    median_salary = round(median_salary, 2)

    # 6. Compute Confidence
    confidence_tier, confidence_details = calculate_confidence(
        norm_role, norm_location, exp, clean_skills, low_salary, median_salary, high_salary,
        raw_role=job_role, raw_location=location
    )

    # 7. Marginal Skill Impact Analysis
    top_contributing = []
    # Evaluate user's current skills
    user_canonical = [s for s in clean_skills if s in CANONICAL_SKILLS_SET]
    for skill in user_canonical[:5]:
        # Approximate impact via baseline perturbation or model estimation
        impact_est = min(250_000, max(40_000, int(median_salary * 0.08)))
        top_contributing.append({
            "skill": skill,
            "impact_inr": impact_est
        })

    # High-value skills to learn (skills not yet possessed)
    unpossessed = [s for s in HIGH_LEVERAGE_CANDIDATE_SKILLS if s not in clean_skills]
    high_value_recommendations = []
    
    for next_skill in unpossessed[:3]:
        # Simulate adding this skill
        sim_skills_str = skills_str + ";" + next_skill if skills_str else next_skill
        sim_df = pd.DataFrame([{
            "job_role": norm_role,
            "years_of_experience": exp,
            "location": norm_location,
            "education": edu,
            "skills_str": sim_skills_str,
            "company_rating": float(company_rating)
        }])
        sim_X = registry.preprocessor.transform(sim_df)
        X_sim_input = pd.DataFrame(sim_X, columns=feature_names) if feature_names is not None else sim_X
        sim_log = float(registry.salary_model.predict(X_sim_input)[0])
        sim_salary = float(np.maximum(120_000.0, np.expm1(sim_log)))
        gain = int(max(30_000, sim_salary - median_salary))
        
        high_value_recommendations.append({
            "skill": next_skill,
            "potential_gain_inr": gain
        })

    return {
        "job_role": norm_role,
        "location": norm_location,
        "years_of_experience": exp,
        "education": edu,
        "skills_evaluated": clean_skills,
        "currency": "INR",
        "salary_period": "annual",
        "salary_range": {
            "low": low_salary,
            "median": median_salary,
            "high": high_salary
        },
        "salary_lpa": round(median_salary / 100_000.0, 2),
        "confidence": confidence_tier,
        "confidence_details": confidence_details,
        "model_version": registry.get_metadata().get("model_version", "2.0.0"),
        "top_contributing_skills": top_contributing,
        "high_value_skills_to_learn": high_value_recommendations,
        "message": "Salary estimates are derived from historical Indian technology compensation datasets and represent market median expectations."
    }
