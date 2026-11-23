# WORTHIQ — WHAT-IF SIMULATION METHODOLOGY & NON-CAUSALITY SPECIFICATION

---

### 1. Conceptual Framework

The What-If Salary Simulator is an exploratory sensitivity analysis tool. It evaluates how WorthIQ's underlying Machine Learning model (`RandomForestRegressor 2.0`) responds when specific profile dimensions (role, experience, location, education, skills) are mutated, holding all other features fixed.

$$\Delta \hat{y} = \hat{f}(X_{\text{simulated}}) - \hat{f}(X_{\text{baseline}})$$

Where:
- $X_{\text{baseline}}$ represents the candidate's verified baseline profile.
- $X_{\text{simulated}}$ represents the counterfactual profile vector.
- $\hat{f}(\cdot)$ is the trained Random Forest model predicting median market salary (P50), along with quantile bounds (P10 conservative, P90 top-tier).

---

### 2. Multi-Scenario Comparative Framework

Users can compare up to 4 scenarios simultaneously:
1. **Baseline Profile:** Ground truth anchor from user profile or custom baseline.
2. **Experiment A:** Incremental skill addition (e.g. adding Kubernetes and AWS).
3. **Experiment B:** Geographic relocation (e.g. Noida to Bengaluru tech hub).
4. **Experiment C:** Career track transition (e.g. Full Stack to Cloud Architect).

For each scenario, WorthIQ computes:
- Absolute compensation delta in ₹ INR and LPA.
- Relative percentage shift ($(\Delta \hat{y} / \hat{y}_{\text{base}}) \times 100\%$).
- Exact feature mutation diff (added skills, removed skills, experience delta, role switch).

---

### 3. Non-Causality Principle & Mandatory Disclaimer

> **Non-Causality Disclaimer:**
> WorthIQ simulation models evaluate correlation patterns observed across 25,000+ technology employment records. Salary bounds are statistical estimates (P10 conservative, P50 median, P90 top-tier) and do not guarantee identical compensation offers from employers. Real offers depend on interview performance, company tier, negotiation, and economic conditions.
