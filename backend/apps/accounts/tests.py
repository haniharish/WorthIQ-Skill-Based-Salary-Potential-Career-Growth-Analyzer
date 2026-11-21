from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.refresh_url = '/api/auth/token/refresh/'
        self.logout_url = '/api/auth/logout/'
        self.me_url = '/api/auth/me/'

        self.user_data = {
            'full_name': 'Test User',
            'email': 'testuser@worthiq.dev',
            'password': 'password123',
            'confirm_password': 'password123',
        }

    def test_user_registration_success(self):
        """Test registering a new user returns 201 and JWT tokens."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], 'testuser@worthiq.dev')
        self.assertNotIn('password', response.data['user'])

    def test_user_registration_duplicate_email(self):
        """Test registration fails when email is already taken."""
        self.client.post(self.register_url, self.user_data, format='json')
        duplicate_response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', duplicate_response.data)

    def test_user_registration_password_mismatch(self):
        """Test registration fails if passwords do not match."""
        invalid_data = self.user_data.copy()
        invalid_data['confirm_password'] = 'mismatch123'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test logging in with valid credentials."""
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(
            self.login_url,
            {'email': 'testuser@worthiq.dev', 'password': 'password123'},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', login_response.data)

    def test_user_login_invalid_password(self):
        """Test login fails with incorrect password."""
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(
            self.login_url,
            {'email': 'testuser@worthiq.dev', 'password': 'wrongpassword'},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_current_user_me_endpoint(self):
        """Test /api/auth/me/ returns authenticated user details and rejects unauthenticated requests."""
        # Unauthenticated request should fail with 401
        unauth_response = self.client.get(self.me_url)
        self.assertEqual(unauth_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request succeeds
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        access_token = reg_resp.data['tokens']['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        auth_response = self.client.get(self.me_url)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertEqual(auth_response.data['email'], 'testuser@worthiq.dev')

    def test_jwt_token_refresh(self):
        """Test refreshing access token using valid refresh token."""
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        refresh_token = reg_resp.data['tokens']['refresh']

        response = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_logout_blacklists_token(self):
        """Test logging out blacklists the refresh token."""
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        access_token = reg_resp.data['tokens']['access']
        refresh_token = reg_resp.data['tokens']['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_resp = self.client.post(self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)

        # Attempting to use the blacklisted refresh token should now fail
        refresh_again = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_again.status_code, status.HTTP_401_UNAUTHORIZED)
