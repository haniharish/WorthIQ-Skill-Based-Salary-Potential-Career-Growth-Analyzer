"""
SHAP Service
Connects Django prediction records with the SHAP TreeExplainer engine,
providing cached persistence and user ownership verification.
"""

import logging
from pathlib import Path
import json
from decimal import Decimal
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from apps.predictions.models import Prediction
from apps.intelligence.models import PredictionExplanation
from ml.src.explainability.shap_explainer import WorthIQShapExplainer

logger = logging.getLogger("intelligence.shap")

def get_or_create_explanation(prediction_id, user=None):
    """
    Retrieves existing SHAP explanation for a prediction or computes and persists it.

    Parameters:
        prediction_id (int): Prediction primary key.
        user (User, optional): Authenticated user to verify ownership.

    Returns:
        PredictionExplanation instance.
    """
    try:
        prediction = Prediction.objects.get(id=prediction_id)
    except Prediction.DoesNotExist:
        raise ObjectDoesNotExist(f"Prediction #{prediction_id} does not exist.")

    # User isolation check
    if user and not user.is_staff and prediction.user_id != user.id:
        raise PermissionDenied("You do not have permission to view this prediction explanation.")

    # Check cache in DB
    explanation = getattr(prediction, 'explanation', None)
    if explanation is not None:
        return explanation

    logger.info(f"Computing real-time SHAP explanation for Prediction #{prediction_id}...")
    explainer = WorthIQShapExplainer()

    input_payload = {
        "job_role": prediction.job_role,
        "years_of_experience": float(prediction.years_of_experience),
        "location": prediction.location,
        "education": prediction.education or "Bachelor's Degree",
        "skills": prediction.skills or [],
        "company_rating": 3.8,
    }

    raw_res = explainer.explain_instance(input_payload)

    # Persist explanation
    explanation = PredictionExplanation.objects.create(
        prediction=prediction,
        base_value_log=raw_res["base_value_log"],
        base_value_inr=Decimal(str(raw_res["base_value_inr"])),
        predicted_value_log=raw_res["predicted_value_log"],
        predicted_value_inr=Decimal(str(raw_res["predicted_value_inr"])),
        total_delta_inr=Decimal(str(raw_res["total_delta_inr"])),
        feature_attributions=raw_res["feature_attributions"],
        positive_contributors=raw_res["positive_contributors"],
        negative_contributors=raw_res["negative_contributors"],
        skills_impact=raw_res["skills_impact"],
        summary_narrative=raw_res["summary_narrative"],
        model_version=raw_res.get("model_version", "2.0.0"),
    )

    return explanation


def get_global_explanations():
    """Returns precomputed global feature importance statistics."""
    from django.conf import settings
    candidate_paths = [
        getattr(settings, 'BASE_DIR').parent / "ml" / "explainability" / "global" / "global_feature_importance.json",
        getattr(settings, 'BASE_DIR') / "ml" / "explainability" / "global" / "global_feature_importance.json",
        Path(__file__).resolve().parents[4] / "ml" / "explainability" / "global" / "global_feature_importance.json",
        Path(__file__).resolve().parent.parent.parent.parent / "ml" / "explainability" / "global" / "global_feature_importance.json",
    ]

    for global_json_path in candidate_paths:
        if global_json_path.exists():
            with open(global_json_path, "r", encoding="utf-8") as f:
                return json.load(f)

    # If not yet generated, compute on the fly
    explainer = WorthIQShapExplainer()
    return explainer.generate_global_explanations(sample_size=500)
