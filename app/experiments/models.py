"""
Experiment data models.

Defines the structure for experiments, runs, and results.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class ExperimentStatus(str, Enum):
    """Experiment execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExperimentConfig(BaseModel):
    """Configuration for an experiment."""

    # Basic configuration
    name: str = Field(description="Experiment name")
    description: str | None = Field(default=None, description="Experiment description")

    # Prompt configuration
    prompt_template: str = Field(description="Prompt template with variables")
    system_prompt: str | None = Field(default=None, description="System prompt")

    # Provider configuration
    providers: list[str] = Field(description="List of provider names to test")
    models: dict[str, list[str]] = Field(description="Models per provider")

    # Generation parameters
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1)

    # Test data
    test_cases: list[dict[str, Any]] = Field(description="Test case variables")

    # Execution configuration
    parallel: bool = Field(default=True, description="Run providers in parallel")
    max_retries: int = Field(default=3, ge=0, description="Max retries per request")


class ExperimentRun(BaseModel):
    """Individual execution run within an experiment."""

    run_id: str
    provider: str
    model: str
    test_case_index: int
    test_case_data: dict[str, Any]

    # Execution details
    status: ExperimentStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None

    # Results
    response_text: str | None = None
    error_message: str | None = None
    usage_stats: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class ExperimentResult(BaseModel):
    """Aggregated results from an experiment."""

    experiment_id: str
    total_runs: int
    successful_runs: int
    failed_runs: int

    # Performance metrics
    avg_duration_ms: float | None = None
    total_duration_ms: int | None = None

    # Provider comparison
    provider_stats: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # All individual runs
    runs: list[ExperimentRun] = Field(default_factory=list)


class Experiment(BaseModel):
    """Complete experiment definition and state."""

    # Identification
    experiment_id: str
    created_by: str
    created_at: datetime

    # Configuration
    config: ExperimentConfig

    # Execution state
    status: ExperimentStatus = ExperimentStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None

    # Results
    result: ExperimentResult | None = None

    class Config:
        use_enum_values = True
