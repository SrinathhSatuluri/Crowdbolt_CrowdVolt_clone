from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from django.contrib.auth import get_user_model

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'user': UserProfileSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return JWT tokens."""
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'user': UserProfileSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """User logout endpoint."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by blacklisting refresh token."""
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """User profile endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Update current user profile."""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(SimpleJWTTokenRefreshView):
    """JWT token refresh endpoint."""
    pass
