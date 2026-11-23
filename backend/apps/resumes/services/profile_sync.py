"""
Service for merging user-confirmed resume skills and metadata into UserProfile.
"""

import logging
from typing import List, Dict, Any
from apps.profiles.models import UserProfile, Skill
from apps.intelligence.services.skill_normalization_service import normalize_skill

logger = logging.getLogger("resumes.profile_sync")

def sync_confirmed_skills_to_profile(
    user=None,
    confirmed_skills: List[str] = None,
    update_meta_fields: Dict[str, Any] = None,
    user_profile=None,
    apply_experience: bool = False,
    experience_val: float = None,
) -> Dict[str, Any]:
    """
    Applies user-confirmed skills to their persistent UserProfile.
    Uses canonical skill objects, prevents duplicates, and updates metadata if specified.
    """
    if confirmed_skills is None:
        confirmed_skills = []

    if user_profile is not None:
        profile = user_profile
        user = profile.user
    elif user is not None:
        profile, _ = UserProfile.objects.get_or_create(user=user)
    else:
        raise ValueError("Either user or user_profile must be provided")

    initial_count = profile.skills.count()

    added_skills = []
    already_present = []

    # Normalized canonical skills
    for raw_skill in confirmed_skills:
        canonical_name = normalize_skill(raw_skill)
        if not canonical_name:
            continue

        skill_obj, _ = Skill.objects.get_or_create(name=canonical_name)
        if profile.skills.filter(id=skill_obj.id).exists():
            already_present.append(canonical_name)
        else:
            profile.skills.add(skill_obj)
            added_skills.append(canonical_name)

    # Optional profile metadata update if user chose to accept detected values
    updated_fields = []
    if apply_experience and experience_val is not None:
        profile.years_of_experience = float(experience_val)
        updated_fields.append("years_of_experience")

    if update_meta_fields:
        if update_meta_fields.get("job_role") and not profile.job_role:
            profile.job_role = update_meta_fields["job_role"]
            updated_fields.append("job_role")
        if update_meta_fields.get("years_of_experience") is not None and (profile.years_of_experience is None or profile.years_of_experience == 0):
            try:
                profile.years_of_experience = float(update_meta_fields["years_of_experience"])
                updated_fields.append("years_of_experience")
            except (ValueError, TypeError):
                pass
        if update_meta_fields.get("education") and not profile.education:
            profile.education = update_meta_fields["education"]
            updated_fields.append("education")

    if updated_fields:
        profile.save()

    return {
        "status": "success",
        "added_count": len(added_skills),
        "initial_skill_count": initial_count,
        "new_skill_count": profile.skills.count(),
        "skills_added": added_skills,
        "skills_already_present": already_present,
        "updated_profile_fields": updated_fields
    }
