import { Button, CircularProgress } from '@mui/material';

interface IRequestQuoteButtonProps {
    onRequestQuote: () => void;
    disabled?: boolean;
    loading?: boolean;
}

const RequestQuoteButton = ({
    onRequestQuote,
    disabled = false,
    loading = false,
}: IRequestQuoteButtonProps) => {
    return (
        <Button
            variant="contained"
            color="primary"
            size="large"
            fullWidth
            onClick={onRequestQuote}
            disabled={disabled || loading}
            startIcon={
                loading ? (
                    <CircularProgress size={20} color="inherit" />
                ) : undefined
            }
            sx={{
                py: 1.5,
                fontSize: '1rem',
                fontWeight: 600,
                textTransform: 'none',
            }}
        >
            {loading ? 'Processing...' : 'Request Quote'}
        </Button>
    );
};

export default RequestQuoteButton;
