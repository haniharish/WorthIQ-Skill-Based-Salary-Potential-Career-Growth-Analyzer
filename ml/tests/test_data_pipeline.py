"""
WorthIQ - Data Engineering and Feature Pipeline Unit and Integration Tests
Tests data validation, preprocessing, leakage prevention, and reproducibility.
"""

import sys
import json
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
import joblib

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.src.features.build_features import (
    MultiLabelSkillsEncoder,
    build_preprocessor,
    CANONICAL_SKILLS
)
from ml.src.preprocessing.clean_data import (
    STANDARDIZED_ROLES,
    STANDARDIZED_CITIES,
    map_job_role,
    extract_experience,
    assign_skills
)

@pytest.fixture
def processed_data_path():
    return PROJECT_ROOT / "ml" / "data" / "processed" / "salary_features_dataset.csv"

@pytest.fixture
def splits_paths():
    p = PROJECT_ROOT / "ml" / "data" / "processed"
    return {
        "X_train_raw": p / "X_train_raw.csv",
        "X_test_raw": p / "X_test_raw.csv",
        "y_train": p / "y_train.csv",
        "y_test": p / "y_test.csv",
        "X_train_trans": p / "X_train_transformed.csv",
        "X_test_trans": p / "X_test_transformed.csv",
        "preprocessor": p / "preprocessor.joblib",
        "metadata": p / "feature_metadata.json",
    }

def test_processed_dataset_integrity(processed_data_path):
    """Verify that processed dataset exists, is non-empty, and adheres to schema."""
    assert processed_data_path.exists(), "Processed dataset does not exist."
    df = pd.read_csv(processed_data_path)
    
    # Check minimum records threshold
    assert len(df) > 20_000, f"Expected >20,000 records, got {len(df)}"
    
    # Check expected columns
    expected_cols = [
        "job_role", "years_of_experience", "location", "education",
        "skills_str", "company_rating", "annual_salary_inr"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    # Zero missing values in primary features
    assert df[expected_cols].isnull().sum().sum() == 0, "Missing values found in processed data."

def test_salary_bounds_and_validity(processed_data_path):
    """Verify all salaries are positive and within realistic Indian tech bounds."""
    df = pd.read_csv(processed_data_path)
    
    salaries = df["annual_salary_inr"]
    assert (salaries > 0).all(), "Non-positive salary detected."
    assert salaries.min() >= 120_000, f"Salary below 1.2 LPA floor: {salaries.min()}"
    assert salaries.max() <= 8_000_000, f"Salary above 80 LPA ceiling: {salaries.max()}"
    
    # Check median and mean are within plausible Indian market expectations
    median_sal = salaries.median()
    assert 300_000 <= median_sal <= 1_500_000, f"Median salary {median_sal} outside realistic range."

def test_category_taxonomies(processed_data_path):
    """Ensure all job roles and locations conform exactly to WorthIQ standard taxonomy."""
    df = pd.read_csv(processed_data_path)
    
    # Check all 8 standardized roles
    unique_roles = set(df["job_role"].unique())
    assert unique_roles.issubset(set(STANDARDIZED_ROLES)), f"Unknown roles found: {unique_roles - set(STANDARDIZED_ROLES)}"
    assert len(unique_roles) == 8, f"Expected 8 roles, found {len(unique_roles)}"
    
    # Check all 6 standardized cities
    unique_cities = set(df["location"].unique())
    assert unique_cities.issubset(set(STANDARDIZED_CITIES)), f"Unknown cities found: {unique_cities - set(STANDARDIZED_CITIES)}"
    assert len(unique_cities) == 6, f"Expected 6 cities, found {len(unique_cities)}"

def test_multilabel_skills_encoder():
    """Verify that the MultiLabelSkillsEncoder correctly binarizes skills."""
    encoder = MultiLabelSkillsEncoder(CANONICAL_SKILLS)
    encoder.fit(None)
    
    test_input = pd.Series([
        "Python;Django;PostgreSQL",
        "React.js;JavaScript;HTML5;CSS3",
        "Docker;Kubernetes;Linux;AWS",
        ""
    ])
    
    matrix = encoder.transform(test_input)
    assert matrix.shape == (4, len(CANONICAL_SKILLS))
    
    feature_names = encoder.get_feature_names_out()
    assert len(feature_names) == len(CANONICAL_SKILLS)
    
    # Verify specific skill indicators
    py_idx = encoder.skill_to_idx_["Python"]
    assert matrix[0, py_idx] == 1.0
    assert matrix[1, py_idx] == 0.0

def test_train_test_split_isolation_and_leakage_prevention(splits_paths):
    """Verify zero overlap between train and test splits, and check preprocessor persistence."""
    for key, path in splits_paths.items():
        assert path.exists(), f"Artifact {key} missing at {path}"
        
    X_train_raw = pd.read_csv(splits_paths["X_train_raw"])
    X_test_raw = pd.read_csv(splits_paths["X_test_raw"])
    y_train = pd.read_csv(splits_paths["y_train"])
    y_test = pd.read_csv(splits_paths["y_test"])
    
    # Lengths matching
    assert len(X_train_raw) == len(y_train)
    assert len(X_test_raw) == len(y_test)
    assert len(X_train_raw) > len(X_test_raw)
    
    # Transformed data integrity
    X_train_trans = pd.read_csv(splits_paths["X_train_trans"])
    X_test_trans = pd.read_csv(splits_paths["X_test_trans"])
    
    assert X_train_trans.shape[0] == len(X_train_raw)
    assert X_test_trans.shape[0] == len(X_test_raw)
    assert X_train_trans.shape[1] == X_test_trans.shape[1] == 55
    
    # Verify no NaNs in transformed feature matrices
    assert X_train_trans.isnull().sum().sum() == 0, "NaNs in X_train_transformed"
    assert X_test_trans.isnull().sum().sum() == 0, "NaNs in X_test_transformed"

def test_preprocessor_joblib_bundle(splits_paths):
    """Verify serialized preprocessor loads and successfully transforms new unseen profile."""
    preprocessor = joblib.load(splits_paths["preprocessor"])
    
    sample_profile = pd.DataFrame([{
        "job_role": "Full Stack Developer",
        "years_of_experience": 3.5,
        "location": "Bengaluru",
        "education": "Bachelor's Degree",
        "skills_str": "Python;Django;React.js;PostgreSQL;Docker;Git",
        "company_rating": 4.2
    }])
    
    transformed = preprocessor.transform(sample_profile)
    assert transformed.shape == (1, 55)
    assert not np.isnan(transformed).any()
