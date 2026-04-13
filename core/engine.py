"""Engine update for advanced KPI calculation."""

import numpy as np
from typing import Dict, List
from core.models import FacilityResults, SimulationOutput
from core.constants import FACILITIES, DEFAULT_NUM_USERS, DEFAULT_TIME_STEPS, DEFAULT_SERVICE_RATE
from core.ai_prediction import predict_crowd_peak_vertex_ai, generate_dynamic_threshold_ai

class CrowdSimulationEngine:
    """Simulation engine with enhanced metric tracking."""

    def __init__(self, 
                 num_users: int = DEFAULT_NUM_USERS, 
                 time_steps: int = DEFAULT_TIME_STEPS, 
                 service_rate: float = DEFAULT_SERVICE_RATE):
        """Initializes with performance-hardened parameters."""
        self.num_users = max(1, min(int(num_users), 10000))
        self.time_steps = max(1, int(time_steps))
        self.service_rate = max(0.01, float(service_rate))

    def run_baseline(self) -> SimulationOutput:
        """Baseline simulation with high peak intensity."""
        all_intents: Dict[str, np.ndarray] = {}
        for facility in FACILITIES:
            peak = self.time_steps - 5 if "Exit" in facility else self.time_steps // 2
            std_dev = 3 if "Exit" in facility else 5
            intents = np.random.normal(loc=peak, scale=std_dev, size=self.num_users // len(FACILITIES))
            all_intents[facility] = np.clip(intents, 0, self.time_steps - 1).astype(int)
        
        return self._simulate(all_intents, "Baseline")

    def run_optimized(self) -> SimulationOutput:
        """FlowSync simulation with predictive smoothing logic."""
        all_final_actions: Dict[str, np.ndarray] = {}
        for facility in FACILITIES:
            # MOCK: Use Vertex AI for predicting the peak time
            historical_data = [10.0, 20.0, 30.0]
            peak = predict_crowd_peak_vertex_ai(historical_data) if "Exit" not in facility else self.time_steps - 5
            std_dev = 3 if "Exit" in facility else 5
            intents = np.sort(np.clip(np.random.normal(loc=peak, scale=std_dev, 
                                                    size=self.num_users // len(FACILITIES)), 
                                    0, self.time_steps - 1).astype(int))
            
            final_actions = np.zeros_like(intents)
            predictive_queue = np.zeros(self.time_steps + 20)
            
            # MOCK: Use GenAI to determine dynamic threshold based on overall service levels
            threshold = generate_dynamic_threshold_ai(congestion_level="High") if "Exit" not in facility else 0.8
            
            for i, start_time in enumerate(intents):
                curr_w = predictive_queue[start_time] / self.service_rate
                future_t = min(start_time + 10, self.time_steps - 1)
                future_w = predictive_queue[future_t] / self.service_rate
                
                actual_t = future_t if future_w < curr_w * threshold else start_time
                final_actions[i] = actual_t
                predictive_queue[actual_t : actual_t + 5] += 1
            
            all_final_actions[facility] = final_actions

        return self._simulate(all_final_actions, "FlowSync")

    def _simulate(self, intents_map: Dict[str, np.ndarray], mode_name: str) -> SimulationOutput:
        """Core simulator with advanced KPI aggregation."""
        results: Dict[str, FacilityResults] = {}
        total_congestion = np.zeros(self.time_steps)
        
        for facility in FACILITIES:
            arrivals = np.bincount(intents_map[facility], minlength=self.time_steps)[:self.time_steps]
            queue_over_time = np.zeros(self.time_steps)
            current_queue = 0.0
            
            for t in range(self.time_steps):
                current_queue += arrivals[t]
                current_queue = max(0.0, current_queue - self.service_rate)
                queue_over_time[t] = current_queue
            
            total_congestion += queue_over_time
            results[facility] = FacilityResults(
                queue_over_time=queue_over_time.tolist(), 
                wait_times=(queue_over_time / self.service_rate).tolist(),
                peak_time=int(np.argmax(queue_over_time))
            )

        all_waits = [w for f in results.values() for w in f.wait_times]
        avg_wait = float(np.mean(all_waits)) if all_waits else 0.0
        
        # User Satisfaction heuristic: 100 minus penalty for waiting
        # penalty = 5 points per minute of wait time
        satisfaction = max(0, min(100, 100 - (avg_wait * 5)))
            
        return SimulationOutput(
            mode=mode_name,
            avg_wait=avg_wait,
            max_queue=float(np.max(total_congestion)),
            peak_congestion_time=int(np.argmax(total_congestion)),
            satisfaction_score=satisfaction,
            data=results,
            time_axis=list(range(self.time_steps))
        )

