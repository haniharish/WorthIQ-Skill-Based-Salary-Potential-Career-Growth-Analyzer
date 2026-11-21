# WorthIQ — Dataset Sources and Provenance Documentation
**Phase 2 Part 1: Dataset Collection, Data Cleaning, and Feature Engineering**

This document provides complete provenance, source verification, and structural documentation for all datasets acquired and evaluated for the **WorthIQ: Skill-Based Salary Potential & Career Growth Analyzer** machine learning pipeline.

---

## 1. Executive Summary of Acquired Datasets

To ensure authentic representation of the Indian technology job market without synthetic hallucination, WorthIQ employs real-world industry compensation and employment datasets acquired from verified open-access repositories.

| Dataset Identifier | Primary Source | Coverage | Original Records | Acquired Size | SHA-256 Checksum Prefix |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Salary_Dataset_with_Extra_Features.csv`** | Glassdoor / AmbitionBox (Sourav Banerjee, Kaggle) | Indian Software Professionals (Tier-1 Tech Hubs) | 22,770 | 1.79 MB | `638831692a8b7e48...` |
| **`ds_salaries.csv`** | ai-jobs.net / Kaggle (Data Science Salaries 2023) | Data Science, ML & Data Analytics Specialists | 3,755 | 210 KB | `b156e54135634169...` |
| **`devops_salaries.csv`** | devops-jobs.net (DevOps & Cloud Engineering) | DevOps, Site Reliability, and Platform Engineers | 728 | 45 KB | `2694b913a430e7e2...` |

---

## 2. Primary Dataset Specification

### Dataset 1: Indian Software Professional Salaries 2022
- **Filename**: `ml/data/raw/Salary_Dataset_with_Extra_Features.csv`
- **Original Source**: Kaggle — *Software Professional Salaries 2022* by Sourav Banerjee
- **Public Mirror URL**: `https://raw.githubusercontent.com/ntclai/Analysis-on-Software-Industry-in-India/main/Salary_Dataset_with_Extra_Features.csv`
- **License**: Open Database License (ODbL) / Public Domain for Research and Educational Use
- **Original Shape**: 22,770 rows × 8 columns
- **Original Format**: Comma-Separated Values (UTF-8)

#### Original Schema
1. `Rating` (Float64): Company rating on a 1.0 to 5.0 scale (0 missing values, 41 unique ratings).
2. `Company Name` (Object): Registered corporate entity or tech employer (1 missing value, 11,260 unique entities).
3. `Job Title` (Object): Specific organizational job title reported by employee (1,080 unique titles, e.g. "Software Development Engineer", "Senior Android Developer", "Software Development Engineer - Intern").
4. `Salary` (Int64): Reported compensation (numeric integer, predominantly annual INR).
5. `Salaries Reported` (Int64): Number of verified compensation submissions for the role at that employer.
6. `Location` (Object): Indian metropolitan location (10 unique locations, top hubs: Bangalore, Hyderabad, New Delhi, Chennai, Pune, Mumbai).
7. `Employment Status` (Object): Employment contract category ("Full Time": 20,083, "Intern": 2,106, "Contractor": 548, "Trainee": 33).
8. `Job Roles` (Object): Broad technology classification ("SDE": 8,183, "Android": 2,945, "Frontend": 2,163, "Java": 1,858, "Testing": 1,740, "IOS": 1,631, "Backend": 1,194, "Web": 999, "Python": 947, "Database": 865, "Mobile": 245).

#### Suitability for WorthIQ
- **Strengths**: Dense coverage across core software engineering, frontend, backend, full stack, mobile, and QA roles in Indian tech hubs (Bengaluru, Hyderabad, Pune, Mumbai, Delhi NCR, Chennai). Direct annual INR figures matching Indian market realities.
- **Identified Limitations & Remediation**: Under-represented in specialized modern AI/ML and Cloud/DevOps roles. Remediated via integration of secondary datasets.

---

## 3. Secondary Dataset Specifications

### Dataset 2: Data Science & Machine Learning Salaries
- **Filename**: `ml/data/raw/ds_salaries.csv`
- **Original Source**: ai-jobs.net open salary survey / Kaggle 2023 edition
- **Public Mirror URL**: `https://raw.githubusercontent.com/JorgeMiGo/Data-Science-Salaries-2023/main/Dataset/ds_salaries.csv`
- **License**: CC0: Public Domain
- **Original Shape**: 3,755 rows × 11 columns
- **Target Roles Sourced**: `Data Scientist` (840), `Data Analyst` (612), `Machine Learning Engineer` (289).
- **Compensation Normalization**: Directly utilizes reported INR compensation for Indian resident records (`employee_residence == 'IN'`). For international role benchmarks, compensation is calibrated to the Indian tech market tier.

### Dataset 3: DevOps & Cloud Engineering Salaries
- **Filename**: `ml/data/raw/devops_salaries.csv`
- **Original Source**: devops-jobs.net salary repository
- **Public Mirror URL**: `https://raw.githubusercontent.com/ShiaraRF/devops-jobs-net-salaries/main/salaries.csv`
- **License**: MIT License
- **Original Shape**: 728 rows × 11 columns
- **Target Roles Sourced**: `DevOps Engineer` (234), `Site Reliability Engineer` (98), `Cloud Engineer` (39), `Platform Engineer` (19).

---

## 4. Acquisition Script & Provenance Tracking

Automated dataset acquisition is implemented in [ml/src/data/download_datasets.py](file:///c:/Users/Lenovo/Desktop/WorthIQ/ml/src/data/download_datasets.py).
The script validates each raw file against minimum byte thresholds and computes SHA-256 hashes to guarantee provenance and prevent corrupted or altered inputs.

```bash
python ml/src/data/download_datasets.py
```
Outputs are stored in `ml/data/raw/` and are treated as strictly immutable inputs.
