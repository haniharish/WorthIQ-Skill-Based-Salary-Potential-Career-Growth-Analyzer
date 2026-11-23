"""
WorthIQ SHAP Explainability Engine
Generates local (per-prediction) and global model explainability using
SHapley Additive exPlanations (TreeExplainer) on the production Random Forest model.
"""

import sys
import os
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

logger = logging.getLogger("ml.explainability")

class WorthIQShapExplainer:
    """
    SHAP TreeExplainer wrapper calibrated for the WorthIQ Random Forest salary model.
    Handles log-scale predictions, feature attribution, and human-readable explanations.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WorthIQShapExplainer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, models_dir=None):
        if self._initialized:
            return

        self.base_dir = BASE_DIR
        self.models_dir = Path(models_dir) if models_dir else self.base_dir / "ml" / "models"
        
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self.explainer = None
        self.expected_value_log = None
        self.expected_value_inr = None
        self.feature_names = None
        
        self._load_artifacts()
        self._initialized = True

    def _load_artifacts(self):
        """Loads model artifacts and initializes TreeExplainer."""
        model_path = self.models_dir / "salary_model.joblib"
        prep_path = self.models_dir / "preprocessing_pipeline.joblib"
        if not prep_path.exists():
            prep_path = self.base_dir / "ml" / "data" / "processed" / "preprocessor.joblib"
        meta_path = self.models_dir / "model_metadata.json"

        if not model_path.exists():
            raise FileNotFoundError(f"Model artifact not found at {model_path}")
        if not prep_path.exists():
            raise FileNotFoundError(f"Preprocessor artifact not found at {prep_path}")
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata artifact not found at {meta_path}")

        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(prep_path)

        with open(meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.feature_names = self.metadata.get("engineered_features", [])

        # Initialize TreeExplainer
        logger.info("Initializing SHAP TreeExplainer for Random Forest...")
        self.explainer = shap.TreeExplainer(self.model)
        
        # Expected value is a scalar or 1D array representing E[log(1+y)]
        ev = self.explainer.expected_value
        if isinstance(ev, (list, np.ndarray)):
            self.expected_value_log = float(ev[0])
        else:
            self.expected_value_log = float(ev)

        # Baseline central salary in INR
        self.expected_value_inr = float(np.expm1(self.expected_value_log))
        logger.info(f"TreeExplainer ready. Base log value: {self.expected_value_log:.4f} (₹{self.expected_value_inr:,.0f} INR)")

    def _clean_feature_name(self, raw_name):
        """Maps internal one-hot/vector column names to readable names and categories."""
        if raw_name.startswith("job_role_"):
            return {
                "clean_name": f"Role: {raw_name.replace('job_role_', '')}",
                "category": "Job Role",
                "display_name": raw_name.replace('job_role_', '')
            }
        elif raw_name.startswith("location_"):
            return {
                "clean_name": f"Location: {raw_name.replace('location_', '')}",
                "category": "Location",
                "display_name": raw_name.replace('location_', '')
            }
        elif raw_name.startswith("education_"):
            return {
                "clean_name": f"Education: {raw_name.replace('education_', '')}",
                "category": "Education",
                "display_name": raw_name.replace('education_', '')
            }
        elif raw_name.startswith("skill__"):
            clean_skill = raw_name.replace("skill__", "").replace("_", " ").title()
            # Handle specific acronyms
            replacements = {
                "Aws": "AWS", "Cpp": "C++", "Ci/Cd": "CI/CD", "Css3": "CSS3",
                "Html5": "HTML5", "Sql": "SQL", "Rest Apis": "REST APIs",
                "React Js": "React.js", "Node Js": "Node.js", "Next Js": "Next.js",
                "Express Js": "Express.js", "Javascript": "JavaScript", "Typescript": "TypeScript"
            }
            display = replacements.get(clean_skill, clean_skill)
            return {
                "clean_name": f"Skill: {display}",
                "category": "Technical Skill",
                "display_name": display
            }
        elif "years_of_experience" in raw_name:
            return {
                "clean_name": "Years of Experience",
                "category": "Experience",
                "display_name": "Experience Tenure"
            }
        elif "company_rating" in raw_name:
            return {
                "clean_name": "Company Tier / Rating",
                "category": "Company Quality",
                "display_name": "Company Rating"
            }
        return {
            "clean_name": raw_name,
            "category": "Other",
            "display_name": raw_name
        }

    def explain_instance(self, input_dict):
        """
        Generates structured local SHAP explanation for a single prediction input.

        Parameters:
            input_dict (dict): Keys: 'job_role', 'years_of_experience', 'location',
                               'education', 'skills', optionally 'company_rating'.

        Returns:
            dict containing:
                - base_value_log
                - base_value_inr
                - predicted_value_log
                - predicted_value_inr
                - total_delta_inr
                - feature_attributions: list of top feature impacts
                - positive_contributors: list of positive factors
                - negative_contributors: list of limiting factors
                - top_skills_impact: specific breakdown of provided skills
                - summary_narrative: plain text summary
        """
        # 1. Format into DataFrame for preprocessor matching salary_prediction.py
        raw_skills = input_dict.get("skills", [])
        if isinstance(raw_skills, list):
            clean_skills = [str(s).strip() for s in raw_skills if str(s).strip()]
            skills_str = ";".join(clean_skills)
        else:
            skills_str = str(raw_skills).strip()

        role = input_dict.get("job_role", "Software Developer")
        loc = input_dict.get("location", "Bengaluru")
        edu = input_dict.get("education", "Bachelor's Degree")
        if edu not in ["Bachelor's Degree", "Master's Degree", "Diploma", "PhD"]:
            edu = "Bachelor's Degree"

        exp_val = max(0.0, min(float(input_dict.get("years_of_experience", 0.0)), 60.0))
        company_rating = float(input_dict.get("company_rating", 3.8))

        row_df = pd.DataFrame([{
            "job_role": role,
            "years_of_experience": exp_val,
            "location": loc,
            "education": edu,
            "skills_str": skills_str,
            "company_rating": company_rating,
        }])

        # 2. Transform through preprocessor
        X_vec = self.preprocessor.transform(row_df)
        X_df = pd.DataFrame(X_vec, columns=self.feature_names)

        # 3. Compute SHAP values
        shap_values = self.explainer.shap_values(X_df)
        if isinstance(shap_values, list):
            # Regression outputs 1D array
            vals = shap_values[0]
        else:
            vals = shap_values[0] if shap_values.ndim > 1 else shap_values

        pred_log = float(self.model.predict(X_df)[0])
        pred_inr = float(np.expm1(pred_log))
        delta_inr = pred_inr - self.expected_value_inr

        # Sum of absolute SHAP values for relative percentage weighting
        sum_abs_shap = float(np.sum(np.abs(vals)))
        if sum_abs_shap == 0:
            sum_abs_shap = 1e-6

        # 4. Parse feature attributions
        attributions = []
        for idx, col in enumerate(self.feature_names):
            phi = float(vals[idx])
            feature_val = float(X_df.iloc[0, idx])
            
            # Skip zero-value binary features (e.g. skills user does not possess, roles they are not in)
            # unless it's a numeric feature or active category
            if feature_val == 0.0 and ("skill__" in col or "job_role_" in col or "location_" in col or "education_" in col):
                continue

            cleaned = self._clean_feature_name(col)
            pct_effect = float((np.exp(phi) - 1.0) * 100.0)
            
            # Apportion total INR delta proportionally
            inr_contrib = float(delta_inr * (abs(phi) / sum_abs_shap) * (1 if phi >= 0 else -1))

            attributions.append({
                "feature_name": col,
                "display_name": cleaned["display_name"],
                "clean_name": cleaned["clean_name"],
                "category": cleaned["category"],
                "feature_value": feature_val,
                "shap_value": round(phi, 4),
                "percentage_impact": round(pct_effect, 2),
                "inr_impact": round(inr_contrib, 2),
                "direction": "positive" if phi >= 0 else "negative",
                "magnitude": round(abs(phi), 4)
            })

        # Sort by absolute SHAP magnitude descending
        attributions.sort(key=lambda x: x["magnitude"], reverse=True)

        positive = [a for a in attributions if a["direction"] == "positive"]
        negative = [a for a in attributions if a["direction"] == "negative"]

        skills_impact = [a for a in attributions if a["category"] == "Technical Skill"]

        # Build narrative summary
        top_pos = positive[0]["clean_name"] if positive else "Base experience"
        top_pos_val = positive[0]["inr_impact"] if positive else 0
        summary_narrative = (
            f"Your predicted compensation of ₹{pred_inr:,.0f} represents a "
            f"{'+' if delta_inr >= 0 else ''}₹{abs(delta_inr):,.0f} variance from the baseline expectation (₹{self.expected_value_inr:,.0f}). "
            f"The primary positive driver is {top_pos} (+₹{abs(top_pos_val):,.0f})."
        )
        if negative:
            top_neg = negative[0]["clean_name"]
            top_neg_val = negative[0]["inr_impact"]
            summary_narrative += f" The most limiting factor is {top_neg} (-₹{abs(top_neg_val):,.0f})."

        return {
            "base_value_log": round(self.expected_value_log, 4),
            "base_value_inr": round(self.expected_value_inr, 2),
            "predicted_value_log": round(pred_log, 4),
            "predicted_value_inr": round(pred_inr, 2),
            "total_delta_inr": round(delta_inr, 2),
            "feature_attributions": attributions[:15],  # Top 15 drivers
            "positive_contributors": positive[:6],
            "negative_contributors": negative[:6],
            "skills_impact": skills_impact[:10],
            "summary_narrative": summary_narrative,
            "model_version": self.metadata.get("model_version", "2.0.0"),
            "units": "log_salary_and_apportioned_inr"
        }

    def generate_global_explanations(self, sample_size=1000, output_dir=None):
        """
        Computes global SHAP statistics on a representative evaluation sample
        and generates summary plots and rankings.
        """
        output_dir = Path(output_dir) if output_dir else self.base_dir / "ml" / "explainability" / "global"
        output_dir.mkdir(parents=True, exist_ok=True)

        dataset_path = self.base_dir / "ml" / "data" / "processed" / "salary_features_dataset.csv"
        if not dataset_path.exists():
            raise FileNotFoundError(f"Processed dataset not found at {dataset_path}")

        logger.info(f"Loading sample of {sample_size} records from {dataset_path.name} for global SHAP...")
        df = pd.read_csv(dataset_path)
        sample_df = df.sample(min(sample_size, len(df)), random_state=42)

        # Preprocess sample
        X_vec = self.preprocessor.transform(sample_df)
        X_df = pd.DataFrame(X_vec, columns=self.feature_names)

        logger.info("Computing global SHAP values with TreeExplainer...")
        shap_values = self.explainer.shap_values(X_df)
        if isinstance(shap_values, list):
            vals = shap_values[0]
        else:
            vals = shap_values

        mean_abs_shap = np.mean(np.abs(vals), axis=0)
        
        # Rank features
        ranking = []
        for idx, col in enumerate(self.feature_names):
            cleaned = self._clean_feature_name(col)
            ranking.append({
                "feature": col,
                "clean_name": cleaned["clean_name"],
                "display_name": cleaned["display_name"],
                "category": cleaned["category"],
                "mean_abs_shap": float(round(mean_abs_shap[idx], 5)),
                "rank": 0
            })

        ranking.sort(key=lambda x: x["mean_abs_shap"], reverse=True)
        for i, item in enumerate(ranking):
            item["rank"] = i + 1

        # Save global rankings JSON
        global_summary = {
            "sample_size": len(sample_df),
            "expected_value_log": self.expected_value_log,
            "expected_value_inr": self.expected_value_inr,
            "feature_rankings": ranking,
            "top_skills": [r for r in ranking if r["category"] == "Technical Skill"][:15],
            "top_categories": [r for r in ranking if r["category"] != "Technical Skill"][:10],
            "generated_at": pd.Timestamp.now().isoformat()
        }

        json_path = output_dir / "global_feature_importance.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(global_summary, f, indent=2)
        logger.info(f"Saved global feature importance JSON to {json_path}")

        # 1. Bar Plot of Top 15 Features
        top_15 = ranking[:15]
        plt.figure(figsize=(10, 6))
        plt.barh([x["clean_name"] for x in reversed(top_15)], [x["mean_abs_shap"] for x in reversed(top_15)], color="#4f46e5")
        plt.xlabel("Mean |SHAP Value| (Impact on log-salary)")
        plt.title("WorthIQ — Global Feature Importance (Top 15 Features)", fontsize=13, fontweight="bold")
        plt.tight_layout()
        bar_plot_path = output_dir / "bar_plot.png"
        plt.savefig(bar_plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved SHAP bar plot to {bar_plot_path}")

        # 2. SHAP Beeswarm Summary Plot
        plt.figure(figsize=(10, 7))
        # Use readable feature names for summary plot
        display_names = [self._clean_feature_name(c)["clean_name"] for c in self.feature_names]
        X_df_display = X_df.copy()
        X_df_display.columns = display_names
        
        shap.summary_plot(vals, X_df_display, max_display=15, show=False)
        plt.title("WorthIQ — SHAP Summary Distribution", fontsize=13, fontweight="bold", pad=15)
        plt.tight_layout()
        summary_plot_path = output_dir / "summary_plot.png"
        plt.savefig(summary_plot_path, dpi=300)
        plt.close()
        logger.info(f"Saved SHAP summary plot to {summary_plot_path}")

        return global_summary

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    explainer = WorthIQShapExplainer()
    print("Testing single instance explanation...")
    test_profile = {
        "job_role": "Full Stack Developer",
        "years_of_experience": 4.5,
        "location": "Bengaluru",
        "education": "Bachelor's Degree",
        "skills": ["JavaScript", "React.js", "Node.js", "PostgreSQL", "Docker", "AWS"],
        "company_rating": 4.2
    }
    res = explainer.explain_instance(test_profile)
    print("Instance Explanation:")
    print(f"Base: ₹{res['base_value_inr']:,.0f} -> Predicted: ₹{res['predicted_value_inr']:,.0f} (Delta: ₹{res['total_delta_inr']:,.0f})")
    print(f"Narrative: {res['summary_narrative']}")
    print(f"Top Positive: {[p['clean_name'] for p in res['positive_contributors']]}")
    print(f"Top Limiting: {[n['clean_name'] for n in res['negative_contributors']]}")
    
    print("\nGenerating global explanations...")
    explainer.generate_global_explanations(sample_size=800)
    print("Global explanations successfully generated!")
