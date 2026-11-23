"""
Unit and Integration Tests for Job Role Matching Engine.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.intelligence.models import JobRole
from apps.intelligence.services.skill_normalization_service import seed_skills_in_db
from apps.intelligence.services.role_matching_service import seed_roles_in_db

User = get_user_model()


class RoleMatchingAPITests(TestCase):
    def setUp(self):
        seed_skills_in_db()
        seed_roles_in_db()
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='rolematch@worthiq.dev',
            password='Password123!',
            full_name='Role Match Tester'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_roles_endpoint(self):
        """GET /api/intelligence/roles/ returns full catalog with required skills."""
        response = self.client.get('/api/intelligence/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertGreaterEqual(len(data), 9)
        role_titles = [r['title'] for r in data]
        self.assertIn('Backend Developer', role_titles)
        self.assertIn('Full Stack Developer', role_titles)
        self.assertIn('DevOps Engineer', role_titles)

    def test_get_role_detail_endpoint(self):
        """GET /api/intelligence/roles/<id>/ returns detailed role profile and skill breakdown."""
        backend_role = JobRole.objects.filter(title='Backend Developer').first()
        self.assertIsNotNone(backend_role)

        response = self.client.get(f'/api/intelligence/roles/{backend_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(data['title'], 'Backend Developer')
        self.assertIn('skill_requirements', data)
        req_skills = [sr['skill_name'] for sr in data['skill_requirements'] if sr['is_mandatory']]
        self.assertIn('Python', req_skills)

    def test_match_roles_for_candidate(self):
        """POST /api/intelligence/roles/match/ computes ranked match scores and gap analysis."""
        payload = {
            'skills': ['Python', 'PostgreSQL', 'Docker', 'Git', 'REST APIs'],
            'years_of_experience': 3.5
        }
        response = self.client.post('/api/intelligence/roles/match/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('matches', data)
        self.assertIn('total_roles_evaluated', data)
        self.assertGreaterEqual(len(data['matches']), 9)

        top_match = data['matches'][0]
        self.assertIn('match_score', top_match)
        self.assertIn('match_category', top_match)
        self.assertIn('matched_required_skills', top_match)
        self.assertIn('missing_required_skills', top_match)
        self.assertIn('missing_preferred_skills', top_match)
        self.assertIn('factors', top_match)

        # For a candidate with Python, PostgreSQL, Docker, Git, REST APIs, Backend Developer should be near the top
        top_roles = [m['title'] for m in data['matches'][:3]]
        self.assertIn('Backend Developer', top_roles)
        self.assertGreaterEqual(top_match['match_score'], 60.0)

    def test_match_roles_empty_skills(self):
        """Empty skills returns matched results with 0 or low scores without crashing."""
        payload = {
            'skills': [],
            'years_of_experience': 1.0
        }
        response = self.client.post('/api/intelligence/roles/match/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('matches', response.data)
