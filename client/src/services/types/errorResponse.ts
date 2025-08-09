import type { ResponseStatus } from './baseResponse.ts';

export interface ErrorResponse {
    status: ResponseStatus;
    code: string;
    message: string;
    timestamp: string;
    errors?: ErrorDetail[];
    errorReference: string;
}

export interface ErrorDetail {
    field?: string;
    message: string;
    rejectedValue?: unknown;
}

export type ErrorCode =
    | 'AUTHENTICATION_FAILED'
    | 'DUPLICATE_RESOURCE'
    | 'EXTERNAL_SERVICE_ERROR'
    | 'FORBIDDEN_ACCESS'
    | 'INTERNAL_SERVER_ERROR'
    | 'INVALID_ARGUMENTS'
    | 'INVALID_FORMAT'
    | 'INVALID_STATE'
    | 'MISSING_REQUIRED_FIELD'
    | 'RESOURCE_NOT_FOUND'
    | 'UNAUTHORIZED_ACCESS';
