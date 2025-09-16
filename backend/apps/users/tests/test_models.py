from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


class UserModelTests(TestCase):
    """Test suite for User model functionality."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful."""
        email = 'test@crowdbolt.com'
        password = 'TestPass123!'
        user = User.objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, 'buyer')  # Default role
        self.assertFalse(user.is_verified)
        self.assertFalse(user.identity_verified)

    def test_user_email_normalized(self):
        """Test email is normalized for new users."""
        email = 'test@CROWDBOLT.COM'
        user = User.objects.create_user(email, 'TestPass123!')
        
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error."""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'TestPass123!')
            
    def test_user_email_unique(self):
        """Test that user emails must be unique."""
        email = 'test@crowdbolt.com'
        User.objects.create_user(email, 'TestPass123!')
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email, 'DifferentPass123!')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            'admin@crowdbolt.com',
            'AdminPass123!'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, 'admin')

    def test_user_role_choices(self):
        """Test user role validation."""
        # These should work
        buyer = User.objects.create_user('buyer@test.com', 'StrongPass123!', role='buyer')
        seller = User.objects.create_user('seller@test.com', 'StrongPass123!', role='seller')
        admin = User.objects.create_user('admin@test.com', 'StrongPass123!', role='admin')
        
        self.assertEqual(buyer.role, 'buyer')
        self.assertEqual(seller.role, 'seller')
        self.assertEqual(admin.role, 'admin')

    def test_user_string_representation(self):
        """Test the user string representation."""
        user = User.objects.create_user(
            email='test@crowdbolt.com',
            password='TestPass123!'
        )
        
        self.assertEqual(str(user), 'test@crowdbolt.com')