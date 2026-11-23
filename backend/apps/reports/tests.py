from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.reports.models import AdvancedReport

User = get_user_model()

class AdvancedReportsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='reports_tester@worthiq.com',
            full_name='Reports Tester',
            password='TestPassword123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_and_download_pdf_report(self):
        payload = {
            'title': 'Senior Engineer Compensation Evaluation',
            'report_type': 'salary_prediction',
            'summary': 'Benchmark evaluation across top Indian tech hubs.',
            'data_snapshot': {
                'role': 'Full Stack Developer',
                'experience': 3.5,
                'location': 'Bengaluru',
                'predicted_salary_lpa': 14.5,
                'p10_lpa': 9.2,
                'p50_lpa': 14.5,
                'p90_lpa': 22.0,
                'skills': ['Python', 'React.js', 'PostgreSQL', 'Docker', 'AWS'],
            }
        }
        create_res = self.client.post('/api/reports/generate/', data=payload, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        report_id = create_res.data['id']

        # Download PDF
        download_res = self.client.get(f'/api/reports/{report_id}/download/')
        self.assertEqual(download_res.status_code, status.HTTP_200_OK)
        self.assertEqual(download_res['Content-Type'], 'application/pdf')
        self.assertTrue(len(download_res.content) > 500)

    def test_export_csv(self):
        # Export scenarios CSV
        csv_res = self.client.get('/api/reports/export/csv/?type=scenarios')
        self.assertEqual(csv_res.status_code, status.HTTP_200_OK)
        self.assertEqual(csv_res['Content-Type'], 'text/csv; charset=utf-8')
