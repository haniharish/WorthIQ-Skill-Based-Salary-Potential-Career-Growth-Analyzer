# WorthIQ — Salary Range Prediction Methodology
## Quantile Regression & Non-Parametric Distribution Modeling

**Project:** WorthIQ — Skill-Based Salary Potential & Career Growth Analyzer  
**Component:** `ml.src.models.train_models` & `backend.apps.predictions.services.salary_prediction`  

---

## 1. Why Point Estimates Are Insufficient for Compensation

In technology employment markets, two software engineers with identical job titles, years of experience, and geographic locations can earn substantially different compensation packages depending on company business tier (Early-stage startup vs. IT services vs. Tier-1 product tech), individual negotiation leverage, and system design proficiency.

A single point estimate (e.g. "₹12.50 LPA") misleads users by creating an impression of fixed compensation. Instead, candidates require actionable percentiles:
- **Floor ($P10$):** The minimum baseline below which only 10% of peers earn.
- **Median ($P50$):** The balanced market expectation.
- **Ceiling ($P90$):** The upper-tier compensation achievable at top product companies.

---

## 2. Why the Gaussian / Standard Deviation Assumption Fails

A common but flawed approach in simple salary tools is taking the point estimate $\hat{y}$ and adding/subtracting standard deviations:
$$\hat{y}_{low} = \hat{y} - 1.96\hat{\sigma}, \quad \hat{y}_{high} = \hat{y} + 1.96\hat{\sigma}$$

This fails in real salary data for two critical mathematical reasons:
1. **Positive Right Skewness:** Tech compensation distributions are heavily right-skewed (log-normal or Pareto-like). The upside potential at elite companies is far greater than the downside floor. A symmetric interval produces artificially low (or negative) floors and underestimates upper percentiles.
2. **Heteroscedasticity:** Compensation variance grows dramatically with experience. Junior engineers exhibit tight variance (₹3.5L to ₹8L), whereas senior engineers with 12+ years experience can range from ₹18L to ₹60L+. Constant variance assumptions fail completely.

---

## 3. Quantile Regression with Pinball Loss

To address this without distributional assumptions, WorthIQ trains three separate gradient-boosted models directly targeting specific percentiles using **Pinball Loss** (asymmetric check function):

$$L_\alpha(y, \hat{y}) = \begin{cases} \alpha(y - \hat{y}), & \text{if } y \ge \hat{y} \\ (1 - \alpha)(\hat{y} - y), & \text{if } y < \hat{y} \end{cases}$$

Where:
- $\alpha = 0.10$ penalizes underestimation with weight $0.10$ and overestimation with weight $0.90$, forcing the model to predict the 10th percentile ($P10$).
- $\alpha = 0.50$ minimizes median absolute deviation (50th percentile, $P50$).
- $\alpha = 0.90$ penalizes underestimation with weight $0.90$, forcing the model to predict the 90th percentile ($P90$).

---

## 4. Empirical Calibration & Coverage Results

On the holdout test set of 5,067 records, our trained quantile models achieved near-perfect empirical coverage:

| Percentile | Target Coverage | Observed Empirical Coverage | Test Pinball Loss (INR) |
|---|---|---|---|
| **$P10$** | 10.00% | **10.20%** | ₹52,653 |
| **$P50$** | 50.00% | **48.10%** | ₹175,157 |
| **$P90$** | 90.00% | **89.30%** | ₹124,283 |

---

## 5. Preventing Quantile Crossing

Because independent quantile models are trained separately, extreme or out-of-distribution feature combinations could theoretically produce quantile crossing (e.g., $P10 > P50$).

WorthIQ enforces monotonic ordering at inference time inside `salary_prediction.py`:
$$\text{Low} = \min(P10, P50)$$
$$\text{Median} = P50$$
$$\text{High} = \max(P90, P50)$$

This strictly guarantees:
$$\text{Low} \le \text{Median} \le \text{High}$$

---

## 6. User Interpretation Guidelines

- **$P10$ (Conservative Floor):** Baseline offer acceptable for transitioning roles, smaller consultancies, or entry-level positions. 90% of peers in the dataset earn above this level.
- **$P50$ (Market Target):** Standard offer expectations for healthy mid-tier companies and enterprise tech.
- **$P90$ (Top-Tier Optimistic):** Stretch target for candidates with strong system design skills targeting Tier-1 product firms, high-growth funded startups, or multinational GCCs.
