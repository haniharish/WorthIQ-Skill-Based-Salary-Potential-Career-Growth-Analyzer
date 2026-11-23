import io
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
            user_profile=self.profile,
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
        self.assertEqual(sync_result['added_count'], 3)
