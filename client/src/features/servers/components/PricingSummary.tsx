import { Box, Card, Typography, Divider } from '@mui/material';
import type {
    IServerConfigurationState,
    IServerConfigurationResponse,
} from '../types';
import PriceLineItem from './PriceLineItem';
import RequestQuoteButton from './RequestQuoteButton';

interface IPricingSummaryProps {
    configuration: IServerConfigurationState;
    pricing: IServerConfigurationResponse;
    onRequestQuote: () => void;
}

const PricingSummary = ({
    configuration,
    pricing,
    onRequestQuote,
}: IPricingSummaryProps) => {
    return (
        <Card sx={{ p: 3, height: 'fit-content', position: 'sticky', top: 24 }}>
            <Typography variant="h6" component="h2" sx={{ mb: 3 }}>
                Your Configuration
            </Typography>

            <Box sx={{ mb: 3 }}>
                {Object.entries(pricing.current_selection).map(([field]) => {
                    const userSelection =
                        configuration[field as keyof IServerConfigurationState];

                    return (
                        <PriceLineItem
                            key={field}
                            label={
                                userSelection
                                    ? userSelection.display_name
                                    : `${field}: Not selected`
                            }
                            price={
                                userSelection ? `+€${userSelection.price}` : ''
                            }
                        />
                    );
                })}
            </Box>

            {pricing.discount_descriptions?.length > 0 && (
                <Box sx={{ mb: 3 }}>
                    <Typography
                        variant="body2"
                        sx={{ color: 'success.main', mb: 1 }}
                    >
                        Discounts Applied:
                    </Typography>
                    {pricing.discount_descriptions.map((discount, index) => (
                        <Typography
                            key={index}
                            variant="body2"
                            sx={{ color: 'success.main' }}
                        >
                            • {discount}
                        </Typography>
                    ))}
                    <Divider sx={{ mt: 2 }} />
                </Box>
            )}

            <Box sx={{ mb: 3 }}>
                <Typography
                    variant="h5"
                    sx={{ fontWeight: 600, textAlign: 'center' }}
                >
                    Total: €{pricing.total_price}/month
                </Typography>
            </Box>

            <RequestQuoteButton
                onRequestQuote={onRequestQuote}
                disabled={!pricing.is_valid}
            />
        </Card>
    );
};

export default PricingSummary;
