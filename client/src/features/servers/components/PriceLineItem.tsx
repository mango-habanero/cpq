import { Box, Typography } from '@mui/material';

interface IPriceLineItemProps {
    label: string;
    price: string;
    isBasePrice?: boolean;
}

const PriceLineItem = ({
    label,
    price,
    isBasePrice = false,
}: IPriceLineItemProps) => {
    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                py: 1,
                borderBottom: isBasePrice ? 1 : 0,
                borderColor: 'divider',
                mb: isBasePrice ? 1 : 0,
            }}
        >
            <Typography
                variant={isBasePrice ? 'body1' : 'body2'}
                sx={{
                    fontWeight: isBasePrice ? 500 : 400,
                    color: isBasePrice ? 'text.primary' : 'text.secondary',
                }}
            >
                {label}
            </Typography>

            <Typography
                variant={isBasePrice ? 'body1' : 'body2'}
                sx={{
                    fontWeight: 500,
                    color: isBasePrice ? 'text.primary' : 'text.secondary',
                    textAlign: 'right',
                }}
            >
                {price}
            </Typography>
        </Box>
    );
};

export default PriceLineItem;
