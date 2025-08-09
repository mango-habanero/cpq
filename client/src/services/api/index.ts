import { createApi } from '@reduxjs/toolkit/query/react';
import { baseQuery } from './baseQuery';
import { mapErrorCodeToMessage } from './errorMap';
import type { ErrorResponse } from '../types';

type BaseQueryFunction = typeof baseQuery;
type BaseQueryArgs = Parameters<BaseQueryFunction>[0];
type BaseQueryApi = Parameters<BaseQueryFunction>[1];
type BaseQueryExtraOptions = Parameters<BaseQueryFunction>[2];

export const baseQueryWithErrorHandling = async (
    args: BaseQueryArgs,
    api: BaseQueryApi,
    extraOptions: BaseQueryExtraOptions
) => {
    const result = await baseQuery(args, api, extraOptions);

    if (result.error) {
        const error = result.error as { data?: ErrorResponse };
        if (error.data?.code) {
            const userMessage = mapErrorCodeToMessage(error.data.code);
            return {
                ...result,
                error: {
                    ...result.error,
                    userMessage,
                },
            };
        }
    }

    return result;
};

export const api = createApi({
    baseQuery: baseQueryWithErrorHandling,
    endpoints: () => ({}),
    reducerPath: 'api',
    tagTypes: ['ServerConfigurations', 'ServerOptions', 'Quotes'],
});
