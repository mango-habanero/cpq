import { fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const baseQuery = fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
    prepareHeaders: (headers) => {
        headers.set('Accept', 'application/json');
        return headers;
    },
    paramsSerializer: (params) => {
        if (!params) return '';

        const stringParams: Record<string, string> = {};
        for (const [key, value] of Object.entries(params)) {
            if (value !== undefined && value !== null) {
                stringParams[key] = String(value);
            }
        }

        return new URLSearchParams(stringParams).toString();
    },
});
