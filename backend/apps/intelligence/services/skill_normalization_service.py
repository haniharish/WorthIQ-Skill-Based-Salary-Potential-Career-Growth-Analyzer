"""
Skill Normalization Service
Provides canonical resolution, alias lookup, and category organization
for technology skills evaluated across WorthIQ.
"""

from ml.src.features.mine_skill_cooccurrence import SKILL_TAXONOMY, ALIAS_LOOKUP
from apps.intelligence.models import CanonicalSkill, SkillAlias

def normalize_skill(raw_name):
    """
    Resolves raw or aliased skill string to its canonical name.
    Example: 'JS' -> 'JavaScript', 'drf' -> 'Django', 'k8s' -> 'Kubernetes'.
    """
    if not raw_name:
        return ""
    cleaned = str(raw_name).strip().lower()
    return ALIAS_LOOKUP.get(cleaned, str(raw_name).strip())

def normalize_skill_list(skills_list):
    """
    Takes an iterable of raw skill strings, normalizes them, removes duplicates
    while preserving order, and returns clean canonical names.
    """
    if not skills_list:
        return []

    seen = set()
    result = []
    for s in skills_list:
        canon = normalize_skill(s)
        if canon and canon.lower() not in seen:
            seen.add(canon.lower())
            result.append(canon)
    return result

def get_taxonomy():
    """Returns the full in-memory canonical skill taxonomy."""
    return SKILL_TAXONOMY

def seed_skills_in_db():
    """Seeds CanonicalSkill and SkillAlias database records from SKILL_TAXONOMY."""
    created_skills = 0
    created_aliases = 0

    for name, data in SKILL_TAXONOMY.items():
        skill_obj, created = CanonicalSkill.objects.get_or_create(
            name=name,
            defaults={
                'category': data['category'],
                'description': data['description'],
                'market_importance_tier': 'Tier-1'
            }
        )
        if created:
            created_skills += 1

        for alias in data.get('aliases', []):
            alias_obj, a_created = SkillAlias.objects.get_or_create(
                alias=alias.lower(),
                defaults={'canonical_skill': skill_obj}
            )
            if a_created:
                created_aliases += 1

    return created_skills, created_aliases
