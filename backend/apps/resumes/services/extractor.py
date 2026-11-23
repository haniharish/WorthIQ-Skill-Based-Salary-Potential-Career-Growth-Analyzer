"""
Information extraction and canonical skill recognition for resume text.
"""

import re
import logging
from typing import Dict, Any, List

from apps.intelligence.services.skill_normalization_service import get_taxonomy
from ml.src.features.mine_skill_cooccurrence import ALIAS_LOOKUP

logger = logging.getLogger("resumes.extractor")

EDUCATION_PATTERNS = [
    (r"\b(?:ph\.?d|doctorate)\b", "Doctorate / Ph.D."),
    (r"\b(?:m\.?tech|m\.?e\.?|master of technology|master of engineering)\b", "Master's Degree"),
    (r"\b(?:m\.?s\.?|master of science|mca)\b", "Master's Degree"),
    (r"\b(?:b\.?tech|b\.?e\.?|bachelor of technology|bachelor of engineering)\b", "Bachelor's Degree"),
    (r"\b(?:b\.?s\.?|bachelor of science|bca)\b", "Bachelor's Degree"),
    (r"\b(?:bachelor'?s|undergraduate|degree)\b", "Bachelor's Degree"),
    (r"\b(?:master'?s|postgraduate)\b", "Master's Degree"),
    (r"\b(?:diploma)\b", "Diploma"),
]

ROLE_KEYWORDS = [
    ("Full Stack Developer", [r"\bfull[\s-]?stack\b"]),
    ("Backend Developer", [r"\bbackend\b", r"\bback[\s-]?end\b"]),
    ("Frontend Developer", [r"\bfrontend\b", r"\bfront[\s-]?end\b", r"\bui developer\b"]),
    ("DevOps Engineer", [r"\bdevops\b", r"\bsre\b", r"\bsite reliability\b", r"\bcloud engineer\b"]),
    ("Data Scientist", [r"\bdata scientist\b", r"\bmachine learning engineer\b", r"\bai engineer\b"]),
    ("Data Analyst", [r"\bdata analyst\b", r"\bbusiness analyst\b"]),
    ("Machine Learning Engineer", [r"\bml engineer\b", r"\bmachine learning\b"]),
    ("Software Developer", [r"\bsoftware developer\b", r"\bsoftware engineer\b", r"\bsde\b"]),
]

def extract_evidence_snippet(text: str, match_start: int, match_end: int, window: int = 50) -> str:
    """Extracts a contextual snippet around the matched skill."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    raw = text[start:end].replace('\n', ' ').strip()
    return f"...{raw}..." if start > 0 or end < len(text) else raw

def extract_skills_from_text(raw_text: str) -> List[Dict[str, Any]]:
    """
    Identifies technical skills present in resume text using the canonical taxonomy and alias mapping.
    Prevents short-token false positives (e.g., 'C' in 'Cat', 'R' in 'Rate').
    """
    taxonomy = get_taxonomy()
    found_skills = {}  # canonical_name -> item dict
    lower_text = raw_text.lower()

    # 1. Match canonical names directly
    for canon_name, data in taxonomy.items():
        # Build regex for canonical name
        pattern_str = r'\b' + re.escape(canon_name.lower()) + r'\b'
        match = re.search(pattern_str, lower_text)
        if match:
            snippet = extract_evidence_snippet(raw_text, match.start(), match.end())
            found_skills[canon_name] = {
                "name": canon_name,
                "canonical_name": canon_name,
                "category": data.get("category", "General Tech"),
                "confidence": 0.95,
                "matched_token": canon_name,
                "evidence_snippet": snippet
            }

    # 2. Match aliases
    for alias, canon_name in ALIAS_LOOKUP.items():
        if canon_name in found_skills:
            continue  # Already recognized canonical
        
        # Guard against single-letter false positives like 'c' or 'r'
        if len(alias) <= 1:
            pattern_str = r'(?:\b|[\s,/])' + re.escape(alias) + r'(?:\b|[\s,/])'
        elif alias in ['go', 'git', 'sql', 'aws']:
            pattern_str = r'\b' + re.escape(alias) + r'\b'
        else:
            pattern_str = r'\b' + re.escape(alias) + r'\b'

        match = re.search(pattern_str, lower_text)
        if match:
            tax_entry = taxonomy.get(canon_name, {})
            snippet = extract_evidence_snippet(raw_text, match.start(), match.end())
            found_skills[canon_name] = {
                "name": canon_name,
                "canonical_name": canon_name,
                "category": tax_entry.get("category", "General Tech"),
                "confidence": 0.88,
                "matched_token": alias,
                "evidence_snippet": snippet
            }

    return list(found_skills.values())


def extract_candidate_metadata(raw_text: str) -> Dict[str, Any]:
    """
    Extracts contact info, detected experience, education, and likely job titles.
    """
    meta = {
        "email": None,
        "phone": None,
        "detected_experience_years": None,
        "education": None,
        "detected_role": None,
    }

    # Email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', raw_text)
    if email_match:
        meta["email"] = email_match.group(0)

    # Phone (Indian & international standard patterns)
    phone_match = re.search(r'(?:\+?91[\s-]?)?[6-9]\d{9}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', raw_text)
    if phone_match:
        meta["phone"] = phone_match.group(0).strip()

    # Education
    lower_text = raw_text.lower()
    for pattern, edu_title in EDUCATION_PATTERNS:
        if re.search(pattern, lower_text):
            meta["education"] = edu_title
            break

    # Experience
    exp_match = re.search(r'\b(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+experience|\s+exp)?\b', lower_text)
    if exp_match:
        try:
            val = float(exp_match.group(1))
            if 0 <= val <= 45:
                meta["detected_experience_years"] = val
                meta["years_of_experience"] = val
        except ValueError:
            pass

    # Job Role
    for role_title, patterns in ROLE_KEYWORDS:
        for p in patterns:
            if re.search(p, lower_text):
                meta["detected_role"] = role_title
                break
        if meta["detected_role"]:
            break

    return meta


def extract_resume_intelligence(raw_text: str) -> Dict[str, Any]:
    """
    Orchestrates full extraction pipeline returning extracted skills, candidate info, and text metrics.
    """
    skills = extract_skills_from_text(raw_text)
    meta = extract_candidate_metadata(raw_text)
    
    return {
        "raw_text_length": len(raw_text),
        "extracted_skills": skills,
        "candidate_info": meta,
        "total_skills_detected": len(skills)
    }
