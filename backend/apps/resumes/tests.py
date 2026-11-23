import io
import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.profiles.models import UserProfile, Skill
from apps.resumes.models import ResumeDocument, ResumeExtraction
from apps.resumes.services.extractor import extract_skills_from_text, extract_candidate_metadata
from apps.resumes.services.profile_sync import sync_confirmed_skills_to_profile

User = get_user_model()

class ResumeExtractionAndSyncTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='resume_test@worthiq.com',
            full_name='Resume Candidate',
            password='TestPassword123!'
        )
        self.other_user = User.objects.create_user(
            email='other_resume_user@worthiq.com',
            full_name='Other Candidate',
            password='TestPassword123!'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            job_role='Backend Developer',
            years_of_experience=2.0,
            location='Bengaluru',
            education="Bachelor's Degree",
        )
        # Pre-seed one skill in profile
        skill_python, _ = Skill.objects.get_or_create(name='Python')
        self.profile.skills.add(skill_python)
        self.client.force_authenticate(user=self.user)

    def test_extract_skills_from_raw_text(self):
        sample_text = """
        Harish Sharma
        harish@example.com | +91 9876543210
        Summary: Full Stack Engineer with 3 years of hands-on experience in building microservices.
        Skills: Python, Django, React.js, Docker, Kubernetes, AWS, PostgreSQL, Redis, Git.
        Education: B.Tech in Computer Science and Engineering.
        """
        extracted = extract_skills_from_text(sample_text)
        skill_names = [s['name'] for s in extracted]
        self.assertIn('Python', skill_names)
        self.assertIn('Docker', skill_names)
        self.assertIn('AWS', skill_names)
        self.assertIn('React.js', skill_names)

        metadata = extract_candidate_metadata(sample_text)
        self.assertEqual(metadata['email'], 'harish@example.com')
        self.assertIn('3', str(metadata['years_of_experience']))

    def test_sync_confirmed_skills_to_profile(self):
        confirmed_skills = ['Docker', 'AWS', 'Kubernetes']
        sync_result = sync_confirmed_skills_to_profile(
            user=self.user,
            confirmed_skills=confirmed_skills,
            apply_experience=True,
            experience_val=4.0,
        )
        self.profile.refresh_from_db()
        current_skills = list(self.profile.skills.values_list('name', flat=True))
        self.assertIn('Python', current_skills)
        self.assertIn('Docker', current_skills)
        self.assertIn('AWS', current_skills)
        self.assertEqual(float(self.profile.years_of_experience), 4.0)
        self.assertEqual(len(sync_result['skills_added']), 3)

    def test_upload_real_pdf_resume(self):
        pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testing', 'test-data', 'sample_resume.pdf'))
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                uploaded_file = SimpleUploadedFile('sample_resume.pdf', f.read(), content_type='application/pdf')
                response = self.client.post('/api/resumes/upload/', {'file': uploaded_file}, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIn('document', response.data)
                self.assertIn('extraction', response.data)
                doc_id = response.data['document']['id']

                # Test get result endpoint
                res_resp = self.client.get(f'/api/resumes/{doc_id}/results/')
                self.assertEqual(res_resp.status_code, status.HTTP_200_OK)
                self.assertIn('comparison', res_resp.data)

                # Test user isolation - other user cannot access
                other_client = APIClient()
                other_client.force_authenticate(user=self.other_user)
                iso_resp = other_client.get(f'/api/resumes/{doc_id}/results/')
                self.assertEqual(iso_resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_upload_real_docx_resume(self):
        docx_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'testing', 'test-data', 'sample_resume.docx'))
        if os.path.exists(docx_path):
            with open(docx_path, 'rb') as f:
                uploaded_file = SimpleUploadedFile('sample_resume.docx', f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response = self.client.post('/api/resumes/upload/', {'file': uploaded_file}, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIn('document', response.data)

    def test_upload_invalid_file_extension_rejected(self):
        fake_exe = SimpleUploadedFile('malicious.exe', b'MZExecutableCode...', content_type='application/octet-stream')
        response = self.client.post('/api/resumes/upload/', {'file': fake_exe}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_oversized_file_rejected(self):
        # 6MB dummy file
        big_data = b'0' * (6 * 1024 * 1024)
        big_pdf = SimpleUploadedFile('oversized.pdf', big_data, content_type='application/pdf')
        response = self.client.post('/api/resumes/upload/', {'file': big_pdf}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_to_profile_endpoint(self):
        fake_file = SimpleUploadedFile('test.pdf', b'%PDF-1.4 sample', content_type='application/pdf')
        doc = ResumeDocument.objects.create(
            user=self.user,
            original_filename='test.pdf',
            file=fake_file,
            file_size=1024,
            file_type='pdf',
            processing_status='extracted'
        )
        ResumeExtraction.objects.create(
            resume_document=doc,
            extracted_skills=[{'canonical_name': 'Docker', 'confidence': 0.95}],
            candidate_info={'detected_experience_years': 3.5, 'detected_role': 'DevOps Engineer', 'education': "Master's Degree"},
            raw_text_length=150
        )
        response = self.client.post(f'/api/resumes/{doc.id}/apply-to-profile/', {
            'confirmed_skills': ['Docker'],
            'apply_experience': True,
            'apply_job_role': False,
            'apply_education': False
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
