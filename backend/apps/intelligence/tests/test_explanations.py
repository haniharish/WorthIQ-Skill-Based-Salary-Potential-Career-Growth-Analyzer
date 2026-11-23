"""
Unit and Integration Tests for SHAP Explainability Engine.
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.predictions.models import Prediction
from apps.intelligence.models import PredictionExplanation
from apps.intelligence.services.skill_normalization_service import seed_skills_in_db

User = get_user_model()


class SHAPExplainabilityAPITests(TestCase):
    def setUp(self):
        seed_skills_in_db()
        self.client_a = APIClient()
        self.client_b = APIClient()

        # User A
        self.user_a = User.objects.create_user(
            email='alice.shap@worthiq.dev',
            password='Password123!',
            full_name='Alice Engineer'
        )
        self.client_a.force_authenticate(user=self.user_a)

        # User B
        self.user_b = User.objects.create_user(
            email='bob.shap@worthiq.dev',
            password='Password123!',
            full_name='Bob Developer'
        )
        self.client_b.force_authenticate(user=self.user_b)

        # Create Prediction for User A
        self.prediction_a = Prediction.objects.create(
            user=self.user_a,
            job_role='Backend Developer',
            years_of_experience=Decimal('4.0'),
            location='Bengaluru',
            education="Bachelor's Degree",
            skills=['Python', 'Django', 'PostgreSQL', 'Docker', 'Git', 'REST APIs'],
            predicted_low_salary=Decimal('450000.00'),
            predicted_median_salary=Decimal('850000.00'),
            predicted_high_salary=Decimal('1800000.00'),
            confidence='High',
            model_version='2.0.0'
        )

        # Create Prediction for User B
        self.prediction_b = Prediction.objects.create(
            user=self.user_b,
            job_role='Frontend Developer',
            years_of_experience=Decimal('2.0'),
            location='Hyderabad',
            education="Bachelor's Degree",
            skills=['JavaScript', 'React.js', 'HTML5', 'CSS3', 'Git'],
            predicted_low_salary=Decimal('300000.00'),
            predicted_median_salary=Decimal('550000.00'),
            predicted_high_salary=Decimal('1100000.00'),
            confidence='Medium',
            model_version='2.0.0'
        )

    def test_unauthenticated_request_rejected(self):
        """Unauthenticated requests to explanation endpoint must be rejected with 401."""
        anon_client = APIClient()
        url = f'/api/intelligence/explanations/{self.prediction_a.id}/'
        response = anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_generate_and_fetch_shap_explanation(self):
        """Authenticated owner can successfully generate and retrieve a SHAP explanation."""
        url = f'/api/intelligence/explanations/{self.prediction_a.id}/'
        response = self.client_a.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertIn('id', data)
        self.assertEqual(data['prediction_id'], self.prediction_a.id)
        self.assertEqual(data['job_role'], 'Backend Developer')
        self.assertGreater(float(data['base_value_inr']), 0)
        self.assertGreater(float(data['predicted_value_inr']), 0)
        self.assertIsInstance(data['feature_attributions'], list)
        self.assertGreater(len(data['feature_attributions']), 0)
        self.assertIsInstance(data['positive_contributors'], list)
        self.assertIsInstance(data['negative_contributors'], list)
        self.assertIn('predicted compensation', data['summary_narrative'])

        # Verify DB persistence
        self.assertTrue(PredictionExplanation.objects.filter(prediction=self.prediction_a).exists())

    def test_cached_explanation_returned_on_subsequent_calls(self):
        """Subsequent requests return the persisted explanation record without error."""
        url = f'/api/intelligence/explanations/{self.prediction_a.id}/'
        res1 = self.client_a.get(url)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        exp_id_1 = res1.data['id']

        res2 = self.client_a.get(url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        exp_id_2 = res2.data['id']

        self.assertEqual(exp_id_1, exp_id_2)
        self.assertEqual(PredictionExplanation.objects.filter(prediction=self.prediction_a).count(), 1)

    def test_user_ownership_isolation(self):
        """User B cannot view User A's prediction explanation (returns 404 or 403)."""
        url = f'/api/intelligence/explanations/{self.prediction_a.id}/'
        response = self.client_b.get(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_nonexistent_prediction_returns_404(self):
        """Request for nonexistent prediction ID returns 404."""
        url = '/api/intelligence/explanations/999999/'
        response = self.client_a.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
