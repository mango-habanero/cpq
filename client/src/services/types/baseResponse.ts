export interface IBaseResponse<T> {
    status: ResponseStatus;
    message: string;
    data?: T;
}

export type ResponseStatus = 'SUCCESS' | 'FAILED';
