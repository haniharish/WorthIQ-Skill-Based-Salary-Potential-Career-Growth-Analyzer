"""
WorthIQ - Exploratory Data Analysis (EDA) Script
Generates professional analytics visualizations and summary tables
evaluating salary distributions, experience dynamics, regional variations,
and skill premiums across the Indian tech job market.
"""

import os
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#D1D5DB"
plt.rcParams["axes.linewidth"] = 0.8

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("eda")

def run_eda():
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "ml" / "data" / "processed" / "salary_features_dataset.csv"
    fig_dir = base_dir / "ml" / "reports" / "figures"
    table_dir = base_dir / "ml" / "reports" / "tables"
    
    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Loading processed dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Parse skills
    df["skill_list"] = df["skills_str"].apply(lambda s: str(s).split(";") if pd.notnull(s) else [])
    df["skill_count"] = df["skill_list"].apply(len)
    df["salary_lpa"] = df["annual_salary_inr"] / 100_000.0
    
    logger.info(f"Loaded {len(df)} records. Commencing EDA visualizations...")
    
    # -------------------------------------------------------------
    # 1. Salary Distribution (Raw and Log-transformed)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
    
    # Raw LPA distribution
    sns.histplot(df["salary_lpa"], bins=40, kde=True, color="#4F46E5", ax=axes[0], edgecolor="white")
    median_lpa = df["salary_lpa"].median()
    mean_lpa = df["salary_lpa"].mean()
    axes[0].axvline(median_lpa, color="#10B981", linestyle="--", linewidth=1.8, label=f"Median: {median_lpa:.1f} LPA")
    axes[0].axvline(mean_lpa, color="#EF4444", linestyle=":", linewidth=1.8, label=f"Mean: {mean_lpa:.1f} LPA")
    axes[0].set_title("Annual Salary Distribution (LPA)", fontsize=13, fontweight="bold", pad=12)
    axes[0].set_xlabel("Salary (Lakhs INR / Year)", fontsize=11)
    axes[0].set_ylabel("Frequency", fontsize=11)
    axes[0].legend(frameon=True, facecolor="white")
    
    # Log-transformed distribution
    log_salary = np.log1p(df["annual_salary_inr"])
    sns.histplot(log_salary, bins=40, kde=True, color="#06B6D4", ax=axes[1], edgecolor="white")
    axes[1].set_title("Log-Transformed Salary Distribution (Normalizing Skew)", fontsize=13, fontweight="bold", pad=12)
    axes[1].set_xlabel("Log(Annual Salary INR)", fontsize=11)
    axes[1].set_ylabel("Frequency", fontsize=11)
    
    plt.tight_layout()
    fig_path1 = fig_dir / "01_salary_distribution.png"
    plt.savefig(fig_path1)
    plt.close()
    logger.info(f"Saved: {fig_path1.name}")

    # -------------------------------------------------------------
    # 2. Salary by Job Role (Boxplot)
    # -------------------------------------------------------------
    plt.figure(figsize=(13, 6), dpi=300)
    order_roles = df.groupby("job_role")["salary_lpa"].median().sort_values(ascending=False).index
    palette = sns.color_palette("mako", len(order_roles))
    
    ax = sns.boxplot(
        data=df,
        x="job_role",
        y="salary_lpa",
        order=order_roles,
        palette=palette,
        fliersize=2,
        linewidth=1.2,
        boxprops=dict(alpha=0.85)
    )
    plt.xticks(rotation=25, ha="right", fontsize=10, fontweight="medium")
    plt.title("Indian Tech Salary Distribution by Job Role", fontsize=14, fontweight="bold", pad=14)
    plt.xlabel("Standardized Job Role", fontsize=11, fontweight="bold")
    plt.ylabel("Annual Salary (LPA)", fontsize=11, fontweight="bold")
    plt.ylim(0, 50)  # Zoom in on primary band 0-50 LPA
    
    # Add median labels on top of boxes
    medians = df.groupby("job_role")["salary_lpa"].median().loc[order_roles]
    for i, med in enumerate(medians):
        ax.text(i, med + 1.2, f"{med:.1f}L", horizontalalignment="center", size=9, weight="bold", color="#1F2937")
        
    plt.tight_layout()
    fig_path2 = fig_dir / "02_salary_by_job_role.png"
    plt.savefig(fig_path2)
    plt.close()
    logger.info(f"Saved: {fig_path2.name}")

    # -------------------------------------------------------------
    # 3. Salary vs Experience (Trend / Regression)
    # -------------------------------------------------------------
    plt.figure(figsize=(12, 6), dpi=300)
    
    # Sample 3,000 points for clear scatter visualization without overplotting
    sample_df = df.sample(n=min(3000, len(df)), random_state=42)
    sns.scatterplot(
        data=sample_df,
        x="years_of_experience",
        y="salary_lpa",
        alpha=0.35,
        color="#6366F1",
        s=30,
        label="Employee Profile"
    )
    
    # Trend line with polynomial fit
    sns.regplot(
        data=df,
        x="years_of_experience",
        y="salary_lpa",
        scatter=False,
        order=2,
        color="#DC2626",
        line_kws={"linewidth": 2.5, "label": "Career Growth Trend (Poly Order 2)"}
    )
    
    plt.title("Experience vs. Annual Salary Trajectory in Indian Tech", fontsize=14, fontweight="bold", pad=14)
    plt.xlabel("Years of Professional Experience", fontsize=11, fontweight="bold")
    plt.ylabel("Annual Salary (LPA)", fontsize=11, fontweight="bold")
    plt.xlim(0, 20)
    plt.ylim(0, 50)
    plt.legend(frameon=True, facecolor="white")
    
    plt.tight_layout()
    fig_path3 = fig_dir / "03_salary_vs_experience.png"
    plt.savefig(fig_path3)
    plt.close()
    logger.info(f"Saved: {fig_path3.name}")

    # -------------------------------------------------------------
    # 4. Salary by City / Location
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5.5), dpi=300)
    city_stats = df.groupby("location").agg(
        median_lpa=("salary_lpa", "median"),
        mean_lpa=("salary_lpa", "mean"),
        count=("salary_lpa", "count")
    ).sort_values(by="median_lpa", ascending=False).reset_index()
    
    palette_city = sns.color_palette("crest", len(city_stats))
    ax = sns.barplot(
        data=city_stats,
        x="location",
        y="median_lpa",
        palette=palette_city,
        edgecolor="#374151"
    )
    for i, row in city_stats.iterrows():
        ax.text(i, row["median_lpa"] + 0.2, f"₹{row['median_lpa']:.1f}L\n(n={row['count']:,})", 
                ha="center", va="bottom", fontsize=9, fontweight="bold")
        
    plt.title("Median Tech Salary Across Major Indian Tech Hubs", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Tech Hub Location", fontsize=11, fontweight="bold")
    plt.ylabel("Median Salary (LPA)", fontsize=11, fontweight="bold")
    plt.ylim(0, city_stats["median_lpa"].max() * 1.25)
    
    plt.tight_layout()
    fig_path4 = fig_dir / "04_salary_by_location.png"
    plt.savefig(fig_path4)
    plt.close()
    logger.info(f"Saved: {fig_path4.name}")

    # -------------------------------------------------------------
    # 5. Top Technical Skills Frequency
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 7), dpi=300)
    all_skills = [skill for sublist in df["skill_list"] for skill in sublist]
    skill_counts = pd.Series(all_skills).value_counts().head(20)
    
    sns.barplot(
        x=skill_counts.values,
        y=skill_counts.index,
        palette="viridis",
        edgecolor="#1F2937",
        alpha=0.85
    )
    for i, v in enumerate(skill_counts.values):
        pct = (v / len(df)) * 100
        plt.text(v + 150, i, f"{v:,} ({pct:.1f}%)", va="center", fontsize=9, fontweight="bold")
        
    plt.title("Top 20 Most Frequent Technical Skills in Indian Tech Profiles", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Profile Frequency Count", fontsize=11, fontweight="bold")
    plt.ylabel("Technical Skill", fontsize=11, fontweight="bold")
    plt.xlim(0, skill_counts.max() * 1.18)
    
    plt.tight_layout()
    fig_path5 = fig_dir / "05_top_skills_frequency.png"
    plt.savefig(fig_path5)
    plt.close()
    logger.info(f"Saved: {fig_path5.name}")

    # -------------------------------------------------------------
    # 6. Correlation Heatmap
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6), dpi=300)
    numeric_corr_df = df[["years_of_experience", "company_rating", "skill_count", "annual_salary_inr", "salary_lpa"]].corr()
    
    sns.heatmap(
        numeric_corr_df,
        annot=True,
        cmap="coolwarm",
        fmt=".3f",
        linewidths=0.8,
        cbar_kws={"label": "Pearson Correlation"}
    )
    plt.title("Feature Correlation Heatmap", fontsize=13, fontweight="bold", pad=12)
    
    plt.tight_layout()
    fig_path6 = fig_dir / "06_correlation_heatmap.png"
    plt.savefig(fig_path6)
    plt.close()
    logger.info(f"Saved: {fig_path6.name}")

    # -------------------------------------------------------------
    # 7. Salary by Education
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 5), dpi=300)
    edu_order = ["Diploma", "Bachelor's Degree", "Master's Degree", "PhD"]
    ax = sns.boxplot(
        data=df,
        x="education",
        y="salary_lpa",
        order=edu_order,
        palette="Spectral",
        linewidth=1.2,
        fliersize=2
    )
    plt.title("Salary Distribution by Education Level", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Highest Education", fontsize=11, fontweight="bold")
    plt.ylabel("Annual Salary (LPA)", fontsize=11, fontweight="bold")
    plt.ylim(0, 45)
    
    edu_medians = df.groupby("education")["salary_lpa"].median().loc[edu_order]
    for i, med in enumerate(edu_medians):
        ax.text(i, med + 1.2, f"{med:.1f}L", horizontalalignment="center", size=9, weight="bold")
        
    plt.tight_layout()
    fig_path7 = fig_dir / "07_salary_by_education.png"
    plt.savefig(fig_path7)
    plt.close()
    logger.info(f"Saved: {fig_path7.name}")

    # -------------------------------------------------------------
    # Summary Tables Generation
    # -------------------------------------------------------------
    # 1. Overall stats
    stats_df = df[["years_of_experience", "company_rating", "skill_count", "annual_salary_inr", "salary_lpa"]].describe().round(2)
    stats_df.to_csv(table_dir / "eda_summary_statistics.csv")
    
    # 2. Location stats
    city_stats.to_csv(table_dir / "eda_location_salary_table.csv", index=False)
    
    # 3. Top skills table
    skills_table = pd.DataFrame({
        "skill": skill_counts.index,
        "count": skill_counts.values,
        "percentage": [(v / len(df)) * 100 for v in skill_counts.values]
    }).round(2)
    skills_table.to_csv(table_dir / "eda_skills_frequency_table.csv", index=False)
    
    # 4. Education stats
    edu_stats = df.groupby("education").agg(
        record_count=("salary_lpa", "count"),
        median_salary_lpa=("salary_lpa", "median"),
        mean_salary_lpa=("salary_lpa", "mean"),
        std_salary_lpa=("salary_lpa", "std")
    ).round(2).loc[edu_order].reset_index()
    edu_stats.to_csv(table_dir / "eda_education_salary_table.csv", index=False)
    
    logger.info("EDA completed successfully. All figures and tables created.")

if __name__ == "__main__":
    run_eda()
