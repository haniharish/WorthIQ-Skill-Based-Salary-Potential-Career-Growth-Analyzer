# WorthIQ — Phase 2 Part 2 Technical Handoff Document
**From: Senior Data Engineer (Gemini 3.8 Flash)**  
**To: Senior Machine Learning Engineer / Software Architect (Claude Sonnet 4.6 Thinking)**  
**Project:** WorthIQ: Skill-Based Salary Potential & Career Growth Analyzer  
**Objective:** Model Training, Comparison, Evaluation, Explainability, Django Prediction API, and Frontend Integration  
**Date:** November 21, 2026  

---

## 1. Executive Summary & Starting State

Welcome to **Phase 2 Part 2** of WorthIQ. 

In **Phase 2 Part 1**, we built the complete data engineering foundation, dataset acquisition, cleaning, exploratory data analysis, and feature engineering pipeline.

### Current Machine Learning State
- **Cleaned Dataset**: 25,332 real records representing Indian software engineers, data scientists, ML engineers, and DevOps professionals.
- **Data Location**: `ml/data/processed/salary_features_dataset.csv`
- **Features Extracted**: 55 engineered numerical features.
- **Preprocessor Bundle**: Serialized scikit-learn `ColumnTransformer` at `ml/data/processed/preprocessor.joblib`.
- **Pre-split Sets**: Disjoint 80/20 train/test splits prepared with zero data leakage (`random_state=42`, stratified by `job_role`).
- **Tests Passing**: 6/6 tests passing in `ml/tests/test_data_pipeline.py`.
- **Phase 1 Status**: Unmodified and intact. Django running at port 8000, React running at port 5180, PostgreSQL running at port 5432.

---

## 2. Inventory of Existing ML Artifacts

All files you will need are located in `ml/data/processed/` and `ml/src/features/`:

| Artifact | File Path | Shape / Size | Description |
| :--- | :--- | :--- | :--- |
| **Transformed Train Features** | `ml/data/processed/X_train_transformed.csv` | 20,265 rows × 55 cols | Ready for direct model training |
| **Transformed Test Features** | `ml/data/processed/X_test_transformed.csv` | 5,067 rows × 55 cols | Held-out for unbiased evaluation |
| **Train Targets** | `ml/data/processed/y_train.csv` | 20,265 rows × 1 col | Continuous annual salary in INR |
| **Test Targets** | `ml/data/processed/y_test.csv` | 5,067 rows × 1 col | Continuous annual salary in INR |
| **Raw Unencoded Train** | `ml/data/processed/X_train_raw.csv` | 20,265 rows × 6 cols | Categorical + continuous string inputs |
| **Raw Unencoded Test** | `ml/data/processed/X_test_raw.csv` | 5,067 rows × 6 cols | Categorical + continuous string inputs |
| **Fitted Preprocessor** | `ml/data/processed/preprocessor.joblib` | 12.4 KB | Loaded directly to encode user profiles |
| **Feature Metadata** | `ml/data/processed/feature_metadata.json` | 3.5 KB | Schema, feature list, distribution metrics |

---

## 3. How to Load Data and the Preprocessor in Python

You can load the training matrices directly into Pandas or NumPy, or load the preprocessor to transform raw dictionary inputs:

```python
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 1. Load Transformed Feature Matrices
X_train = pd.read_csv("ml/data/processed/X_train_transformed.csv")
X_test = pd.read_csv("ml/data/processed/X_test_transformed.csv")
y_train = pd.read_csv("ml/data/processed/y_train.csv")["annual_salary_inr"]
y_test = pd.read_csv("ml/data/processed/y_test.csv")["annual_salary_inr"]

# 2. Recommended: Log-transform target for training
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)

# 3. Load the Fitted Preprocessor Bundle
preprocessor = joblib.load("ml/data/processed/preprocessor.joblib")

# 4. Transform a new raw user profile (e.g. from API request)
sample_profile = pd.DataFrame([{
    "job_role": "Backend Developer",
    "years_of_experience": 4.0,
    "location": "Bengaluru",
    "education": "Bachelor's Degree",
    "skills_str": "Python;Django;PostgreSQL;Docker;Git;REST APIs",
    "company_rating": 4.1
}])
X_new = preprocessor.transform(sample_profile) # Shape: (1, 55)
```

---

## 4. Exact Engineered Features Ordering (55 Features)

The 55 output columns from `preprocessor.transform()` are strictly ordered as follows:

```
[00-07] Categorical One-Hot: job_role
        - job_role_Backend Developer
        - job_role_Data Analyst
        - job_role_Data Scientist
        - job_role_DevOps Engineer
        - job_role_Frontend Developer
        - job_role_Full Stack Developer
        - job_role_Machine Learning Engineer
        - job_role_Software Developer

[08-13] Categorical One-Hot: location
        - location_Bengaluru
        - location_Chennai
        - location_Delhi NCR
        - location_Hyderabad
        - location_Mumbai
        - location_Pune

[14-17] Categorical One-Hot: education
        - education_Bachelor's Degree
        - education_Diploma
        - education_Master's Degree
        - education_PhD

[18-19] Continuous Scaled: num
        - num__years_of_experience  (z-score standardized)
        - num__company_rating       (z-score standardized)

[20-54] Multi-Label Binary Indicators: skill__ (35 Canonical Skills)
        - skill__aws, skill__cpp, skill__ci_cd, skill__css3, skill__data_analysis
        - skill__django, skill__docker, skill__express_js, skill__fastapi, skill__flutter
        - skill__git, skill__go, skill__graphql, skill__html5, skill__java
        - skill__javascript, skill__kubernetes, skill__linux, skill__machine_learning
        - skill__microservices, skill__mongodb, skill__next_js, skill__node_js
        - skill__numpy, skill__pandas, skill__postgresql, skill__python, skill__rest_apis
        - skill__react_js, skill__redis, skill__sql, skill__scikit_learn
        - skill__spring_boot, skill__tailwind_css, skill__typescript
```

---

## 5. Machine Learning Models to Train in Part 2

You are requested to implement, benchmark, and compare the following model families:

1. **Baseline Regularized Linear Models**:
   - `Ridge(alpha=1.0)` / `Lasso(alpha=0.01)` / `ElasticNet`
   - Purpose: Baseline benchmark and coefficient interpretability.
2. **Non-Linear Tree Ensemble**:
   - `RandomForestRegressor(n_estimators=150, max_depth=16, random_state=42)`
   - Purpose: Captures feature interactions without strict linearity assumptions.
3. **Gradient Boosted Decision Trees**:
   - `XGBoost` (`XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6)`)
   - `LightGBM` (`LGBMRegressor`)
   - Expected winner in predictive accuracy and inference speed.

### Target Space Recommendation
- **Train in Log Space**: Fit models on $y_{\text{train\_log}} = \log(1 + y_{\text{train}})$.
- **Predict in Linear Space**: Compute $\hat{y} = \exp(\hat{y}_{\text{log}}) - 1$.
- *Rationale*: Solves right-skewness, stabilizes heteroscedastic residuals, and prevents negative salary predictions.

### Evaluation Metrics to Compare
- **$R^2$ Score** (Coefficient of determination)
- **RMSE** (Root Mean Squared Error in INR)
- **MAE** (Mean Absolute Error in INR)
- **MedAE** (Median Absolute Error in INR — robust to outliers)
- **MAPE** (Mean Absolute Percentage Error, e.g. $< 15\%$)

---

## 6. Explainability and Salary Band Specifications

In Part 2, WorthIQ requires explainable predictions:

### 1. Salary Confidence Bands
For a prediction $\hat{y}$:
- **Median Estimated Salary**: $\hat{y}$
- **Low Salary Estimate**: $\hat{y} \times 0.82$ (or 15th percentile / prediction interval)
- **High Salary Estimate**: $\hat{y} \times 1.25$ (or 85th percentile / prediction interval)
- **Confidence Score**: Inverse function of residual variance, e.g. $88\% - 95\%$.

### 2. Skill Impact Analysis
- Use Tree SHAP (`shap.TreeExplainer` on XGBoost or Random Forest) or marginal feature perturbation:
  - Calculate marginal $\Delta \text{Salary}$ for each skill currently possessed by user.
  - Calculate recommended skill additions ($\Delta \text{Salary}$ if user adds `Docker`, `Kubernetes`, `AWS`, or `Next.js`).

---

## 7. Django Backend Integration Requirements

Create a new Django app or endpoints in `backend/apps/predictions/`:
- **Endpoint**: `POST /api/predictions/predict/`
- **Request Payload**:
  ```json
  {
    "job_role": "Backend Developer",
    "years_of_experience": 3.5,
    "location": "Bengaluru",
    "education": "Bachelor's Degree",
    "skills": ["Python", "Django", "PostgreSQL", "Docker", "Git"]
  }
  ```
- **Response Format**:
  ```json
  {
    "predicted_salary": 950000,
    "salary_lpa": 9.5,
    "salary_range": {
      "low": 780000,
      "median": 950000,
      "high": 1180000
    },
    "confidence_score": 0.89,
    "top_contributing_skills": [
      {"skill": "Python", "impact_inr": 120000},
      {"skill": "Django", "impact_inr": 85000},
      {"skill": "Docker", "impact_inr": 95000}
    ],
    "high_value_skills_to_learn": [
      {"skill": "FastAPI", "potential_gain_inr": 140000},
      {"skill": "AWS", "potential_gain_inr": 180000}
    ]
  }
  ```

---

## 8. Frontend React Integration Requirements

In `frontend/src/`:
- Integrate prediction calls into the WorthIQ SaaS dashboard.
- Display:
  - Big KPI salary cards: Estimated Market Value, Range (Low/High).
  - Career Trajectory interactive chart using Recharts.
  - Skill Premium & Value-Add simulation sliders ("What if I learn Docker?").

All ML foundations in `ml/` are verified, reproducible, and ready for you to build upon. Good luck with Phase 2 Part 2!
