"""
Skill Intelligence Views
Endpoints for skill taxonomy, ablation valuation, co-occurrence matrix,
and controlled counterfactual What-If comparisons.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.intelligence.models import CanonicalSkill
from apps.intelligence.serializers import (
    CanonicalSkillSerializer,
    CounterfactualCompareSerializer
)
from apps.intelligence.services.skill_normalization_service import (
    get_taxonomy,
    normalize_skill_list
)
from apps.intelligence.services.skill_cooccurrence_service import (
    get_skill_statistics,
    get_top_cooccurrences,
    analyze_bundle_synergy
)
from apps.intelligence.services.skill_impact_service import (
    evaluate_skill_impact,
    compare_counterfactual
)

class SkillListView(APIView):
    """
    GET /api/intelligence/skills/
    Returns full canonical skill taxonomy grouped by categories.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = CanonicalSkill.objects.prefetch_related('aliases').all()
        if skills.exists():
            serializer = CanonicalSkillSerializer(skills, many=True)
            skill_list = serializer.data
        else:
            tax = get_taxonomy()
            skill_list = [
                {
                    "name": k,
                    "category": v["category"],
                    "description": v["description"],
                    "aliases": v["aliases"]
                }
                for k, v in tax.items()
            ]

        # Group by category
        categories = {}
        for s in skill_list:
            cat = s["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(s)

        return Response({
            "total_count": len(skill_list),
            "categories": categories,
            "skills": skill_list
        }, status=status.HTTP_200_OK)


class SkillImpactView(APIView):
    """
    GET /api/intelligence/skills/impact/
    Evaluates marginal compensation contributions of the authenticated user's
    skills (or query params) through controlled single-skill ablation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = getattr(request.user, 'profile', None)
        except Exception:
            profile = None
        
        # Pull defaults from profile or query params
        role = request.query_params.get('job_role') or (profile.job_role if profile else "Software Developer")
        exp = float(request.query_params.get('years_of_experience') or (profile.years_of_experience if profile else 3.0))
        loc = request.query_params.get('location') or (profile.location if profile else "Bengaluru")
        edu = request.query_params.get('education') or (profile.education if profile else "Bachelor's Degree")

        skills_param = request.query_params.get('skills')
        if skills_param:
            skills = [s.strip() for s in skills_param.split(',') if s.strip()]
        elif profile:
            skills = [s.name for s in profile.skills.all()]
        else:
            skills = ["Python", "SQL", "Git", "REST APIs", "Docker"]

        profile_payload = {
            "job_role": role,
            "years_of_experience": exp,
            "location": loc,
            "education": edu,
            "skills": skills
        }

        impacts = evaluate_skill_impact(profile_payload)
        synergy = analyze_bundle_synergy(skills)

        return Response({
            "evaluated_profile": profile_payload,
            "skill_impacts": impacts,
            "bundle_synergy": synergy
        }, status=status.HTTP_200_OK)


class SkillCoOccurrenceView(APIView):
    """
    GET /api/intelligence/skills/co-occurrence/
    Returns empirical pairwise co-occurrence frequencies, lift, and median compensation.
    Query params: 'skill' (optional), 'limit' (default 25).
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skill_name = request.query_params.get('skill', None)
        limit = int(request.query_params.get('limit', 25))

        pairs = get_top_cooccurrences(skill_name=skill_name, limit=limit)
        stats = get_skill_statistics(skill_name=skill_name) if skill_name else None

        return Response({
            "skill_filter": skill_name,
            "statistics": stats,
            "pair_count": len(pairs),
            "co_occurrences": pairs
        }, status=status.HTTP_200_OK)


class SkillCompareView(APIView):
    """
    POST /api/intelligence/skills/compare/
    Controlled What-If counterfactual comparing compensation before vs after
    adding or removing technical skills.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CounterfactualCompareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = compare_counterfactual(
            profile_data={
                "job_role": data["job_role"],
                "years_of_experience": data["years_of_experience"],
                "location": data["location"],
                "education": data["education"],
                "skills": data["skills"]
            },
            add_skills=data.get("add_skills", []),
            remove_skills=data.get("remove_skills", [])
        )

        return Response(result, status=status.HTTP_200_OK)
