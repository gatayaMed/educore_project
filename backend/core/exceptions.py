"""
Custom exception handler for consistent API error responses
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all errors consistently.
    """
    # First call DRF's default exception handler
    response = exception_handler(exc, context)
    
    # Handle Django ValidationErrors
    if isinstance(exc, DjangoValidationError):
        data = {'detail': exc.message if hasattr(exc, 'message') else str(exc)}
        response = Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # Format response if we have one
    if response is not None:
        formatted_data = {
            'error': {
                'code': response.status_code,
                'message': _get_error_message(response.data, exc),
                'details': response.data
            }
        }
        response.data = formatted_data
    
    return response


def _get_error_message(data, exc):
    """Extract a user-friendly error message from the data."""
    if isinstance(data, dict) and 'detail' in data:
        return str(data['detail'])
    
    if isinstance(data, dict):
        for field, errors in data.items():
            if errors and isinstance(errors, list) and len(errors) > 0:
                return f"{field}: {errors[0]}"
            elif errors and isinstance(errors, str):
                return errors
    
    return str(exc)