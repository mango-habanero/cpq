export interface IServerOption {
    available: boolean;
    display_name: string;
    id: string;
    price: string;
}

export interface IOptionSelection {
    id: string;
    display_name: string;
    price: number;
}

export interface IServerConfigurationState {
    [categoryId: string]: IOptionSelection | null;
}

export interface IServerConfigurationParams {
    [key: string]: string | undefined;
}

export interface IServerConfigurationSelection {
    [categoryId: string]: string | null;
}

export interface IServerConfigurationResponse {
    current_selection: IServerConfigurationSelection;
    total_price: string;
    total_discount?: string;
    discount_descriptions: string[];
    is_valid: boolean;
}

export type ServerOptionsResponse = Record<string, IServerOption[]>;
