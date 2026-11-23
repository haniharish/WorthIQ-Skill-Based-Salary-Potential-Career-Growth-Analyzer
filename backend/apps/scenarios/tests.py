import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.scenarios.models import SalaryScenario

User = get_user_model()

class ScenarioAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='scenario_test@worthiq.com',
            full_name='Scenario Tester',
            password='TestPassword123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_and_list_scenario(self):
        payload = {
            'name': 'Cloud Architect Transition',
            'job_role': 'Cloud Architect',
            'years_of_experience': 5.0,
            'location': 'Bengaluru',
            'education': "Bachelor's Degree",
            'skills': ['AWS', 'Docker', 'Kubernetes', 'Python', 'Terraform'],
            'notes': 'Targeting senior cloud infrastructure engineering role',
        }
        res = self.client.post('/api/scenarios/', data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'Cloud Architect Transition')
        self.assertIn('prediction_snapshot', res.data)
        self.assertIn('p50_lpa', res.data['prediction_snapshot'])

        # List scenarios
        res_list = self.client.get('/api/scenarios/')
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

    def test_duplicate_scenario(self):
        scenario = SalaryScenario.objects.create(
            user=self.user,
            name='DevOps Base',
            job_role='DevOps Engineer',
            years_of_experience=3.0,
            location='Hyderabad',
            education="Bachelor's Degree",
            skills=['Docker', 'Linux', 'Git'],
        )
        res = self.client.post(f'/api/scenarios/{scenario.id}/duplicate/')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('(Copy)', res.data['name'])
        self.assertEqual(SalaryScenario.objects.filter(user=self.user).count(), 2)

    def test_compare_scenarios(self):
        payload = {
            'baseline': {
                'job_role': 'Full Stack Developer',
                'years_of_experience': 2.0,
                'location': 'Delhi NCR',
                'education': "Bachelor's Degree",
                'skills': ['Python', 'React.js', 'PostgreSQL'],
            },
            'scenarios': [
                {
                    'name': 'Upskill Docker & AWS',
                    'job_role': 'Full Stack Developer',
                    'years_of_experience': 3.0,
                    'location': 'Bengaluru',
                    'education': "Bachelor's Degree",
                    'skills': ['Python', 'React.js', 'PostgreSQL', 'Docker', 'AWS'],
                }
            ]
        }
        res = self.client.post('/api/scenarios/compare/', data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('baseline', res.data)
        self.assertIn('scenarios', res.data)
        self.assertIn('disclaimer', res.data)
        self.assertEqual(len(res.data['scenarios']), 2)
        self.assertIn('delta_vs_baseline', res.data['scenarios'][1])
