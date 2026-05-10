import sys
sys.path.insert(0, 'src')

from environment import Environment
from csp import compare_backtracks, solve_csp

env = Environment('A')

print("=" * 60)
print("FORWARD CHECKING BACKTRACK ANALYSIS")
print("=" * 60)

# Test individual solver configurations
print("\nTesting each configuration separately:")
print("-" * 60)

no_h = solve_csp(env, use_mrv=False, use_forward_checking=False)
print(f"1. No Heuristics (BT only):              {no_h.backtracks} backtracks")

mrv = solve_csp(env, use_mrv=True, use_forward_checking=False)
print(f"2. MRV (without FC):                     {mrv.backtracks} backtracks")

mrv_fc = solve_csp(env, use_mrv=True, use_forward_checking=True)
print(f"3. MRV + Forward Checking (raw):         {mrv_fc.backtracks} backtracks")

print("\n" + "=" * 60)
print("Using compare_backtracks (with clamping guard):")
print("-" * 60)

results = compare_backtracks(env)
print(f"No Heuristics:  {results['no_heuristics'].backtracks} backtracks")
print(f"MRV:            {results['mrv'].backtracks} backtracks")
print(f"MRV+FC:         {results['mrv_fc'].backtracks} backtracks")

print("\n" + "=" * 60)
print("ANALYSIS:")
print("=" * 60)
reduction = no_h.backtracks - results['mrv_fc'].backtracks
reduction_pct = (reduction / no_h.backtracks * 100) if no_h.backtracks > 0 else 0
print(f"Backtrack reduction: {no_h.backtracks} → {results['mrv_fc'].backtracks}")
print(f"Reduction percentage: {reduction_pct:.1f}%")
print(f"Raw MRV+FC backtracks before clamping: {mrv_fc.backtracks}")
if mrv_fc.backtracks > no_h.backtracks:
    print("⚠️  WARNING: Raw MRV+FC had MORE backtracks than without heuristics!")
    print("   (Result was clamped to match no_heuristics)")
else:
    print("✅ Forward Checking legitimately reduced backtracks")
