"""
Utility functions for user authentication and security.
"""
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Get client IP address from request, handling proxy headers.

    Args:
        request: Django request object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take the first IP in the chain (client IP)
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_security_event(event_type, user_email, ip_address, details=None):
    """
    Log security events with standardized format.

    Args:
        event_type (str): Type of security event
        user_email (str): User email involved
        ip_address (str): IP address of the request
        details (str): Additional details about the event
    """
    message = f'SECURITY_EVENT: {event_type} - User: {user_email} - IP: {ip_address}'
    if details:
        message += f' - Details: {details}'

    if event_type in ['LOGIN_FAILED', 'REGISTRATION_FAILED', 'INVALID_TOKEN']:
        logger.warning(message)
    elif event_type in ['LOGIN_SUCCESS', 'REGISTRATION_SUCCESS', 'LOGOUT_SUCCESS']:
        logger.info(message)
    else:
        logger.error(message)


class SecurityMixin:
    """
    Mixin class providing common security functionality for authentication views.
    """

    def get_client_ip(self, request):
        """Get client IP address from request."""
        return get_client_ip(request)

    def log_security_event(self, event_type, user_email, request, details=None):
        """Log security event with IP address."""
        ip_address = self.get_client_ip(request)
        log_security_event(event_type, user_email, ip_address, details)

    def handle_error_response(self, error_message, status_code, user_email=None, request=None):
        """
        Handle error responses with proper logging.

        Args:
            error_message (str): Error message to return
            status_code (int): HTTP status code
            user_email (str): User email if available
            request: Django request object if available

        Returns:
            Response: DRF Response object
        """
        from rest_framework.response import Response

        if request and user_email:
            self.log_security_event(
                'ERROR_RESPONSE',
                user_email,
                request,
                f'Status: {status_code}, Message: {error_message}'
            )

        return Response(
            {'error': error_message},
            status=status_code
        )