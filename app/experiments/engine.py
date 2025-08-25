"""
Experiment execution engine.

Orchestrates the execution of experiments across multiple providers.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any

import structlog

from ..providers import get_provider
from ..providers.base import CompletionRequest
from .models import Experiment
from .models import ExperimentConfig
from .models import ExperimentResult
from .models import ExperimentRun
from .models import ExperimentStatus

logger = structlog.get_logger(__name__)


class ExperimentEngine:
    """
    Engine for executing AI experiments across multiple providers.

    Handles the orchestration, parallel execution, and result aggregation
    of experiments that compare AI providers and models.
    """

    def __init__(self):
        self.active_experiments: dict[str, Experiment] = {}

    async def create_experiment(self, config: ExperimentConfig, created_by: str) -> Experiment:
        """
        Create a new experiment.

        Args:
            config: Experiment configuration
            created_by: User ID who created the experiment

        Returns:
            Created experiment instance
        """
        experiment_id = str(uuid.uuid4())

        experiment = Experiment(
            experiment_id=experiment_id,
            created_by=created_by,
            created_at=datetime.utcnow(),
            config=config,
        )

        self.active_experiments[experiment_id] = experiment

        logger.info(
            "Experiment created",
            experiment_id=experiment_id,
            providers=config.providers,
            test_cases=len(config.test_cases),
        )

        return experiment

    async def run_experiment(self, experiment_id: str) -> ExperimentResult:
        """
        Execute an experiment.

        Args:
            experiment_id: ID of experiment to run

        Returns:
            Experiment results

        Raises:
            KeyError: If experiment not found
            ValueError: If experiment is not in pending status
        """
        experiment = self.active_experiments.get(experiment_id)
        if not experiment:
            raise KeyError(f"Experiment {experiment_id} not found")

        if experiment.status != ExperimentStatus.PENDING:
            raise ValueError(f"Experiment {experiment_id} is not pending (status: {experiment.status})")

        # Update experiment status
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.utcnow()

        logger.info("Starting experiment execution", experiment_id=experiment_id)

        try:
            # Generate all run configurations
            runs = self._generate_runs(experiment.config)

            # Execute runs
            if experiment.config.parallel:
                completed_runs = await self._execute_parallel(runs)
            else:
                completed_runs = await self._execute_sequential(runs)

            # Create result
            result = self._create_result(experiment_id, completed_runs)

            # Update experiment
            experiment.status = ExperimentStatus.COMPLETED
            experiment.completed_at = datetime.utcnow()
            experiment.result = result

            logger.info(
                "Experiment completed",
                experiment_id=experiment_id,
                successful_runs=result.successful_runs,
                failed_runs=result.failed_runs,
            )

            return result

        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.completed_at = datetime.utcnow()
            logger.error("Experiment failed", experiment_id=experiment_id, error=str(e))
            raise

    def _generate_runs(self, config: ExperimentConfig) -> list[ExperimentRun]:
        """Generate all run configurations for the experiment."""
        runs = []

        for test_case_index, test_case_data in enumerate(config.test_cases):
            for provider_name in config.providers:
                models = config.models.get(provider_name, [])
                for model in models:
                    run_id = str(uuid.uuid4())
                    run = ExperimentRun(
                        run_id=run_id,
                        provider=provider_name,
                        model=model,
                        test_case_index=test_case_index,
                        test_case_data=test_case_data,
                        status=ExperimentStatus.PENDING,
                    )
                    runs.append(run)

        return runs

    async def _execute_parallel(self, runs: list[ExperimentRun]) -> list[ExperimentRun]:
        """Execute runs in parallel."""
        tasks = [self._execute_run(run) for run in runs]
        return await asyncio.gather(*tasks, return_exceptions=False)

    async def _execute_sequential(self, runs: list[ExperimentRun]) -> list[ExperimentRun]:
        """Execute runs sequentially."""
        completed_runs = []
        for run in runs:
            completed_run = await self._execute_run(run)
            completed_runs.append(completed_run)
        return completed_runs

    async def _execute_run(self, run: ExperimentRun) -> ExperimentRun:
        """Execute a single experimental run."""
        run.status = ExperimentStatus.RUNNING
        run.started_at = datetime.utcnow()

        try:
            # Get provider
            provider = get_provider(run.provider)
            if not provider:
                raise ValueError(f"Provider {run.provider} not available")

            # Format prompt with test case data
            prompt = self._format_prompt(run.test_case_data)

            # Create completion request
            request = CompletionRequest(
                prompt=prompt,
                model=run.model,
            )

            # Execute completion
            response = await provider.complete(request)

            # Record success
            run.status = ExperimentStatus.COMPLETED
            run.response_text = response.text
            run.usage_stats = response.usage
            run.metadata = response.metadata

        except Exception as e:
            # Record failure
            run.status = ExperimentStatus.FAILED
            run.error_message = str(e)
            logger.error("Run failed", run_id=run.run_id, provider=run.provider, model=run.model, error=str(e))

        finally:
            run.completed_at = datetime.utcnow()
            if run.started_at:
                duration = run.completed_at - run.started_at
                run.duration_ms = int(duration.total_seconds() * 1000)

        return run

    def _format_prompt(self, test_case_data: dict[str, Any]) -> str:
        """Format prompt template with test case variables."""
        # Simple template substitution - could be enhanced with Jinja2
        prompt = self.config.prompt_template
        for key, value in test_case_data.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt

    def _create_result(self, experiment_id: str, runs: list[ExperimentRun]) -> ExperimentResult:
        """Create aggregated result from completed runs."""
        successful_runs = [r for r in runs if r.status == ExperimentStatus.COMPLETED]
        failed_runs = [r for r in runs if r.status == ExperimentStatus.FAILED]

        # Calculate average duration
        durations = [r.duration_ms for r in successful_runs if r.duration_ms]
        avg_duration = sum(durations) / len(durations) if durations else None
        total_duration = sum(durations) if durations else None

        return ExperimentResult(
            experiment_id=experiment_id,
            total_runs=len(runs),
            successful_runs=len(successful_runs),
            failed_runs=len(failed_runs),
            avg_duration_ms=avg_duration,
            total_duration_ms=total_duration,
            runs=runs,
        )


# Global engine instance
_engine = ExperimentEngine()


async def create_experiment(config: ExperimentConfig, created_by: str) -> Experiment:
    """Create a new experiment using the global engine."""
    return await _engine.create_experiment(config, created_by)


async def run_experiment(experiment_id: str) -> ExperimentResult:
    """Run an experiment using the global engine."""
    return await _engine.run_experiment(experiment_id)
