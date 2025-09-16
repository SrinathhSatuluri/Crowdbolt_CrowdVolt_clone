from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')

        # Normalize email (lowercase domain)
        email = self.normalize_email(email)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Invalid email format')

        # Validate password strength
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise ValueError(f'Password validation failed: {"; ".join(e.messages)}')

        # Create user instance (username will be auto-generated from email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Log user creation for audit trail
        logger.info(f'User created: {email} with role: {user.role}')

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'buyer')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model for CrowdBolt marketplace."""

    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    # Use email as the unique identifier
    email = models.EmailField(
        unique=True,
        help_text='Required. Enter a valid email address.'
    )

    # Make username optional (override AbstractUser)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text='Optional. Auto-generated from email if not provided.'
    )

    # Role field for marketplace permissions
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='buyer',
        help_text='User role in the marketplace'
    )

    # Additional fields for marketplace functionality
    is_verified = models.BooleanField(
        default=False,
        help_text='Designates whether this user has verified their email address.'
    )

    identity_verified = models.BooleanField(
        default=False,
        help_text='Designates whether this user has completed identity verification.'
    )

    failed_login_attempts = models.IntegerField(
        default=0,
        help_text='Number of consecutive failed login attempts'
    )

    last_failed_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp of last failed login attempt'
    )

    # Timestamps for audit and ordering
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        help_text='Timestamp when user was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when user was last updated'
    )

    # Use email for authentication instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required by USERNAME_FIELD

    # Use our custom manager
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'  # Keep same table name for compatibility
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='users_email_idx'),
            models.Index(fields=['role'], name='users_role_idx'),
            models.Index(fields=['is_verified'], name='users_verified_idx'),
            models.Index(fields=['created_at'], name='users_created_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(role__in=['buyer', 'seller', 'admin']),
                name='valid_role_check'
            ),
        ]

    def save(self, *args, **kwargs):
        """Override save to auto-generate username from email if not provided."""
        if not self.username and self.email:
            # Generate unique username from email
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1

            # Ensure username is unique
            while User.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1

            self.username = username

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.email.split('@')[0]

    def is_buyer(self):
        """Check if user has buyer role."""
        return self.role == 'buyer'

    def is_seller(self):
        """Check if user has seller role."""
        return self.role == 'seller'

    def is_marketplace_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])

    def increment_failed_login_attempts(self):
        """Increment failed login attempts and update timestamp."""
        from django.utils import timezone
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])

    def is_account_locked(self):
        """Check if account is locked due to too many failed attempts."""
        from django.utils import timezone
        from datetime import timedelta

        if self.failed_login_attempts >= 5:
            # Account locked for 15 minutes after 5 failed attempts
            if self.last_failed_login:
                lockout_duration = timedelta(minutes=15)
                return timezone.now() - self.last_failed_login < lockout_duration
        return False

    def can_login(self):
        """Check if user can login (not locked and verified if required)."""
        return not self.is_account_locked() and self.is_active
