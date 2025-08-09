# CPQ Server Configuration System

A high-performance Configure, Price, Quote (CPQ) system built with Python for server hardware configuration and pricing. This application provides a rules-based engine for dynamic server configuration, pricing calculations, and quote generation with real-time business rule evaluation.

## Getting Started

### Prerequisites

- **Python**: 3.13.0 (managed via [pyenv](https://p-venv.readthedocs.io/en/stable/))
- **Package Manager**: [UV](https://docs.astral.sh/uv/) (for Python dependencies)

### Installation

1. **Clone the repository**
    ```shell script
    git clone https://github.com/mango-habanero/cpq.git
    cd cpq/backend
    ```

2. **Install dependencies**
    ```shell script
    uv sync --extra dev --extra docs
    ```

### Environment Setup

1. **Create environment configuration**
    ```shell script
    cp .env.example .env
    ```
2. **Configure environment variables** (`.env`):
    ```dotenv
       # server Configuration
       HOST=127.0.0.1
       PORT=8000
       WORKERS=1

       # application Configuration
       ENVIRONMENT=development

       # logging Configuration
       LOG_LEVEL=DEBUG
       LOG_JSON_FORMAT=false
    ```


### Quick Start

1. **Start the development server**
    ```shell script
    granian --interface asgi app.main:app
    ```

2. **Verify the installation**
    ```shell script
    curl http://localhost:8000/health
    ```

3. **Access the API documentation**
   Open `http://localhost:8000/docs` in your browser

## Project Structure

```
backend/
├── app/                         # Main application package
│   ├── api/                     # API layer
│   │   ├── routes/              # API route definitions
│   │   ├──dependencies.py       # Dependency injection
│   │   └── health.py            # Health check endpoints
│   ├── core/                    # Core application components
│   │   ├── app.py               # Application factory
│   │   ├── settings.py          # Configuration management
│   │   ├── logger.py            # Structured logging setup
│   │   └── exceptions/          # Custom exception handling
│   ├── data/                    # Data layer
│   │   ├── models/              # Data models and schemas
│   │   ├── store/               # Data persistence layer
│   │   ├── provider.py          # Data access abstraction
│   │   ├── enums.py             # Constants and enumerations
│   │   └── utilities.py         # Helper functions
│   ├── rules/                   # Rules engine
│   │   ├── engine.py            # Core rules processing
│   │   ├── condition_evaluator.py # Rule condition evaluation
│   │   └── handlers/            # Rule type handlers
│   ├── services/                # Business logic services
│   │   ├── quote.py             # Quote management
│   │   └── server.py            # Server configuration
│   ├── middleware/              # Request/response middleware
│   └── main.py                  # Application entry point
├── tests/                       # Test suite
├── scripts/                     # Utility scripts
├── .env.example                 # Environment template
├── pyproject.toml               # Project configuration
└── uv.lock                      # Dependency lock file
```

