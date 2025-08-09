import { Container } from '@mui/material';
import ServerConfigurationPage from './features/servers/pages/ServerConfigurationPage';

function App() {
    return (
        <Container maxWidth="xl" sx={{ py: 4 }}>
            <ServerConfigurationPage />
        </Container>
    );
}

export default App;
