#!/usr/bin/env python
"""Get Simulated Annealing metrics for table entries."""
from __future__ import annotations

import os
import sys

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from environment import Environment
from search import search
from fuzzy import FuzzyRisk
from ml_model import MLModel

def test_simulated_annealing():
    """Test Simulated Annealing algorithm."""
    print("=" * 80)
    print("SIMULATED ANNEALING - METRICS FOR TABLE ENTRY")
    print("=" * 80)
    print()
    
    env = Environment("A")
    ml_model = MLModel()
    fuzzy = FuzzyRisk()
    
    start = env.ambulances[0].pos  # (0, 9)
    goal = env.victims[0].pos      # (1, 2)
    
    print(f"Start: {start}, Goal: {goal}")
    print()
    
    # Run simulated annealing with different temperatures
    configs = [
        {"temperature": 1.0, "cooling_rate": 0.995, "max_iterations": 1000, "label": "Default (T=1.0)"},
        {"temperature": 0.5, "cooling_rate": 0.99, "max_iterations": 1000, "label": "Low Temp (T=0.5)"},
        {"temperature": 2.0, "cooling_rate": 0.995, "max_iterations": 500, "label": "High Temp (T=2.0)"},
    ]
    
    alpha = 1.0
    
    for config in configs:
        label = config.pop("label")
        try:
            result = search(env, start, goal, "simulated_annealing", ml_model, fuzzy, alpha, algorithm_params=config)
            print(f"\n{label}:")
            print(f"  Path Length: {len(result.path)}")
            print(f"  Path Cost: {result.total_cost:.2f}")
            print(f"  Nodes Expanded: {result.nodes_expanded}")
            print(f"  Risk Score: {result.risk_score:.4f}")
            print(f"  Optimality Ratio: {result.optimality_ratio:.4f}")
            print(f"  Runtime: {result.runtime_sec:.4f} seconds")
            print()
        except Exception as e:
            print(f"{label}: ERROR - {e}")
            print()

if __name__ == "__main__":
    test_simulated_annealing()
