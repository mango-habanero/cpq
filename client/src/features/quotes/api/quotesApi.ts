import { api } from '../../../services/api';
import type { BaseResponse } from '../../../services/types';
import type { QuoteRequest, QuoteResponse } from '../types';
import { toSnakeCase } from '../../../shared/utilities/apiUtility.ts';

export const quotesApi = api.injectEndpoints({
    endpoints: (build) => ({
        createQuoteRequest: build.mutation<
            BaseResponse<QuoteResponse>,
            QuoteRequest
        >({
            query: (body) => ({
                url: '/quotes/requests',
                method: 'POST',
                body: toSnakeCase(body),
            }),
            invalidatesTags: ['Quotes'],
        }),
    }),
});

export const { useCreateQuoteRequestMutation } = quotesApi;
