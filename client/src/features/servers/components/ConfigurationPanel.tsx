import { Box, Typography } from '@mui/material';
import type {
    IServerConfigurationState,
    ServerOptionsResponse,
} from '../types';
import ConfigurationSection from './ConfigurationSection';

interface IConfigurationPanelProps {
    options: ServerOptionsResponse;
    configuration: IServerConfigurationState;
    onConfigChange: (field: string, id: string) => void;
}

const ConfigurationPanel = ({
    options,
    configuration,
    onConfigChange,
}: IConfigurationPanelProps) => {
    return (
        <Box>
            <Typography
                variant="h4"
                component="h1"
                sx={{
                    mb: 4,
                    fontWeight: 500,
                    color: 'text.primary',
                }}
            >
                Configure Your Server
            </Typography>

            {Object.entries(options).map(([sectionKey, sectionOptions]) => {
                const selection = configuration[sectionKey];

                return (
                    <ConfigurationSection
                        key={sectionKey}
                        title={sectionKey}
                        options={sectionOptions}
                        selectedValue={selection?.id || null}
                        onSelectionChange={(id) =>
                            onConfigChange(sectionKey, id)
                        }
                    />
                );
            })}
        </Box>
    );
};

export default ConfigurationPanel;
