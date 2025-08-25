# Shadow Cauldron - AI Generation Experimentation Platform

## Executive Summary

Shadow Cauldron is a complete an AI image generation experimentation system using modern Python architecture. The platform will support systematic exploration of AI generation parameters through batch processing, with provider-agnostic design for future extensibility into video and multimedia generation.

**Project Name**: Shadow Cauldron
**Core Architecture**: Modular Monolith with Plugin System
**Primary AI Backend**: HuggingFace Diffusers  
**Target Hardware**: RTX 4080, Mac M4 with 128GB RAM
**Foundation**: Bootstrap from ai-code-project-template

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Frontend (React)                    │
│                Socket.IO Real-time Updates                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                  FastAPI Backend                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │     API     │ │    Core     │ │      Extensions         ││
│  │   Routes    │ │   Config    │ │   (Future: LLM/Video)   ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ Experiments │ │  Providers  │ │        Jobs             ││
│  │   Engine    │ │ (AI Plugin) │ │   (Redis Queue)         ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│  ┌─────────────┐   │   ┌─────────────┐ ┌─────────────────┐  │
│  │ PostgreSQL  │   │   │    Redis    │ │  File Storage   │  │
│  │  Database   │   │   │  Job Queue  │ │  (Images/Meta)  │  │
│  └─────────────┘   │   └─────────────┘ └─────────────────┘  │
└─────────────────────┼───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────────────────┐
        │             │                         │
   ┌─────────┐  ┌─────────────┐  ┌─────────────────────┐
   │Diffusers│  │   ComfyUI   │  │   Future Providers  │
   │Provider │  │   Provider  │  │   (Video/Custom)    │
   └─────────┘  └─────────────┘  └─────────────────────┘
```

## Implementation Phases

### Phase 1: Foundation & Bootstrap (Weeks 1-2)

**Template Integration**
```bash
# Initial setup commands
git clone https://github.com/bkrabach/ai-code-project-template shadow-cauldron
cd shadow-cauldron
make install  # Use template's makefile system
```

**Project Structure**
```
shadow-cauldron/
├── Makefile                    # From template
├── pyproject.toml             # Python 3.11+ dependencies  
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── config.py             # Settings and environment
│   ├── api/                  # REST API routes
│   ├── core/                 # Auth, logging, middleware
│   ├── providers/            # AI provider plugin system
│   ├── experiments/          # Workflow engine
│   ├── storage/              # File and database management
│   ├── models/               # SQLAlchemy database models
│   └── jobs/                 # Async task processing
├── frontend/                 # React TypeScript UI
├── tests/                    # Comprehensive test suite
├── docker/                   # Container configurations
└── docs/                     # API and user documentation
```

**Core Dependencies**
- FastAPI + Uvicorn for async web framework
- PostgreSQL + SQLAlchemy for data persistence  
- Redis for job queuing and real-time updates
- Alembic for database migrations
- Pytest for testing framework

### Phase 2: AI Provider System (Weeks 3-4)

**Provider Abstraction Interface**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class GenerationParams:
    prompt: str
    model: str
    sampler: str
    steps: int
    cfg_scale: float
    seed: int
    width: int = 512
    height: int = 512

@dataclass  
class GenerationResult:
    image_path: str
    metadata: Dict[str, Any]
    generation_time: float
    memory_used: int

class AIProvider(ABC):
    @abstractmethod
    async def generate_image(self, params: GenerationParams) -> GenerationResult:
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        pass
    
    @abstractmethod
    async def optimize_for_hardware(self, device: str) -> None:
        pass
    
    @abstractmethod
    async def get_hardware_info(self) -> Dict[str, Any]:
        pass
```

**HuggingFace Diffusers Provider**
```python
class DiffusersProvider(AIProvider):
    def __init__(self):
        self.device = None
        self.pipeline = None
        self.current_model = None
    
    async def optimize_for_hardware(self, device: str):
        if "cuda" in device:
            # RTX 4080 optimizations
            import torch
            torch.backends.cudnn.benchmark = True
            self.device = device
        elif "mps" in device:
            # Mac M4 Metal optimizations  
            self.device = device
        
    async def generate_image(self, params: GenerationParams) -> GenerationResult:
        # Implement Diffusers pipeline execution
        # Include progress callbacks and memory management
        pass
```

**Job Processing System**
- Redis-based job queue using Celery or RQ
- Progress tracking via Redis pub/sub
- GPU resource management and allocation
- Error handling with retry logic

### Phase 3: Experimentation Framework (Weeks 5-6)

**Database Schema**
```python
# SQLAlchemy models for experiment tracking
class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(ExperimentType), nullable=False) 
    config = Column(JSON, nullable=False)
    status = Column(Enum(ExperimentStatus), default=ExperimentStatus.CREATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(UUID, ForeignKey("users.id"))
    
    runs = relationship("ExperimentRun", back_populates="experiment")

class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID, ForeignKey("experiment_runs.id"))
    prompt = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    file_path = Column(String, nullable=False)
    metadata = Column(JSON, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
```

**Experiment Types**
```python
class ExperimentEngine:
    async def create_convergence_experiment(
        self,
        prompts: List[str],
        models: List[str],
        samplers: List[str], 
        step_ranges: List[range]
    ) -> Experiment:
        """Create cross-product experiment: models×samplers×steps"""
        
    async def create_cfg_experiment(
        self,
        base_generation_id: UUID,
        cfg_range: range
    ) -> Experiment:
        """Explore CFG scale variations from base generation"""
        
    async def create_parameter_sweep(
        self,
        base_params: GenerationParams,
        parameter_ranges: Dict[str, List[Any]]
    ) -> Experiment:
        """Custom parameter exploration"""
```

**Workflow Execution**
- Async experiment execution with progress tracking  
- Batch generation with hardware optimization
- Result aggregation and analysis tools
- Automatic retry for failed generations

### Phase 4: Web Interface (Weeks 7-8)

**Frontend Technology Stack**
- React 18+ with TypeScript for type safety
- Tanstack Query for server state management
- Zustand for lightweight client state
- Chakra UI for consistent component library
- Socket.IO for real-time progress updates
- Vite for fast development and building

**Key Interface Components**

**Experiment Builder**
```typescript
interface ExperimentBuilderProps {
  type: 'convergence' | 'cfg' | 'parameter_sweep';
  onSubmit: (config: ExperimentConfig) => void;
  availableModels: string[];
  availableSamplers: string[];
}

const ExperimentBuilder: React.FC<ExperimentBuilderProps> = ({
  type,
  onSubmit,
  availableModels,
  availableSamplers
}) => {
  // Form components for experiment configuration
  // Dynamic parameter inputs based on experiment type
  // Real-time validation and preview
};
```

**Real-time Progress Monitor**  
```typescript
const ExperimentRunner: React.FC<{experimentId: string}> = ({experimentId}) => {
  const socket = useSocket();
  const [progress, setProgress] = useState<ExperimentProgress>();
  
  useEffect(() => {
    socket.on(`experiment:${experimentId}:progress`, setProgress);
    return () => socket.off(`experiment:${experimentId}:progress`);
  }, [experimentId]);
  
  return (
    <ProgressTracker 
      current={progress?.completed || 0}
      total={progress?.total || 0}
      currentImage={progress?.latest_image}
    />
  );
};
```

**Comparison Grid**
```typescript  
const ComparisonGrid: React.FC<{
  generations: Generation[];
  groupBy: 'sampler' | 'model' | 'steps';
  sortBy: string;
}> = ({generations, groupBy, sortBy}) => {
  // Grid layout with image thumbnails
  // Hover effects for parameter overlay
  // Click handling for detailed view
  // Keyboard navigation support
};
```

### Phase 5: Production Deployment (Weeks 9-10)

**Containerization**
```dockerfile
# Multi-stage Docker build
FROM pytorch/pytorch:2.1.0-cuda11.8-runtime-ubuntu20.04 as base

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app/ /app/
WORKDIR /app

# Production server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Development Environment**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/shadow_cauldron
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: shadow_cauldron
      POSTGRES_USER: user  
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Monitoring & Observability**
- Prometheus metrics for system performance
- Grafana dashboards for GPU utilization  
- Structured logging with correlation IDs
- Health checks and alerting
- Sentry integration for error tracking

## Future Extension Architecture

**Plugin System Design**
```python
class ExtensionPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        pass
    
    @abstractmethod
    async def process_generation(self, generation: Generation) -> Dict[str, Any]:
        pass

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, ExtensionPlugin] = {}
    
    def register_plugin(self, plugin: ExtensionPlugin):
        self.plugins[plugin.get_name()] = plugin
    
    async def process_with_plugins(self, generation: Generation):
        results = {}
        for name, plugin in self.plugins.items():
            results[name] = await plugin.process_generation(generation)
        return results
```

**LLM Integration Plugin**
```python
class LLMDescriptionPlugin(ExtensionPlugin):
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    async def process_generation(self, generation: Generation) -> Dict[str, Any]:
        image_description = await self.llm_client.describe_image(
            image_path=generation.file_path,
            prompt=f"Describe this image generated from: {generation.prompt}"
        )
        
        return {
            "auto_description": image_description,
            "tags": self.extract_tags(image_description),
            "quality_score": self.assess_quality(image_description)
        }
```

**ComfyUI Workflow Integration**  
```python
class ComfyUIWorkflowPlugin(ExtensionPlugin):
    async def export_workflow(self, generation: Generation) -> ComfyUIWorkflow:
        # Convert generation parameters to ComfyUI node graph
        workflow = ComfyUIWorkflow()
        
        # Add nodes based on generation parameters
        workflow.add_text_node(generation.prompt)
        workflow.add_model_node(generation.model_name)  
        workflow.add_sampler_node(generation.parameters['sampler'])
        
        return workflow
    
    async def import_from_comfyui(self, workflow: ComfyUIWorkflow) -> GenerationParams:
        # Parse ComfyUI workflow into our parameter format
        return GenerationParams(...)
```

**Video Generation Support**
```python
class VideoProvider(ABC):
    @abstractmethod
    async def generate_video(self, params: VideoGenerationParams) -> VideoResult:
        pass

@dataclass
class VideoGenerationParams:
    prompt: str
    duration: float
    fps: int
    resolution: Tuple[int, int]
    style_reference: Optional[str] = None
    motion_strength: float = 1.0
```

## Mobile App Strategy (Progressive Web App)

**PWA Features**
- Service Worker for offline capability
- Responsive design optimized for touch
- Local network discovery via mDNS
- Push notifications for experiment completion
- Image gallery optimized for mobile viewing
- Experiment monitoring dashboard

**Local Network Access**
```typescript
// PWA service worker for local network access
const discoverLocalServers = async (): Promise<string[]> => {
  // Scan common IP ranges for AI lab servers
  // Use mDNS discovery where available
  // Cache discovered servers for offline access
};

const ExperimentMonitor: React.FC = () => {
  const [serverUrl, setServerUrl] = useState<string>();
  
  useEffect(() => {
    discoverLocalServers().then(servers => {
      if (servers.length > 0) {
        setServerUrl(servers[0]);
      }
    });
  }, []);
  
  return <ExperimentDashboard serverUrl={serverUrl} />;
};
```

## Getting Started Guide

### Prerequisites Setup
1. **Hardware Requirements**:
   - NVIDIA RTX 4080 with latest drivers OR Mac M4 with 128GB RAM
   - Docker with GPU support (nvidia-docker2)
   - 50GB+ free disk space for models and images

2. **Development Environment**:
   ```bash
   # Clone and setup
   git clone https://github.com/bkrabach/ai-code-project-template shadow-cauldron
   cd shadow-cauldron
   
   # Install Python dependencies
   make install
   
   # Start development services
   docker-compose up -d postgres redis
   
   # Run database migrations  
   make migrate
   
   # Start development server
   make dev
   ```

### First Week Implementation Checklist

**Day 1-2: Foundation**
- [ ] Template integration and makefile adaptation
- [ ] Python environment setup with GPU support  
- [ ] Basic FastAPI application structure
- [ ] Docker development environment running

**Day 3-5: Core Systems**
- [ ] Database models and migrations working
- [ ] Redis connection and basic job queuing
- [ ] Provider abstraction interfaces defined
- [ ] Basic authentication and API middleware

**Week 2: AI Integration**  
- [ ] Simple Diffusers provider implementation
- [ ] Hardware detection and optimization
- [ ] Basic image generation endpoint functional
- [ ] Progress tracking and job management

### Verification Steps
```bash
# Test basic functionality
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "test generation",
    "model": "stabilityai/stable-diffusion-xl-base-1.0", 
    "steps": 20
  }'

# Check GPU utilization
nvidia-smi  # For RTX 4080
# OR
Activity Monitor -> GPU tab  # For Mac M4

# Verify database connectivity
make db-test

# Run test suite
make test
```

## Success Metrics & Milestones

### Performance Benchmarks

**RTX 4080 Targets**:
- SDXL generation: < 25 seconds per image
- Batch processing: 150+ images per hour
- VRAM utilization: < 14GB for normal operations
- Concurrent experiments: 2-3 simultaneous workflows

**Mac M4 Targets**:  
- SDXL generation: < 30 seconds per image
- Memory efficiency: Leverage 128GB unified memory
- Metal backend optimization active
- Comparable batch processing performance

**System Performance**:
- API response times: < 2 seconds
- Real-time progress updates: < 500ms latency
- Database queries: < 100ms for typical operations
- File storage: Efficient image compression and retrieval

### Quality Gates

**Code Quality**:
- [ ] 80%+ test coverage across all modules
- [ ] Type checking passing with mypy
- [ ] Linting passing with ruff
- [ ] Security scan passing with bandit

**Functionality**:  
- [ ] All experiment types operational
- [ ] Real-time progress tracking working
- [ ] Hardware optimization validated
- [ ] Plugin system extensible

**User Experience**:
- [ ] Intuitive experiment creation workflow
- [ ] Effective result comparison tools  
- [ ] Responsive design working on tablets
- [ ] Comprehensive error handling

This comprehensive plan provides a complete roadmap from initial template setup through production deployment, with clear architectural decisions supporting future extensions for LLM integration, ComfyUI workflows, and video generation capabilities.