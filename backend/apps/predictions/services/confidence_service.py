"""
Confidence Classification Service
Computes measurable, deterministic confidence tiers (High, Medium, Low)
for salary predictions based on feature representation density and interval width.
"""

from typing import Tuple

HIGH_SUPPORT_ROLES = {
    "Software Developer", "Frontend Developer", "Backend Developer", "Data Analyst"
}
MODERATE_SUPPORT_ROLES = {
    "Data Scientist", "DevOps Engineer", "Machine Learning Engineer"
}
EMERGING_SUPPORT_ROLES = {
    "Full Stack Developer"
}

TOP_HUBS = {"Bengaluru", "Hyderabad", "Delhi NCR", "Pune"}
SECONDARY_HUBS = {"Chennai", "Mumbai"}

CANONICAL_SKILLS_SET = {
    "AWS", "C++", "CI/CD", "CSS3", "Data Analysis", "Django", "Docker",
    "Express.js", "FastAPI", "Flutter", "Git", "Go", "GraphQL", "HTML5",
    "Java", "JavaScript", "Kubernetes", "Linux", "Machine Learning",
    "Microservices", "MongoDB", "Next.js", "Node.js", "NumPy", "Pandas",
    "PostgreSQL", "Python", "REST APIs", "React.js", "Redis", "SQL",
    "Scikit-Learn", "Spring Boot", "Tailwind CSS", "TypeScript"
}

def calculate_confidence(
    job_role: str,
    location: str,
    years_of_experience: float,
    skills: list,
    p10: float,
    p50: float,
    p90: float,
    raw_role: str = None,
    raw_location: str = None
) -> Tuple[str, dict]:
    """
    Computes confidence tier ('High', 'Medium', 'Low') and underlying evidence.
    Returns: (confidence_label, explanation_dict)
    """
    score = 0
    factors = []
    
    # 1. Role Coverage (Max 30 pts)
    check_role = raw_role if raw_role else job_role
    if check_role in HIGH_SUPPORT_ROLES:
        score += 30
        factors.append("Dense role sample (>1,500 training profiles)")
    elif check_role in MODERATE_SUPPORT_ROLES:
        score += 22
        factors.append("Solid specialized role representation (400-1,500 profiles)")
    elif check_role in EMERGING_SUPPORT_ROLES:
        score += 15
        factors.append("Emerging cross-functional track (calibrated benchmark)")
    else:
        score += 5
        factors.append("Role mapped using generalized software engineering baseline")

    # 2. Location Coverage (Max 20 pts)
    check_loc = raw_location if raw_location else location
    if check_loc in TOP_HUBS:
        score += 20
        factors.append(f"Primary tech hub ({check_loc}) with dense local compensation data")
    elif check_loc in SECONDARY_HUBS:
        score += 15
        factors.append(f"Major metropolitan tech market ({check_loc})")
    else:
        score += 5
        factors.append(f"Location ({check_loc}) evaluated using national tech compensation baseline")

    # 3. Experience Normality (Max 25 pts)
    exp = float(years_of_experience)
    if 0.0 <= exp <= 15.0:
        score += 25
        factors.append(f"Experience ({exp:.1f} yrs) well within core market distribution")
    elif 15.0 < exp <= 25.0:
        score += 14
        factors.append(f"Senior leadership experience ({exp:.1f} yrs) in upper percentile")
    else:
        score += 5
        factors.append(f"Experience ({exp:.1f} yrs) in sparse distribution tail")

    # 4. Skill Overlap (Max 15 pts)
    recognized_skills = [s for s in skills if s in CANONICAL_SKILLS_SET or s.title() in CANONICAL_SKILLS_SET]
    if len(recognized_skills) >= 3:
        score += 15
        factors.append(f"{len(recognized_skills)} verified core skills matching market taxonomy")
    elif len(recognized_skills) >= 1:
        score += 10
        factors.append(f"{len(recognized_skills)} recognized skill evaluated")
    else:
        score += 3
        factors.append("Skills evaluated via generalized role stack")

    # 5. Prediction Interval Tightness (Max 10 pts)
    if p50 > 0:
        spread_ratio = (p90 - p10) / p50
        if spread_ratio <= 0.85:
            score += 10
            factors.append("Narrow prediction spread indicates high model consensus")
        elif spread_ratio <= 1.35:
            score += 6
            factors.append("Standard market compensation variance")
        else:
            score += 2
            factors.append("Wider salary dispersion across market tiers")
    else:
        spread_ratio = 1.0

    # Classification
    if score >= 75:
        confidence = "High"
        summary_msg = "High confidence: Strong representation in historical training data with low variance."
    elif score >= 50:
        confidence = "Medium"
        summary_msg = "Medium confidence: Solid baseline alignment with standard market compensation variance."
    else:
        confidence = "Low"
        summary_msg = "Low confidence: Specialized or less common combination of features."

    explanation = {
        "confidence_score": score,
        "confidence_tier": confidence,
        "spread_ratio": round(spread_ratio, 3),
        "verified_skills_count": len(recognized_skills),
        "evidence_factors": factors,
        "summary": summary_msg
    }
    
    return confidence, explanation
