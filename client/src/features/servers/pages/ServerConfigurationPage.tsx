import {useMemo, useState} from 'react';
import { Grid, Box, CircularProgress, Alert } from '@mui/material';
import {
    useGetServerOptionsQuery,
    useGetServerConfigurationQuery,
} from '../api';
import type {
    IServerConfigurationState,
    IOptionSelection
} from '../types';
import { ConfigurationPanel, PricingSummary } from '../components';
import { QuoteModal } from '../../quotes/components';
import { ErrorBoundary } from '../../../shared/components/ErrorBoundary.tsx';
import type { FetchBaseQueryError } from '@reduxjs/toolkit/query';

const ServerConfigurationPage = () => {
    const [configuration, setConfiguration] =
        useState<IServerConfigurationState>({});

    const [quoteModalOpen, setQuoteModalOpen] = useState(false);

    const {
        data: optionsResponse,
        isLoading: optionsLoading,
        error: optionsError,
    } = useGetServerOptionsQuery();

    const configParams = useMemo(() => {
        const params: Record<string, string> = {};
        Object.entries(configuration).forEach(([id, selection]) => {
            if (selection) {
                params[id] = selection.id;
            }
        });
        return params;
    }, [configuration]);

    // Always call configuration API - let backend handle validation
    const {
        data: pricingResponse,
        isLoading: pricingLoading,
        error: pricingError,
    } = useGetServerConfigurationQuery(configParams);

    const handleConfigurationChange = (field: string, id: string) => {
        if (!optionsResponse?.data) return;

        const option = optionsResponse.data[field]?.find(opt => opt.id === id);
        if (!option) return;

        const optionSelection: IOptionSelection = {
            id: id,
            display_name: option.display_name,
            price: parseFloat(option.price),
        };

        setConfiguration(prev => ({
            ...prev,
            [field]: optionSelection,
        }));
    };

    const handleRequestQuote = () => {
        setQuoteModalOpen(true);
    };

    const handleQuoteModalClose = () => {
        setQuoteModalOpen(false);
    };

    // Handle options loading and errors
    if (optionsLoading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="400px"
            >
                <CircularProgress />
            </Box>
        );
    }

    if (optionsError || !optionsResponse?.data) {
        return (
            <Alert severity="error">
                Unable to load server configuration options. Please try again.
            </Alert>
        );
    }

    return (
        <>
            <Grid container spacing={4}>
                <Grid size={{ xs: 12, md: 7 }}>
                    <ConfigurationPanel
                        options={optionsResponse.data}
                        configuration={configuration}
                        onConfigChange={handleConfigurationChange}
                    />
                </Grid>

                <Grid size={{ xs: 12, md: 5 }}>
                    <ErrorBoundary
                        error={pricingError as FetchBaseQueryError}
                        variant={'error'}
                    >
                        {pricingResponse?.data ? (
                            <PricingSummary
                                configuration={configuration}
                                pricing={pricingResponse.data}
                                onRequestQuote={handleRequestQuote}
                            />
                        ) : pricingLoading ? (
                            <Box display="flex" justifyContent="center" mt={4}>
                                <CircularProgress size={24} />
                            </Box>
                        ) : null}
                    </ErrorBoundary>
                </Grid>
            </Grid>

            {/* Quote Modal */}
            {pricingResponse?.data && (
                <QuoteModal
                    open={quoteModalOpen}
                    onClose={handleQuoteModalClose}
                    configuration={configuration}
                    pricing={pricingResponse.data}
                />
            )}
        </>
    );
};

export default ServerConfigurationPage;
