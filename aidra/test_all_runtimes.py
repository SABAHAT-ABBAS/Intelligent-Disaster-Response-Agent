#!/usr/bin/env python
"""Get runtime metrics for all search algorithms."""
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

def test_all_runtimes():
    """Test runtime for all algorithms."""
    print("=" * 100)
    print("SEARCH ALGORITHM RUNTIMES - COMPREHENSIVE COMPARISON")
    print("=" * 100)
    print()
    
    env = Environment("A")
    ml_model = MLModel()
    fuzzy = FuzzyRisk()
    
    start = env.ambulances[0].pos  # (0, 9)
    goal = env.victims[0].pos      # (1, 2)
    
    print(f"Start: {start}, Goal: {goal}")
    print(f"Grid Size: {env.size}×{env.size} = {env.size**2} cells")
    print()
    
    algorithms = ["bfs", "dfs", "greedy", "astar"]
    alpha = 1.0
    
    results = {}
    print("=" * 100)
    print("INDIVIDUAL ALGORITHM RESULTS")
    print("=" * 100)
    print()
    
    for algo in algorithms:
        try:
            result = search(env, start, goal, algo, ml_model, fuzzy, alpha)
            results[algo] = result
            print(f"{algo.upper()}:")
            print(f"  Path Length: {len(result.path)}")
            print(f"  Path Cost: {result.total_cost:.4f}")
            print(f"  Nodes Expanded: {result.nodes_expanded}")
            print(f"  Risk Score: {result.risk_score:.4f}")
            print(f"  Runtime: {result.runtime_sec:.6f} seconds ({result.runtime_sec*1000:.4f} ms)")
            print(f"  Optimality Ratio: {result.optimality_ratio:.4f}")
            print()
        except Exception as e:
            print(f"{algo.upper()}: ERROR - {e}")
            print()
    
    # Simulated Annealing with multiple configurations
    print("=" * 100)
    print("SIMULATED ANNEALING VARIANTS")
    print("=" * 100)
    print()
    
    sa_configs = [
        {"temperature": 1.0, "cooling_rate": 0.995, "max_iterations": 100, "label": "SA (100 iter)"},
        {"temperature": 1.0, "cooling_rate": 0.995, "max_iterations": 500, "label": "SA (500 iter)"},
        {"temperature": 1.0, "cooling_rate": 0.995, "max_iterations": 1000, "label": "SA (1000 iter)"},
    ]
    
    for config in sa_configs:
        label = config.pop("label")
        try:
            result = search(env, start, goal, "simulated_annealing", ml_model, fuzzy, alpha, algorithm_params=config)
            results[label] = result
            print(f"{label}:")
            print(f"  Path Length: {len(result.path)}")
            print(f"  Path Cost: {result.total_cost:.4f}")
            print(f"  Nodes Expanded (cumulative): {result.nodes_expanded}")
            print(f"  Risk Score: {result.risk_score:.4f}")
            print(f"  Runtime: {result.runtime_sec:.6f} seconds ({result.runtime_sec*1000:.4f} ms)")
            print(f"  Optimality Ratio: {result.optimality_ratio:.4f}")
            print()
        except Exception as e:
            print(f"{label}: ERROR - {e}")
            print()
    
    # Summary table
    print("=" * 100)
    print("RUNTIME COMPARISON TABLE")
    print("=" * 100)
    print()
    print(f"{'Algorithm':<25} {'Nodes Exp':<12} {'Path Cost':<12} {'Runtime (s)':<15} {'Runtime (ms)':<12} {'Speed':<12}")
    print("-" * 100)
    
    baseline_runtime = results.get("astar", None).runtime_sec if "astar" in results else 1.0
    
    for algo in algorithms:
        if algo in results:
            result = results[algo]
            speedup = baseline_runtime / result.runtime_sec if result.runtime_sec > 0 else 0
            print(f"{algo.upper():<25} {result.nodes_expanded:<12} {result.total_cost:<12.4f} {result.runtime_sec:<15.6f} {result.runtime_sec*1000:<12.4f} {speedup:>10.2f}x")
    
    print()
    print("Simulated Annealing Variants:")
    for algo in ["SA (100 iter)", "SA (500 iter)", "SA (1000 iter)"]:
        if algo in results:
            result = results[algo]
            speedup = baseline_runtime / result.runtime_sec if result.runtime_sec > 0 else 0
            print(f"{algo:<25} {result.nodes_expanded:<12} {result.total_cost:<12.4f} {result.runtime_sec:<15.6f} {result.runtime_sec*1000:<12.4f} {speedup:>10.2f}x")
    
    print()
    print("=" * 100)
    print("KEY OBSERVATIONS")
    print("=" * 100)
    print()
    
    # Find fastest
    fastest_algo = min(algorithms, key=lambda a: results[a].runtime_sec)
    fastest_time = results[fastest_algo].runtime_sec
    print(f"Fastest Algorithm: {fastest_algo.upper()} ({fastest_time*1000:.4f} ms)")
    
    # Find slowest among standard algorithms
    slowest_algo = max(algorithms, key=lambda a: results[a].runtime_sec)
    slowest_time = results[slowest_algo].runtime_sec
    print(f"Slowest Algorithm (standard): {slowest_algo.upper()} ({slowest_time*1000:.4f} ms)")
    
    # SA slowest
    sa_slowest = max(["SA (100 iter)", "SA (500 iter)", "SA (1000 iter)"], 
                     key=lambda a: results[a].runtime_sec if a in results else 0)
    if sa_slowest in results:
        print(f"Slowest Algorithm (with SA): {sa_slowest} ({results[sa_slowest].runtime_sec*1000:.4f} ms)")
    
    # Ratio
    ratio = slowest_time / fastest_time
    print(f"\nSlowest/Fastest Ratio: {ratio:.2f}x")
    
    if "SA (1000 iter)" in results:
        sa_ratio = results["SA (1000 iter)"].runtime_sec / fastest_time
        print(f"SA(1000) / Fastest: {sa_ratio:.2f}x")

if __name__ == "__main__":
    test_all_runtimes()
