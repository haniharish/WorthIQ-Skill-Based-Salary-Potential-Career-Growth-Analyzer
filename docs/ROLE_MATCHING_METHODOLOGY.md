# WorthIQ Job Role Matching Methodology
## Multi-Dimensional Composite Scoring, TF-IDF Semantic Overlap, and Skill Gap Analysis

---

## 1. Executive Summary

Traditional job boards rely on simplistic keyword filtering that either floods candidates with irrelevant roles or rejects qualified applicants due to minor lexical differences. 

**WorthIQ Phase 3 Module C** introduces an AI-powered role matching engine that evaluates candidate fit across four orthogonal dimensions:
1. **Mandatory Competencies (40% Weight)**: Core technical non-negotiables required for day-one operational effectiveness.
2. **Preferred Competencies (15% Weight)**: Secondary technical skills that distinguish competitive applicants.
3. **Semantic Profile Similarity (25% Weight)**: TF-IDF vectorization and cosine distance across overall technical profile texts.
4. **Experience Tenure Fit (20% Weight)**: Compatibility between candidate seniority and role expectations.

---

## 2. Curated Technology Role Catalog

The WorthIQ role catalog contains 9 specialized engineering and data roles calibrated against Indian hiring benchmarks:

| Role Title | Min/Max Exp (Yrs) | Market Median | Core Mandatory Skills | Preferred Skills |
|:---|:---:|:---:|:---|:---|
| **Full Stack Developer** | 1.0 – 12.0 | ₹7.20L | JavaScript, React.js, Node.js, SQL, Git | TypeScript, Docker, PostgreSQL, REST APIs, Next.js, Tailwind CSS |
| **Backend Developer** | 1.0 – 15.0 | ₹7.50L | Python, PostgreSQL, REST APIs, Git, SQL | Django, FastAPI, Docker, Redis, Microservices, Kubernetes, Linux |
| **Frontend Developer** | 0.5 – 10.0 | ₹6.50L | JavaScript, React.js, HTML5, CSS3, Git | TypeScript, Next.js, Tailwind CSS, REST APIs, Flutter |
| **DevOps Engineer** | 2.0 – 15.0 | ₹8.50L | Linux, Docker, Kubernetes, CI/CD, Git | AWS, Python, Go, Microservices, Redis |
| **Data Scientist** | 1.5 – 12.0 | ₹8.00L | Python, Machine Learning, Pandas, NumPy, SQL | Scikit-learn, Data Analysis, Docker, FastAPI, PostgreSQL |
| **Machine Learning Engineer**| 2.0 – 14.0 | ₹9.00L | Python, Machine Learning, Scikit-learn, Docker, Pandas | Kubernetes, FastAPI, REST APIs, AWS, Linux, SQL |
| **Data Analyst** | 0.5 – 8.0 | ₹5.50L | SQL, Data Analysis, Pandas, Python | NumPy, PostgreSQL, Git |
| **Software Developer** | 0.0 – 12.0 | ₹6.00L | Java, SQL, Git, REST APIs | Spring Boot, Docker, Linux, PostgreSQL, Microservices, C++ |
| **Cloud Engineer** | 2.0 – 14.0 | ₹8.20L | AWS, Linux, Docker, Kubernetes, CI/CD | Python, Go, Microservices, Git, Redis |

---

## 3. Mathematical Scoring Formulation

For a candidate profile with skills $S_c$ and experience $E_c$ evaluated against a target role $R_j$:

### 3.1 Dimension 1: Mandatory Skill Coverage ($S_{\text{req}}$) — Weight: 40%

$$S_{\text{req}} = \frac{|S_c \cap R_{j,\text{mandatory}}|}{|R_{j,\text{mandatory}}|}$$

Measures what percentage of non-negotiable core skills the candidate possesses. A candidate missing foundational requirements suffers an immediate penalty.

### 3.2 Dimension 2: Preferred Skill Coverage ($S_{\text{pref}}$) — Weight: 15%

$$S_{\text{pref}} = \frac{|S_c \cap R_{j,\text{preferred}}|}{\max(1, |R_{j,\text{preferred}}|)}$$

Rewards breadth and specialization without penalizing candidates who have the core skills.

### 3.3 Dimension 3: TF-IDF Semantic Profile Similarity ($S_{\text{cos}}$) — Weight: 25%

To capture contextual relevance beyond exact set intersections, candidate skills and role descriptions are tokenized and vectorized:

$$\vec{v}_{\text{user}} = \text{TF-IDF}(S_c)$$
$$\vec{v}_{\text{role}} = \text{TF-IDF}(R_j)$$

$$S_{\text{cos}} = \frac{\vec{v}_{\text{user}} \cdot \vec{v}_{\text{role}}}{\|\vec{v}_{\text{user}}\| \|\vec{v}_{\text{role}}\|}$$

This handles cross-domain overlap and rewards technological alignment.

### 3.4 Dimension 4: Experience Tenure Compatibility ($S_{\text{exp}}$) — Weight: 20%

Evaluates whether the candidate fits within the target role's seniority bracket $[\text{Min}_E, \text{Max}_E]$:

$$S_{\text{exp}} = \begin{cases} 
1.0 & \text{if } \text{Min}_E \le E_c \le \text{Max}_E \\
\max(0.20, 1.0 - 0.25 \times (\text{Min}_E - E_c)) & \text{if } E_c < \text{Min}_E \\
\max(0.50, 1.0 - 0.08 \times (E_c - \text{Max}_E)) & \text{if } E_c > \text{Max}_E 
\end{cases}$$

- **Within Band**: 100% score.
- **Under-Experienced**: Steep penalty (0.25 per missing year), reflecting difficulty meeting role demands.
- **Over-Experienced**: Mild taper (0.08 per extra year), recognizing leadership potential while accounting for over-qualification risk.

### 3.5 Composite Match Score

$$\text{Match Score} = \left( 0.40 \cdot S_{\text{req}} + 0.15 \cdot S_{\text{pref}} + 0.25 \cdot S_{\text{cos}} + 0.20 \cdot S_{\text{exp}} \right) \times 100$$

Bounded strictly within $[0.0, 100.0]$.

---

## 4. Match Tier Categorization

| Score Range | Category Badge | Color Theme | Interpretation & Guidance |
|:---:|:---|:---:|:---|
| **80.0% – 100%** | **Strong Match** | Emerald Green | Candidate possesses core competencies and tenure. Prime applicant ready for interview rounds. |
| **65.0% – 79.9%** | **Good Match** | Indigo Blue | Strong alignment with 1–2 minor skill gaps. Feasible with 4–6 weeks of targeted upskilling. |
| **50.0% – 64.9%** | **Moderate Match**| Sky Blue | Adjacent capability. Suitable as a career transition target via structured roadmap. |
| **< 50.0%** | **Low Match** | Amber/Slate | Substantial domain gap. Requires foundational retraining across multiple competencies. |

---

## 5. Automated Skill Gap Extraction

Every matched role response provides explicit skill delta breakdowns:
- `matched_required_skills`: Skills held that satisfy non-negotiables.
- `missing_required_skills`: Critical gaps preventing day-one readiness.
- `missing_preferred_skills`: Value-add skills that elevate competitive standing.

These gaps directly feed into **Module D (Career Growth Roadmaps)**, generating targeted learning sequences that bridge the candidate's exact shortcomings.
