"""
WorthIQ - Dataset Inspection Script
Analyzes raw datasets in ml/data/raw/ and generates comprehensive structural
and statistical reports in ml/reports/tables/.
"""

import os
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("inspect_datasets")

def inspect_dataset(filepath: Path, output_dir: Path):
    logger.info(f"Inspecting raw dataset at: {filepath}")
    df = pd.read_csv(filepath)
    rows, cols = df.shape
    
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    
    inspection_df = pd.DataFrame({
        "dataset": filepath.name,
        "column_name": df.columns,
        "dtype": [str(d) for d in df.dtypes],
        "non_null_count": df.notnull().sum().values,
        "missing_count": missing_counts.values,
        "missing_percentage": missing_pct.values.round(2),
        "unique_values_count": [df[c].nunique() for c in df.columns],
        "sample_value": [str(df[c].dropna().iloc[0]) if df[c].notnull().any() else "" for c in df.columns]
    })
    
    summary_data = {
        "file_name": filepath.name,
        "row_count": int(rows),
        "column_count": int(cols),
        "columns": list(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_summary": {c: int(missing_counts[c]) for c in df.columns},
        "sample_rows": df.head(3).to_dict(orient="records")
    }
    
    return inspection_df, summary_data

def main():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    raw_dir = base_dir / "ml" / "data" / "raw"
    output_dir = base_dir / "ml" / "reports" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    files = [
        raw_dir / "Salary_Dataset_with_Extra_Features.csv",
        raw_dir / "ds_salaries.csv",
        raw_dir / "devops_salaries.csv"
    ]
    
    all_inspections = []
    summaries = {}
    
    for f in files:
        if f.exists():
            insp_df, summary = inspect_dataset(f, output_dir)
            all_inspections.append(insp_df)
            summaries[f.name] = summary
        else:
            logger.warning(f"File not found: {f}")
            
    if all_inspections:
        combined_inspection = pd.concat(all_inspections, ignore_index=True)
        table_path = output_dir / "raw_dataset_inspection.csv"
        combined_inspection.to_csv(table_path, index=False)
        logger.info(f"Saved combined inspection table to {table_path}")
        
        json_path = output_dir / "raw_dataset_summary.json"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(summaries, jf, indent=2, default=str)
        logger.info(f"Saved inspection summary JSON to {json_path}")
        
        print("\n" + "="*70)
        print("ALL DATASETS INSPECTION COMPLETED")
        print("="*70)
        for name, summ in summaries.items():
            print(f"- {name}: {summ['row_count']:,} rows, {summ['column_count']} columns, {summ['duplicate_rows']} duplicates")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()
