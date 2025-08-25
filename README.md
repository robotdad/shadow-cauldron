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
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)
- Git

**Note**: This project uses SQLite by default for development (no additional database setup required). PostgreSQL can be used for production.

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/robotdad/shadow-cauldron.git
cd shadow-cauldron

# 2. Install dependencies (creates .venv automatically)
make install

# 3. Set up environment (optional for development)
cp .env.example .env
# Edit .env if you need custom settings

# 4. Initialize database
make migrate

# 5. Start development server
make dev
```

The application will be available at: **http://localhost:8000**

- Health check: http://localhost:8000/health
- API status: http://localhost:8000/api/v1/status  
- API docs: http://localhost:8000/docs (in debug mode)

### Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"shadow-cauldron"}

# Run tests
make test
# Should show: 3 passed

# Check code quality
make check
# Should format and lint code successfully
```

### Environment Variables (Optional)

The application works out of the box with sensible defaults. Environment variables are prefixed with `SC_`:

**Required for production:**
- `SC_SECRET_KEY`: Secret key for JWT tokens (defaults to dev key)

**Optional:**
- `SC_DATABASE_URL`: Database connection URL (defaults to SQLite: `sqlite+aiosqlite:///./shadow_cauldron.db`)
- `SC_DEBUG`: Enable debug mode (defaults to `false`)
- `SC_HOST`: Server host (defaults to `0.0.0.0`)
- `SC_PORT`: Server port (defaults to `8000`)
- `SC_OPENAI_API_KEY`: OpenAI API key for AI providers
- `SC_ANTHROPIC_API_KEY`: Anthropic API key for AI providers

**Example `.env` file:**
```bash
SC_DEBUG=true
SC_SECRET_KEY=your-secure-secret-key-here
SC_OPENAI_API_KEY=your-openai-key
SC_ANTHROPIC_API_KEY=your-anthropic-key
```

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

### Troubleshooting

**Common Issues:**

1. **`uv` not found**: Install uv from https://docs.astral.sh/uv/getting-started/installation/
2. **Permission errors**: Make sure you have write permissions in the project directory
3. **Port 8000 in use**: Either stop the service using port 8000 or set `SC_PORT=8001` in your `.env`
4. **Database errors**: Run `make reset-db` to recreate the database from scratch

**Getting Help:**
- Check the logs when running `make dev`
- Verify all tests pass with `make test`
- Ensure code quality with `make check`

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

## Current Status

**Phase 1: Foundation ✅ Complete**
- ✅ Modular architecture with 7 self-contained bricks
- ✅ FastAPI backend with JWT authentication
- ✅ SQLite database with migrations
- ✅ Provider plugin system foundation
- ✅ Experiment orchestration framework  
- ✅ Development tools and testing

**Phase 2: AI Provider Integration (Planned)**
- 🔄 HuggingFace Diffusers integration
- 🔄 OpenAI and Anthropic providers
- 🔄 RTX 4080 GPU optimizations
- 🔄 Parallel experiment execution

## Contributing

Contributions are welcome! When modifying the codebase:

1. Each brick should remain self-contained
2. Changes to public contracts require updating dependent bricks  
3. Prefer regenerating entire bricks over line-by-line edits
4. Add tests for new functionality
5. Update documentation for contract changes

## License

MIT License - see LICENSE file for details.