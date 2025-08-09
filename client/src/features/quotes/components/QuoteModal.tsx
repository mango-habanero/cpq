import { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Box,
    Divider,
    IconButton,
    Alert,
    Snackbar,
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import { useCreateQuoteRequestMutation } from '../api';
import type {
    IServerConfigurationState,
    IServerConfigurationResponse,
} from '../../servers/types';
import ContactForm, { type ContactFormData } from './ContactForm';
import type { ErrorResponse } from '../../../services/types';

interface QuoteModalProps {
    open: boolean;
    onClose: () => void;
    configuration: IServerConfigurationState;
    pricing: IServerConfigurationResponse;
}

const QuoteModal = ({
    open,
    onClose,
    configuration,
    pricing,
}: QuoteModalProps) => {
    const [createQuoteRequest, { isLoading }] = useCreateQuoteRequestMutation();
    const [showSuccess, setShowSuccess] = useState(false);
    const [submitError, setSubmitError] = useState<string>('');

    const selectedOptions = Object.entries(configuration)
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        .filter(([_, selection]) => selection !== null)
        .map(([key, selection]) => ({
            key,
            value: selection!.id,
            price: selection!.price,
        }));

    const handleFormSubmit = async (contactData: ContactFormData) => {
        try {
            setSubmitError('');

            // Convert the enhanced state back to API format for submission
            const configurationData = {
                cpu_architecture: configuration.cpu_architecture?.id || null,
                cpu_cores: configuration.cpu_cores?.id || null,
                ram: configuration.ram?.id || null,
                storage: configuration.storage?.id || null,
                os: configuration.os?.id || null,
            };

            const quoteRequest = {
                configuration: configurationData,
                contact_name: contactData.contact_name,
                contact_email: contactData.contact_email,
                company: contactData.company,
            };

            await createQuoteRequest(quoteRequest).unwrap();
            setShowSuccess(true);
            onClose();
        } catch (error: unknown) {
            // Handle API errors
            const errorMessage =
                (error as ErrorResponse)?.message ||
                'Failed to submit quote request. Please try again.';
            setSubmitError(errorMessage);
        }
    };

    const handleClose = () => {
        setSubmitError('');
        onClose();
    };

    const handleSuccessClose = () => {
        setShowSuccess(false);
    };

    return (
        <>
            <Dialog
                open={open}
                onClose={handleClose}
                maxWidth="sm"
                fullWidth
                slotProps={{
                    paper: {
                        sx: { borderRadius: 2 },
                    },
                }}
            >
                <DialogTitle
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                    }}
                >
                    <Typography variant="h5" component="h2">
                        Request Quote
                    </Typography>
                    <IconButton
                        onClick={handleClose}
                        disabled={isLoading}
                        sx={{ color: 'grey.500' }}
                    >
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>

                <DialogContent dividers>
                    {/* Configuration Summary */}
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" sx={{ mb: 2 }}>
                            Your Configuration
                        </Typography>

                        <Box
                            sx={{
                                bgcolor: 'grey.50',
                                p: 2,
                                borderRadius: 1,
                                mb: 2,
                            }}
                        >
                            {selectedOptions.map(({ key, value, price }) => (
                                <Typography
                                    key={key}
                                    variant="body2"
                                    color="text.secondary"
                                >
                                    {value}: +€{price}
                                </Typography>
                            ))}

                            <Divider sx={{ my: 1 }} />

                            <Typography variant="h6" color="primary.main">
                                Total: €{pricing.total_price}/month
                            </Typography>

                            {pricing.discount_descriptions?.length > 0 && (
                                <Box sx={{ mt: 1 }}>
                                    {pricing.discount_descriptions.map(
                                        (discount, index) => (
                                            <Typography
                                                key={index}
                                                variant="body2"
                                                color="success.main"
                                            >
                                                • {discount}
                                            </Typography>
                                        )
                                    )}
                                </Box>
                            )}
                        </Box>
                    </Box>

                    <Divider sx={{ mb: 2 }} />

                    {/* Contact Form */}
                    <ContactForm
                        onSubmit={handleFormSubmit}
                        loading={isLoading}
                        error={submitError}
                    />
                </DialogContent>

                <DialogActions sx={{ p: 3 }}>
                    <Button
                        onClick={handleClose}
                        disabled={isLoading}
                        color="inherit"
                    >
                        Cancel
                    </Button>
                    <Button
                        type="submit"
                        form="contact-form"
                        variant="contained"
                        disabled={isLoading}
                        sx={{ minWidth: 120 }}
                    >
                        {isLoading ? 'Submitting...' : 'Submit Request'}
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Success Notification */}
            <Snackbar
                open={showSuccess}
                autoHideDuration={6000}
                onClose={handleSuccessClose}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert
                    onClose={handleSuccessClose}
                    severity="success"
                    sx={{ width: '100%' }}
                >
                    Quote request submitted successfully! We'll contact you
                    soon.
                </Alert>
            </Snackbar>
        </>
    );
};

export default QuoteModal;
