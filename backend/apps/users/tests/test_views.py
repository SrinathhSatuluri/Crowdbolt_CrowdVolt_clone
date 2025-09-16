from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationTests(APITestCase):
    """Test suite for user registration API."""

    def setUp(self):
        self.register_url = reverse('users:register')
        self.valid_payload = {
            'email': 'test@crowdbolt.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'role': 'buyer'
        }

    def test_user_registration_successful(self):
        """Test successful user registration."""
        response = self.client.post(self.register_url, self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Check user was created
        user = User.objects.get(email=self.valid_payload['email'])
        self.assertEqual(user.email, self.valid_payload['email'])
        self.assertEqual(user.role, self.valid_payload['role'])

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email fails."""
        # Create user first
        User.objects.create_user(
            email=self.valid_payload['email'],
            password='SomePass123!'
        )
        
        response = self.client.post(self.register_url, self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_invalid_email(self):
        """Test registration with invalid email fails."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'invalid-email'
        
        response = self.client.post(self.register_url, invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch fails."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password_confirm'] = 'DifferentPass123!'
        
        response = self.client.post(self.register_url, invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_weak_password(self):
        """Test registration with weak password fails."""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['password'] = '123'
        invalid_payload['password_confirm'] = '123'
        
        response = self.client.post(self.register_url, invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(APITestCase):
    """Test suite for user login API."""

    def setUp(self):
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            email='test@crowdbolt.com',
            password='TestPass123!'
        )

    def test_user_login_successful(self):
        """Test successful user login."""
        payload = {
            'email': 'test@crowdbolt.com',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials fails."""
        payload = {
            'email': 'test@crowdbolt.com',
            'password': 'WrongPassword123!'
        }
        
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_nonexistent_email(self):
        """Test login with non-existent email fails."""
        payload = {
            'email': 'nonexistent@crowdbolt.com',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTests(APITestCase):
    """Test suite for user profile API."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@crowdbolt.com',
            password='TestPass123!'
        )
        self.profile_url = reverse('users:profile')
        
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_user_profile_authenticated(self):
        """Test getting user profile when authenticated."""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['role'], self.user.role)

    def test_get_user_profile_unauthenticated(self):
        """Test getting user profile when unauthenticated fails."""
        self.client.credentials()  # Remove authentication
        
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)