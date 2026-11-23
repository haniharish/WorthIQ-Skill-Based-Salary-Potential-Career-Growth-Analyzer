# WorthIQ — Model Retraining & Deployment Guide
## Step-by-Step Instructions for Updating Compensation Models

**Project:** WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer  

---

## 1. Prerequisites & Virtual Environment

Ensure the backend Python virtual environment is activated and requirements are installed:

```bash
# Windows PowerShell
cd c:\Users\Lenovo\Desktop\WorthIQ
.\backend\venv\Scripts\Activate.ps1

# Install / update machine learning dependencies
pip install scikit-learn xgboost pandas numpy joblib matplotlib seaborn
```

---

## 2. Ingesting & Validating New Raw Data

When new salary records are acquired, place raw CSVs in `ml/data/raw/` and execute the feature engineering pipeline:

```bash
# Execute Phase 2 Part 1 data pipeline
python ml/src/data/clean_data.py
python ml/src/features/build_features.py
python ml/src/data/validate_data.py
```

Verify that `ml/data/processed/salary_features_dataset.csv` contains zero nulls in required columns and reflects valid positive salaries.

---

## 3. Retraining Regression & Quantile Models

Execute the unified training pipeline:

```bash
python ml/src/models/train_models.py
```

This automated script performs:
1. Stratified 80/20 train/test split with seed `42`.
2. Fits Linear Regression, Random Forest, and XGBoost with 5-fold cross-validation.
3. Automatically evaluates MAE, RMSE, $R^2$, and MedAE.
4. Selects the winning model based on lowest cross-validation MAE.
5. Fits Gradient Boosting Quantile Regressors for $\alpha = 0.10, 0.50, 0.90$.
6. Verifies empirical quantile coverage on the test set.
7. Saves production artifacts to `ml/models/`:
   - `salary_model.joblib`
   - `quantile_models/quantile_p10.joblib`
   - `quantile_models/quantile_p50.joblib`
   - `quantile_models/quantile_p90.joblib`
   - `model_metadata.json`
8. Generates diagnostic plots in `ml/reports/figures/`:
   - `actual_vs_predicted.png`
   - `residuals_distribution.png`
   - `model_comparison_chart.png`

---

## 4. Retraining Verification Checklist

After training finishes, verify the generated artifacts:

- [ ] `ml/models/salary_model.joblib` exists and is non-empty (>50MB).
- [ ] `ml/models/quantile_models/` contains all 3 quantile models.
- [ ] `ml/models/model_metadata.json` contains updated `training_timestamp` and metrics.
- [ ] Run automated ML tests:
  ```bash
  pytest ml/tests/
  ```
- [ ] Run Django prediction API integration tests:
  ```bash
  python backend/manage.py test apps.predictions.tests
  ```

---

## 5. Hot-Reloading in Django Service

The Django application uses an in-memory singleton cache (`ModelRegistry`). When model artifacts are replaced on disk, either:
1. Restart the Django development server (`manage.py runserver`).
2. Or call `ModelRegistry.reload()` in a Django shell session:
   ```python
   python backend/manage.py shell -c "from apps.predictions.services.model_loader import ModelRegistry; ModelRegistry.get_instance().reload()"
   ```
