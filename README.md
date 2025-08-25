# Shadow Cauldron - AI Experimentation Platform

## Purpose

Shadow Cauldron is a modular AI experimentation platform that enables parallel testing and comparison of different AI providers and models. Built following the "bricks and studs" philosophy, it provides a structured way to design, execute, and analyze AI experiments.

## Architecture

This application is built as a collection of self-contained "bricks" that communicate through well-defined contracts:

```
shadow-cauldron/
├── app/                        # Main application
│   ├── config/                # Configuration brick
│   ├── core/                  # Auth, middleware, logging brick
│   ├── api/                   # API routes brick
│   ├── models/                # Database models brick
│   ├── providers/             # AI provider plugin system brick
│   ├── experiments/           # Experiment engine brick
│   └── storage/               # File & data management brick
├── tests/                     # Test suite
├── docker/                    # Container configurations
└── alembic/                   # Database migrations
```

## Modular Design Principles

Each brick follows these principles:

1. **Single Responsibility**: Each brick has one clear purpose
2. **Contract-Based**: Public interfaces defined in `__init__.py`
3. **Self-Contained**: All code, tests, and dependencies within brick folder
4. **Regeneratable**: Can be rebuilt from specification without breaking connections
5. **Minimal Dependencies**: Bricks connect only through public contracts

## Public Contracts

### Config Brick
```python
from app.config import settings, Settings, DatabaseConfig
```

### Core Brick  
```python
from app.core import setup_logging, setup_middleware, get_current_user, AuthenticatedUser
```

### API Brick
```python
from app.api import router
```

### Models Brick
```python
from app.models import Base, SessionLocal, get_db, User
```

### Providers Brick
```python
from app.providers import ProviderRegistry, BaseProvider, get_provider, list_providers
```

### Experiments Brick
```python
from app.experiments import ExperimentEngine, Experiment, ExperimentRun, create_experiment, run_experiment
```

### Storage Brick
```python
from app.storage import StorageManager, upload_file, get_file, delete_file
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for development)
- uv (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd shadow-cauldron

# Install dependencies
make install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
make migrate

# Start development server
make dev
```

### Environment Variables

Required environment variables (prefix with `SC_`):

- `SC_SECRET_KEY`: Secret key for JWT tokens
- `SC_DATABASE_URL`: Database connection URL
- `SC_OPENAI_API_KEY`: OpenAI API key (optional)
- `SC_ANTHROPIC_API_KEY`: Anthropic API key (optional)

### Development

```bash
# Run all checks (lint, format, type check)
make check

# Run tests
make test

# Start development server with hot reload
make dev

# Create database migration
make revision MSG="Add new table"

# Apply migrations
make migrate
```

### Docker

```bash
# Build and run with Docker
make docker-run

# Development with Docker Compose
make docker-dev
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/status` - API status
- `GET /api/v1/protected` - Protected endpoint (requires authentication)
- `GET /api/v1/experiments` - List experiments
- `GET /api/v1/providers` - List AI providers

## Key Features

### Multi-Provider Support
- Plugin-based AI provider system
- Support for OpenAI, Anthropic, and custom providers
- Unified interface for all providers

### Parallel Experimentation
- Run experiments across multiple providers simultaneously
- Compare results, performance, and costs
- Structured experiment configuration

### Storage Management
- File upload and management
- Experiment data persistence
- Result archiving and retrieval

### Authentication & Security
- JWT-based authentication
- Role-based access control
- Secure API key management

## Extension Points

To add new functionality:

1. **New Provider**: Implement `BaseProvider` in `app/providers/`
2. **New API Routes**: Add routes in `app/api/routes.py`
3. **New Models**: Add SQLAlchemy models in `app/models/`
4. **New Storage Backend**: Extend `StorageManager` in `app/storage/`

## Testing

The project includes comprehensive testing at multiple levels:

- **Unit Tests**: Test individual brick functionality
- **Integration Tests**: Test brick interactions
- **End-to-End Tests**: Test complete user workflows

## Contributing

When modifying the codebase:

1. Each brick should remain self-contained
2. Changes to public contracts require updating dependent bricks
3. Prefer regenerating entire bricks over line-by-line edits
4. Add tests for new functionality
5. Update documentation for contract changes

## License

[License information here]