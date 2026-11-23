# WorthIQ — Machine Learning Model Report
## Phase 2 Part 2: Supervised Regression & Quantile Range Estimation

**Project:** WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer  
**Artifact Version:** 2.0.0  
**Target Variable:** `annual_salary_inr` (Trained in $\log(1+y)$ space, evaluated on original INR scale)  
**Sample Sizes:** $N_{total} = 25,332$, $N_{train} = 20,265$, $N_{test} = 5,067$ (80/20 Stratified Split)  
**Engineered Features:** 55 dimensions (One-Hot Roles & Locations, Multi-Label Binary Skills, Continuous Experience & Rating)

---

## 1. Executive Summary

In Phase 2 Part 2, three supervised regression algorithms were implemented, benchmarked, and evaluated under identical 5-fold cross-validation and holdout test splits on 25,332 verified Indian tech compensation records:
1. **Linear Regression (Baseline OLS)**
2. **Random Forest Regressor (Nonlinear Ensemble)**
3. **XGBoost Regressor (Gradient Boosted Decision Trees)**

In addition, three dedicated quantile regression models ($\alpha = 0.10, 0.50, 0.90$) were trained using gradient boosted quantile loss (Pinball Loss) to compute statistically sound salary ranges (Conservative $P10$, Median $P50$, Top Tier $P90$) rather than assuming unrealistic symmetric Gaussian distributions.

**Winning Model:** **Random Forest Regressor** achieved superior generalization, achieving a 5-fold Cross-Validation MAE of **₹3,35,066** ($R^2 = 0.4109$) and Test MAE of **₹3,51,027** ($R^2 = 0.3597$, Median Absolute Error = ₹2,15,291). It was selected and exported as the primary production engine (`ml/models/salary_model.joblib`).

---

## 2. Model Comparison Matrix

The table below summarizes the empirical evaluation metrics across all candidate models:

| Metric | Linear Regression | XGBoost Regressor | Random Forest (Winner) |
|---|---|---|---|
| **CV MAE (5-Fold)** | ₹3,55,217 | ₹3,35,819 | **₹3,35,066** |
| **CV RMSE (5-Fold)** | ₹5,75,116 | ₹5,56,434 | **₹5,56,273** |
| **CV $R^2$ (5-Fold)** | 0.3703 | 0.4105 | **0.4109** |
| **Test MAE (Holdout)** | ₹3,71,270 | ₹3,51,741 | **₹3,51,026** |
| **Test RMSE (Holdout)** | ₹6,26,449 | ₹6,08,385 | **₹6,07,555** |
| **Test $R^2$ (Holdout)** | 0.3193 | 0.3580 | **0.3597** |
| **Test Median AE (MedAE)** | ₹2,27,840 | ₹2,15,888 | **₹2,15,291** |
| **Test MAPE (%)** | 58.74% | 55.62% | **55.58%** |
| **Training Latency** | 0.12s | 3.42s | 18.25s |
| **Inference Latency** | < 1 ms | < 1 ms | ~ 2.5 ms |

---

## 3. Winning Model Details: Random Forest Regressor

### 3.1 Hyperparameter Configuration
- `n_estimators`: 150
- `max_depth`: 16
- `min_samples_split`: 4
- `min_samples_leaf`: 2
- `random_state`: 42
- `n_jobs`: -1

### 3.2 Key Error Analysis
- **Median Absolute Error (MedAE):** ₹2.15 Lakhs. While the mean absolute error is ₹3.51 Lakhs due to high-earning long-tail compensation outliers (>₹40L), the median error demonstrates that 50% of predictions fall within ₹2.15L of actual compensation.
- **Log Target Transformation:** Training in $\log(1 + y)$ stabilized heteroscedasticity across experience tiers and strictly prevented negative salary estimates when taking $\exp(\hat{y}) - 1$.
- **Residual Distribution:** Residuals are bell-shaped and centered around zero, confirming zero structural bias across junior, mid-level, and senior experience brackets.

---

## 4. Quantile Regression Performance

To predict reliable compensation bands without assuming symmetric Gaussian distributions, three Gradient Boosting Regressors were trained using pinball loss $L_\alpha(y, \hat{y}) = \max(\alpha(y - \hat{y}), (\alpha - 1)(y - \hat{y}))$:

| Quantile | Target Alpha ($\alpha$) | Empirical Coverage on Test Set | Pinball Loss (INR) | Interpretation |
|---|---|---|---|---|
| **$P10$** | 0.10 (10th percentile) | **10.20%** (Expected 10.0%) | ₹52,653 | Conservative Floor (Entry-level peer baseline) |
| **$P50$** | 0.50 (50th percentile) | **48.10%** (Expected 50.0%) | ₹175,157 | Market Median (Central compensation target) |
| **$P90$** | 0.90 (90th percentile) | **89.30%** (Expected 90.0%) | ₹124,283 | Top Tier Ceiling (High-performing product companies) |

### Monotonicity Guarantee
To guarantee logical ordering across all input combinations and prevent crossing ($P10 \le P50 \le P90$), post-inference monotonicity enforcement is applied:
$$\text{low} = \min(P10, P50), \quad \text{high} = \max(P90, P50)$$

---

## 5. Feature Importance & Coefficients

Top feature importances derived from Random Forest:
1. `years_of_experience`: **48.2%** — Dominant single determinant of compensation.
2. `job_role_Data Scientist` & `job_role_Machine Learning Engineer`: **11.4%** combined.
3. `location_Bengaluru`: **6.8%** — Premier tech hub geographic premium.
4. `skill__kubernetes`, `skill__docker`, `skill__aws`: **9.1%** combined — Cloud infrastructure premiums.
5. `skill__machine_learning`, `skill__python`: **5.3%** combined.
6. `location_Hyderabad` & `location_Pune`: **4.2%** combined.

---

## 6. Model Limitations & Governance

1. **Long-Tail Outliers:** Tech compensation above ₹40 LPA in India typically incorporates Variable Bonuses and Stock Options (ESOPs/RSUs), which exhibit higher variance than base cash salary.
2. **Taxonomy Scope:** Inputs outside the primary 8 tech roles and 6 metro hubs are automatically normalized to their closest semantic equivalent, and the prediction confidence score is downgraded accordingly.
3. **Historical Calibration:** Data reflects compensation benchmarks up to late 2026 and should be periodically retrained using the instructions in `docs/MODEL_TRAINING_GUIDE.md`.
