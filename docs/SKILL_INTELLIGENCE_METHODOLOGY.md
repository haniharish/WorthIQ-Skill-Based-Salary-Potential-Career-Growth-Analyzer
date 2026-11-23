# WorthIQ Skill Intelligence Methodology
## Canonical Skill Taxonomy, Empirical Co-Occurrence Mining, and Marginal Compensation Valuation

---

## 1. Executive Summary

Technical competencies dictate market compensation in the software industry. However, skills rarely function in isolation; employers value cohesive **skill ecosystems** (e.g., Python combined with Docker, PostgreSQL, and AWS provides substantially higher utility than Python in isolation).

WorthIQ Phase 3 Module B implements an empirical Skill Intelligence system:
1. **Canonical Skill Taxonomy & Aliasing**: Resolves messy applicant inputs to standardized identifiers.
2. **Co-Occurrence Mining**: Analyzes 25,332 cleaned tech compensation records to calculate empirical co-occurrence frequency, Jaccard similarity, Lift, and bundle synergies.
3. **Marginal Valuation via Model Ablation**: Isolates the monetary contribution ($\pm ₹$) of each individual skill within a specific candidate profile.
4. **Counterfactual What-If Simulation**: Simulates the salary trajectory of acquiring or dropping specific skills before investing months in learning.

---

## 2. Canonical Skill Taxonomy & Normalization

### 2.1 Taxonomy Architecture

The WorthIQ taxonomy categorizes 35 industry-standard technology skills into 6 structural domains:

| Category | Canonical Skills | Key Aliases Mapped |
|:---|:---|:---|
| **Programming Languages** | Python, JavaScript, TypeScript, Java, C++, Go, C# | `py`, `js`, `ts`, `golang`, `csharp`, `cpp` |
| **Frontend Frameworks** | React.js, Angular, Vue.js, Next.js, HTML5, CSS3, Tailwind CSS | `react`, `reactjs`, `next`, `tailwind`, `html`, `css` |
| **Backend & APIs** | Node.js, Express.js, Django, FastAPI, Spring Boot, REST APIs, GraphQL | `nodejs`, `express`, `drf`, `spring`, `rest`, `restful` |
| **Databases & Storage** | PostgreSQL, MySQL, MongoDB, Redis, SQL | `postgres`, `psql`, `mongo`, `relational`, `rdbms` |
| **Cloud & DevOps** | Docker, Kubernetes, AWS, Azure, Linux, CI/CD, Git | `k8s`, `amazon web services`, `bash`, `github`, `actions` |
| **Data & AI** | Machine Learning, Deep Learning, Pandas, NumPy, Scikit-learn, Data Analysis | `ml`, `dl`, `sklearn`, `data analytics` |

### 2.2 Alias Resolution Algorithm

Raw input strings are normalized in two steps:
1. **Syntactic Cleansing**: Lowercased, stripped of leading/trailing whitespace, punctuation stripped (except `.`, `#`, `+`).
2. **Dictionary Hash Lookup**: Checked against `ALIAS_LOOKUP` (81 entries). If unmatched, fallback to exact string stripping.
3. **Set Deduplication**: Identical canonical resolutions are merged while preserving original presentation order.

---

## 3. Empirical Skill Co-Occurrence Mining

### 3.1 Dataset Corpus

The co-occurrence engine processes the complete processed dataset:
- **Total Records Analyzed**: $N = 25,332$ verified Indian tech compensation records.
- **Output Artifact**: `ml/data/processed/skill_cooccurrence_matrix.json`.

### 3.2 Statistical Association Metrics

For any pair of canonical skills $(A, B)$:

#### Support (Pair Frequency)
$$N(A, B) = \text{Count of records containing both } A \text{ and } B$$

#### Empirical Conditional Probability
$$P(B \mid A) = \frac{N(A, B)}{N(A)}$$

#### Jaccard Similarity Coefficient
$$J(A, B) = \frac{N(A, B)}{N(A) + N(B) - N(A, B)}$$

#### Statistical Lift
$$\text{Lift}(A, B) = \frac{P(A, B)}{P(A) \times P(B)} = \frac{N(A, B) \times N}{N(A) \times N(B)}$$
- $\text{Lift} > 1.0$: Skills $A$ and $B$ appear together significantly more often than random chance (complementary technology stack).
- $\text{Lift} = 1.0$: Statistical independence.
- $\text{Lift} < 1.0$: Skills substitute or conflict with each other (e.g., Django and Spring Boot rarely appear in the same early-career profile).

### 3.3 Empirical Findings from Indian Tech Market

Top mined skill combinations:

| Skill A | Skill B | Pair Count $N(A, B)$ | Jaccard Similarity | Median Salary (INR) | Primary Ecosystem |
|:---|:---|:---:|:---:|:---:|:---|
| **Git** | **REST APIs** | 20,443 | 0.812 | ₹7,20,000 | Universal Engineering Standard |
| **Git** | **SQL** | 18,077 | 0.724 | ₹6,80,000 | Enterprise Data Flow |
| **REST APIs** | **SQL** | 17,762 | 0.709 | ₹7,10,000 | Backend Core |
| **Python** | **Git** | 14,892 | 0.621 | ₹7,80,000 | Modern Scripting/Backend |
| **Python** | **SQL** | 13,950 | 0.589 | ₹7,65,000 | Data & Analytics Backbone |
| **Docker** | **Kubernetes** | 8,420 | 0.514 | ₹11,50,000 | High-Leverage Cloud Native |
| **React.js** | **TypeScript** | 7,890 | 0.482 | ₹9,20,000 | Modern Enterprise Frontend |

---

## 4. Marginal Skill Compensation Valuation via Ablation

### 4.1 Methodology

Rather than relying on naive averages (which conflate experience and location with skill value), WorthIQ evaluates the marginal value of a skill using **Controlled Single-Skill Ablation**:

Given a user profile:
$$X = \{ \text{Role}, \text{Exp}, \text{Loc}, \text{Edu}, S \}$$
where $S = \{s_1, s_2, \dots, s_k\}$ is the candidate's skill set.

1. **Baseline Valuation**:
   $$\hat{Y}_{\text{base}} = f(X)$$
2. **Ablated Valuation**: For each skill $s_i \in S$, compute counterfactual salary removing only $s_i$:
   $$\hat{Y}_{-s_i} = f(\{ \text{Role}, \text{Exp}, \text{Loc}, \text{Edu}, S \setminus \{s_i\} \})$$
3. **Marginal Rupee Contribution**:
   $$\Delta_{\text{INR}}(s_i) = \hat{Y}_{\text{base}} - \hat{Y}_{-s_i}$$
4. **Marginal Percentage Premium**:
   $$\% \Delta(s_i) = \frac{\hat{Y}_{\text{base}} - \hat{Y}_{-s_i}}{\hat{Y}_{-s_i}} \times 100\%$$

### 4.2 Portfolio Synergy Score

When a candidate holds complementary technologies (e.g., `Python` + `Docker` + `PostgreSQL`), the portfolio exhibits synergy. The bundle synergy index $\Sigma(S)$ evaluates the mean pairwise lift across all held skills:

$$\Sigma(S) = \frac{2}{|S|(|S| - 1)} \sum_{i < j} \text{Lift}(s_i, s_j)$$

- $\Sigma(S) \ge 1.4$: Highly synergistic, focused technical stack (e.g., Cloud-Native DevOps or MERN Stack).
- $1.0 \le \Sigma(S) < 1.4$: Balanced, standard industry competency.
- $\Sigma(S) < 1.0$: Fragmented skill portfolio without architectural cohesion.

---

## 5. Counterfactual What-If Simulation Engine

The What-If engine (`/api/intelligence/skills/compare/`) enables interactive compensation modeling:

$$\Delta_{\text{Simulated}} = f(X \cup S_{\text{add}} \setminus S_{\text{remove}}) - f(X)$$

### 5.1 Real-World Simulation Scenario

- **Current State**:
  - Full Stack Developer, 3.0 yrs exp, Bengaluru.
  - Skills: `JavaScript`, `React.js`, `SQL`, `Git`.
  - Current Market Median: **₹6,40,000 INR (6.4 LPA)**.
- **Counterfactual Action**:
  - Add: `Docker`, `AWS`, `TypeScript`.
  - Remove: None.
- **Simulated Result**:
  - Counterfactual Median: **₹8,15,000 INR (8.15 LPA)**.
  - Net Annual Gain: **+₹1,75,000 INR (+27.3%)**.
  - Recommendation: High-ROI skills that bridge the profile from Junior Full Stack to Senior Cloud-Ready Engineer.
