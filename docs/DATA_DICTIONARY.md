# WorthIQ — Data Dictionary
**Phase 2 Part 1: Processed and Engineered Features Schema**

This document specifies the exact data types, valid value domains, business definitions, and engineering specifications for all features in the WorthIQ machine learning dataset.

---

## 1. Processed Dataset Schema (`ml/data/processed/salary_features_dataset.csv`)

| Column Name | Storage Type | Python/Pandas Dtype | Constraints / Allowed Domain | Nullable | Description & Business Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`job_role`** | String / Categorical | `object` / `string` | 8 Standard Roles (see Section 2.1) | No | Standardized professional job role classification. Primary career track for prediction and benchmarking. |
| **`years_of_experience`** | Numeric Float | `float64` | `0.0 <= x <= 25.0` (1 decimal place) | No | Continuous years of relevant software engineering / tech industry experience. Freshers/interns: 0.0 to 0.8 yrs. |
| **`location`** | String / Categorical | `object` / `string` | 6 Major Tech Hubs (see Section 2.2) | No | Standardized Indian technology metropolitan hub representing local market compensation dynamics. |
| **`education`** | String / Categorical | `object` / `string` | 4 Standard Buckets (see Section 2.3) | No | Highest completed academic qualification level. |
| **`skills_str`** | String / Delimited | `object` / `string` | Semicolon-delimited canonical skills | No | Semicolon-separated list of technical skills from WorthIQ canonical taxonomy (e.g. `Python;Django;PostgreSQL`). |
| **`company_rating`** | Numeric Float | `float64` | `1.0 <= x <= 5.0` (1 decimal place) | No | Employer Glassdoor/AmbitionBox satisfaction rating, reflecting corporate tier and workplace culture. |
| **`annual_salary_inr`** | Numeric Float | `float64` | `120,000.0 <= y <= 8,000,000.0` | No | **TARGET VARIABLE ($y$)**. Annual gross compensation in Indian Rupees (INR), ranging from 1.2 LPA to 80.0 LPA. |

---

## 2. Categorical Value Domains

### 2.1 Standardized Job Roles (`job_role`)
1. **`Software Developer`**: Core software development engineers (SDE I/II/III, Java/C++/Go/Python engineers, mobile app developers, SDET / QA test engineers).
2. **`Full Stack Developer`**: Engineers building end-to-end client-server web applications across frontend and backend tiers.
3. **`Frontend Developer`**: Client-side UI/UX engineers specializing in React, Next.js, TypeScript, JavaScript, CSS/Tailwind, and modern web interfaces.
4. **`Backend Developer`**: Server-side systems engineers focused on APIs, microservices, databases (PostgreSQL/Redis), and backend frameworks (Django/FastAPI/Node.js/Spring).
5. **`Data Analyst`**: Analytics specialists extracting business intelligence using SQL, Python, Pandas, data warehousing, and reporting.
6. **`Data Scientist`**: Quantitative and statistical modelers applying machine learning algorithms, hypothesis testing, and advanced predictive analytics.
7. **`Machine Learning Engineer`**: Production ML systems engineers deploying deep learning and ML pipelines, feature stores, and containerized inference services.
8. **`DevOps Engineer`**: Infrastructure, CI/CD, cloud architecture (AWS), container orchestration (Kubernetes, Docker), and site reliability engineering (SRE).

### 2.2 Standardized Tech Hubs (`location`)
1. **`Bengaluru`**: Karnataka (Silicon Valley of India; highest tech compensation density).
2. **`Hyderabad`**: Telangana (Major cloud, enterprise software, and MNC tech hub).
3. **`Pune`**: Maharashtra (Prominent IT services, automotive software, and product engineering center).
4. **`Mumbai`**: Maharashtra (Financial technology, enterprise consulting, and commercial capital).
5. **`Delhi NCR`**: National Capital Region (Encompasses New Delhi, Gurgaon/Gurugram, and Noida startup ecosystem).
6. **`Chennai`**: Tamil Nadu (SaaS capital of India, deep tech, and enterprise engineering).

### 2.3 Standardized Education Levels (`education`)
1. **`Bachelor's Degree`**: B.Tech, B.E., BCA, B.Sc in Computer Science, IT, or related STEM fields (~75% market prevalence).
2. **`Master's Degree`**: M.Tech, M.S., MCA, M.Sc in Computing disciplines (~20% market prevalence).
3. **`Diploma`**: Polytechnic or vocational 3-year technical diploma (~3% market prevalence).
4. **`PhD`**: Doctorate in Computer Science, Artificial Intelligence, or Quantitative disciplines (~2% market prevalence).

---

## 3. Canonical Skills Taxonomy (35 Skills)

The WorthIQ skill feature space matches Phase 1 database seeding (`DEFAULT_SKILLS` in `backend/apps/profiles/views.py`):

| Skill Name | Canonical Identifier (`skills_str`) | Engineered Feature Column | Domain Classification |
| :--- | :--- | :--- | :--- |
| AWS | `AWS` | `skill__aws` | Cloud & Infrastructure |
| C++ | `C++` | `skill__cpp` | Systems Programming |
| CI/CD | `CI/CD` | `skill__ci_cd` | DevOps & Tooling |
| CSS3 | `CSS3` | `skill__css3` | Web Presentation |
| Data Analysis | `Data Analysis` | `skill__data_analysis` | Data Science |
| Django | `Django` | `skill__django` | Backend Web Framework |
| Docker | `Docker` | `skill__docker` | Containerization |
| Express.js | `Express.js` | `skill__express_js` | Backend Framework |
| FastAPI | `FastAPI` | `skill__fastapi` | Modern Python API |
| Flutter | `Flutter` | `skill__flutter` | Cross-Platform Mobile |
| Git | `Git` | `skill__git` | Version Control |
| Go | `Go` | `skill__go` | Systems & Cloud Language |
| GraphQL | `GraphQL` | `skill__graphql` | API Protocol |
| HTML5 | `HTML5` | `skill__html5` | Web Semantics |
| Java | `Java` | `skill__java` | Enterprise Language |
| JavaScript | `JavaScript` | `skill__javascript` | Core Web Language |
| Kubernetes | `Kubernetes` | `skill__kubernetes` | Container Orchestration |
| Linux | `Linux` | `skill__linux` | Operating Systems |
| Machine Learning | `Machine Learning` | `skill__machine_learning` | Artificial Intelligence |
| Microservices | `Microservices` | `skill__microservices` | System Architecture |
| MongoDB | `MongoDB` | `skill__mongodb` | NoSQL Database |
| Next.js | `Next.js` | `skill__next_js` | Full Stack React Framework |
| Node.js | `Node.js` | `skill__node_js` | JavaScript Runtime |
| NumPy | `NumPy` | `skill__numpy` | Numerical Computing |
| Pandas | `Pandas` | `skill__pandas` | Data Manipulation |
| PostgreSQL | `PostgreSQL` | `skill__postgresql` | Relational Database |
| Python | `Python` | `skill__python` | General Purpose / Data Language |
| REST APIs | `REST APIs` | `skill__rest_apis` | API Architecture |
| React.js | `React.js` | `skill__react_js` | Frontend UI Library |
| Redis | `Redis` | `skill__redis` | In-Memory Cache/Store |
| SQL | `SQL` | `skill__sql` | Query Language |
| Scikit-Learn | `Scikit-Learn` | `skill__scikit_learn` | Machine Learning Library |
| Spring Boot | `Spring Boot` | `skill__spring_boot` | Enterprise Java Framework |
| Tailwind CSS | `Tailwind CSS` | `skill__tailwind_css` | Utility-first CSS |
| TypeScript | `TypeScript` | `skill__typescript` | Typed JavaScript |

---

## 4. Engineered Feature Matrix (55 Features)

The output feature vector produced by `preprocessor.joblib` consists of 55 numeric columns:
- **18 Categorical One-Hot Columns**:
  - `job_role` (8 columns): `job_role_Backend Developer`, `job_role_Data Analyst`, `job_role_Data Scientist`, `job_role_DevOps Engineer`, `job_role_Frontend Developer`, `job_role_Full Stack Developer`, `job_role_Machine Learning Engineer`, `job_role_Software Developer`
  - `location` (6 columns): `location_Bengaluru`, `location_Chennai`, `location_Delhi NCR`, `location_Hyderabad`, `location_Mumbai`, `location_Pune`
  - `education` (4 columns): `education_Bachelor's Degree`, `education_Diploma`, `education_Master's Degree`, `education_PhD`
- **2 Scaled Numeric Columns**:
  - `num__years_of_experience` (Standardized z-score)
  - `num__company_rating` (Standardized z-score)
- **35 Binary Skill Indicator Columns**:
  - Binary `0.0` or `1.0` indicator for each canonical skill.
