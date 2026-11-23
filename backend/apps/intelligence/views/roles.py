"""
Job Role Matching Views
Endpoints for role catalog exploration, multi-metric AI matching, and recommendations.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from apps.intelligence.models import JobRole
from apps.intelligence.serializers import JobRoleSerializer, RoleMatchInputSerializer
from apps.intelligence.services.role_matching_service import (
    match_candidate_roles,
    DEFAULT_ROLES_DATA
)

class JobRoleListView(APIView):
    """
    GET /api/intelligence/roles/
    Returns the technology job role catalog with compensation benchmarks.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roles = JobRole.objects.prefetch_related('skill_requirements__skill').all()
        if roles.exists():
            serializer = JobRoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(DEFAULT_ROLES_DATA, status=status.HTTP_200_OK)


class JobRoleDetailView(APIView):
    """
    GET /api/intelligence/roles/{id}/
    Returns detailed specifications, required skills, and salary bands for a role.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        role = get_object_or_404(
            JobRole.objects.prefetch_related('skill_requirements__skill'),
            pk=pk
        )
        serializer = JobRoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleMatchView(APIView):
    """
    POST /api/intelligence/roles/match/
    Evaluates role compatibility against submitted skills and experience.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RoleMatchInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        skills = data.get("skills", [])
        exp = data.get("experience", 0.0)

        # If user is authenticated and didn't provide skills, prefill from profile
        if not skills and request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                skills = [s.name for s in profile.skills.all()]
                if exp == 0.0:
                    exp = float(profile.years_of_experience)

        matches = match_candidate_roles(candidate_skills=skills, experience=exp)

        return Response({
            "evaluated_skills": skills,
            "evaluated_experience": exp,
            "total_roles_evaluated": len(matches),
            "matches": matches
        }, status=status.HTTP_200_OK)


class RoleRecommendationsView(APIView):
    """
    GET /api/intelligence/roles/recommendations/
    Generates personalized role recommendations using the authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return Response(
                {"detail": "User profile not found. Please complete profile setup first."},
                status=status.HTTP_404_NOT_FOUND
            )

        skills = [s.name for s in profile.skills.all()]
        exp = float(profile.years_of_experience)

        matches = match_candidate_roles(candidate_skills=skills, experience=exp)

        return Response({
            "user_job_role": profile.job_role,
            "user_experience": exp,
            "user_skills": skills,
            "top_match": matches[0] if matches else None,
            "recommendations": matches
        }, status=status.HTTP_200_OK)
