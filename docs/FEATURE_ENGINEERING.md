# WorthIQ — Feature Engineering and Preprocessing Documentation
**Phase 2 Part 1: Transformation Architecture, Pipelines, and Leakage Prevention**

This document specifies the feature engineering architecture, encoding strategies, pipeline serialization, and strict zero-leakage protocols implemented in the WorthIQ ML codebase.

---

## 1. Feature Engineering Architecture

The feature transformation pipeline is encapsulated in [ml/src/features/build_features.py](file:///c:/Users/Lenovo/Desktop/WorthIQ/ml/src/features/build_features.py) using a scikit-learn `ColumnTransformer`.

```
Raw Input Record:
[job_role, years_of_experience, location, education, skills_str, company_rating]
                               |
                               v
                    [ColumnTransformer]
      +------------------------+------------------------+
      |                        |                        |
[OneHotEncoder]        [StandardScaler]      [MultiLabelSkillsEncoder]
(job_role: 8)           (exp: 1, rating: 1)   (skills: 35)
(location: 6)
(education: 4)
      |                        |                        |
      v                        v                        v
  18 Features              2 Features               35 Features
      +------------------------+------------------------+
                               |
                               v
           Engineered Feature Vector (55 dimensions)
```

---

## 2. Transformer Specifications

### 2.1 Multi-Label Skills Encoder (`MultiLabelSkillsEncoder`)
- **Challenge**: Profiles possess a variable-length list of technical skills (e.g. `['Python', 'Django', 'PostgreSQL', 'Docker']`). Standard one-hot encoders cannot handle multi-label arrays without cross-talk or cardinality explosion.
- **Implementation**: A custom scikit-learn estimator adhering to the scikit-learn 1.9+ `BaseEstimator` / `TransformerMixin` API:
  - Canonical skills list (35 skills) mapped to fixed binary array indices.
  - Implements `.fit()`, `.transform()`, and `.get_feature_names_out()`.
  - Produces binary indicator vectors (`1.0` if skill present, `0.0` if absent).
  - Handles unseen or extra skills gracefully by ignoring them without crashing.

### 2.2 Categorical One-Hot Encoding (`OneHotEncoder`)
- Applied to `job_role`, `location`, and `education`.
- Configured with `handle_unknown="ignore"` and `sparse_output=False`.
- Prevents inference failure when encountering rare or novel categories in future user profiles.
- Generates 18 orthogonal binary indicator columns.

### 2.3 Numeric Standardization (`StandardScaler`)
- Applied to continuous features: `years_of_experience` and `company_rating`.
- Fits sample mean ($\mu$) and standard deviation ($\sigma$) **strictly on the training split**.
- Standardizes features to zero mean and unit variance ($z = \frac{x - \mu}{\sigma}$).

---

## 3. Strict Data Leakage Prevention Protocol

Data leakage can introduce severe optimistic bias into model evaluation. To guarantee absolute evaluation validity:

1. **Split-First Policy**:
   - The dataset is split into an 80% training set ($N = 20,265$) and a 20% test set ($N = 5,067$) **before** any fitting or scaling occurs.
   - Stratified by `job_role` with a fixed random seed (`random_state=42`).
2. **Train-Only Preprocessor Fitting**:
   - The `preprocessor` pipeline executes `.fit(X_train_raw)` exclusively on the training split.
   - The test set is transformed via `.transform(X_test_raw)` using the parameters learned from the training set.
3. **Artifact Isolation**:
   - Both unencoded raw splits (`X_train_raw.csv`, `X_test_raw.csv`) and transformed feature matrices (`X_train_transformed.csv`, `X_test_transformed.csv`) are saved separately.
   - Preprocessor state is serialized to `ml/data/processed/preprocessor.joblib`.

---

## 4. Top Engineered Features by Salary Correlation

Computed Pearson correlation coefficient ($r$) between the 55 engineered features and the target variable `annual_salary_inr` on the training set:

| Feature Name | Feature Category | Pearson $r$ | Impact Direction |
| :--- | :--- | :--- | :--- |
| **`skill__pandas`** | Skill Indicator | **+0.4811** | High positive premium (Data Science) |
| **`skill__numpy`** | Skill Indicator | **+0.4679** | High positive premium (Data Science) |
| **`skill__data_analysis`** | Skill Indicator | **+0.4277** | High positive premium (Analytics) |
| **`num__years_of_experience`** | Numeric Scaled | **+0.4250** | Strongest continuous predictor |
| **`job_role_Data Analyst`** | Categorical One-Hot | **+0.3610** | High base compensation tier |
| **`skill__machine_learning`** | Skill Indicator | **+0.3115** | Modern AI compensation premium |
| **`skill__scikit_learn`** | Skill Indicator | **+0.3115** | Predictive modeling premium |
| **`skill__python`** | Skill Indicator | **+0.2814** | Universal high-leverage language |
| **`job_role_Data Scientist`** | Categorical One-Hot | **+0.2690** | Specialized modeling track |
| **`skill__postgresql`** | Skill Indicator | **+0.1994** | Core backend data persistence |
| **`location_Bengaluru`** | Categorical One-Hot | **+0.1745** | Highest regional metro premium |
| **`skill__docker`** | Skill Indicator | **+0.1412** | Cloud/DevOps infrastructure premium |
| **`num__company_rating`** | Numeric Scaled | **+0.0821** | Modest employer quality premium |
| **`location_Chennai`** | Categorical One-Hot | **-0.0912** | Lower cost-of-living market |
| **`job_role_Frontend Developer`**| Categorical One-Hot | **-0.1852** | High volume, junior-heavy tier |
| **`job_role_Software Developer`**| Categorical One-Hot | **-0.2104** | Anchored by mass-market IT services |

---

## 5. Artifact Summary

- **Preprocessor Bundle**: `ml/data/processed/preprocessor.joblib` (12.4 KB)
- **Feature Metadata**: `ml/data/processed/feature_metadata.json`
- **Correlation Table**: `ml/reports/tables/feature_target_correlations.csv`
- **Feature Matrices**:
  - `X_train_transformed.csv` (20,265 rows × 55 columns)
  - `X_test_transformed.csv` (5,067 rows × 55 columns)
  - `y_train.csv` (20,265 rows × 1 column)
  - `y_test.csv` (5,067 rows × 1 column)
