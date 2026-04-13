"""Unit tests for the FlowSync simulation engine."""

import pytest
import numpy as np
from core.engine import CrowdSimulationEngine
from core.models import SimulationOutput

def test_engine_initialization_validation():
    """Verifies that the engine sanitizes and bounds-checks user inputs."""
    engine = CrowdSimulationEngine(num_users=20000)
    assert engine.num_users == 10000
    
    engine = CrowdSimulationEngine(num_users=-500)
    assert engine.num_users == 1
    
    engine = CrowdSimulationEngine(service_rate=0)
    assert engine.service_rate == 0.01

def test_baseline_run_valid_output():
    """Ensures that a baseline run returns a structured SimulationOutput."""
    engine = CrowdSimulationEngine(num_users=100)
    output = engine.run_baseline()
    
    assert isinstance(output, SimulationOutput)
    assert output.mode == "Baseline"
    assert len(output.data) > 0
    assert output.avg_wait >= 0
    assert output.satisfaction_score >= 0 and output.satisfaction_score <= 100
    assert output.peak_congestion_time >= 0

def test_optimized_run_valid_output():
    """Ensures that an optimized run returns a structured SimulationOutput."""
    engine = CrowdSimulationEngine(num_users=100)
    output = engine.run_optimized()
    
    assert isinstance(output, SimulationOutput)
    assert output.mode == "FlowSync"
    assert output.avg_wait >= 0

def test_simulation_queue_logic():
    """Verifies the accuracy of the O(N) queue calculation logic."""
    engine = CrowdSimulationEngine(num_users=10, time_steps=10, service_rate=1.0)
    
    intents = {
        "Food 🍔": np.array([2, 2, 2, 2, 2]),
        "Restroom 🚻": np.array([2]),
        "Exit 🚪": np.array([2])
    }
    
    output = engine._simulate(intents, "TestMode")
    
    food_queues = output.data["Food 🍔"].queue_over_time
    assert food_queues[2] == 4.0
    assert food_queues[3] == 3.0
    assert food_queues[6] == 0.0

def test_flowsync_decision_logic():
    """Tests that FlowSync correctly shifts actions for skewed distributions."""
    engine = CrowdSimulationEngine(num_users=30, service_rate=0.5)
    base = engine.run_baseline()
    opt = engine.run_optimized()
    assert opt.avg_wait <= base.avg_wait or opt.max_queue <= base.max_queue

def test_edge_case_zero_users():
    """Tests that the simulation handles zero population gracefully."""
    engine = CrowdSimulationEngine(num_users=0)
    output = engine.run_baseline()
    assert output.avg_wait >= 0
    assert output.max_queue >= 0

def test_high_service_rate():
    """Tests that high service capacity results in near-zero wait times."""
    engine = CrowdSimulationEngine(num_users=10, service_rate=100.0)
    output = engine.run_baseline()
    assert output.avg_wait == 0.0
    assert output.max_queue == 0.0
