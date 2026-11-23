"""
Views for Salary Scenarios and What-If Simulations.
"""

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SalaryScenario
from .serializers import (
    SalaryScenarioSerializer,
    ScenarioCreateUpdateSerializer,
    ScenarioCompareInputSerializer
)
from .services import (
    evaluate_scenario_profile,
    build_scenario_snapshot,
    compare_multiple_scenarios,
    DISCLAIMER_TEXT
)

class ScenarioListCreateView(APIView):
    """
    GET /api/scenarios/ - List all scenarios belonging to the authenticated user.
    POST /api/scenarios/ - Create a new scenario and compute its salary prediction snapshot.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        scenarios = SalaryScenario.objects.filter(user=request.user)
        serializer = SalaryScenarioSerializer(scenarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        input_serializer = ScenarioCreateUpdateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        # Run Phase 2 prediction
        pred = evaluate_scenario_profile(
            job_role=data["job_role"],
            years_of_experience=float(data["years_of_experience"]),
            location=data["location"],
            skills=data["skills"],
            education=data.get("education", "Bachelor's Degree")
        )
        snapshot = build_scenario_snapshot(pred)

        scenario = SalaryScenario.objects.create(
            user=request.user,
            name=data["name"],
            job_role=data["job_role"],
            years_of_experience=data["years_of_experience"],
            location=data["location"],
            education=data.get("education", "Bachelor's Degree"),
            skills=data["skills"],
            prediction_snapshot=snapshot,
            notes=data.get("notes", "")
        )

        return Response(
            SalaryScenarioSerializer(scenario).data,
            status=status.HTTP_201_CREATED
        )


class ScenarioDetailView(APIView):
    """
    GET /api/scenarios/{id}/ - Retrieve a single scenario.
    PATCH /api/scenarios/{id}/ - Update scenario attributes and re-evaluate prediction.
    DELETE /api/scenarios/{id}/ - Delete a scenario.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(SalaryScenario, pk=pk, user=user)

    def get(self, request, pk):
        scenario = self.get_object(pk, request.user)
        return Response(SalaryScenarioSerializer(scenario).data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        scenario = self.get_object(pk, request.user)
        input_serializer = ScenarioCreateUpdateSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        for field in ['name', 'job_role', 'years_of_experience', 'location', 'education', 'skills', 'notes']:
            if field in data:
                setattr(scenario, field, data[field])

        # Re-evaluate snapshot if profile inputs changed
        pred = evaluate_scenario_profile(
            job_role=scenario.job_role,
            years_of_experience=float(scenario.years_of_experience),
            location=scenario.location,
            skills=scenario.skills,
            education=scenario.education
        )
        scenario.prediction_snapshot = build_scenario_snapshot(pred)
        scenario.save()

        return Response(SalaryScenarioSerializer(scenario).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        scenario = self.get_object(pk, request.user)
        scenario.delete()
        return Response({"message": "Scenario deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ScenarioDuplicateView(APIView):
    """
    POST /api/scenarios/{id}/duplicate/
    Duplicates an existing scenario under a new name with cloned prediction snapshot.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        original = get_object_or_404(SalaryScenario, pk=pk, user=request.user)
        new_name = request.data.get("name") or f"{original.name} (Copy)"

        clone = SalaryScenario.objects.create(
            user=request.user,
            name=new_name,
            job_role=original.job_role,
            years_of_experience=original.years_of_experience,
            location=original.location,
            education=original.education,
            skills=list(original.skills),
            prediction_snapshot=original.prediction_snapshot,
            notes=original.notes
        )

        return Response(SalaryScenarioSerializer(clone).data, status=status.HTTP_201_CREATED)


class ScenarioPredictView(APIView):
    """
    POST /api/scenarios/{id}/predict/
    Forces re-evaluation of scenario prediction against current ML model version.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        scenario = get_object_or_404(SalaryScenario, pk=pk, user=request.user)
        pred = evaluate_scenario_profile(
            job_role=scenario.job_role,
            years_of_experience=float(scenario.years_of_experience),
            location=scenario.location,
            skills=scenario.skills,
            education=scenario.education
        )
        scenario.prediction_snapshot = build_scenario_snapshot(pred)
        scenario.save(update_fields=['prediction_snapshot', 'updated_at'])

        return Response(SalaryScenarioSerializer(scenario).data, status=status.HTTP_200_OK)


class ScenarioCompareView(APIView):
    """
    POST /api/scenarios/compare/
    Multi-scenario comparative evaluation engine.
    Compares baseline profile + up to 3 scenarios with delta metrics and visualization points.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ScenarioCompareInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        comparison = compare_multiple_scenarios(
            user=request.user,
            scenario_ids=data.get("scenario_ids", []),
            new_scenarios=data.get("new_scenarios", []),
            include_baseline=data.get("include_baseline", True),
            custom_baseline=data.get("baseline"),
        )

        return Response(comparison, status=status.HTTP_200_OK)
