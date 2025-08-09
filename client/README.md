# CPQ Client Application

A React frontend for the CPQ (Configure, Price, Quote) system that provides an interface for server configuration and quote generation. Built with React, TypeScript, and Material-UI to consume the FastAPI backend.

## Key Features

- **Server Configuration Interface** - Select CPU, RAM, storage, and OS options
- **Real-time Pricing** - Dynamic price calculations based on backend rules
- **Quote Request System** - Submit configuration with contact details
- **Responsive Design** - Material-UI components for desktop and mobile
- **Type-Safe API Integration** - RTK Query for backend communication

## Getting Started

### Prerequisites

- **Node.js**: 18.0.0+
- **Package Manager**: pnpm
- **Backend**: CPQ FastAPI server running on `http://localhost:8000`

### Installation

1. **Install dependencies**

```bash
pnpm install
```

2. **Configure environment** (`.env`):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

3. **Start development server**

```bash
pnpm dev
```

The application will be available at `http://localhost:5173`.

## Available Scripts

```bash
pnpm dev       # Start development server
pnpm build     # Build for production
pnpm preview   # Preview production build
pnpm lint      # Run ESLint
pnpm format    # Format code with Prettier
```

## Project Structure

```
src/
├── app/                    # Redux store configuration
├── features/
│   ├── servers/           # Server configuration features
│   │   ├── api/          # Server API endpoints
│   │   ├── components/   # UI components
│   │   ├── pages/        # Configuration page
│   │   └── types/        # TypeScript types
│   └── quotes/           # Quote request features
│       ├── api/          # Quote API endpoints
│       ├── components/   # Quote modal and forms
│       └── types/        # TypeScript types
├── services/             # Shared API configuration
├── shared/               # Reusable components
└── styles/               # Global styles and theme
```
