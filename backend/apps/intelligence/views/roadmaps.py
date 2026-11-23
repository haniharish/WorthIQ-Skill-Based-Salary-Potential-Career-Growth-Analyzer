"""
Career Roadmap Views
Endpoints for generating, retrieving, tracking progress, and managing personal roadmaps.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.intelligence.models import (
    CareerRoadmap,
    RoadmapStage,
    RoadmapSkillProgress
)
from apps.intelligence.serializers import (
    CareerRoadmapListSerializer,
    CareerRoadmapDetailSerializer,
    GenerateRoadmapInputSerializer,
    UpdateProgressSerializer
)
from apps.intelligence.services.roadmap_service import generate_roadmap_for_user

class RoadmapListCreateView(APIView):
    """
    GET /api/intelligence/roadmaps/
    Lists saved career growth roadmaps for the authenticated user.

    POST /api/intelligence/roadmaps/generate/
    Generates and saves a new personalized career growth roadmap.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        roadmaps = CareerRoadmap.objects.filter(user=request.user).select_related('target_role')
        serializer = CareerRoadmapListSerializer(roadmaps, many=True)
        return Response({
            "count": roadmaps.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GenerateRoadmapInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        roadmap = generate_roadmap_for_user(
            user=request.user,
            target_role_id=data["target_role_id"],
            current_role=data.get("current_role"),
            current_experience=data.get("current_experience"),
            current_skills=data.get("current_skills")
        )

        detail_serializer = CareerRoadmapDetailSerializer(roadmap)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class RoadmapDetailView(APIView):
    """
    GET /api/intelligence/roadmaps/{id}/
    Retrieves complete roadmap with stages, milestones, and project recommendations.

    DELETE /api/intelligence/roadmaps/{id}/
    Deletes the saved roadmap.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        roadmap = get_object_or_404(
            CareerRoadmap.objects.prefetch_related(
                'stages__skills_progress',
                'target_role'
            ),
            pk=pk,
            user=request.user
        )
        serializer = CareerRoadmapDetailSerializer(roadmap)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        roadmap = get_object_or_404(CareerRoadmap, pk=pk, user=request.user)
        roadmap.delete()
        return Response(
            {"detail": "Career roadmap deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class RoadmapProgressUpdateView(APIView):
    """
    PATCH /api/intelligence/roadmaps/{id}/progress/
    Updates completion status of a specific skill or entire stage, and recalculates
    overall roadmap progress percentage.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        roadmap = get_object_or_404(CareerRoadmap, pk=pk, user=request.user)
        serializer = UpdateProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        is_completed = data["is_completed"]
        skill_id = data.get("skill_progress_id")
        stage_id = data.get("stage_id")

        if skill_id:
            skill_progress = get_object_or_404(
                RoadmapSkillProgress,
                pk=skill_id,
                stage__roadmap=roadmap
            )
            skill_progress.is_completed = is_completed
            skill_progress.completed_at = timezone.now() if is_completed else None
            skill_progress.save()

            # Check if all skills in that stage are now completed
            stage = skill_progress.stage
            all_stage_skills = stage.skills_progress.all()
            if all_stage_skills.exists() and all(s.is_completed for s in all_stage_skills):
                stage.is_completed = True
                stage.completed_at = timezone.now()
            else:
                stage.is_completed = False
                stage.completed_at = None
            stage.save()

        elif stage_id:
            stage = get_object_or_404(RoadmapStage, pk=stage_id, roadmap=roadmap)
            stage.is_completed = is_completed
            stage.completed_at = timezone.now() if is_completed else None
            stage.save()
            # Also update all skills in this stage
            stage.skills_progress.update(
                is_completed=is_completed,
                completed_at=timezone.now() if is_completed else None
            )

        # Recalculate roadmap overall progress
        new_progress = roadmap.update_progress()

        detail_serializer = CareerRoadmapDetailSerializer(roadmap)
        return Response({
            "detail": "Roadmap progress updated successfully.",
            "overall_progress_pct": new_progress,
            "roadmap": detail_serializer.data
        }, status=status.HTTP_200_OK)
