import { Box, Typography, Stack } from '@mui/material';
import type { IServerOption } from '../types';
import ConfigurationOption from './ConfigurationOption';

interface IConfigurationSectionProps {
    title: string;
    options: IServerOption[];
    selectedValue: string | null;
    onSelectionChange: (value: string) => void;
    disabled?: boolean;
}

const ConfigurationSection = ({
    title,
    options,
    selectedValue,
    onSelectionChange,
    disabled = false,
}: IConfigurationSectionProps) => {
    return (
        <Box sx={{ mb: 3 }}>
            <Typography
                variant="h6"
                component="h3"
                sx={{
                    mb: 2,
                    fontWeight: 500,
                    color: disabled ? 'text.disabled' : 'text.primary',
                }}
            >
                {title.replace(/_/g, ' ').toUpperCase()}
            </Typography>

            <Stack spacing={1}>
                {options.map((option) => (
                    <ConfigurationOption
                        key={option.display_name}
                        option={option}
                        isSelected={selectedValue === option.id}
                        onClick={() => onSelectionChange(option.id)}
                        disabled={disabled || !option.available}
                    />
                ))}
            </Stack>
        </Box>
    );
};

export default ConfigurationSection;
