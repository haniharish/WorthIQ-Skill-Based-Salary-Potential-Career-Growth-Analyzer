import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error

def validate_ml():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    processed_dir = os.path.join(base_dir, 'ml', 'data', 'processed')
    models_dir = os.path.join(base_dir, 'ml', 'models')

    print("Loading test dataset and model artifacts...")
    X_test_raw = pd.read_csv(os.path.join(processed_dir, 'X_test_raw.csv'))
    X_test_trans = pd.read_csv(os.path.join(processed_dir, 'X_test_transformed.csv'))
    y_df = pd.read_csv(os.path.join(processed_dir, 'y_test.csv'))
    y_col = 'annual_salary_inr' if 'annual_salary_inr' in y_df.columns else y_df.columns[0]
    y_test = y_df[y_col].values

    # Load models
    rf_model = joblib.load(os.path.join(models_dir, 'salary_model.joblib'))
    p10_model = joblib.load(os.path.join(models_dir, 'quantile_models', 'quantile_p10.joblib'))
    p50_model = joblib.load(os.path.join(models_dir, 'quantile_models', 'quantile_p50.joblib'))
    p90_model = joblib.load(os.path.join(models_dir, 'quantile_models', 'quantile_p90.joblib'))

    print(f"Test samples count: {len(y_test)}")

    # 1. Random Forest Predictions (trained in log space)
    y_pred_log = rf_model.predict(X_test_trans)
    y_pred_rf = np.maximum(0, np.expm1(y_pred_log))

    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)
    medae_rf = median_absolute_error(y_test, y_pred_rf)

    # 2. Quantile Predictions (trained in log space)
    y_pred_p10 = np.maximum(0, np.expm1(p10_model.predict(X_test_trans)))
    y_pred_p50 = np.maximum(0, np.expm1(p50_model.predict(X_test_trans)))
    y_pred_p90 = np.maximum(0, np.expm1(p90_model.predict(X_test_trans)))

    cov_p10 = np.mean(y_test <= y_pred_p10) * 100.0
    cov_p50 = np.mean(y_test <= y_pred_p50) * 100.0
    cov_p90 = np.mean(y_test <= y_pred_p90) * 100.0
    cov_interval_80 = np.mean((y_test >= y_pred_p10) & (y_test <= y_pred_p90)) * 100.0
    crossing_violations = int(np.sum((y_pred_p10 > y_pred_p50) | (y_pred_p50 > y_pred_p90)))

    # 3. Subgroup analysis by Experience
    exp_col = X_test_raw['years_of_experience'].values
    exp_brackets = {
        "Entry Level (0-2 yrs)": (exp_col <= 2.0),
        "Mid Level (2-5 yrs)": ((exp_col > 2.0) & (exp_col <= 5.0)),
        "Senior Level (5-10 yrs)": ((exp_col > 5.0) & (exp_col <= 10.0)),
        "Staff/Lead (10+ yrs)": (exp_col > 10.0)
    }

    subgroup_exp = {}
    for label, mask in exp_brackets.items():
        if np.sum(mask) > 0:
            subgroup_exp[label] = {
                "count": int(np.sum(mask)),
                "mae_inr": float(mean_absolute_error(y_test[mask], y_pred_rf[mask])),
                "rmse_inr": float(np.sqrt(mean_squared_error(y_test[mask], y_pred_rf[mask]))),
                "r2": float(r2_score(y_test[mask], y_pred_rf[mask])),
                "mean_actual_lpa": float(np.mean(y_test[mask]) / 100000.0),
                "mean_pred_lpa": float(np.mean(y_pred_rf[mask]) / 100000.0),
            }

    # 4. Subgroup analysis by Job Role
    role_col = X_test_raw['job_role'].values
    unique_roles = np.unique(role_col)
    subgroup_roles = {}
    for role in unique_roles:
        mask = (role_col == role)
        if np.sum(mask) >= 20: # statistically valid sample
            subgroup_roles[role] = {
                "count": int(np.sum(mask)),
                "mae_inr": float(mean_absolute_error(y_test[mask], y_pred_rf[mask])),
                "rmse_inr": float(np.sqrt(mean_squared_error(y_test[mask], y_pred_rf[mask]))),
                "r2": float(r2_score(y_test[mask], y_pred_rf[mask])),
            }

    # Summary Result
    results = {
        "dataset_size_test": len(y_test),
        "metrics_rf": {
            "mae_inr": float(mae_rf),
            "mae_lpa": float(mae_rf / 100000.0),
            "rmse_inr": float(rmse_rf),
            "rmse_lpa": float(rmse_rf / 100000.0),
            "r2_score": float(r2_rf),
            "medae_inr": float(medae_rf),
            "medae_lpa": float(medae_rf / 100000.0)
        },
        "quantile_calibration": {
            "empirical_coverage_p10_pct": float(cov_p10),
            "empirical_coverage_p50_pct": float(cov_p50),
            "empirical_coverage_p90_pct": float(cov_p90),
            "empirical_interval_80_pct": float(cov_interval_80)
        },
        "subgroup_experience": subgroup_exp,
        "subgroup_roles": subgroup_roles
    }

    out_json = os.path.join(base_dir, 'testing', 'reports', 'ml', 'ml_validation_metrics.json')
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=2)

    print("\n--- ML MODEL EVALUATION RESULTS ---")
    print(f"Samples: {len(y_test)}")
    print(f"R^2 Score: {r2_rf:.4f}")
    print(f"MAE: Rs. {mae_rf:,.2f} ({mae_rf/100000.0:.2f} LPA)")
    print(f"RMSE: Rs. {rmse_rf:,.2f} ({rmse_rf/100000.0:.2f} LPA)")
    print(f"Median Absolute Error: Rs. {medae_rf:,.2f} ({medae_rf/100000.0:.2f} LPA)")
    print("\n--- QUANTILE CALIBRATION ---")
    print(f"P10 Empirical Coverage (nominal 10%): {cov_p10:.2f}%")
    print(f"P50 Empirical Coverage (nominal 50%): {cov_p50:.2f}%")
    print(f"P90 Empirical Coverage (nominal 90%): {cov_p90:.2f}%")
    print(f"[P10 - P90] 80% Confidence Interval Coverage: {cov_interval_80:.2f}%")

if __name__ == '__main__':
    validate_ml()
