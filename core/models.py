"""Data models for advanced simulation metrics."""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class FacilityResults:
    """Stores detailed metrics for a single facility."""
    queue_over_time: List[float]
    wait_times: List[float]
    peak_time: int  # The minute of maximum congestion

@dataclass
class SimulationOutput:
    """Stores the complete output of a simulation run with advanced KPIs."""
    mode: str
    avg_wait: float
    max_queue: float
    peak_congestion_time: int
    satisfaction_score: float  # 0 to 100
    data: Dict[str, FacilityResults]
    time_axis: List[int]
