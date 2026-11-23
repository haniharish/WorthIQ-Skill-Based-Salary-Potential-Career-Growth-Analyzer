"""
Skill Co-occurrence Service
Loads and serves empirical pairwise co-occurrence frequencies,
support/confidence metrics, and compensation lift from the 25,332 records dataset.
"""

import json
from pathlib import Path
from functools import lru_cache

COOCCURRENCE_FILE = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "ml"
    / "data"
    / "processed"
    / "skill_cooccurrence_matrix.json"
)

@lru_cache(maxsize=1)
def load_cooccurrence_data():
    """Loads and caches the pre-mined skill co-occurrence JSON matrix."""
    if not COOCCURRENCE_FILE.exists():
        return {
            "total_dataset_records": 25332,
            "taxonomy": {},
            "skill_statistics": {},
            "top_cooccurrences": []
        }
    with open(COOCCURRENCE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_skill_statistics(skill_name=None):
    """Returns frequency, support %, and median salary for skills."""
    data = load_cooccurrence_data()
    stats = data.get("skill_statistics", {})
    if skill_name:
        return stats.get(skill_name)
    return stats

def get_top_cooccurrences(skill_name=None, limit=25):
    """
    Returns top co-occurring skill pairs. If skill_name is given,
    filters pairs containing that skill.
    """
    data = load_cooccurrence_data()
    pairs = data.get("top_cooccurrences", [])

    if skill_name:
        skill_clean = skill_name.strip().lower()
        filtered = [
            p for p in pairs
            if p["skill_a"].lower() == skill_clean or p["skill_b"].lower() == skill_clean
        ]
        return filtered[:limit]

    return pairs[:limit]

def analyze_bundle_synergy(skills_list):
    """
    Analyzes co-occurrence strength and synergy among a set of skills.
    Returns matched pairs, overall synergy score, and highest-value pairings.
    """
    if not skills_list or len(skills_list) < 2:
        return {
            "pair_count": 0,
            "pairs": [],
            "synergy_score": 50,
            "synergy_label": "Baseline / Isolated Skills"
        }

    data = load_cooccurrence_data()
    pairs_catalog = {
        (p["skill_a"].lower(), p["skill_b"].lower()): p
        for p in data.get("top_cooccurrences", [])
    }

    found_pairs = []
    total_lift = 0.0

    lower_skills = [s.strip().lower() for s in skills_list]
    for i in range(len(lower_skills)):
        for j in range(i + 1, len(lower_skills)):
            s1, s2 = sorted([lower_skills[i], lower_skills[j]])
            if (s1, s2) in pairs_catalog:
                matched = pairs_catalog[(s1, s2)]
                found_pairs.append(matched)
                total_lift += matched.get("lift", 1.0)

    avg_lift = (total_lift / len(found_pairs)) if found_pairs else 1.0
    # Normalize synergy score 0-100
    synergy_score = min(100, int(avg_lift * 50 + len(found_pairs) * 3))

    if synergy_score >= 80:
        label = "High Architectural Synergy"
    elif synergy_score >= 60:
        label = "Complementary Tech Stack"
    else:
        label = "Moderate Stacking"

    return {
        "pair_count": len(found_pairs),
        "pairs": found_pairs[:15],
        "synergy_score": synergy_score,
        "synergy_label": label
    }
