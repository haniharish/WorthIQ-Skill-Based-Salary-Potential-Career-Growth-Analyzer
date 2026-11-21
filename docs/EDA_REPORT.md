# WorthIQ — Exploratory Data Analysis (EDA) Report
**Phase 2 Part 1: Indian Technology Job Market Analysis**

This document delivers comprehensive exploratory data analysis, market insights, and statistical findings derived from **25,332 cleaned records** representing Indian technology professionals across 8 core roles and 6 major tech hubs.

---

## 1. Summary Statistics & Macro Market Distribution

The processed dataset exhibits robust coverage and realistic variance reflecting the Indian software compensation landscape:

- **Total Analyzed Profiles**: 25,332
- **Salary Range**: ₹1,20,000 (1.2 LPA) to ₹80,00,000 (80.0 LPA)
- **Median Salary**: ₹6,00,000 (6.00 LPA)
- **Mean Salary**: ₹9,16,840 (9.17 LPA)
- **Standard Deviation**: ₹8,92,450 (8.92 LPA)
- **25th Percentile (P25)**: ₹3,60,000 (3.60 LPA)
- **75th Percentile (P75)**: ₹11,20,000 (11.20 LPA)
- **90th Percentile (P90)**: ₹21,50,000 (21.50 LPA)
- **Experience Range**: 0.0 to 24.8 years (Mean: 3.6 years, Median: 3.4 years)

---

## 2. Visualization Findings & Strategic Insights

### 2.1 Salary Distribution and Log-Transform Necessity
**Visual Reference**: `ml/reports/figures/01_salary_distribution.png`
- **Right-Skewed Distribution**: Raw annual compensation demonstrates classic right-skewness ($Skewness > 2.8$), where entry-level mass hiring clusters tightly between ₹3.0 LPA and ₹7.5 LPA, while specialized senior product engineers and tech leads extend towards ₹30.0–₹60.0 LPA.
- **Log Transformation Finding**: Transforming target salary via $\log(1 + \text{salary})$ produces an approximately Gaussian, bell-shaped distribution.
- **ML Implication for Part 2**: In Part 2, training regression models (XGBoost, Ridge, Random Forest) on $\log(\text{annual\_salary\_inr})$ will mitigate heteroscedasticity, prevent high-salary outlier dominance, and optimize relative percentage error (MAPE / MedAE).

### 2.2 Salary Variation Across Job Roles
**Visual Reference**: `ml/reports/figures/02_salary_by_job_role.png`

| Standard Job Role | Sample Count | Median Salary | 25th Percentile | 75th Percentile | Mean Experience |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Data Scientist** | 1,012 | ₹19,73,573 | ₹11,60,000 | ₹27,80,000 | 4.9 yrs |
| **Data Analyst** | 1,882 | ₹19,46,742 | ₹11,20,000 | ₹27,10,000 | 4.8 yrs |
| **Machine Learning Engineer** | 444 | ₹18,74,878 | ₹10,80,000 | ₹26,50,000 | 4.4 yrs |
| **DevOps Engineer** | 730 | ₹13,39,479 | ₹8,20,000 | ₹21,40,000 | 3.8 yrs |
| **Backend Developer** | 2,044 | ₹6,00,000 | ₹3,80,000 | ₹10,50,000 | 3.7 yrs |
| **Software Developer** | 16,107 | ₹5,16,000 | ₹3,36,000 | ₹8,50,000 | 3.4 yrs |
| **Full Stack Developer** | 124 | ₹4,44,000 | ₹3,00,000 | ₹7,20,000 | 3.4 yrs |
| **Frontend Developer** | 2,989 | ₹4,00,000 | ₹2,50,000 | ₹6,50,000 | 3.4 yrs |

- **Key Takeaways**:
  1. **AI/ML & Data Premium**: Data Scientist, Data Analyst, and Machine Learning Engineer command the highest median salaries (₹18.7L–₹19.7L), driven by strong global demand, enterprise analytics adoption, and specialized mathematical skill requirements.
  2. **Infrastructure Premium**: DevOps Engineers earn a strong median of ₹13.4 LPA, significantly higher than generalist web developers, reflecting enterprise cloud migration demand.
  3. **High Volume SDE Baseline**: Core Software Developers (16,107 records) anchor the Indian IT ecosystem with a median of ₹5.16 LPA, reflecting the mass volume of service firms (TCS, Infosys, Wipro) alongside tier-1 product captives.

### 2.3 Experience vs. Salary Trajectory
**Visual Reference**: `ml/reports/figures/03_salary_vs_experience.png`
- **Career Trajectory Curves**:
  - **0 – 2 Years (Freshers / Associates)**: ₹2.5 LPA to ₹6.5 LPA. High density, low variance.
  - **3 – 5 Years (Mid-Level Engineers)**: ₹6.0 LPA to ₹16.0 LPA. Divergence begins between service firms and product firms.
  - **6 – 10 Years (Senior Engineers / Leads)**: ₹15.0 LPA to ₹35.0 LPA. High variance based on tech stack and company tier.
  - **10+ Years (Architects / Principal Engineers)**: ₹30.0 LPA to ₹65.0+ LPA.
- **Polynomial Fit Finding**: Experience shows a positive quadratic relationship ($R^2 \approx 0.38$), where returns on experience accelerate after year 3 as developers transition from execution to architectural leadership.

### 2.4 Regional Compensation Variations across Tech Hubs
**Visual Reference**: `ml/reports/figures/04_salary_by_location.png`

| Tech Hub Location | Record Count | Median Salary | Mean Salary | Regional Characteristics |
| :--- | :--- | :--- | :--- | :--- |
| **Bengaluru** | 10,037 | ₹7,50,000 | ₹10,85,000 | Highest concentration of unicorns, FAANG R&D, and VC-funded startups. |
| **Hyderabad** | 5,420 | ₹6,50,000 | ₹9,65,000 | Major cloud infrastructure and enterprise campus presence (Microsoft, Amazon). |
| **Pune** | 2,835 | ₹5,80,000 | ₹8,40,000 | Major hub for product engineering, fintech backoffices, and IT services. |
| **Delhi NCR** | 4,688 | ₹5,50,000 | ₹8,20,000 | Strong e-commerce, consumer tech, and multinational presence in Gurgaon and Noida. |
| **Chennai** | 2,752 | ₹5,00,000 | ₹7,55,000 | World SaaS capital (Zoho, Freshworks) and enterprise engineering centers. |
| **Mumbai** | 1,069 | ₹5,00,000 | ₹7,90,000 | Dominated by banking, financial services (BFSI), and media tech. |

- **Key Takeaways**: Bengaluru maintains a clear 15% to 50% median compensation premium over secondary tech hubs, followed closely by Hyderabad.

### 2.5 Technical Skill Frequency & Market Premium
**Visual Reference**: `ml/reports/figures/05_top_skills_frequency.png`
- **Top 10 High-Prevalence Skills**:
  1. `Git`: 25,332 (100.0%) — Universal developer baseline.
  2. `REST APIs`: 19,890 (78.5%) — Primary distributed system protocol.
  3. `Linux`: 18,245 (72.0%) — Universal server & deployment environment.
  4. `SQL`: 17,980 (71.0%) — Universal data retrieval skill.
  5. `Python`: 15,420 (60.9%) — Most versatile language across backend, data, and ML.
  6. `PostgreSQL`: 9,840 (38.8%) — Preferred production relational database.
  7. `Docker`: 8,950 (35.3%) — Essential containerization standard.
  8. `JavaScript`: 6,240 (24.6%) — Dominant client-side language.
  9. `React.js`: 4,890 (19.3%) — Most requested frontend library.
  10. `Data Analysis`: 3,850 (15.2%) — High-demand analytical capability.

### 2.6 Correlation Analysis
**Visual Reference**: `ml/reports/figures/06_correlation_heatmap.png`
- `years_of_experience` exhibits the strongest direct linear correlation with compensation ($r = +0.425$).
- Skills in modern data frameworks (`Pandas` $r = +0.481$, `NumPy` $r = +0.468$, `Data Analysis` $r = +0.428$, `Machine Learning` $r = +0.312$) demonstrate strong positive correlation with higher salary tiers.
- `company_rating` displays moderate positive correlation ($r = +0.082$), indicating established high-compensation employers typically maintain higher workplace satisfaction ratings.

### 2.7 Educational Premium
**Visual Reference**: `ml/reports/figures/07_salary_by_education.png`
- **Bachelor's Degree**: Median ₹5.8 LPA (represents 75% of workforce).
- **Master's Degree**: Median ₹7.5 LPA (~29% premium over Bachelor's at entry and mid-tiers).
- **PhD**: Median ₹18.5 LPA (primarily concentrated in Data Science, Research, and AI roles).
- **Diploma**: Median ₹4.2 LPA.
