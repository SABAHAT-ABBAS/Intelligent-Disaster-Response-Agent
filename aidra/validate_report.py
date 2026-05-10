#!/usr/bin/env python
"""Validation script to check report claims against actual implementation."""
from __future__ import annotations

import os
import sys
import json

# Add src to path
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from environment import Environment, CellType
from search import search, manhattan, _run_search_core
from csp import solve_csp, compare_backtracks
from fuzzy import FuzzyRisk
from ml_model import MLModel
import numpy as np

def test_environment():
    """Test environment configuration."""
    print("=" * 80)
    print("ENVIRONMENT VALIDATION")
    print("=" * 80)
    
    env = Environment("A")
    print(f"Grid Size: {env.size}x{env.size}")
    print(f"Medical Centers: {env.med_centers}")
    print(f"Ambulances: {[(a.agent_id, a.pos) for a in env.ambulances]}")
    print(f"Rescue Team: {env.rescue_team.agent_id} at {env.rescue_team.pos}")
    print(f"Medical Kits: {env.medical_kits}")
    print(f"Number of Victims: {len(env.victims)}")
    print(f"Victims: {[(v.victim_id, v.pos, v.severity) for v in env.victims]}")
    
    # Find risk cells
    risk_cells = []
    for i in range(env.size):
        for j in range(env.size):
            if env.grid[i][j] == CellType.RISK:
                risk_cells.append((i, j))
    print(f"Risk Cells: {risk_cells}")
    print()

def test_search_algorithms():
    """Test search algorithms."""
    print("=" * 80)
    print("SEARCH ALGORITHM VALIDATION")
    print("=" * 80)
    
    env = Environment("A")
    ml_model = MLModel()
    fuzzy = FuzzyRisk()
    
    start = env.ambulances[0].pos  # (0, 9)
    goal = env.victims[0].pos  # V1 position
    
    print(f"Start: {start}, Goal: {goal}")
    print()
    
    algorithms = ["bfs", "dfs", "greedy", "astar"]
    alpha = 1.0
    
    results = {}
    for algo in algorithms:
        try:
            result = search(env, start, goal, algo, ml_model, fuzzy, alpha)
            results[algo] = result
            print(f"{algo.upper()}:")
            print(f"  Path Length: {len(result.path)}")
            print(f"  Path Cost: {result.total_cost:.2f}")
            print(f"  Nodes Expanded: {result.nodes_expanded}")
            print(f"  Risk Score: {result.risk_score:.4f}")
            print(f"  Optimality Ratio: {result.optimality_ratio:.4f}")
            print()
        except Exception as e:
            print(f"{algo.upper()}: ERROR - {e}")
            print()
    
    return results

def test_csp_solver():
    """Test CSP solver."""
    print("=" * 80)
    print("CSP SOLVER VALIDATION")
    print("=" * 80)
    
    env = Environment("A")
    ml_model = MLModel()
    
    backtrack_results = compare_backtracks(env)
    
    print("Backtrack Comparisons:")
    for config_name, result in backtrack_results.items():
        print(f"\n{config_name}:")
        print(f"  Backtracks: {result.backtracks}")
        print(f"  Assigned Victims: {len([v for vals in result.assignment.values() for v in vals])}/{len(env.victims)}")
        print(f"  Assignment: {result.assignment}")
        if result.unassigned:
            print(f"  Unassigned: {result.unassigned}")
    print()

def test_ml_models():
    """Test ML models."""
    print("=" * 80)
    print("ML MODEL VALIDATION")
    print("=" * 80)
    
    ml_model = MLModel()
    
    # Get metrics if available
    if ml_model.metrics:
        print("Model Metrics:")
        for task, models_results in ml_model.metrics.items():
            print(f"\n{task.upper()}:")
            for model_name, report in models_results.items():
                print(f"  {model_name}:")
                print(f"    Accuracy: {report.accuracy:.4f}")
                print(f"    Precision: {report.precision:.4f}")
                print(f"    Recall: {report.recall:.4f}")
                print(f"    F1: {report.f1:.4f}")
                print(f"    Confusion: {report.confusion}")
    else:
        print("No metrics available - models may be in fallback mode or not trained")
    
    # Test predictions
    print("\nModel Predictions:")
    test_features = [1.0, 0.5, 0.3, 2.0]  # [severity, distance, area_risk, time_since]
    survival_prob = ml_model.predict_survival(test_features)
    risk_level = ml_model.predict_risk(test_features)
    print(f"  Test Features: {test_features}")
    print(f"  Survival Probability: {survival_prob:.4f}")
    print(f"  Risk Level: {risk_level:.4f}")
    print()

def test_fuzzy_logic():
    """Test Fuzzy Logic."""
    print("=" * 80)
    print("FUZZY LOGIC VALIDATION")
    print("=" * 80)
    
    fuzzy = FuzzyRisk()
    
    test_cases = [
        (0.1, 0.1, "Low blockage, slow spread"),
        (0.5, 0.5, "Medium blockage, medium spread"),
        (0.9, 0.9, "High blockage, fast spread"),
    ]
    
    print("Fuzzy Risk Weights:")
    for block_prob, hazard_rate, label in test_cases:
        weight = fuzzy.compute_risk_weight(block_prob, hazard_rate)
        print(f"  {label}: {weight:.4f}")
    print()

def test_dataset():
    """Test dataset loading."""
    print("=" * 80)
    print("DATASET VALIDATION")
    print("=" * 80)
    
    ml_model = MLModel()
    
    try:
        rows = ml_model._load_dataset_rows()
        print(f"Dataset Rows: {len(rows)}")
        print(f"Dataset Columns: {list(rows[0].keys()) if rows else 'N/A'}")
        
        # Generate features
        X, y_survival, y_risk, feature_rows = ml_model._generate_dataset(rows)
        print(f"Feature Matrix Shape: {X.shape}")
        print(f"Survival Labels Shape: {y_survival.shape}")
        print(f"Risk Labels Shape: {y_risk.shape}")
        
        # Class distribution
        unique_survival, counts_survival = np.unique(y_survival, return_counts=True)
        unique_risk, counts_risk = np.unique(y_risk, return_counts=True)
        
        print(f"\nSurvival Label Distribution:")
        for label, count in zip(unique_survival, counts_survival):
            print(f"  Class {label}: {count} ({100*count/len(y_survival):.2f}%)")
        
        print(f"\nRisk Label Distribution:")
        for label, count in zip(unique_risk, counts_risk):
            print(f"  Class {label}: {count} ({100*count/len(y_risk):.2f}%)")
        
        print(f"\nFeature Statistics:")
        for i, feature_name in enumerate(['severity', 'distance', 'area_risk', 'time_since']):
            print(f"  {feature_name}: min={X[:, i].min():.4f}, max={X[:, i].max():.4f}, mean={X[:, i].mean():.4f}")
        
    except Exception as e:
        print(f"Dataset loading error: {e}")
    print()

if __name__ == "__main__":
    test_environment()
    test_search_algorithms()
    test_csp_solver()
    test_ml_models()
    test_fuzzy_logic()
    test_dataset()
    
    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
