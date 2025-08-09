import { type ReactNode, useEffect, useState } from 'react';
import { Alert, Box, Snackbar } from '@mui/material';
import type { ErrorResponse } from '../../services/types';
import type { FetchBaseQueryError } from '@reduxjs/toolkit/query';

interface IErrorBoundaryProps {
    error: FetchBaseQueryError;
    variant: 'error' | 'warning' | 'info' | 'success';
    onClose?: () => void;
    children?: ReactNode;
}
export const ErrorBoundary = ({
    error,
    variant,
    children,
}: IErrorBoundaryProps) => {
    const data = error?.data as ErrorResponse;
    const [hasError, setHasError] = useState(false);
    const [open, setOpen] = useState(false);
    const handleClose = () => {
        setOpen(false);
    };
    useEffect(() => {
        setOpen(true);
        if (error) {
            setHasError(true);
        }
    }, [error, error?.data]);
    return (
        <Box>
            <Snackbar
                open={open && hasError}
                autoHideDuration={6000}
                onClose={handleClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert
                    onClose={handleClose}
                    severity={variant}
                    sx={{ width: '100%' }}
                >
                    {data?.message}
                </Alert>
            </Snackbar>
            {children}
        </Box>
    );
};
