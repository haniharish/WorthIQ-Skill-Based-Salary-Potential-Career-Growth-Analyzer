"""
Unit and API Integration Tests for Predictions App.
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Prediction

User = get_user_model()

class SalaryPredictionAPITests(TestCase):
    def setUp(self):
        self.client_a = APIClient()
        self.client_b = APIClient()
        
        self.predict_url = '/api/predictions/salary/'
        self.history_url = '/api/predictions/history/'
        self.model_info_url = '/api/predictions/model-info/'

        # User A
        self.user_a = User.objects.create_user(
            email='alice@worthiq.dev',
            password='Password123!',
            full_name='Alice Engineer'
        )
        self.client_a.force_authenticate(user=self.user_a)

        # User B
        self.user_b = User.objects.create_user(
            email='bob@worthiq.dev',
            password='Password123!',
            full_name='Bob Developer'
        )
        self.client_b.force_authenticate(user=self.user_b)

        self.valid_payload = {
            "job_role": "Backend Developer",
            "years_of_experience": 3.5,
            "location": "Bengaluru",
            "education": "Bachelor's Degree",
            "skills": ["Python", "Django", "PostgreSQL", "Docker", "Git"]
        }

    def test_unauthenticated_request_rejected(self):
        """Unauthenticated requests must be rejected with 401."""
        anon_client = APIClient()
        response = anon_client.post(self.predict_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = anon_client.get(self.history_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_salary_prediction(self):
        """Authenticated prediction returns 201 with full prediction contract."""
        response = self.client_a.post(self.predict_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        
        self.assertIn("prediction_id", data)
        self.assertEqual(data["currency"], "INR")
        self.assertEqual(data["salary_period"], "annual")
        self.assertIn("salary_range", data)
        
        range_data = data["salary_range"]
        self.assertIn("low", range_data)
        self.assertIn("median", range_data)
        self.assertIn("high", range_data)
        
        # Non-negative and monotonic
        self.assertGreaterEqual(range_data["low"], 120_000)
        self.assertLessEqual(range_data["low"], range_data["median"])
        self.assertLessEqual(range_data["median"], range_data["high"])
        
        self.assertIn(data["confidence"], ["High", "Medium", "Low"])
        self.assertEqual(data["model_version"], "2.0.0")
        self.assertIsInstance(data["top_contributing_skills"], list)
        self.assertIsInstance(data["high_value_skills_to_learn"], list)

    def test_prediction_persisted_in_database(self):
        """Successful prediction is stored in Prediction model with user link."""
        self.assertEqual(Prediction.objects.count(), 0)
        response = self.client_a.post(self.predict_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Prediction.objects.count(), 1)
        record = Prediction.objects.first()
        self.assertEqual(record.user, self.user_a)
        self.assertEqual(record.job_role, "Backend Developer")
        self.assertEqual(record.location, "Bengaluru")
        self.assertEqual(record.years_of_experience, Decimal('3.5'))
        self.assertGreaterEqual(record.predicted_median_salary, Decimal('120000.00'))

    def test_invalid_negative_experience(self):
        """Negative years of experience must be rejected with 400."""
        payload = self.valid_payload.copy()
        payload["years_of_experience"] = -2.0
        response = self.client_a.post(self.predict_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("years_of_experience", response.data)

    def test_invalid_excessive_experience(self):
        """Years of experience over 60 must be rejected with 400."""
        payload = self.valid_payload.copy()
        payload["years_of_experience"] = 75.0
        response = self.client_a.post(self.predict_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("years_of_experience", response.data)

    def test_missing_skills_rejected(self):
        """Missing skills payload field must return 400."""
        payload = self.valid_payload.copy()
        del payload["skills"]
        response = self.client_a.post(self.predict_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("skills", response.data)

    def test_empty_skills_list_rejected(self):
        """Empty skills list must return 400."""
        payload = self.valid_payload.copy()
        payload["skills"] = []
        response = self.client_a.post(self.predict_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("skills", response.data)

    def test_missing_job_role_rejected(self):
        """Blank or missing job_role must return 400."""
        payload = self.valid_payload.copy()
        payload["job_role"] = ""
        response = self.client_a.post(self.predict_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("job_role", response.data)

    def test_prediction_history_and_user_isolation(self):
        """User B must NOT see User A's prediction history or single records."""
        # Create prediction for User A
        res_a = self.client_a.post(self.predict_url, self.valid_payload, format='json')
        pred_a_id = res_a.data["prediction_id"]

        # User A checks history
        history_a = self.client_a.get(self.history_url)
        self.assertEqual(history_a.status_code, status.HTTP_200_OK)
        # Results are paginated: check count
        self.assertEqual(history_a.data["count"], 1)

        # User B checks history: must be empty
        history_b = self.client_b.get(self.history_url)
        self.assertEqual(history_b.status_code, status.HTTP_200_OK)
        self.assertEqual(history_b.data["count"], 0)

        # User B tries to view User A's prediction by ID: must return 404
        detail_b = self.client_b.get(f'/api/predictions/history/{pred_a_id}/')
        self.assertEqual(detail_b.status_code, status.HTTP_404_NOT_FOUND)

        # User A retrieves own prediction: returns 200
        detail_a = self.client_a.get(f'/api/predictions/history/{pred_a_id}/')
        self.assertEqual(detail_a.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_a.data["id"], pred_a_id)

    def test_model_info_endpoint(self):
        """Model info endpoint returns safe public metadata."""
        response = self.client_a.get(self.model_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIn("model_name", data)
        self.assertIn("model_version", data)
        self.assertIn("target_variable", data)
        self.assertIn("supported_taxonomies", data)
        self.assertIn("training_rows", data)
