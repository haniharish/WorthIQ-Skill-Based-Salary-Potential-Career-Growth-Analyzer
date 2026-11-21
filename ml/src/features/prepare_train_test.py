"""
WorthIQ - Train/Test Preparation and Feature Pipeline Execution
Splits dataset with fixed random seed, applies feature transformation
strictly on training set to prevent data leakage, and serializes
fitted preprocessor bundle and transformed datasets for Part 2.
"""

import sys
import json
import logging
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.src.features.build_features import build_preprocessor, get_engineered_feature_names

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prepare_train_test")

RANDOM_SEED = 42

def prepare_and_save_data():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / "ml" / "data" / "processed"
    tables_dir = base_dir / "ml" / "reports" / "tables"
    
    input_csv = data_dir / "salary_features_dataset.csv"
    if not input_csv.exists():
        logger.error(f"Processed dataset not found at {input_csv}. Run clean_data.py first.")
        return
        
    logger.info(f"Loading processed dataset from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    # Define features and target
    feature_cols = ["job_role", "years_of_experience", "location", "education", "skills_str", "company_rating"]
    target_col = "annual_salary_inr"
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # 80/20 train/test split stratified by job_role
    logger.info("Executing 80/20 train/test split (stratified by job_role, random_state=42)...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=df["job_role"]
    )
    
    logger.info(f"Train split: {len(X_train_raw)} rows, Test split: {len(X_test_raw)} rows")
    
    # Save raw unencoded splits
    X_train_raw.to_csv(data_dir / "X_train_raw.csv", index=False)
    X_test_raw.to_csv(data_dir / "X_test_raw.csv", index=False)
    y_train.to_csv(data_dir / "y_train.csv", index=False, header=True)
    y_test.to_csv(data_dir / "y_test.csv", index=False, header=True)
    logger.info("Saved raw unencoded train and test splits.")
    
    # Build and fit preprocessor strictly on X_train (zero leakage)
    logger.info("Fitting ColumnTransformer preprocessor strictly on X_train...")
    preprocessor = build_preprocessor(categorical_strategy="onehot", numeric_scaler="standard")
    preprocessor.fit(X_train_raw)
    
    # Transform both splits
    logger.info("Transforming X_train and X_test...")
    X_train_trans = preprocessor.transform(X_train_raw)
    X_test_trans = preprocessor.transform(X_test_raw)
    
    # Extract feature names
    feature_names = get_engineered_feature_names(preprocessor)
    logger.info(f"Total engineered features: {len(feature_names)}")
    
    # Convert to DataFrames
    X_train_df = pd.DataFrame(X_train_trans, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_trans, columns=feature_names)
    
    # Save transformed datasets
    train_trans_path = data_dir / "X_train_transformed.csv"
    test_trans_path = data_dir / "X_test_transformed.csv"
    X_train_df.to_csv(train_trans_path, index=False)
    X_test_df.to_csv(test_trans_path, index=False)
    logger.info(f"Saved transformed train ({train_trans_path.name}) and test ({test_trans_path.name}) datasets.")
    
    # Serialize fitted preprocessor bundle
    preprocessor_bundle_path = data_dir / "preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_bundle_path)
    logger.info(f"Serialized preprocessor bundle to {preprocessor_bundle_path}")
    
    # Compute feature correlations with target
    logger.info("Computing engineered feature correlations with annual salary...")
    corr_series = X_train_df.apply(lambda col: col.corr(pd.Series(y_train.values)))
    corr_df = pd.DataFrame({
        "feature": corr_series.index,
        "pearson_correlation": corr_series.values
    }).sort_values(by="pearson_correlation", ascending=False).reset_index(drop=True)
    
    corr_table_path = tables_dir / "feature_target_correlations.csv"
    corr_df.to_csv(corr_table_path, index=False)
    logger.info(f"Saved feature-target correlations to {corr_table_path}")
    
    # Save complete metadata JSON
    metadata = {
        "random_seed": RANDOM_SEED,
        "train_rows": int(len(X_train_raw)),
        "test_rows": int(len(X_test_raw)),
        "total_rows": int(len(df)),
        "split_ratio": "80/20",
        "stratification": "job_role",
        "input_features": feature_cols,
        "target_variable": target_col,
        "engineered_feature_count": int(len(feature_names)),
        "engineered_features": feature_names,
        "preprocessor_bundle": str(preprocessor_bundle_path.name),
        "target_statistics_train": {
            "mean": float(round(y_train.mean(), 2)),
            "median": float(round(y_train.median(), 2)),
            "min": float(round(y_train.min(), 2)),
            "max": float(round(y_train.max(), 2)),
            "std": float(round(y_train.std(), 2)),
        },
        "target_statistics_test": {
            "mean": float(round(y_test.mean(), 2)),
            "median": float(round(y_test.median(), 2)),
            "min": float(round(y_test.min(), 2)),
            "max": float(round(y_test.max(), 2)),
            "std": float(round(y_test.std(), 2)),
        }
    }
    
    meta_path = data_dir / "feature_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as jf:
        json.dump(metadata, jf, indent=2)
    logger.info(f"Saved feature metadata to {meta_path}")
    
    print("\n" + "="*70)
    print("FEATURE PIPELINE AND TRAIN/TEST PREPARATION COMPLETE")
    print("="*70)
    print(f"Train Shape: {X_train_df.shape} | Test Shape: {X_test_df.shape}")
    print(f"Total Features: {len(feature_names)}")
    print("\nTop 10 Positively Correlated Features with Salary:")
    for _, row in corr_df.head(10).iterrows():
        print(f" - {row['feature']:<38}: {row['pearson_correlation']:>+.4f}")
    print("="*70 + "\n")

if __name__ == "__main__":
    prepare_and_save_data()
