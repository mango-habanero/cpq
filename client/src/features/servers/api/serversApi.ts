import { api } from '../../../services/api';
import type { IBaseResponse } from '../../../services/types';
import type {
    IServerConfigurationParams,
    IServerConfigurationResponse,
    ServerOptionsResponse,
} from '../types';

export const serversApi = api.injectEndpoints({
    endpoints: (build) => ({
        getServerConfiguration: build.query<
            IBaseResponse<IServerConfigurationResponse>,
            IServerConfigurationParams
        >({
            query: (params) => ({
                url: '/servers/configure',
                method: 'GET',
                params,
            }),
            providesTags: ['ServerConfigurations'],
        }),
        getServerOptions: build.query<
            IBaseResponse<ServerOptionsResponse>,
            void
        >({
            query: () => ({
                url: '/servers/options',
                method: 'GET',
            }),
            providesTags: ['ServerOptions'],
        }),
    }),
});

export const { useGetServerConfigurationQuery, useGetServerOptionsQuery } =
    serversApi;
