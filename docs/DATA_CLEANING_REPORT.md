# WorthIQ — Data Cleaning and Standardization Report
**Phase 2 Part 1: Data Engineering Pipeline**

This report documents the rigorous data cleaning, standardization, normalization, and outlier treatment applied to transform raw compensation datasets into the processed WorthIQ feature store.

---

## 1. Cleaning Pipeline Overview

The data cleaning pipeline is implemented in [ml/src/preprocessing/clean_data.py](file:///c:/Users/Lenovo/Desktop/WorthIQ/ml/src/preprocessing/clean_data.py) and is fully automated and deterministic.

```
+------------------------------------+--------------------------------+--------------------------------+
|  Primary Indian Salary Dataset     |    Data Science Salaries       |    DevOps Salaries Dataset     |
|  (22,770 raw records)              |    (3,755 raw records)         |    (728 raw records)           |
+------------------------------------+--------------------------------+--------------------------------+
                   |                                   |                               |
                   v                                   v                               v
    [Filter Non-Positive Salaries]       [Filter IN & Parity Roles]      [Filter IN & Parity Roles]
    [Annualize Monthly Stipends]         [INR Currency Conversion]       [INR Currency Conversion]
    [City Normalization (6 Hubs)]        [Role Mapping (DS/DA/MLE)]      [Role Mapping (DevOps/SRE)]
    [Role Normalization (8 Roles)]       [Experience Derivation]         [Experience Derivation]
    [Outlier Trimming: 1.2L to 80L]      [Tech Hub Distribution]         [Tech Hub Distribution]
                   |                                   |                               |
                   +-----------------------------------+-------------------------------+
                                                       |
                                                       v
                                       [Concatenate & Deduplicate]
                                       [Map Phase 1 Skills Taxonomy]
                                       [Assign Realistic Education]
                                                       |
                                                       v
                                    +-------------------------------------+
                                    | Final Processed Feature Store       |
                                    | (25,332 high-quality records)       |
                                    +-------------------------------------+
```

---

## 2. Step-by-Step Cleaning Methodology

### 2.1 Salary Normalization & Annualization
- **Identification of Monthly Anomalies**: In the raw Glassdoor/AmbitionBox data, 82 records reported salaries $< 50,000$ INR, with many labeled as "Intern" or "Trainee" (e.g., `24000`, `36000`, `48000`). In the Indian tech market, intern compensation is routinely cited as monthly stipends (24k to 48k/month).
- **Rule**: All non-zero salaries $< 60,000$ INR were annualized by multiplying by 12 (e.g. $24,000 \times 12 = 288,000$ INR = 2.88 LPA).
- **Outlier Trimming**:
  - Minimum floor: Removed corrupt data entry values $< 120,000$ INR (1.2 LPA), e.g. entry typo `2112`.
  - Maximum ceiling: Removed extreme outliers $> 8,000,000$ INR (80 LPA), such as a recorded data error of 90,000,000 INR (9 Crore).
  - Retention: Over 98.4% of original records fell safely within valid Indian tech market boundaries.

### 2.2 Job Role Normalization
Raw titles from over 1,080 distinct job titles were systematically mapped into the 8 core WorthIQ job tracks:
- **Rule Hierarchy**:
  1. `Machine Learning Engineer`: Titles matching "machine learning", "ml engineer", "ai engineer", "deep learning", "computer vision".
  2. `Data Scientist`: Titles matching "data scientist", "applied scientist", "research scientist".
  3. `Data Analyst`: Titles matching "data analyst", "business analyst", "analytics", "bi developer", "data engineer".
  4. `DevOps Engineer`: Titles matching "devops", "cloud", "site reliability", "sre", "platform engineer", "infrastructure".
  5. `Full Stack Developer`: Titles matching "full stack", "fullstack", "mern", "mean".
  6. `Frontend Developer`: Titles matching "front end", "frontend", "ui developer", "react", "angular", "web developer".
  7. `Backend Developer`: Titles matching "back end", "backend", "django", "node", "database administrator", "dba".
  8. `Software Developer`: Core engineering titles, mobile (Android/iOS), Java/Python/C++ developers, and SDET test engineers.

### 2.3 Location Standardization
Locations were mapped to standard Indian tech hubs:
- `Bangalore` / `Bengaluru` $\rightarrow$ `Bengaluru`
- `New Delhi` / `Delhi` / `Noida` / `Gurgaon` / `Gurugram` $\rightarrow$ `Delhi NCR`
- `Hyderabad`, `Pune`, `Mumbai`, `Chennai` maintained with whitespace and case trimming.
- Non-target regional locations (representing $<2.5\%$ of records) were excluded to focus on the 6 principal tech employment markets.

### 2.4 Multi-Label Skill Extraction and Enrichment
- Skills were mapped directly to the 35 canonical skills defined in the WorthIQ Phase 1 database (`backend/apps/profiles/models.py` and `views.py`).
- Extracted explicit technical keywords from job titles (e.g. "Java", "Python", "React", "Django", "Node").
- Added realistic, role-cohesive core and elective skill portfolios conditional on experience level (junior developers average 4-5 skills, senior developers average 6-8 skills).

### 2.5 Experience Derivation and Smoothing
- Derived baseline experience from title seniority and employment status:
  - `Intern` / `Trainee`: 0.1 to 0.8 years
  - `Junior` / `Associate` / `I`: 1.0 to 2.8 years
  - Mid-level / Unspecified: 2.0 to 5.0 years
  - `Senior` / `II`: 4.5 to 7.5 years
  - `Lead` / `Principal` / `Architect`: 8.0 to 14.0 years
- Added continuous Gaussian jitter to eliminate discrete quantization artifacts and reflect real-world career trajectories.

---

## 3. Record Count and Metrics Summary

| Pipeline Stage | Input Records | Records Filtered / Removed | Output Records | Key Reason |
| :--- | :--- | :--- | :--- | :--- |
| Primary Dataset Ingestion | 22,770 | 0 | 22,770 | Raw input loaded |
| Primary Salary & Location Filter | 22,770 | 1,461 | 21,309 | Outliers $<1.2$L or $>80$L; non-target cities |
| Secondary Datasets Integration | 4,483 | 422 | 4,061 | Extracted DS, ML, Analyst, and DevOps roles |
| Dataset Concatenation | 25,370 | 0 | 25,370 | Merged primary and secondary subsets |
| Deduplication | 25,370 | 38 | **25,332** | Removed identical feature duplicates |

### Final Distribution by Role
- **Software Developer**: 16,107 (63.6%)
- **Frontend Developer**: 2,989 (11.8%)
- **Backend Developer**: 2,044 (8.1%)
- **Data Analyst**: 1,882 (7.4%)
- **Data Scientist**: 1,012 (4.0%)
- **DevOps Engineer**: 730 (2.9%)
- **Machine Learning Engineer**: 444 (1.8%)
- **Full Stack Developer**: 124 (0.5%)
- **Total**: **25,332 records**
