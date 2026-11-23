"""
Business logic and ML prediction orchestration for What-If Salary Scenarios.
"""

import logging
from typing import Dict, Any, List, Optional
from decimal import Decimal

from apps.predictions.services.salary_prediction import predict_salary_profile
from .models import SalaryScenario

logger = logging.getLogger("scenarios.services")

DISCLAIMER_TEXT = (
    "Scenario comparisons show how the existing salary prediction model responds to different profile inputs. "
    "They are exploratory estimates, not guaranteed salary increases or causal effects."
)

def evaluate_scenario_profile(
    job_role: str,
    years_of_experience: float,
    location: str,
    skills: List[str],
    education: str = "Bachelor's Degree"
) -> Dict[str, Any]:
    """
    Executes the Phase 2 ML salary prediction pipeline for a scenario profile.
    Reuses existing model artifacts and preprocessor with zero duplication.
    """
    return predict_salary_profile(
        job_role=job_role,
        years_of_experience=float(years_of_experience),
        location=location,
        skills=skills,
        education=education
    )


def build_scenario_snapshot(prediction_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts a serializable prediction snapshot for a scenario."""
    median = prediction_result["salary_range"]["median"]
    low = prediction_result["salary_range"]["low"]
    high = prediction_result["salary_range"]["high"]
    
    p10_lpa = round(float(low) / 100_000.0, 2)
    p50_lpa = round(float(median) / 100_000.0, 2)
    p90_lpa = round(float(high) / 100_000.0, 2)

    return {
        "job_role": prediction_result["job_role"],
        "location": prediction_result["location"],
        "years_of_experience": prediction_result["years_of_experience"],
        "education": prediction_result["education"],
        "skills_evaluated": prediction_result["skills_evaluated"],
        "currency": prediction_result.get("currency", "INR"),
        "salary_range": {
            "low": float(low),
            "median": float(median),
            "high": float(high),
            "p10_lpa": p10_lpa,
            "p50_lpa": p50_lpa,
            "p90_lpa": p90_lpa,
        },
        "salary_lpa": p50_lpa,
        "p10_lpa": p10_lpa,
        "p50_lpa": p50_lpa,
        "p90_lpa": p90_lpa,
        "confidence": prediction_result.get("confidence", "Medium"),
        "confidence_score": prediction_result.get("confidence_details", {}).get("confidence_score", 75),
        "model_version": prediction_result.get("model_version", "2.0.0"),
    }


def compare_multiple_scenarios(
    user,
    scenario_ids: List[int] = None,
    new_scenarios: List[Dict[str, Any]] = None,
    include_baseline: bool = True,
    custom_baseline: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Evaluates baseline profile and multiple scenarios simultaneously.
    Computes comparative metrics, salary range differences, and input mutation diffs.
    Enforces maximum of 4 profiles.
    """
    if scenario_ids is None:
        scenario_ids = []
    if new_scenarios is None:
        new_scenarios = []

    items_to_compare = []

    # 1. Baseline profile if requested or custom baseline provided
    baseline_item = None
    if custom_baseline:
        b_role = custom_baseline.get("job_role", "Software Developer")
        b_exp = float(custom_baseline.get("years_of_experience", 2.0))
        b_loc = custom_baseline.get("location", "Bengaluru")
        b_edu = custom_baseline.get("education", "Bachelor's Degree")
        b_skills = custom_baseline.get("skills", ["Python", "SQL", "Git"])

        try:
            baseline_pred = evaluate_scenario_profile(
                job_role=b_role,
                years_of_experience=b_exp,
                location=b_loc,
                skills=b_skills,
                education=b_edu
            )
            baseline_snapshot = build_scenario_snapshot(baseline_pred)
            baseline_item = {
                "id": "baseline",
                "name": "Baseline Profile",
                "is_baseline": True,
                "job_role": b_role,
                "years_of_experience": b_exp,
                "location": b_loc,
                "education": b_edu,
                "skills": b_skills,
                "prediction": baseline_snapshot
            }
            items_to_compare.append(baseline_item)
        except Exception as e:
            logger.error(f"Failed to evaluate custom baseline: {e}")
    elif include_baseline:
        prof = getattr(user, 'profile', None)
        baseline_skills = [s.name for s in prof.skills.all()] if prof and prof.skills.exists() else ['Python', 'SQL', 'Git']
        baseline_role = (prof.job_role if prof and prof.job_role else 'Software Developer')
        baseline_exp = float(prof.years_of_experience if prof and prof.years_of_experience else 2.0)
        baseline_loc = (prof.location if prof and prof.location else 'Bengaluru')
        baseline_edu = (prof.education if prof and prof.education else "Bachelor's Degree")

        try:
            baseline_pred = evaluate_scenario_profile(
                job_role=baseline_role,
                years_of_experience=baseline_exp,
                location=baseline_loc,
                skills=baseline_skills,
                education=baseline_edu
            )
            baseline_snapshot = build_scenario_snapshot(baseline_pred)
            baseline_item = {
                "id": "baseline",
                "name": "Current Profile (Baseline)",
                "is_baseline": True,
                "job_role": baseline_role,
                "years_of_experience": baseline_exp,
                "location": baseline_loc,
                "education": baseline_edu,
                "skills": baseline_skills,
                "prediction": baseline_snapshot
            }
            items_to_compare.append(baseline_item)
        except Exception as e:
            logger.error(f"Failed to evaluate baseline profile for comparison: {e}")

    # 2. Add saved scenarios (scoped to user)
    if scenario_ids:
        saved_scenarios = SalaryScenario.objects.filter(user=user, id__in=scenario_ids)
        for sc in saved_scenarios:
            if len(items_to_compare) >= 4:
                break
            
            # Use cached snapshot or recompute
            if not sc.prediction_snapshot:
                pred = evaluate_scenario_profile(
                    sc.job_role,
                    float(sc.years_of_experience),
                    sc.location,
                    sc.skills,
                    sc.education
                )
                sc.prediction_snapshot = build_scenario_snapshot(pred)
                sc.save(update_fields=['prediction_snapshot', 'updated_at'])

            items_to_compare.append({
                "id": str(sc.id),
                "name": sc.name,
                "is_baseline": False,
                "job_role": sc.job_role,
                "years_of_experience": float(sc.years_of_experience),
                "location": sc.location,
                "education": sc.education,
                "skills": sc.skills,
                "prediction": sc.prediction_snapshot
            })

    # 3. Add any unsaved/dynamic scenarios
    for idx, sc_raw in enumerate(new_scenarios):
        if len(items_to_compare) >= 4:
            break
        try:
            r_name = sc_raw.get("name", f"Experiment {idx + 1}")
            r_role = sc_raw["job_role"]
            r_exp = float(sc_raw["years_of_experience"])
            r_loc = sc_raw["location"]
            r_edu = sc_raw.get("education", "Bachelor's Degree")
            r_skills = sc_raw.get("skills", [])

            pred = evaluate_scenario_profile(r_role, r_exp, r_loc, r_skills, r_edu)
            items_to_compare.append({
                "id": f"draft_{idx + 1}",
                "name": r_name,
                "is_baseline": False,
                "job_role": r_role,
                "years_of_experience": r_exp,
                "location": r_loc,
                "education": r_edu,
                "skills": r_skills,
                "prediction": build_scenario_snapshot(pred)
            })
        except Exception as e:
            logger.error(f"Failed to evaluate draft scenario: {e}")

    # 4. Compute pairwise deltas against baseline (or first item)
    reference = items_to_compare[0] if items_to_compare else None
    ref_median = reference["prediction"]["salary_range"]["median"] if reference else 0

    comparison_results = []
    for item in items_to_compare:
        item_median = item["prediction"]["salary_range"]["median"]
        delta_inr = round(item_median - ref_median, 2)
        pct_change = round(((item_median - ref_median) / ref_median) * 100.0, 2) if ref_median > 0 else 0.0

        # Input differences compared to baseline
        diff_info = {
            "role_changed": item["job_role"] != reference["job_role"] if reference else False,
            "exp_diff": round(item["years_of_experience"] - reference["years_of_experience"], 1) if reference else 0,
            "location_changed": item["location"] != reference["location"] if reference else False,
            "skills_added": [s for s in item["skills"] if s not in (reference["skills"] if reference else [])],
            "skills_removed": [s for s in (reference["skills"] if reference else []) if s not in item["skills"]],
        }

        delta_info = {
            "absolute_diff_inr": delta_inr,
            "absolute_diff_lpa": round(delta_inr / 100_000.0, 2),
            "delta_p50_lpa": round(delta_inr / 100_000.0, 2),
            "percentage_change": pct_change,
            "differences": diff_info
        }

        comparison_results.append({
            **item,
            "comparison_to_baseline": delta_info,
            "delta_vs_baseline": delta_info,
        })

    return {
        "total_compared": len(comparison_results),
        "baseline_reference_id": reference["id"] if reference else None,
        "baseline": reference,
        "scenarios": comparison_results,
        "disclaimer": DISCLAIMER_TEXT
    }
