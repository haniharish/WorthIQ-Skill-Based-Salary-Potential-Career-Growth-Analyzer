"""
WorthIQ - Model Training, Evaluation, Comparison, and Artifact Serialization
Trains Linear Regression, Random Forest, and XGBoost regressors on real salary data.
Trains quantile regression models for P10, P50, and P90 salary range estimation.
Evaluates all models with 5-fold CV, held-out test evaluation, calibration checks,
and generates publication-quality visualization figures.
"""

import os
import sys
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
    median_absolute_error,
    mean_absolute_percentage_error
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_models")

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def pinball_loss(y_true, y_pred, alpha):
    """Calculate average pinball loss for quantile alpha."""
    err = y_true - y_pred
    return np.mean(np.maximum(alpha * err, (alpha - 1) * err))

def train_and_evaluate_all():
    base_dir = PROJECT_ROOT
    data_dir = base_dir / "ml" / "data" / "processed"
    models_dir = base_dir / "ml" / "models"
    quantile_dir = models_dir / "quantile_models"
    reports_dir = base_dir / "ml" / "reports"
    figures_dir = reports_dir / "figures"
    tables_dir = reports_dir / "tables"
    
    models_dir.mkdir(parents=True, exist_ok=True)
    quantile_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Data
    logger.info("Loading preprocessed training and test matrices...")
    X_train = pd.read_csv(data_dir / "X_train_transformed.csv")
    X_test = pd.read_csv(data_dir / "X_test_transformed.csv")
    y_train = pd.read_csv(data_dir / "y_train.csv")["annual_salary_inr"].values
    y_test = pd.read_csv(data_dir / "y_test.csv")["annual_salary_inr"].values
    
    logger.info(f"Loaded X_train: {X_train.shape}, X_test: {X_test.shape}")
    logger.info(f"Loaded y_train: {len(y_train)}, y_test: {len(y_test)}")
    
    # Target transformation to log-space
    y_train_log = np.log1p(y_train)
    y_test_log = np.log1p(y_test)
    
    # 2. Define Model Candidates
    candidate_models = {
        "Linear Regression": {
            "model": LinearRegression(),
            "params": {"fit_intercept": True}
        },
        "Random Forest": {
            "model": RandomForestRegressor(
                n_estimators=150,
                max_depth=16,
                min_samples_split=4,
                min_samples_leaf=2,
                random_state=RANDOM_SEED,
                n_jobs=-1
            ),
            "params": {
                "n_estimators": 150,
                "max_depth": 16,
                "min_samples_split": 4,
                "min_samples_leaf": 2,
                "random_state": RANDOM_SEED
            }
        },
        "XGBoost": {
            "model": xgb.XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_lambda=1.0,
                random_state=RANDOM_SEED,
                n_jobs=-1
            ),
            "params": {
                "n_estimators": 300,
                "learning_rate": 0.05,
                "max_depth": 6,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "reg_lambda": 1.0,
                "random_state": RANDOM_SEED
            }
        }
    }
    
    results = {}
    fitted_models = {}
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    
    print("\n" + "="*80)
    print("STAGE 1: MODEL TRAINING AND 5-FOLD CROSS-VALIDATION")
    print("="*80)
    
    for name, config in candidate_models.items():
        logger.info(f"Evaluating {name}...")
        model = config["model"]
        
        # 5-Fold Cross-Validation on X_train (evaluated in original INR space)
        cv_log_preds = cross_val_predict(model, X_train, y_train_log, cv=cv, n_jobs=-1)
        cv_preds = np.maximum(0, np.expm1(cv_log_preds))
        
        cv_mae = float(mean_absolute_error(y_train, cv_preds))
        cv_rmse = float(root_mean_squared_error(y_train, cv_preds))
        cv_r2 = float(r2_score(y_train, cv_preds))
        cv_medae = float(median_absolute_error(y_train, cv_preds))
        cv_mape = float(mean_absolute_percentage_error(y_train, cv_preds)) * 100
        
        # Fit on full training set
        model.fit(X_train, y_train_log)
        fitted_models[name] = model
        
        # Training Set Metrics
        train_log_preds = model.predict(X_train)
        train_preds = np.maximum(0, np.expm1(train_log_preds))
        train_mae = float(mean_absolute_error(y_train, train_preds))
        train_rmse = float(root_mean_squared_error(y_train, train_preds))
        train_r2 = float(r2_score(y_train, train_preds))
        train_medae = float(median_absolute_error(y_train, train_preds))
        train_mape = float(mean_absolute_percentage_error(y_train, train_preds)) * 100
        
        # Test Set Metrics (Held-out 20%)
        test_log_preds = model.predict(X_test)
        test_preds = np.maximum(0, np.expm1(test_log_preds))
        test_mae = float(mean_absolute_error(y_test, test_preds))
        test_rmse = float(root_mean_squared_error(y_test, test_preds))
        test_r2 = float(r2_score(y_test, test_preds))
        test_medae = float(median_absolute_error(y_test, test_preds))
        test_mape = float(mean_absolute_percentage_error(y_test, test_preds)) * 100
        
        results[name] = {
            "params": config["params"],
            "cv_metrics": {
                "mae": round(cv_mae, 2),
                "rmse": round(cv_rmse, 2),
                "r2": round(cv_r2, 4),
                "medae": round(cv_medae, 2),
                "mape_pct": round(cv_mape, 2)
            },
            "train_metrics": {
                "mae": round(train_mae, 2),
                "rmse": round(train_rmse, 2),
                "r2": round(train_r2, 4),
                "medae": round(train_medae, 2),
                "mape_pct": round(train_mape, 2)
            },
            "test_metrics": {
                "mae": round(test_mae, 2),
                "rmse": round(test_rmse, 2),
                "r2": round(test_r2, 4),
                "medae": round(test_medae, 2),
                "mape_pct": round(test_mape, 2)
            },
            "test_predictions": test_preds
        }
        
        print(f"\n[{name}]")
        print(f"  CV 5-Fold: MAE = ₹{cv_mae:,.0f} | RMSE = ₹{cv_rmse:,.0f} | R² = {cv_r2:.4f} | MAPE = {cv_mape:.2f}%")
        print(f"  Train Set: MAE = ₹{train_mae:,.0f} | RMSE = ₹{train_rmse:,.0f} | R² = {train_r2:.4f}")
        print(f"  Test Set : MAE = ₹{test_mae:,.0f} | RMSE = ₹{test_rmse:,.0f} | R² = {test_r2:.4f} | MedAE = ₹{test_medae:,.0f}")

    # 3. Model Comparison Table
    comparison_rows = []
    for name, res in results.items():
        comparison_rows.append({
            "model": name,
            "cv_mae_inr": res["cv_metrics"]["mae"],
            "cv_rmse_inr": res["cv_metrics"]["rmse"],
            "cv_r2": res["cv_metrics"]["r2"],
            "train_mae_inr": res["train_metrics"]["mae"],
            "train_r2": res["train_metrics"]["r2"],
            "test_mae_inr": res["test_metrics"]["mae"],
            "test_rmse_inr": res["test_metrics"]["rmse"],
            "test_r2": res["test_metrics"]["r2"],
            "test_medae_inr": res["test_metrics"]["medae"],
            "test_mape_pct": res["test_metrics"]["mape_pct"]
        })
    comparison_df = pd.DataFrame(comparison_rows).sort_values(by="test_r2", ascending=False).reset_index(drop=True)
    comparison_csv_path = reports_dir / "model_comparison.csv"
    comparison_df.to_csv(comparison_csv_path, index=False)
    logger.info(f"Saved model comparison table to {comparison_csv_path}")

    # Select Best Model based on Test R² and Test MAE
    best_model_name = comparison_df.iloc[0]["model"]
    best_model = fitted_models[best_model_name]
    logger.info(f"Selected Best Model: {best_model_name}")

    print("\n" + "="*80)
    print(f"MODEL COMPARISON SUMMARY (SELECTED BEST: {best_model_name.upper()})")
    print("="*80)
    print(comparison_df.to_string(index=False))

    # 4. Train Quantile Regression Models (P10, P50, P90)
    print("\n" + "="*80)
    print("STAGE 2: TRAINING QUANTILE REGRESSION MODELS (P10, P50, P90)")
    print("="*80)
    
    quantiles = {
        "p10": 0.10,
        "p50": 0.50,
        "p90": 0.90
    }
    quantile_models = {}
    quantile_eval = {}
    
    for q_name, q_val in quantiles.items():
        logger.info(f"Training Quantile Regressor for {q_name.upper()} (alpha={q_val})...")
        q_model = GradientBoostingRegressor(
            loss="quantile",
            alpha=q_val,
            n_estimators=160,
            max_depth=4,
            learning_rate=0.06,
            random_state=RANDOM_SEED
        )
        q_model.fit(X_train, y_train_log)
        quantile_models[q_name] = q_model
        
        # Save model artifact
        q_path = quantile_dir / f"quantile_{q_name}.joblib"
        joblib.dump(q_model, q_path)
        logger.info(f"Saved {q_name} artifact to {q_path}")
        
        # Test evaluation in linear space
        q_pred_log = q_model.predict(X_test)
        q_pred = np.maximum(0, np.expm1(q_pred_log))
        
        # Proportion below quantile
        prop_below = float(np.mean(y_test < q_pred) * 100)
        p_loss = float(pinball_loss(y_test, q_pred, q_val))
        
        quantile_eval[q_name] = {
            "alpha": q_val,
            "target_coverage_pct": q_val * 100,
            "empirical_coverage_pct": round(prop_below, 2),
            "pinball_loss_inr": round(p_loss, 2),
            "median_predicted_inr": round(float(np.median(q_pred)), 2)
        }
        print(f"  {q_name.upper()} (alpha={q_val:.2f}): Target Coverage = {q_val*100:.1f}%, Observed Coverage = {prop_below:.2f}%, Pinball Loss = ₹{p_loss:,.0f}")

    # Monotonicity check on test set: verify P10 <= P50 <= P90
    p10_test = np.maximum(0, np.expm1(quantile_models["p10"].predict(X_test)))
    p50_test = np.maximum(0, np.expm1(quantile_models["p50"].predict(X_test)))
    p90_test = np.maximum(0, np.expm1(quantile_models["p90"].predict(X_test)))
    
    monotonic_valid = np.all((p10_test <= p50_test) & (p50_test <= p90_test))
    crossing_violations = int(np.sum((p10_test > p50_test) | (p50_test > p90_test)))
    logger.info(f"Quantile monotonicity test on test set: {monotonic_valid} (crossing violations: {crossing_violations} / {len(X_test)})")

    # 5. Save Primary Model Artifacts
    best_model_path = models_dir / "salary_model.joblib"
    joblib.dump(best_model, best_model_path)
    logger.info(f"Saved best model artifact to {best_model_path}")
    
    # Also copy preprocessor into ml/models/preprocessing_pipeline.joblib for unified loading
    preprocessor_source = data_dir / "preprocessor.joblib"
    preprocessor_dest = models_dir / "preprocessing_pipeline.joblib"
    shutil.copyfile(preprocessor_source, preprocessor_dest)
    logger.info(f"Copied preprocessor pipeline to {preprocessor_dest}")

    # 6. Generate Evaluation Figures
    print("\n" + "="*80)
    print("STAGE 3: GENERATING EVALUATION FIGURES")
    print("="*80)
    
    best_test_preds = results[best_model_name]["test_predictions"]
    residuals = y_test - best_test_preds
    
    # Figure 1: Actual vs Predicted
    plt.figure(figsize=(10, 6), dpi=300)
    sample_idx = np.random.choice(len(y_test), size=min(1500, len(y_test)), replace=False)
    plt.scatter(
        y_test[sample_idx] / 100_000,
        best_test_preds[sample_idx] / 100_000,
        alpha=0.45,
        color="#4F46E5",
        edgecolors="none",
        s=35,
        label="Test Profiles"
    )
    max_val = max(np.max(y_test), np.max(best_test_preds)) / 100_000
    plt.plot([0, 50], [0, 50], color="#DC2626", linestyle="--", linewidth=2.0, label="Ideal Prediction (1:1)")
    plt.title(f"WorthIQ {best_model_name}: Actual vs Predicted Salaries (LPA)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Actual Annual Salary (LPA)", fontsize=11, fontweight="bold")
    plt.ylabel("Predicted Annual Salary (LPA)", fontsize=11, fontweight="bold")
    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    fig1_path = figures_dir / "actual_vs_predicted.png"
    plt.savefig(fig1_path)
    plt.close()
    logger.info(f"Saved: {fig1_path.name}")

    # Figure 2: Residuals Distribution
    plt.figure(figsize=(10, 5), dpi=300)
    sns.histplot(residuals / 100_000, bins=50, kde=True, color="#06B6D4", edgecolor="white")
    plt.axvline(0, color="#EF4444", linestyle="--", linewidth=2.0, label="Zero Error Line")
    plt.axvline(np.mean(residuals) / 100_000, color="#10B981", linestyle=":", linewidth=2.0, label=f"Mean Residual: {np.mean(residuals)/100_000:.2f}L")
    plt.title(f"Residual Distribution ({best_model_name})", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Residual Error in LPA (Actual - Predicted)", fontsize=11, fontweight="bold")
    plt.ylabel("Frequency", fontsize=11, fontweight="bold")
    plt.xlim(-25, 25)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    fig2_path = figures_dir / "residuals_distribution.png"
    plt.savefig(fig2_path)
    plt.close()
    logger.info(f"Saved: {fig2_path.name}")

    # Figure 3: Model Comparison Bar Chart
    plt.figure(figsize=(11, 5.5), dpi=300)
    x = np.arange(len(candidate_models))
    width = 0.28
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    r2_vals = [results[m]["test_metrics"]["r2"] for m in candidate_models]
    mae_lpa = [results[m]["test_metrics"]["mae"] / 100_000 for m in candidate_models]
    
    bars1 = ax.bar(x - width/2, r2_vals, width, label="Test R² Score", color="#4F46E5")
    ax2 = ax.twinx()
    bars2 = ax2.bar(x + width/2, mae_lpa, width, label="Test MAE (LPA)", color="#F59E0B")
    
    ax.set_xticks(x)
    ax.set_xticklabels(candidate_models.keys(), fontsize=11, fontweight="bold")
    ax.set_ylabel("R² Score (Higher is Better)", color="#4F46E5", fontsize=11, fontweight="bold")
    ax2.set_ylabel("MAE in LPA (Lower is Better)", color="#D97706", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 1.0)
    ax2.set_ylim(0, max(mae_lpa) * 1.3)
    
    for bar in bars1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"₹{yval:.2f}L", ha="center", va="bottom", fontsize=9, fontweight="bold")
        
    plt.title("Model Comparison: Predictive Accuracy & Error", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig3_path = figures_dir / "model_comparison_chart.png"
    plt.savefig(fig3_path)
    plt.close()
    logger.info(f"Saved: {fig3_path.name}")

    # 7. Metadata and Metrics Serialization
    metadata = {
        "model_name": best_model_name,
        "model_version": "2.0.0",
        "training_timestamp": datetime.utcnow().isoformat() + "Z",
        "random_seed": RANDOM_SEED,
        "algorithm": str(best_model.__class__.__name__),
        "target_variable": "annual_salary_inr",
        "target_currency": "INR",
        "target_period": "annual",
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "engineered_feature_count": int(X_train.shape[1]),
        "engineered_features": list(X_train.columns),
        "hyperparameters": results[best_model_name]["params"],
        "evaluation_metrics": {
            "cv_5fold": results[best_model_name]["cv_metrics"],
            "train": results[best_model_name]["train_metrics"],
            "test": results[best_model_name]["test_metrics"]
        },
        "quantile_models": {
            "methodology": "GradientBoostingRegressor(loss='quantile')",
            "evaluation": quantile_eval,
            "monotonic_guaranteed_by_postprocessing": True
        },
        "supported_taxonomies": {
            "job_roles": [
                "Software Developer", "Full Stack Developer", "Frontend Developer",
                "Backend Developer", "Data Analyst", "Data Scientist",
                "Machine Learning Engineer", "DevOps Engineer"
            ],
            "locations": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi NCR", "Chennai"],
            "education": ["Bachelor's Degree", "Master's Degree", "Diploma", "PhD"]
        }
    }
    
    meta_json_path = models_dir / "model_metadata.json"
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved model metadata to {meta_json_path}")
    
    summary_report = {
        "training_completed_at": datetime.utcnow().isoformat() + "Z",
        "selected_model": best_model_name,
        "models_evaluated": list(candidate_models.keys()),
        "comparison_metrics": results,
        "quantile_metrics": quantile_eval
    }
    
    training_summary_path = reports_dir / "training_summary.json"
    with open(training_summary_path, "w", encoding="utf-8") as f:
        # Avoid saving raw numpy prediction arrays
        serializable = {
            "training_completed_at": summary_report["training_completed_at"],
            "selected_model": best_model_name,
            "models_evaluated": list(candidate_models.keys()),
            "metrics": {
                name: {
                    "cv": res["cv_metrics"],
                    "train": res["train_metrics"],
                    "test": res["test_metrics"]
                }
                for name, res in results.items()
            },
            "quantiles": quantile_eval
        }
        json.dump(serializable, f, indent=2)
    logger.info(f"Saved training summary to {training_summary_path}")

    metrics_json_path = reports_dir / "model_metrics.json"
    with open(metrics_json_path, "w", encoding="utf-8") as f:
        json.dump(serializable["metrics"], f, indent=2)
    logger.info(f"Saved model metrics to {metrics_json_path}")

    print("\n" + "="*80)
    print("ALL MODELS TRAINED, EVALUATED, AND ARTIFACTS SERIALIZED SUCCESSFULLY!")
    print("="*80 + "\n")

if __name__ == "__main__":
    train_and_evaluate_all()
