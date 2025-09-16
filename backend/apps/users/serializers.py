
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'role', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'role': {'required': False},
        }

    def validate(self, attrs):
        """Validate password confirmation and strength."""
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords don't match.")

        # Validate password strength using Django's validators
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        return attrs

    def create(self, validated_data):
        """Create user with validated data."""
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm', None)

        # Create user
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Authenticate user with email and password."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user exists and can login
            try:
                user = User.objects.get(email=email)
                if not user.can_login():
                    raise serializers.ValidationError(
                        'Account is temporarily locked due to too many failed login attempts.'
                    )
            except User.DoesNotExist:
                # Don't reveal that user doesn't exist
                pass

            # Authenticate user
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                # Handle failed login attempt
                try:
                    failed_user = User.objects.get(email=email)
                    failed_user.increment_failed_login_attempts()
                except User.DoesNotExist:
                    pass

                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )

            # Reset failed login attempts on successful login
            user.reset_failed_login_attempts()
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role',
            'is_verified', 'identity_verified', 'date_joined',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'date_joined', 'created_at', 'updated_at',
            'is_verified', 'identity_verified'
        )