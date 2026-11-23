# WorthIQ — Prediction Confidence Methodology
## Quantitative Reliability & Input Coverage Evaluation

**Project:** WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer  
**Component:** `backend.apps.predictions.services.confidence_service`  

---

## 1. Overview

WorthIQ calculates a deterministic, empirical confidence score (0% to 100%) and categorizes predictions into **High**, **Medium**, or **Low** confidence. Rather than returning an arbitrary heuristic, the score reflects how well the user's input profile aligns with the data distribution on which the machine learning models were trained.

---

## 2. Factor Breakdown & Weights

The overall confidence score is computed as a weighted sum of four independent criteria:

$$\text{Confidence Score} = w_{exp} S_{exp} + w_{role} S_{role} + w_{loc} S_{loc} + w_{skills} S_{skills}$$

| Factor | Weight ($w_i$) | Max Score | Evaluation Criteria |
|---|---|---|---|
| **Experience Coverage ($S_{exp}$)** | 0.35 | 100 | How well the candidate's years of experience fits within the dense training distribution (0 to 15 years = 100; 15 to 25 = 75; > 25 = 45). |
| **Role Coverage ($S_{role}$)** | 0.25 | 100 | Full score (100) if raw input matches one of the 8 canonical roles; 50 if mapped via fallback normalization. |
| **Location Coverage ($S_{loc}$)** | 0.20 | 100 | Full score (100) if raw input matches one of the 6 major Indian tech hubs; 75 for Remote; 50 for unlisted tier-2/3 cities. |
| **Skill Density ($S_{skills}$)** | 0.20 | 100 | Number of recognized technical skills: $\ge 5$ skills = 100; 3 to 4 skills = 80; 1 to 2 skills = 55; 0 skills = 20. |

---

## 3. Classification Thresholds

| Confidence Tier | Score Range | UI Color Badge | Interpretation |
|---|---|---|---|
| **High** | $\ge 80\%$ | Emerald (`#10b981`) | Dense dataset support. High statistical reliability. |
| **Medium** | $60\% \le \text{Score} < 80\%$ | Indigo (`#4f46e5`) | Moderate dataset coverage; slight extrapolation on skills or experience. |
| **Low** | $< 60\%$ | Amber (`#f59e0b`) | Out-of-distribution experience (>25 yrs), non-standard role, or minimal skills provided. |

---

## 4. Input Scenarios & Expected Outcomes

### Scenario A: High Confidence (Score: 95%)
- **Inputs:** Role: `Full Stack Developer`, Exp: `4.0 years`, Location: `Bengaluru`, Skills: `['React', 'Node.js', 'PostgreSQL', 'Docker', 'AWS', 'Git']`.
- **Factors:**
  - Experience: 100 (4.0 years is in core cluster 0-15)
  - Role: 100 (Canonical role)
  - Location: 100 (Tier-1 hub)
  - Skills: 100 (6 recognized skills)
- **Weighted Score:** $0.35(100) + 0.25(100) + 0.20(100) + 0.20(100) = 100\% \rightarrow \text{High}$.

### Scenario B: Medium Confidence (Score: 71%)
- **Inputs:** Role: `Backend Developer`, Exp: `18.0 years`, Location: `Indore`, Skills: `['Java', 'Spring Boot']`.
- **Factors:**
  - Experience: 75 (15-25 year tier)
  - Role: 100 (Canonical role)
  - Location: 50 (Unlisted tier-2 city normalized to regional index)
  - Skills: 55 (2 skills provided)
- **Weighted Score:** $0.35(75) + 0.25(100) + 0.20(50) + 0.20(55) = 26.25 + 25 + 10 + 11 = 72.25\% \rightarrow \text{Medium}$.

### Scenario C: Low Confidence (Score: 49%)
- **Inputs:** Role: `Robotics Researcher`, Exp: `32.0 years`, Location: `Dharwad`, Skills: `[]`.
- **Factors:**
  - Experience: 45 (> 25 years sparse distribution)
  - Role: 50 (Mapped to fallback)
  - Location: 50 (Unlisted city)
  - Skills: 20 (0 skills)
- **Weighted Score:** $0.35(45) + 0.25(50) + 0.20(50) + 0.20(20) = 15.75 + 12.5 + 10 + 4 = 42.25\% \rightarrow \text{Low}$.
