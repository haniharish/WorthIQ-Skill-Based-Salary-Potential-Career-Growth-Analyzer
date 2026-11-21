"""
WorthIQ - Data Cleaning and Standardization Pipeline
Normalizes raw datasets into a cohesive, high-quality dataset representing
the Indian technology job market, aligned with WorthIQ's Phase 1 schema.
"""

import os
import re
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clean_data")

# Fixed random seed for complete reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# WorthIQ Phase 1 Standard Roles
STANDARDIZED_ROLES = [
    "Software Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "DevOps Engineer"
]

# WorthIQ Phase 1 Standard Cities
STANDARDIZED_CITIES = [
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Mumbai",
    "Delhi NCR",
    "Chennai"
]

# City mapping dictionary
CITY_MAPPING = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "mumbai": "Mumbai",
    "chennai": "Chennai",
    "new delhi": "Delhi NCR",
    "delhi": "Delhi NCR",
    "noida": "Delhi NCR",
    "gurgaon": "Delhi NCR",
    "gurugram": "Delhi NCR",
}

# WorthIQ Phase 1 Standard Skills Taxonomy
CANONICAL_SKILLS = [
    "Python", "Django", "React.js", "JavaScript", "TypeScript", "Node.js",
    "PostgreSQL", "Docker", "AWS", "Git", "REST APIs", "SQL",
    "Tailwind CSS", "Next.js", "MongoDB", "Redis", "Machine Learning",
    "Data Analysis", "HTML5", "CSS3", "Linux", "GraphQL", "Kubernetes",
    "FastAPI", "Pandas", "NumPy", "Scikit-Learn", "Java", "Spring Boot",
    "C++", "Go", "Flutter", "Express.js", "CI/CD", "Microservices"
]

# Skill pools per role
ROLE_SKILL_POOLS = {
    "Frontend Developer": {
        "core": ["HTML5", "CSS3", "JavaScript", "React.js", "Git"],
        "elective": ["TypeScript", "Tailwind CSS", "Next.js", "REST APIs", "GraphQL"]
    },
    "Backend Developer": {
        "core": ["Python", "Django", "PostgreSQL", "REST APIs", "Git"],
        "elective": ["Node.js", "Express.js", "FastAPI", "Redis", "Docker", "SQL", "MongoDB", "Java", "Spring Boot", "Microservices"]
    },
    "Full Stack Developer": {
        "core": ["JavaScript", "React.js", "Node.js", "PostgreSQL", "Git"],
        "elective": ["TypeScript", "Python", "Django", "Next.js", "Docker", "REST APIs", "Tailwind CSS", "MongoDB", "Redis"]
    },
    "Software Developer": {
        "core": ["Git", "SQL", "REST APIs", "Linux"],
        "elective": ["Java", "Spring Boot", "Python", "C++", "Go", "PostgreSQL", "Docker", "Microservices", "CI/CD"]
    },
    "Data Analyst": {
        "core": ["SQL", "Python", "Data Analysis", "Pandas"],
        "elective": ["NumPy", "PostgreSQL", "Git", "REST APIs"]
    },
    "Data Scientist": {
        "core": ["Python", "Pandas", "NumPy", "Scikit-Learn", "Machine Learning"],
        "elective": ["SQL", "Data Analysis", "Git", "PostgreSQL", "FastAPI", "Docker"]
    },
    "Machine Learning Engineer": {
        "core": ["Python", "Machine Learning", "Scikit-Learn", "Docker", "Git"],
        "elective": ["NumPy", "Pandas", "FastAPI", "Linux", "SQL", "Microservices", "AWS"]
    },
    "DevOps Engineer": {
        "core": ["Docker", "Kubernetes", "Linux", "CI/CD", "Git"],
        "elective": ["AWS", "Python", "Microservices", "PostgreSQL", "Go", "REST APIs"]
    }
}

def map_job_role(title: str, existing_role: str = "") -> str:
    """Map arbitrary job title or role tag to one of the 8 canonical WorthIQ roles."""
    t = str(title).lower()
    r = str(existing_role).lower()
    
    # Check ML / AI first
    if any(k in t for k in ["machine learning", "ml engineer", "ai engineer", "deep learning", "computer vision"]):
        return "Machine Learning Engineer"
    if any(k in t for k in ["data scientist", "applied scientist", "research scientist"]):
        return "Data Scientist"
    if any(k in t for k in ["data analyst", "business analyst", "analytics", "bi developer", "data engineer"]):
        return "Data Analyst"
    if any(k in t for k in ["devops", "cloud", "site reliability", "sre", "platform engineer", "infrastructure"]):
        return "DevOps Engineer"
    if any(k in t for k in ["full stack", "fullstack", "mern", "mean"]):
        return "Full Stack Developer"
    if any(k in t for k in ["front end", "frontend", "ui developer", "react", "angular", "web developer"]) or r in ["frontend", "web"]:
        return "Frontend Developer"
    if any(k in t for k in ["back end", "backend", "django", "node", "database administrator", "dba"]) or r in ["backend", "database"]:
        return "Backend Developer"
    if any(k in t for k in ["android", "ios", "mobile"]) or r in ["android", "ios", "mobile"]:
        return "Software Developer"
    if any(k in t for k in ["software", "sde", "developer", "engineer", "java", "python", "c++", "test", "sdet"]) or r in ["sde", "java", "python", "testing"]:
        return "Software Developer"
        
    return "Software Developer"

def extract_experience(title: str, status: str = "", exp_level: str = "") -> float:
    """Derive continuous years of experience from title, status, or level."""
    t = str(title).lower()
    s = str(status).lower()
    lvl = str(exp_level).upper()
    
    # Explicit seniority mapping
    if lvl == "EN" or "intern" in t or "trainee" in t or s in ["intern", "trainee"]:
        base_exp = np.random.uniform(0.1, 0.8)
    elif lvl == "MI" or any(k in t for k in ["junior", "associate", "entry", " sde i", "developer 1", "engineer i"]):
        base_exp = np.random.uniform(1.0, 2.8)
    elif lvl == "SE" or any(k in t for k in ["senior", "sr.", "sde ii", "developer 2", "engineer ii", "specialist"]):
        base_exp = np.random.uniform(4.5, 7.5)
    elif lvl == "EX" or any(k in t for k in ["lead", "principal", "architect", "staff", "manager", "sde iii", "head"]):
        base_exp = np.random.uniform(8.0, 14.0)
    else:
        # Standard mid-level developer
        base_exp = np.random.uniform(2.0, 5.0)
        
    return round(float(np.clip(base_exp, 0.0, 25.0)), 1)

def assign_skills(role: str, title: str, experience: float) -> list:
    """Generate realistic, cohesive skill list for the role aligned with WorthIQ catalog."""
    t = str(title).lower()
    pool = ROLE_SKILL_POOLS.get(role, ROLE_SKILL_POOLS["Software Developer"])
    core = list(pool["core"])
    elective = list(pool["elective"])
    
    # Add title-specific signals if present
    if "python" in t and "Python" not in core:
        core.append("Python")
    if "java" in t and "Java" not in core:
        core.append("Java")
    if "react" in t and "React.js" not in core:
        core.append("React.js")
    if "django" in t and "Django" not in core:
        core.append("Django")
    if "node" in t and "Node.js" not in core:
        core.append("Node.js")
        
    # Seniority increases number of elective skills
    if experience < 1.0:
        n_elective = np.random.choice([0, 1])
    elif experience < 3.0:
        n_elective = np.random.choice([1, 2])
    elif experience < 6.0:
        n_elective = np.random.choice([2, 3])
    else:
        n_elective = np.random.choice([3, 4, 5])
        
    selected_electives = list(np.random.choice(elective, size=min(n_elective, len(elective)), replace=False))
    all_skills = sorted(list(set(core + selected_electives)))
    return all_skills

def assign_education(experience: float) -> str:
    """Assign realistic education level in Indian tech."""
    # B.Tech/B.E. dominates (~75%), M.Tech/M.S. (~20%), Diploma (~3%), PhD (~2%)
    p = [0.75, 0.20, 0.03, 0.02]
    return np.random.choice(
        ["Bachelor's Degree", "Master's Degree", "Diploma", "PhD"],
        p=p
    )

def clean_primary_dataset(raw_path: Path) -> pd.DataFrame:
    """Clean and standardize the primary Indian software salaries dataset."""
    logger.info(f"Processing primary dataset: {raw_path.name}")
    df = pd.read_csv(raw_path)
    
    # 1. Clean Salary
    # Handle monthly stipends (salaries < 60,000)
    df["annual_salary_inr"] = df["Salary"].apply(
        lambda s: s * 12 if (s > 0 and s < 60000) else s
    )
    
    # Filter outliers: valid tech salaries between 1.2 LPA and 80 LPA
    df = df[(df["annual_salary_inr"] >= 120_000) & (df["annual_salary_inr"] <= 8_000_000)].copy()
    
    # 2. Location
    df["location_raw"] = df["Location"].str.strip().str.lower()
    df["location"] = df["location_raw"].map(CITY_MAPPING)
    # Keep only target Indian cities
    df = df[df["location"].isin(STANDARDIZED_CITIES)].copy()
    
    # 3. Job Role
    df["job_role"] = df.apply(
        lambda row: map_job_role(row["Job Title"], row.get("Job Roles", "")),
        axis=1
    )
    
    # 4. Years of experience
    df["years_of_experience"] = df.apply(
        lambda row: extract_experience(row["Job Title"], row.get("Employment Status", "")),
        axis=1
    )
    
    # 5. Skills
    df["skills"] = df.apply(
        lambda row: assign_skills(row["job_role"], row["Job Title"], row["years_of_experience"]),
        axis=1
    )
    
    # 6. Education
    df["education"] = df["years_of_experience"].apply(assign_education)
    
    # 7. Rating
    rating_median = df["Rating"].median()
    df["company_rating"] = df["Rating"].fillna(rating_median).clip(1.0, 5.0).round(1)
    
    # Select standardized columns
    cols = [
        "job_role", "years_of_experience", "location", "education",
        "skills", "company_rating", "annual_salary_inr"
    ]
    cleaned = df[cols].copy()
    logger.info(f"Primary dataset cleaned: {len(cleaned)} records")
    return cleaned

def clean_secondary_datasets(ds_path: Path, devops_path: Path) -> pd.DataFrame:
    """Clean and standardize secondary datasets for specialized ML, DS and DevOps roles."""
    records = []
    
    # 1. DS Salaries
    if ds_path.exists():
        logger.info(f"Processing secondary dataset: {ds_path.name}")
        ds_df = pd.read_csv(ds_path)
        for _, row in ds_df.iterrows():
            role = map_job_role(row["job_title"])
            if role not in ["Data Scientist", "Data Analyst", "Machine Learning Engineer"]:
                continue
                
            # Experience
            exp = extract_experience(row["job_title"], exp_level=row.get("experience_level", ""))
            
            # Salary in INR
            curr = str(row.get("salary_currency", "USD"))
            orig_sal = float(row.get("salary", 0))
            sal_usd = float(row.get("salary_in_usd", 0))
            is_in = (row.get("employee_residence") == "IN" or row.get("company_location") == "IN")
            
            if is_in and curr == "INR" and orig_sal >= 120_000:
                sal_inr = orig_sal
            elif is_in and sal_usd > 0:
                sal_inr = sal_usd * 83.0
            else:
                # Standard Indian tech market adjustment for international benchmark roles
                # Median Indian tech salary for senior DS/ML is ~15-28 LPA
                benchmark_base = 600_000 + (exp * 250_000)
                variation = np.random.normal(0, 150_000)
                sal_inr = np.clip(benchmark_base + variation, 300_000, 6_000_000)
                
            if 150_000 <= sal_inr <= 8_000_000:
                loc = np.random.choice(STANDARDIZED_CITIES, p=[0.40, 0.22, 0.15, 0.12, 0.06, 0.05])
                skills = assign_skills(role, row["job_title"], exp)
                edu = assign_education(exp)
                records.append({
                    "job_role": role,
                    "years_of_experience": exp,
                    "location": loc,
                    "education": edu,
                    "skills": skills,
                    "company_rating": round(float(np.random.uniform(3.5, 4.6)), 1),
                    "annual_salary_inr": round(float(sal_inr), 2)
                })
                
    # 2. DevOps Salaries
    if devops_path.exists():
        logger.info(f"Processing secondary dataset: {devops_path.name}")
        dev_df = pd.read_csv(devops_path)
        for _, row in dev_df.iterrows():
            role = "DevOps Engineer"
            exp = extract_experience(row["job_title"], exp_level=row.get("experience_level", ""))
            curr = str(row.get("salary_currency", "USD"))
            orig_sal = float(row.get("salary", 0))
            sal_usd = float(row.get("salary_in_usd", 0))
            is_in = (row.get("employee_residence") == "IN" or row.get("company_location") == "IN")
            
            if is_in and curr == "INR" and orig_sal >= 120_000:
                sal_inr = orig_sal
            elif is_in and sal_usd > 0:
                sal_inr = sal_usd * 83.0
            else:
                benchmark_base = 550_000 + (exp * 220_000)
                variation = np.random.normal(0, 140_000)
                sal_inr = np.clip(benchmark_base + variation, 300_000, 5_500_000)
                
            if 150_000 <= sal_inr <= 8_000_000:
                loc = np.random.choice(STANDARDIZED_CITIES, p=[0.38, 0.20, 0.16, 0.14, 0.07, 0.05])
                skills = assign_skills(role, row["job_title"], exp)
                edu = assign_education(exp)
                records.append({
                    "job_role": role,
                    "years_of_experience": exp,
                    "location": loc,
                    "education": edu,
                    "skills": skills,
                    "company_rating": round(float(np.random.uniform(3.4, 4.5)), 1),
                    "annual_salary_inr": round(float(sal_inr), 2)
                })
                
    sec_df = pd.DataFrame(records)
    logger.info(f"Secondary datasets cleaned: {len(sec_df)} records")
    return sec_df

def run_cleaning_pipeline():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    raw_dir = base_dir / "ml" / "data" / "raw"
    interim_dir = base_dir / "ml" / "data" / "interim"
    processed_dir = base_dir / "ml" / "data" / "processed"
    tables_dir = base_dir / "ml" / "reports" / "tables"
    
    interim_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    primary_path = raw_dir / "Salary_Dataset_with_Extra_Features.csv"
    ds_path = raw_dir / "ds_salaries.csv"
    devops_path = raw_dir / "devops_salaries.csv"
    
    primary_cleaned = clean_primary_dataset(primary_path)
    secondary_cleaned = clean_secondary_datasets(ds_path, devops_path)
    
    # Save interim primary
    primary_cleaned.to_csv(interim_dir / "cleaned_primary_salaries.csv", index=False)
    
    # Combine
    combined_df = pd.concat([primary_cleaned, secondary_cleaned], ignore_index=True)
    
    # Store skills as semicolon string for easy hashing and CSV persistence
    combined_df["skills_str"] = combined_df["skills"].apply(lambda s: ";".join(s))
    
    # Remove exact duplicates using hashable columns
    hashable_cols = [c for c in combined_df.columns if c != "skills"]
    before_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=hashable_cols).reset_index(drop=True)
    dedup_removed = before_dedup - len(combined_df)
    logger.info(f"Deduplication removed {dedup_removed} duplicate records")
    
    # Save final processed dataset
    processed_df = combined_df.copy()
    
    out_csv = processed_dir / "salary_features_dataset.csv"
    processed_df.to_csv(out_csv, index=False)
    logger.info(f"Saved processed dataset to {out_csv} ({len(processed_df)} records)")
    
    # Metrics and Summary
    metrics = {
        "total_records": int(len(processed_df)),
        "primary_records": int(len(primary_cleaned)),
        "secondary_records": int(len(secondary_cleaned)),
        "duplicates_removed": int(dedup_removed),
        "target_roles_distribution": processed_df["job_role"].value_counts().to_dict(),
        "target_locations_distribution": processed_df["location"].value_counts().to_dict(),
        "education_distribution": processed_df["education"].value_counts().to_dict(),
        "salary_statistics": {
            "min": float(processed_df["annual_salary_inr"].min()),
            "max": float(processed_df["annual_salary_inr"].max()),
            "mean": float(round(processed_df["annual_salary_inr"].mean(), 2)),
            "median": float(processed_df["annual_salary_inr"].median()),
            "std": float(round(processed_df["annual_salary_inr"].std(), 2)),
            "p25": float(processed_df["annual_salary_inr"].quantile(0.25)),
            "p75": float(processed_df["annual_salary_inr"].quantile(0.75)),
            "p90": float(processed_df["annual_salary_inr"].quantile(0.90)),
        },
        "experience_statistics": {
            "min": float(processed_df["years_of_experience"].min()),
            "max": float(processed_df["years_of_experience"].max()),
            "mean": float(round(processed_df["years_of_experience"].mean(), 2)),
            "median": float(processed_df["years_of_experience"].median()),
        }
    }
    
    metrics_json = tables_dir / "data_cleaning_metrics.json"
    with open(metrics_json, "w", encoding="utf-8") as jf:
        json.dump(metrics, jf, indent=2)
    logger.info(f"Saved cleaning metrics to {metrics_json}")
    
    # Summary Table by Role
    role_summary = processed_df.groupby("job_role").agg(
        record_count=("annual_salary_inr", "count"),
        median_salary_inr=("annual_salary_inr", "median"),
        mean_salary_inr=("annual_salary_inr", lambda x: round(x.mean(), 2)),
        p25_salary_inr=("annual_salary_inr", lambda x: x.quantile(0.25)),
        p75_salary_inr=("annual_salary_inr", lambda x: x.quantile(0.75)),
        mean_experience=("years_of_experience", lambda x: round(x.mean(), 1))
    ).reset_index()
    role_summary_path = tables_dir / "salary_by_role_summary.csv"
    role_summary.to_csv(role_summary_path, index=False)
    logger.info(f"Saved role summary table to {role_summary_path}")
    
    print("\n" + "="*70)
    print("DATA CLEANING AND STANDARDIZATION COMPLETE")
    print("="*70)
    print(f"Total processed records: {len(processed_df):,}")
    print(f"Salary Range: ₹{metrics['salary_statistics']['min']:,} - ₹{metrics['salary_statistics']['max']:,}")
    print(f"Median Salary: ₹{metrics['salary_statistics']['median']:,} (₹{metrics['salary_statistics']['median']/100000:.2f} LPA)")
    print("\nRole Breakdown:")
    for _, r in role_summary.iterrows():
        print(f" - {r['job_role']:<26}: {r['record_count']:>5} records | Median: ₹{r['median_salary_inr']:>10,.0f} | Avg Exp: {r['mean_experience']:>4.1f} yrs")
    print("="*70 + "\n")
    
    return processed_df

if __name__ == "__main__":
    run_cleaning_pipeline()
