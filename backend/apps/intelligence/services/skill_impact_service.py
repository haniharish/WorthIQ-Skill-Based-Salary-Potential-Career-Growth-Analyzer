"""
Skill Impact & Counterfactual Evaluation Service
Evaluates the marginal salary contribution of individual skills through
controlled counterfactual ablation and empirical dataset distributions.
"""

from decimal import Decimal
import numpy as np
from apps.predictions.services.salary_prediction import predict_salary_profile
from apps.intelligence.services.skill_normalization_service import normalize_skill, normalize_skill_list
from apps.intelligence.services.skill_cooccurrence_service import get_skill_statistics

def evaluate_skill_impact(profile_data):
    """
    Ranks the impact of each skill currently in the user's profile
    using single-skill ablation (counterfactual removal holding all other variables constant).
    """
    current_skills = normalize_skill_list(profile_data.get("skills", []))
    if not current_skills:
        return []

    role = profile_data.get("job_role", "Software Developer")
    exp = float(profile_data.get("years_of_experience", 3.0))
    loc = profile_data.get("location", "Bengaluru")
    edu = profile_data.get("education", "Bachelor's Degree")

    # Baseline prediction with all current skills
    base_res = predict_salary_profile(
        job_role=role,
        years_of_experience=exp,
        location=loc,
        education=edu,
        skills=current_skills
    )
    base_salary = base_res.get("salary_range", {}).get("median", base_res.get("median_salary", 600000.0))

    impacts = []
    for skill in current_skills:
        # Counterfactual: Remove this specific skill
        ablated_skills = [s for s in current_skills if s != skill]
        ablated_res = predict_salary_profile(
            job_role=role,
            years_of_experience=exp,
            location=loc,
            education=edu,
            skills=ablated_skills
        )
        ablated_salary = ablated_res.get("salary_range", {}).get("median", ablated_res.get("median_salary", base_salary))
        marginal_delta = base_salary - ablated_salary
        pct = ((base_salary - ablated_salary) / max(1.0, ablated_salary)) * 100.0

        stats = get_skill_statistics(skill) or {}

        impacts.append({
            "skill_name": skill,
            "category": stats.get("category", "Technical Skill"),
            "marginal_contribution_inr": round(marginal_delta, 2),
            "percentage_impact": round(pct, 2),
            "dataset_median_salary": stats.get("median_salary", base_salary),
            "dataset_support_pct": stats.get("support_pct", 0.0),
            "status": "Possessed"
        })

    impacts.sort(key=lambda x: x["marginal_contribution_inr"], reverse=True)
    return impacts


def compare_counterfactual(profile_data, add_skills=None, remove_skills=None):
    """
    Performs controlled What-If comparison between a base candidate profile and a
    counterfactual profile modified with added or removed skills.
    """
    base_skills = normalize_skill_list(profile_data.get("skills", []))
    add_list = normalize_skill_list(add_skills or [])
    remove_list = normalize_skill_list(remove_skills or [])

    # Calculate counterfactual skill set
    mod_skills = [s for s in base_skills if s not in remove_list]
    for s in add_list:
        if s not in mod_skills:
            mod_skills.append(s)

    role = profile_data.get("job_role", "Software Developer")
    exp = float(profile_data.get("years_of_experience", 3.0))
    loc = profile_data.get("location", "Bengaluru")
    edu = profile_data.get("education", "Bachelor's Degree")

    base_res = predict_salary_profile(
        job_role=role,
        years_of_experience=exp,
        location=loc,
        education=edu,
        skills=base_skills
    )
    mod_res = predict_salary_profile(
        job_role=role,
        years_of_experience=exp,
        location=loc,
        education=edu,
        skills=mod_skills
    )

    orig_salary = base_res.get("salary_range", {}).get("median", base_res.get("median_salary", 600000.0))
    new_salary = mod_res.get("salary_range", {}).get("median", mod_res.get("median_salary", orig_salary))
    delta = new_salary - orig_salary
    pct_change = ((new_salary - orig_salary) / max(1.0, orig_salary)) * 100.0

    return {
        "original_salary_annual": round(orig_salary, 2),
        "original_salary_lpa": round(orig_salary / 100_000.0, 2),
        "counterfactual_salary_annual": round(new_salary, 2),
        "counterfactual_salary_lpa": round(new_salary / 100_000.0, 2),
        "delta_annual": round(delta, 2),
        "delta_lpa": round(delta / 100_000.0, 2),
        "percentage_change": round(pct_change, 2),
        "added_skills": add_list,
        "removed_skills": remove_list,
        "resulting_skill_count": len(mod_skills),
        "disclaimer": (
            "Counterfactual predictions are statistical approximations derived from multi-variable "
            "regression models holding all other features constant. They do not constitute guaranteed "
            "compensation offers or causal guarantees."
        )
    }
