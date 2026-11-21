from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile, Skill

User = get_user_model()

class ProfileTests(TestCase):
    def setUp(self):
        self.client_a = APIClient()
        self.client_b = APIClient()
        self.profile_url = '/api/profile/'
        self.skills_url = '/api/profile/skills/'

        # User A
        self.user_a = User.objects.create_user(
            email='alice@worthiq.dev',
            password='password123',
            full_name='Alice Engineer'
        )
        self.client_a.force_authenticate(user=self.user_a)

        # User B
        self.user_b = User.objects.create_user(
            email='bob@worthiq.dev',
            password='password123',
            full_name='Bob Developer'
        )
        self.client_b.force_authenticate(user=self.user_b)

    def test_unauthenticated_profile_access_denied(self):
        """Unauthenticated requests to /api/profile/ must return 401."""
        anon_client = APIClient()
        response = anon_client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_not_found_initially(self):
        """GET /api/profile/ returns 404 before profile is created."""
        response = self.client_a.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_profile_success(self):
        """POST /api/profile/ creates profile and associates normalized skills."""
        payload = {
            'job_role': 'Full Stack Developer',
            'years_of_experience': 3.5,
            'location': 'Bengaluru, India',
            'education': 'B.Tech in Computer Science',
            'current_salary': 12.5,
            'skills_input': ['Python', 'Django', 'React.js', 'PostgreSQL', 'Docker'],
        }
        response = self.client_a.post(self.profile_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['job_role'], 'Full Stack Developer')
        self.assertEqual(len(response.data['skills']), 5)

        # Verify Skill records were created in normalized table
        self.assertTrue(Skill.objects.filter(name='React.js').exists())
        self.assertTrue(Skill.objects.filter(name='PostgreSQL').exists())

    def test_duplicate_profile_creation_fails(self):
        """Creating profile a second time returns 400 Bad Request."""
        payload = {
            'job_role': 'Frontend Developer',
            'years_of_experience': 2,
            'skills_input': ['React.js'],
        }
        self.client_a.post(self.profile_url, payload, format='json')
        second_response = self.client_a.post(self.profile_url, payload, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_put_and_patch(self):
        """Test PUT and PATCH updates on existing profile."""
        payload = {
            'job_role': 'Junior Developer',
            'years_of_experience': 1,
            'skills_input': ['Python'],
        }
        self.client_a.post(self.profile_url, payload, format='json')

        # PATCH update
        patch_resp = self.client_a.patch(
            self.profile_url,
            {'job_role': 'Senior Full Stack Engineer', 'years_of_experience': 5},
            format='json'
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_resp.data['job_role'], 'Senior Full Stack Engineer')
        self.assertEqual(float(patch_resp.data['years_of_experience']), 5.0)

    def test_negative_experience_rejected(self):
        """Experience cannot be negative."""
        payload = {
            'job_role': 'Tester',
            'years_of_experience': -2,
            'skills_input': ['Selenium'],
        }
        response = self.client_a.post(self.profile_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_data_isolation(self):
        """User B cannot see or overwrite User A's profile data."""
        # Alice creates profile
        self.client_a.post(
            self.profile_url,
            {'job_role': 'Alice Role', 'years_of_experience': 4, 'skills_input': ['Django']},
            format='json'
        )

        # Bob gets his own profile, which is initially 404
        bob_get = self.client_b.get(self.profile_url)
        self.assertEqual(bob_get.status_code, status.HTTP_404_NOT_FOUND)

        # Bob creates his own profile
        self.client_b.post(
            self.profile_url,
            {'job_role': 'Bob Role', 'years_of_experience': 2, 'skills_input': ['React.js']},
            format='json'
        )

        # Alice retrieves profile and verifies it was not modified by Bob
        alice_get = self.client_a.get(self.profile_url)
        self.assertEqual(alice_get.data['job_role'], 'Alice Role')
        self.assertEqual(alice_get.data['user']['email'], 'alice@worthiq.dev')

    def test_skills_catalog_endpoint(self):
        """GET /api/profile/skills/ returns available skills."""
        response = self.client_a.get(self.skills_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
