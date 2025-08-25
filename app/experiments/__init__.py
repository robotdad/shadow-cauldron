"""
Experiments Brick

PUBLIC CONTRACT:
- ExperimentEngine: Main experiment orchestration
- Experiment: Experiment model
- ExperimentRun: Individual run model
- create_experiment(): Factory function
- run_experiment(): Execution function

RESPONSIBILITIES:
- Experiment design and configuration
- Multi-provider parallel execution
- Result comparison and analysis
- Experiment tracking and history
"""

from .engine import ExperimentEngine
from .engine import create_experiment
from .engine import run_experiment
from .models import Experiment
from .models import ExperimentRun

__all__ = ["ExperimentEngine", "Experiment", "ExperimentRun", "create_experiment", "run_experiment"]
