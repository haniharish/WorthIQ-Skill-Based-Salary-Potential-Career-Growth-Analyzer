"""
Unit and Integration Tests for Career Growth Roadmap Engine.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.intelligence.models import JobRole, CareerRoadmap, RoadmapSkillProgress
from apps.intelligence.services.skill_normalization_service import seed_skills_in_db
from apps.intelligence.services.role_matching_service import seed_roles_in_db

User = get_user_model()


class CareerRoadmapAPITests(TestCase):
    def setUp(self):
        seed_skills_in_db()
        seed_roles_in_db()
        self.client_a = APIClient()
        self.client_b = APIClient()

        # User A
        self.user_a = User.objects.create_user(
            email='alice.roadmap@worthiq.dev',
            password='Password123!',
            full_name='Alice Roadmap'
        )
        self.client_a.force_authenticate(user=self.user_a)

        # User B
        self.user_b = User.objects.create_user(
            email='bob.roadmap@worthiq.dev',
            password='Password123!',
            full_name='Bob Roadmap'
        )
        self.client_b.force_authenticate(user=self.user_b)

        self.target_role = JobRole.objects.filter(title='DevOps Engineer').first()
        self.assertIsNotNone(self.target_role)

    def test_unauthenticated_request_rejected(self):
        """Unauthenticated requests are rejected with 401."""
        anon = APIClient()
        response = anon.get('/api/intelligence/roadmaps/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_generate_and_retrieve_roadmap(self):
        """Generates DAG stages, project briefs, and persists the roadmap."""
        payload = {
            'target_role_id': self.target_role.id,
            'current_skills': ['Git', 'Linux'],
            'current_experience': 2.0
        }
        response = self.client_a.post('/api/intelligence/roadmaps/generate/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data

        self.assertIn('id', data)
        self.assertEqual(data['target_role_title'], 'DevOps Engineer')
        self.assertIn('stages', data)
        self.assertGreater(len(data['stages']), 0)
        self.assertIn('project_suggestion', data['stages'][0])

        roadmap_id = data['id']

        # Verify list roadmaps
        list_resp = self.client_a.get('/api/intelligence/roadmaps/')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(list_resp.data['count'], 1)

        # Verify get roadmap detail
        detail_resp = self.client_a.get(f'/api/intelligence/roadmaps/{roadmap_id}/')
        self.assertEqual(detail_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_resp.data['id'], roadmap_id)

    def test_toggle_skill_progress(self):
        """Toggling skill completion updates progress percentage accurately."""
        payload = {
            'target_role_id': self.target_role.id,
            'current_skills': ['Git'],
            'current_experience': 1.0
        }
        gen_resp = self.client_a.post('/api/intelligence/roadmaps/generate/', payload, format='json')
        self.assertEqual(gen_resp.status_code, status.HTTP_201_CREATED)
        roadmap_id = gen_resp.data['id']

        # Find a skill progress record
        progress_records = RoadmapSkillProgress.objects.filter(stage__roadmap_id=roadmap_id)
        self.assertGreater(progress_records.count(), 0)
        first_progress = progress_records.first()

        # Toggle skill to completed using PATCH
        toggle_payload = {
            'skill_progress_id': first_progress.id,
            'is_completed': True
        }
        prog_resp = self.client_a.patch(
            f'/api/intelligence/roadmaps/{roadmap_id}/progress/',
            toggle_payload,
            format='json'
        )
        self.assertEqual(prog_resp.status_code, status.HTTP_200_OK)
        self.assertGreater(prog_resp.data['overall_progress_pct'], 0)

        first_progress.refresh_from_db()
        self.assertTrue(first_progress.is_completed)

    def test_user_isolation_on_roadmaps(self):
        """User B cannot access or modify User A's roadmap."""
        payload = {
            'target_role_id': self.target_role.id,
            'current_skills': ['Git'],
            'current_experience': 1.0
        }
        gen_resp = self.client_a.post('/api/intelligence/roadmaps/generate/', payload, format='json')
        self.assertEqual(gen_resp.status_code, status.HTTP_201_CREATED)
        roadmap_id = gen_resp.data['id']

        # User B trying to view
        view_resp = self.client_b.get(f'/api/intelligence/roadmaps/{roadmap_id}/')
        self.assertEqual(view_resp.status_code, status.HTTP_404_NOT_FOUND)

        # User B trying to update progress
        update_resp = self.client_b.patch(
            f'/api/intelligence/roadmaps/{roadmap_id}/progress/',
            {'skill_progress_id': 999999, 'is_completed': True},
            format='json'
        )
        self.assertEqual(update_resp.status_code, status.HTTP_404_NOT_FOUND)

        # User B trying to delete
        del_resp = self.client_b.delete(f'/api/intelligence/roadmaps/{roadmap_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_roadmap(self):
        """Owner can successfully delete a roadmap."""
        payload = {
            'target_role_id': self.target_role.id,
            'current_skills': ['Git'],
            'current_experience': 1.0
        }
        gen_resp = self.client_a.post('/api/intelligence/roadmaps/generate/', payload, format='json')
        roadmap_id = gen_resp.data['id']

        del_resp = self.client_a.delete(f'/api/intelligence/roadmaps/{roadmap_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CareerRoadmap.objects.filter(id=roadmap_id).exists())
