"""
Unit tests for ML models, quantile predictors, serialization, and confidence service.
"""

import sys
import json
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.src.models.train_models import pinball_loss
from backend.apps.predictions.services.model_loader import get_model_registry
from backend.apps.predictions.services.confidence_service import calculate_confidence
from backend.apps.predictions.services.salary_prediction import predict_salary_profile, normalize_role, normalize_location

@pytest.fixture(scope="module")
def model_registry():
    registry = get_model_registry()
    registry.load_artifacts(force_reload=True)
    return registry

def test_model_artifacts_exist_and_load(model_registry):
    """Verify that all model artifacts exist and load into memory."""
    assert model_registry.is_ready()
    assert model_registry.salary_model is not None
    assert model_registry.preprocessor is not None
    assert model_registry.quantile_p10 is not None
    assert model_registry.quantile_p50 is not None
    assert model_registry.quantile_p90 is not None
    assert model_registry.metadata is not None

def test_model_metadata_structure(model_registry):
    """Verify model metadata adheres to schema."""
    meta = model_registry.metadata
    assert meta["model_version"] == "2.0.0"
    assert meta["target_variable"] == "annual_salary_inr"
    assert meta["engineered_feature_count"] == 55
    assert meta["training_rows"] > 20_000
    assert "evaluation_metrics" in meta
    assert meta["evaluation_metrics"]["test"]["r2"] > 0.30

def test_prediction_output_and_types(model_registry):
    """Test salary prediction returns valid numerical outputs and ranges."""
    res = predict_salary_profile(
        job_role="Data Scientist",
        years_of_experience=4.5,
        location="Bengaluru",
        skills=["Python", "Pandas", "Scikit-Learn", "Machine Learning", "SQL"],
        education="Master's Degree"
    )
    
    assert res["currency"] == "INR"
    assert res["salary_period"] == "annual"
    assert res["salary_range"]["low"] >= 120_000
    assert res["salary_range"]["median"] >= res["salary_range"]["low"]
    assert res["salary_range"]["high"] >= res["salary_range"]["median"]
    assert res["confidence"] in ["High", "Medium", "Low"]
    assert len(res["top_contributing_skills"]) > 0

def test_quantile_ordering_monotonicity():
    """Verify that salary range low <= median <= high holds across multiple profiles."""
    test_profiles = [
        {"role": "Software Developer", "exp": 0.5, "loc": "Chennai", "skills": ["Java", "SQL"]},
        {"role": "Frontend Developer", "exp": 3.0, "loc": "Pune", "skills": ["React.js", "JavaScript", "HTML5", "CSS3"]},
        {"role": "DevOps Engineer", "exp": 6.0, "loc": "Hyderabad", "skills": ["Docker", "Kubernetes", "AWS", "Linux"]},
        {"role": "Data Analyst", "exp": 2.0, "loc": "Delhi NCR", "skills": ["Python", "SQL", "Pandas", "Data Analysis"]},
        {"role": "Full Stack Developer", "exp": 5.0, "loc": "Mumbai", "skills": ["React.js", "Node.js", "PostgreSQL", "Git"]},
    ]
    
    for p in test_profiles:
        res = predict_salary_profile(
            job_role=p["role"],
            years_of_experience=p["exp"],
            location=p["loc"],
            skills=p["skills"]
        )
        rng = res["salary_range"]
        assert rng["low"] <= rng["median"], f"Violation: Low ({rng['low']}) > Median ({rng['median']}) for {p['role']}"
        assert rng["median"] <= rng["high"], f"Violation: Median ({rng['median']}) > High ({rng['high']}) for {p['role']}"
        assert rng["low"] > 0, "Non-positive salary returned"

def test_unseen_category_and_skill_handling():
    """Model must gracefully handle unseen/exotic skills and unlisted roles without raising exceptions."""
    res = predict_salary_profile(
        job_role="Quantum Computing Architect",
        years_of_experience=5.0,
        location="Coimbatore",
        skills=["Qiskit", "Superconducting Qubits", "Quantum Decoherence"],
        education="PhD"
    )
    
    assert res["salary_range"]["median"] >= 120_000
    assert res["confidence"] in ["Medium", "Low"]
    # Unseen role maps gracefully to normalized category
    assert res["job_role"] in ["Software Developer", "Data Scientist", "Backend Developer"]

def test_confidence_classification_logic():
    """Test confidence scoring tiers with empirical inputs."""
    # High confidence: core role, top hub, normal exp, 4+ canonical skills, tight interval
    conf_high, details_high = calculate_confidence(
        job_role="Software Developer",
        location="Bengaluru",
        years_of_experience=3.0,
        skills=["Java", "Spring Boot", "Git", "SQL", "REST APIs"],
        p10=450_000,
        p50=600_000,
        p90=850_000
    )
    assert conf_high == "High"
    assert details_high["confidence_score"] >= 75

    # Low confidence: obscure role, secondary hub, outlier exp, no skills, wide interval
    conf_low, details_low = calculate_confidence(
        job_role="Unknown Track",
        location="Remote Town",
        years_of_experience=28.0,
        skills=[],
        p10=200_000,
        p50=700_000,
        p90=1_900_000
    )
    assert conf_low == "Low"
    assert details_low["confidence_score"] < 50

def test_pinball_loss_calculation():
    """Verify pinball loss function produces positive non-zero error."""
    y_true = np.array([500_000, 800_000, 1_200_000])
    y_pred = np.array([450_000, 820_000, 1_100_000])
    loss_10 = pinball_loss(y_true, y_pred, 0.10)
    loss_90 = pinball_loss(y_true, y_pred, 0.90)
    assert loss_10 > 0
    assert loss_90 > 0
