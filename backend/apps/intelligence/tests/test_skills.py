"""
Unit and Integration Tests for Skill Intelligence Services and Endpoints.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.intelligence.services.skill_normalization_service import (
    seed_skills_in_db,
    normalize_skill,
    normalize_skill_list
)

User = get_user_model()


class SkillIntelligenceAPITests(TestCase):
    def setUp(self):
        seed_skills_in_db()
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='skilltester@worthiq.dev',
            password='Password123!',
            full_name='Skill Tester'
        )
        self.client.force_authenticate(user=self.user)

    def test_skill_normalization_service(self):
        """Test normalize_skill and normalize_skill_list logic."""
        self.assertEqual(normalize_skill('py'), 'Python')
        self.assertEqual(normalize_skill('reactjs'), 'React.js')
        self.assertEqual(normalize_skill('k8s'), 'Kubernetes')
        self.assertEqual(normalize_skill('postgres'), 'PostgreSQL')

        raw_list = ['python', 'py', 'react', 'react.js', 'docker', 'k8s']
        clean = normalize_skill_list(raw_list)
        # Deduplication preserving canonical order
        self.assertIn('Python', clean)
        self.assertIn('React.js', clean)
        self.assertIn('Docker', clean)
        self.assertIn('Kubernetes', clean)
        self.assertEqual(len(clean), 4)

    def test_get_taxonomy_endpoint(self):
        """GET /api/intelligence/skills/ returns structured canonical catalog."""
        response = self.client.get('/api/intelligence/skills/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('skills', data)
        self.assertIn('categories', data)
        self.assertIn('total_count', data)
        self.assertGreaterEqual(data['total_count'], 30)

        # Check Python exists
        skills = data['skills']
        python_skill = next((s for s in skills if s['name'] == 'Python'), None)
        self.assertIsNotNone(python_skill)
        self.assertEqual(python_skill['category'], 'Programming Languages')

    def test_cooccurrence_endpoint(self):
        """GET /api/intelligence/skills/co-occurrence/ returns complementary skills."""
        response = self.client.get('/api/intelligence/skills/co-occurrence/?skill=Python&limit=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('co_occurrences', data)
        self.assertIsInstance(data['co_occurrences'], list)
        self.assertIn('pair_count', data)
        self.assertEqual(data['skill_filter'], 'Python')

    def test_portfolio_impact_endpoint(self):
        """GET /api/intelligence/skills/impact/ computes marginal skill valuations."""
        url = (
            '/api/intelligence/skills/impact/'
            '?job_role=Backend+Developer'
            '&years_of_experience=4.0'
            '&location=Bengaluru'
            "&education=Bachelor's+Degree"
            '&skills=Python,PostgreSQL,Docker,Git'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('evaluated_profile', data)
        self.assertIn('skill_impacts', data)
        self.assertIn('bundle_synergy', data)
        self.assertEqual(len(data['skill_impacts']), 4)

    def test_what_if_counterfactual_endpoint(self):
        """POST /api/intelligence/skills/compare/ compares base vs modified scenario."""
        payload = {
            'job_role': 'Full Stack Developer',
            'years_of_experience': 3.0,
            'location': 'Bengaluru',
            'education': "Bachelor's Degree",
            'skills': ['JavaScript', 'React.js', 'SQL', 'Git'],
            'add_skills': ['Docker', 'AWS', 'TypeScript'],
            'remove_skills': []
        }
        response = self.client.post('/api/intelligence/skills/compare/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('original_salary_annual', data)
        self.assertIn('counterfactual_salary_annual', data)
        self.assertIn('delta_annual', data)
        self.assertIn('percentage_change', data)
