# WorthIQ — Phase 2 Part 1 Setup and Execution Guide
**ML Environment, Ingestion, Cleaning, EDA, and Feature Pipeline**

This guide provides reproducible, step-by-step instructions for running the complete Phase 2 Part 1 data engineering and ML preprocessing pipeline.

---

## 1. Prerequisites and Environment

- **Python Version**: Python 3.11+ (verified on Python 3.14.7 in `backend/venv`)
- **Required Packages**: Specified in [ml/requirements-ml.txt](file:///c:/Users/Lenovo/Desktop/WorthIQ/ml/requirements-ml.txt)
  - `numpy >= 1.26.0`
  - `pandas >= 2.2.0`
  - `scikit-learn >= 1.4.0`
  - `matplotlib >= 3.8.0`
  - `seaborn >= 0.13.0`
  - `scipy >= 1.12.0`
  - `joblib >= 1.3.0`
  - `pytest >= 8.0.0`

To install or verify ML dependencies:
```bash
# Inside project root
.\backend\venv\Scripts\pip install -r ml/requirements-ml.txt
```

---

## 2. Execution Sequence

The complete data engineering pipeline consists of four sequential, idempotent stages:

### Step 1: Raw Dataset Acquisition
Downloads real Indian software and tech compensation datasets into `ml/data/raw/` with SHA-256 validation:
```bash
.\backend\venv\Scripts\python.exe ml/src/data/download_datasets.py
```
*Expected Output*: Verified files in `ml/data/raw/` (`Salary_Dataset_with_Extra_Features.csv`, `ds_salaries.csv`, `devops_salaries.csv`).

### Step 2: Raw Dataset Inspection
Generates structural, type, and missing-value diagnostics:
```bash
.\backend\venv\Scripts\python.exe ml/src/data/inspect_datasets.py
```
*Expected Output*: Tables in `ml/reports/tables/raw_dataset_inspection.csv` and `raw_dataset_summary.json`.

### Step 3: Data Cleaning and Standardization Pipeline
Normalizes salary into annual INR, filters outliers, maps job roles into 8 standard tracks, standardizes cities into 6 tech hubs, derives experience, and maps 35 canonical skills:
```bash
.\backend\venv\Scripts\python.exe ml/src/preprocessing/clean_data.py
```
*Expected Output*:
- `ml/data/interim/cleaned_primary_salaries.csv`
- `ml/data/processed/salary_features_dataset.csv` (25,332 records)
- `ml/reports/tables/data_cleaning_metrics.json`
- `ml/reports/tables/salary_by_role_summary.csv`

### Step 4: Exploratory Data Analysis (EDA)
Generates high-resolution publication charts and statistical summary tables:
```bash
.\backend\venv\Scripts\python.exe ml/notebooks/01_exploratory_data_analysis.py
```
*Expected Output*: 7 figures in `ml/reports/figures/` and 4 tables in `ml/reports/tables/`.

### Step 5: Feature Engineering and Train/Test Splitting
Executes zero-leakage 80/20 train/test split, fits `ColumnTransformer` strictly on `X_train`, transforms feature matrices, and serializes the preprocessor:
```bash
.\backend\venv\Scripts\python.exe ml/src/features/prepare_train_test.py
```
*Expected Output*:
- `ml/data/processed/X_train_transformed.csv` (20,265 rows × 55 columns)
- `ml/data/processed/X_test_transformed.csv` (5,067 rows × 55 columns)
- `ml/data/processed/y_train.csv` (20,265 rows)
- `ml/data/processed/y_test.csv` (5,067 rows)
- `ml/data/processed/preprocessor.joblib`
- `ml/data/processed/feature_metadata.json`
- `ml/reports/tables/feature_target_correlations.csv`

---

## 3. Running Automated Tests

To execute the unit and integration test suite:
```bash
.\backend\venv\Scripts\pytest.exe ml/tests/test_data_pipeline.py -v
```
All 6 test cases must return `PASSED`.
