# WorthIQ SHAP Explainability Guide
## TreeExplainer Methodology, Additive Attributions, and Local/Global Salary Interpretability

---

## 1. Executive Overview

Machine learning models deployed in high-stakes human capital contexts—such as compensation estimation and career benchmarking—must satisfy rigorous interpretability standards. A black-box salary estimate without actionable explanations diminishes user trust and limits career utility.

**WorthIQ Phase 3 Module A** implements an Explainable AI (XAI) engine powered by **SHAP (SHapley Additive exPlanations)**. The engine translates complex tree ensemble predictions into transparent, mathematically sound feature attributions in Indian Rupees (₹ INR).

```
+-----------------------------------------------------------------------------------+
|                            WorthIQ SHAP Architecture                              |
|                                                                                   |
|  [User Profile Inputs]                                                            |
|         │                                                                         |
|         ▼                                                                         |
|  [Trained Preprocessor] ───► [Engineered Features Matrix (X)]                     |
|                                         │                                         |
|                                         ├───► [Random Forest Regressor]           |
|                                         │           │                             |
|                                         │           ▼                             |
|                                         │    [y_pred = ln(1 + Salary)]            |
|                                         │                                         |
|                                         ▼                                         |
|                             [shap.TreeExplainer]                                  |
|                                         │                                         |
|                                         ├── Base Expected Value E[f(X)] = 13.3680 |
|                                         ├── Raw Shapley Values [phi_1, ..., phi_k]|
|                                         │                                         |
|                                         ▼                                         |
|                             [Log-to-INR Conversion Engine]                        |
|                                         │                                         |
|         ┌───────────────────────────────┴───────────────────────────────┐         |
|         ▼                                                               ▼         |
|  [Local Waterfall Attributions]                                 [Summary Narrative]|
|  - INR Marginal Impacts (+/- ₹)                                 - Primary Drivers |
|  - Recharts Waterfall Chart                                     - Limiting Factors|
+-----------------------------------------------------------------------------------+
```

---

## 2. Theoretical Foundations: Shapley Values & TreeSHAP

### 2.1 Shapley Additive Explanations

Rooted in cooperative game theory (Lloyd Shapley, 1953), Shapley values distribute the total "payout" (model prediction minus base expected value) among all participating "players" (input features).

For a prediction function $f(x)$ and feature subset $S \subseteq F \setminus \{i\}$:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

Shapley values uniquely satisfy four fundamental axioms:
1. **Efficiency**: $\sum_{i=1}^{|F|} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$. The sum of all feature attributions exactly equals the difference between the prediction and the baseline expected value.
2. **Symmetry**: If feature $i$ and feature $j$ contribute equally to all possible feature subsets, $\phi_i = \phi_j$.
3. **Dummy / Null Player**: If feature $i$ contributes nothing to any subset ($f(S \cup \{i\}) = f(S)$), then $\phi_i = 0$.
4. **Additivity**: If model $f$ is an ensemble sum of sub-models $f = \sum_m f_m$, the attribution is $\phi_i = \sum_m \phi_{i,m}$.

### 2.2 TreeSHAP Algorithm

Evaluating exact Shapley values requires $2^{|F|}$ subset evaluations, which is computationally intractable for production latency. WorthIQ utilizes **TreeSHAP** (Lundberg et al., Nature Machine Intelligence 2020), an algorithm optimized for decision tree ensembles:

- **Time Complexity**: $O(T L D^2)$, where $T$ is the number of trees ($T=150$), $L$ is the maximum number of leaves, and $D$ is maximum tree depth ($D=16$).
- **Runtime Latency**: Computes exact attributions in **$< 45\text{ ms}$** per prediction on commodity CPU instances, enabling real-time interactive UI rendering.

---

## 3. Log-Scale to Indian Rupee (₹ INR) Conversion

### 3.1 The Scale Transformation Problem

WorthIQ's best-performing regressor (`Random Forest`, $R^2 = 0.771$, $\text{RMSE} = 0.2874$) was trained on log-transformed targets to stabilize exponential salary right-skewness:

$$\hat{y} = \ln(1 + \text{Salary}_{\text{INR}})$$

The TreeExplainer computes Shapley values $\phi_i$ in log space:

$$\hat{y} = \mathbb{E}[\ln(1 + \text{Salary})] + \sum_{i=1}^{|F|} \phi_i$$

Where:
- $\mathbb{E}[\ln(1 + \text{Salary})] = 13.368021$
- Baseline Expected Salary in INR:

$$\text{Base Salary}_{\text{INR}} = \exp(13.368021) - 1 \approx ₹6,39,242\text{ INR}$$

### 3.2 Marginal Attribution Apportionment

Directly exponentiating individual $\phi_i$ values ($\exp(\phi_i) - 1$) yields relative percentage changes, but does not sum to the total rupee difference due to non-linearity:

$$\Delta_{\text{Total INR}} = \text{Predicted Salary}_{\text{INR}} - \text{Base Salary}_{\text{INR}}$$

$$\Delta_{\text{Total INR}} \neq \sum_{i=1}^{|F|} (\exp(\phi_i) - 1)$$

To provide users with intuitive, additive Rupee attributions where $\sum \Delta_i = \Delta_{\text{Total}}$, WorthIQ implements **Proportional Marginal Apportionment**:

$$\Delta_i = \Delta_{\text{Total INR}} \times \frac{|\phi_i|}{\sum_{j=1}^{|F|} |\phi_j|} \times \text{sign}(\phi_i)$$

Each feature attribution returned to the frontend includes:
1. `feature`: Display name (e.g., `Location: Bengaluru`, `Years of Experience`, `Skill: Docker`).
2. `shap_log_value`: Exact raw Shapley value $\phi_i$.
3. `impact_percentage`: Relative percentage multiplier $\left(e^{\phi_i} - 1\right) \times 100\%$.
4. `inr_marginal_impact`: Apportioned additive Rupee impact ($\pm ₹$).
5. `direction`: `"positive"` (raises salary above baseline) or `"negative"` (drives salary below baseline).

---

## 4. Local Explainability Engine

When a user predicts their salary or views a saved report, `shap_service.py` executes `WorthIQShapExplainer.explain_prediction()`:

### 4.1 Sample Local Waterfall Output

For a profile with:
- **Role**: Backend Developer
- **Experience**: 4.0 Years
- **Location**: Bengaluru
- **Skills**: Python, Django, PostgreSQL, Docker, Git, REST APIs

```json
{
  "prediction_id": 104,
  "job_role": "Backend Developer",
  "base_salary_inr": 639242.0,
  "predicted_salary_inr": 850000.0,
  "total_delta_inr": 210758.0,
  "top_positive_features": [
    { "feature": "Location: Bengaluru", "inr_impact": 68420.0, "pct_impact": 10.7 },
    { "feature": "Years of Experience (4.0 yrs)", "inr_impact": 52190.0, "pct_impact": 8.2 },
    { "feature": "Skill: Docker", "inr_impact": 31450.0, "pct_impact": 4.9 },
    { "feature": "Skill: PostgreSQL", "inr_impact": 28600.0, "pct_impact": 4.5 }
  ],
  "top_negative_features": [
    { "feature": "Education: Bachelor's Degree", "inr_impact": -8450.0, "pct_impact": -1.3 }
  ],
  "summary_narrative": "Your predicted compensation of ₹8,50,000 represents a +₹2,10,758 variance from the baseline expectation (₹6,39,242). The primary positive driver is Location: Bengaluru (+₹68,420). The most limiting factor is Education: Bachelor's Degree (-₹8,450)."
}
```

### 4.2 Automated Narrative Generation Algorithm

The narrative engine converts numeric tensors into natural human language:
1. Compares $\text{Predicted Salary}$ with $\text{Base Salary}$ to determine overall market variance.
2. Identifies the single largest positive contributor ($\max \phi_i > 0$).
3. Identifies the single largest limiting feature ($\min \phi_i < 0$).
4. Evaluates whether missing high-leverage skills (e.g., Kubernetes, Cloud) dampened the upside.
5. Emits a concise, calibrated assessment designed for career development discussions.

---

## 5. Global Explainability Artifacts

Global explainability aggregates mean absolute Shapley values across the representative validation dataset ($N = 2,500$ holdout samples):

$$I_j = \frac{1}{N} \sum_{k=1}^N |\phi_{j}^{(k)}|$$

### 5.1 Global Feature Importance Ranking

| Rank | Feature | Mean Absolute SHAP (log) | Primary Impact Area |
|:---:|:---|:---:|:---|
| 1 | `years_of_experience` | 0.2418 | Baseline wage trajectory |
| 2 | `job_role` (One-Hot) | 0.1874 | Industry ceiling & demand |
| 3 | `location` (Bengaluru/Gurugram) | 0.1295 | Cost-of-living & tech clustering |
| 4 | `company_rating` | 0.0841 | Employer premium |
| 5 | `skill: Docker` | 0.0612 | Containerization premium |
| 6 | `skill: Kubernetes` | 0.0589 | Cloud infrastructure orchestration |
| 7 | `skill: AWS` | 0.0543 | Cloud public provider competency |
| 8 | `skill: Python` | 0.0491 | Core language versatility |
| 9 | `skill: Machine Learning` | 0.0468 | Specialized domain premium |
| 10 | `skill: React.js` | 0.0415 | Modern frontend architecture |

### 5.2 Generated Visualizations

Pre-computed and saved in `ml/explainability/global/`:
- `bar_plot.png`: Global bar chart of top 20 features ranked by mean absolute SHAP value.
- `summary_plot.png`: Beeswarm plot visualizing feature values vs impact on log compensation.
- `global_feature_importance.json`: Machine-readable rankings consumed by the `/api/intelligence/explanations/global/` endpoint.

---

## 6. Frontend Recharts Waterfall Architecture

In `frontend/src/pages/PredictionExplanationPage.jsx`:
- **Waterfall Chart Component**: Uses Recharts `<BarChart>` with floating baseline segments to render the step-by-step bridge from `₹6.39L (Baseline)` through individual positive/negative drivers to `₹8.50L (Final Prediction)`.
- **Color Coding**:
  - Emerald Green (`#10b981`): Positive drivers that elevate compensation.
  - Rose Red (`#f43f5e`): Limiting factors or unrepresented capabilities.
  - Indigo Blue (`#6366f1`): Baseline and Final result anchors.
- **Responsive Controls**: Includes toggle between Rupee impact (₹) and Percentage impact (%).
