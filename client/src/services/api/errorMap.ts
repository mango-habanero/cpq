import type { ErrorCode } from '../types';

const ERROR_MESSAGE_MAP: Record<ErrorCode, string> = {
    AUTHENTICATION_FAILED: 'Please check your credentials and try again',
    DUPLICATE_RESOURCE: 'This resource already exists',
    EXTERNAL_SERVICE_ERROR: 'An external service is currently unavailable',
    FORBIDDEN_ACCESS: 'You do not have permission to perform this action',
    INTERNAL_SERVER_ERROR:
        'An unexpected error occurred. Our team has been notified',
    INVALID_ARGUMENTS: 'Request contains invalid or incomplete information',
    INVALID_FORMAT: 'One or more fields have invalid formatting',
    INVALID_STATE: 'The resource is in an invalid state for this operation',
    MISSING_REQUIRED_FIELD: 'Required information is missing',
    RESOURCE_NOT_FOUND: 'The requested resource could not be found',
    UNAUTHORIZED_ACCESS: 'You are not authorized to access this resource',
};

export const mapErrorCodeToMessage = (code: string): string => {
    return (
        ERROR_MESSAGE_MAP[code as ErrorCode] || 'An unexpected error occurred'
    );
};
