import { ButtonBase, Typography } from '@mui/material';
import type { IServerOption } from '../types';

interface IConfigurationOptionProps {
    option: IServerOption;
    isSelected: boolean;
    onClick: () => void;
    disabled?: boolean;
}

const ConfigurationOption = ({
    option,
    isSelected,
    onClick,
    disabled = false,
}: IConfigurationOptionProps) => {
    const priceValue = parseFloat(option.price);
    const isFreeTier = priceValue === 0;

    const priceDisplay = isFreeTier ? '+€0' : `+€${priceValue}`;

    return (
        <ButtonBase
            onClick={onClick}
            disabled={disabled}
            sx={{
                width: '100%',
                borderRadius: 1,
                border: 2,
                borderColor: isSelected ? 'primary.main' : 'grey.300',
                backgroundColor: isSelected ? 'primary.50' : 'background.paper',
                p: 2,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                transition: 'all 0.2s ease-in-out',
                '&:hover:not(:disabled)': {
                    borderColor: isSelected ? 'primary.main' : 'primary.light',
                    backgroundColor: isSelected ? 'primary.100' : 'grey.50',
                    transform: 'translateY(-1px)',
                    boxShadow: 1,
                },
                '&:disabled': {
                    opacity: 0.5,
                    cursor: 'not-allowed',
                },
            }}
        >
            <Typography
                variant="body1"
                sx={{
                    fontWeight: isSelected ? 500 : 400,
                    color: disabled ? 'text.disabled' : 'text.primary',
                }}
            >
                {option.display_name}
            </Typography>

            <Typography
                variant="body2"
                sx={{
                    fontWeight: 500,
                    color: disabled
                        ? 'text.disabled'
                        : isFreeTier
                          ? 'text.secondary'
                          : 'primary.main',
                }}
            >
                {priceDisplay}
            </Typography>
        </ButtonBase>
    );
};

export default ConfigurationOption;
