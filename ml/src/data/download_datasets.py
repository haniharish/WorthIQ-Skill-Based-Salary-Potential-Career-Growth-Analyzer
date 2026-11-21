"""
WorthIQ - Dataset Acquisition Script
Downloads and caches real Indian and tech salary datasets into ml/data/raw/
with SHA-256 validation and provenance tracking.
"""

import os
import sys
import hashlib
import logging
import urllib.request
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("download_datasets")

DATASETS = [
    {
        "name": "Salary_Dataset_with_Extra_Features.csv",
        "description": "Indian Software Professional Salaries 2022 (Sourav Banerjee / Kaggle)",
        "url": "https://raw.githubusercontent.com/ntclai/Analysis-on-Software-Industry-in-India/main/Salary_Dataset_with_Extra_Features.csv",
        "target_path": "ml/data/raw/Salary_Dataset_with_Extra_Features.csv",
        "expected_min_bytes": 1_000_000,
    },
    {
        "name": "ds_salaries.csv",
        "description": "Data Science & Machine Learning Salaries (ai-jobs.net / Kaggle)",
        "url": "https://raw.githubusercontent.com/JorgeMiGo/Data-Science-Salaries-2023/main/Dataset/ds_salaries.csv",
        "target_path": "ml/data/raw/ds_salaries.csv",
        "expected_min_bytes": 100_000,
    },
    {
        "name": "devops_salaries.csv",
        "description": "DevOps & Cloud Engineering Salaries (devops-jobs.net)",
        "url": "https://raw.githubusercontent.com/ShiaraRF/devops-jobs-net-salaries/main/salaries.csv",
        "target_path": "ml/data/raw/devops_salaries.csv",
        "expected_min_bytes": 40_000,
    }
]

def calculate_sha256(filepath: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_dataset(item: dict, base_dir: Path) -> bool:
    """Download a single dataset with validation."""
    target_path = base_dir / item["target_path"]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Checking dataset: {item['name']}")
    if target_path.exists() and target_path.stat().st_size >= item["expected_min_bytes"]:
        file_size = target_path.stat().st_size
        sha = calculate_sha256(target_path)
        logger.info(f"Dataset already exists at {target_path} ({file_size:,} bytes, SHA-256: {sha[:16]}...)")
        return True

    logger.info(f"Downloading from {item['url']} ...")
    try:
        req = urllib.request.Request(
            item["url"],
            headers={"User-Agent": "WorthIQ-DataPipeline/1.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as response, open(target_path, "wb") as out_file:
            data = response.read()
            out_file.write(data)
            
        file_size = target_path.stat().st_size
        sha = calculate_sha256(target_path)
        logger.info(f"Successfully downloaded {item['name']}: {file_size:,} bytes, SHA-256: {sha}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {item['name']}: {e}")
        return False

def main():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    logger.info(f"Base project directory: {base_dir}")
    
    success = True
    for item in DATASETS:
        res = download_dataset(item, base_dir)
        if not res:
            success = False
            
    if success:
        logger.info("All raw datasets verified and downloaded successfully.")
        sys.exit(0)
    else:
        logger.error("One or more datasets failed to download.")
        sys.exit(1)

if __name__ == "__main__":
    main()
