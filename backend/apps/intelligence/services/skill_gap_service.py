"""
Skill Gap Analysis Service
Evaluates skill deficits between candidate's current capabilities
and a target technology role using DAG topological dependencies.
"""

from apps.intelligence.models import JobRole
from apps.intelligence.services.skill_normalization_service import normalize_skill_list
from apps.intelligence.services.role_matching_service import DEFAULT_ROLES_DATA

# Directed Acyclic Graph (DAG) of technology skill prerequisites
SKILL_DEPENDENCY_GRAPH = {
    # Web & Full Stack track
    "HTML5": [],
    "CSS3": ["HTML5"],
    "Tailwind CSS": ["CSS3"],
    "JavaScript": ["HTML5"],
    "TypeScript": ["JavaScript"],
    "React.js": ["JavaScript", "HTML5", "CSS3"],
    "Next.js": ["React.js", "TypeScript"],
    "Node.js": ["JavaScript"],
    "Express.js": ["Node.js"],
    "REST APIs": ["Node.js"],
    "GraphQL": ["REST APIs", "Node.js"],
    
    # Python & Backend track
    "Python": [],
    "SQL": [],
    "PostgreSQL": ["SQL"],
    "MongoDB": [],
    "Redis": ["SQL"],
    "Django": ["Python", "SQL", "REST APIs"],
    "FastAPI": ["Python", "REST APIs"],
    "Java": [],
    "Spring Boot": ["Java", "SQL", "REST APIs"],
    "C++": [],
    "Go": [],
    "Microservices": ["REST APIs", "Docker"],

    # Cloud & DevOps track
    "Linux": [],
    "Git": [],
    "Docker": ["Linux", "Git"],
    "CI/CD": ["Git", "Docker"],
    "Kubernetes": ["Docker", "Linux"],
    "AWS": ["Linux", "Docker"],

    # Data & AI track
    "Data Analysis": ["SQL"],
    "Pandas": ["Python"],
    "NumPy": ["Python"],
    "Scikit-learn": ["Python", "NumPy", "Pandas"],
    "Machine Learning": ["Python", "NumPy", "Pandas", "Scikit-learn"],
}

def analyze_skill_gap(candidate_skills, target_role_id_or_title):
    """
    Computes precise skill gap for a target role.

    Returns:
        dict containing:
            - target_role_title
            - already_possessed: list of possessed skills
            - missing_required: list of mandatory missing skills
            - missing_preferred: list of high-value preferred missing skills
            - total_gap_count
            - readiness_score
    """
    norm_candidate = set(s.lower() for s in normalize_skill_list(candidate_skills))

    # Lookup role
    role_dict = None
    if isinstance(target_role_id_or_title, int) or (isinstance(target_role_id_or_title, str) and target_role_id_or_title.isdigit()):
        db_role = JobRole.objects.filter(id=int(target_role_id_or_title)).first()
        if db_role:
            role_dict = {
                "id": db_role.id,
                "title": db_role.title,
                "required_skills": [sr.skill.name for sr in db_role.skill_requirements.filter(is_mandatory=True)],
                "preferred_skills": [sr.skill.name for sr in db_role.skill_requirements.filter(is_mandatory=False)],
            }

    if not role_dict:
        # Match by title in DEFAULT_ROLES_DATA
        target_title = str(target_role_id_or_title).strip().lower()
        for r in DEFAULT_ROLES_DATA:
            if r["title"].lower() == target_title:
                role_dict = r
                break

    if not role_dict:
        role_dict = DEFAULT_ROLES_DATA[0]  # Fallback to Full Stack Developer

    required = role_dict["required_skills"]
    preferred = role_dict["preferred_skills"]

    possessed_req = [s for s in required if s.lower() in norm_candidate]
    missing_req = [s for s in required if s.lower() not in norm_candidate]

    possessed_pref = [s for s in preferred if s.lower() in norm_candidate]
    missing_pref = [s for s in preferred if s.lower() not in norm_candidate]

    all_possessed = possessed_req + possessed_pref
    total_role_skills = len(required) + len(preferred)
    readiness = int((len(all_possessed) / max(1, total_role_skills)) * 100)

    return {
        "role_id": role_dict.get("id"),
        "role_title": role_dict["title"],
        "already_possessed": all_possessed,
        "missing_required": missing_req,
        "missing_preferred": missing_pref,
        "total_missing_count": len(missing_req) + len(missing_pref),
        "readiness_score": readiness
    }
