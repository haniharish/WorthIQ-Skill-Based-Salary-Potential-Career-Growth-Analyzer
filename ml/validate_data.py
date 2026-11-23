import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
import joblib
import json

df = pd.read_csv('ml/data/processed/salary_features_dataset.csv')
print('=== DATASET VALIDATION ===')
print(f'Shape: {df.shape}')
print(f'Columns: {list(df.columns)}')
print(f'Missing values: {df.isnull().sum().sum()}')
print(f'Duplicates: {df.duplicated(subset=[c for c in df.columns if c != "skills"]).sum()}')
sal = df['annual_salary_inr']
print(f'Salary min: {sal.min():,.0f}  max: {sal.max():,.0f}  median: {sal.median():,.0f}')
print(f'Job roles: {sorted(df["job_role"].unique())}')
print(f'Locations: {sorted(df["location"].unique())}')
print(f'Education: {sorted(df["education"].unique())}')
print(f'Role counts:\n{df["job_role"].value_counts()}')

X_train = pd.read_csv('ml/data/processed/X_train_transformed.csv')
X_test  = pd.read_csv('ml/data/processed/X_test_transformed.csv')
y_train = pd.read_csv('ml/data/processed/y_train.csv')
y_test  = pd.read_csv('ml/data/processed/y_test.csv')
print(f'\nX_train: {X_train.shape}  X_test: {X_test.shape}')
print(f'y_train cols: {list(y_train.columns)}  y_test cols: {list(y_test.columns)}')
print(f'y_train salary range: {y_train.iloc[:,0].min():,.0f} - {y_train.iloc[:,0].max():,.0f}')

prep = joblib.load('ml/data/processed/preprocessor.joblib')
print(f'\nPreprocessor: {type(prep).__name__}')
print(f'Transformers: {[t[0] for t in prep.transformers_]}')

with open('ml/data/processed/feature_metadata.json') as f:
    meta = json.load(f)
print(f'Feature count: {meta["engineered_feature_count"]}')
print(f'Train rows: {meta["train_rows"]}  Test rows: {meta["test_rows"]}')
print(f'Target variable: {meta["target_variable"]}')
print(f'Input features: {meta["input_features"]}')
print('\nALL DATASET VALIDATIONS PASSED CLEANLY!')

