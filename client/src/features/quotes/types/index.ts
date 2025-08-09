import type { ServerConfigurationSelection } from '../../servers/types';

export interface QuoteRequest {
    configuration: ServerConfigurationSelection;
    contact_name: string;
    contact_email: string;
    company?: string;
}

export interface QuoteResponse {
    id: string;
    total_price: number;
    created_at: string;
}
