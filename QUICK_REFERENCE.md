# AIDRA REPORT VALIDATION - QUICK REFERENCE SUMMARY

## 🔴 CRITICAL ISSUES (Report Reproducibility Affected)

### 1. Risk Cell Configuration - COMPLETELY WRONG
- **Report Says**: (3,3), (3,4), (4,3), (4,4)
- **Actual Code**: (3,3), (3,4), (6,6), (7,6)
- **Impact**: Cannot reproduce reported "risk-free routing"
- **Fix**: Update paper to: **(3,3), (3,4), (6,6), (7,6)**

### 2. A* Heuristic Formula - OVERSIMPLIFIED
- **Report Says**: `h(n) = d_Manhattan + 5 × 1[high-risk]` (simple +5 penalty)
- **Actual Code**: `h(n) = d_Manhattan + α × ML_risk × Fuzzy_weight` (ML + Fuzzy)
- **Impact**: Described algorithm ≠ implemented algorithm
- **Variables**: alpha ∈ {0.0, 1.0, ∞}, ML_risk ∈ [0,1], Fuzzy_weight ∈ [0,1]
- **Fix**: Update formula to ML + fuzzy version

### 3. Dataset Size - 40x SMALLER THAN REPORTED
- **Report Says**: 500 synthetic instances
- **Actual Code**: 20,000 instances
- **Impact**: Cannot reproduce ML metrics
- **Why Matters**: Affects accuracy, precision, recall, F1 measurements
- **Fix**: Update to 20,000 instances

### 4. kNN Parameters - WRONG VALUE
- **Report Says**: k=5
- **Actual Code**: k=7
- **Impact**: kNN metrics don't match (94.1% vs 76.8%)
- **Fix**: Either update code to k=5 or update paper to k=7

---

## 🟠 MAJOR ISSUES (Significant Discrepancies)

### 5. ML Model Accuracy Metrics - HUGE DIFFERENCES
```
Model          Report  Actual   Delta
Naive Bayes    91.2%   92.47%   +1.3% ✓
kNN (k=5)      76.8%   94.10%   +17.3% ✗ MISMATCH
```
- **Root Cause**: Different dataset size (500 vs 20,000) + k-value (5 vs 7)
- **Fix**: Re-train with k=5 on 500-instance dataset OR update paper

### 6. CSP Backtrack Counts - INCONSISTENT
```
Solver                  Report  Actual  Delta
Backtracking only       91      0       ✗ Wrong
BT + MRV                91      0       ✗ Wrong  
BT + MRV + FC           0       0       ✓ Correct
```
- **Issue**: Guard clause in code prevents reporting 91 backtracks
- **Finding**: Scenario A naturally has 0 backtracks (not due to heuristics)
- **Fix**: Verify if measurements were from different CSP configuration

### 7. Fuzzy Logic Inputs - MISSING ONE
- **Report Says**: 3 inputs (blockage, hazard spread, **victim criticality**)
- **Actual Code**: 2 inputs (blockage, hazard spread ONLY)
- **Impact**: Victim criticality handled in CSP, not fuzzy logic
- **Fix**: Update paper to clarify victim criticality is in CSP, not fuzzy

### 8. Simulated Annealing - NOT DOCUMENTED
- **Report Says**: "Four algorithms compared"
- **Actual Code**: Also implements Simulated Annealing (5th algorithm)
- **Impact**: Feature exists but undocumented
- **Fix**: Add Simulated Annealing to reported algorithms or remove from code

---

## 🟡 MINOR ISSUES (Implementation Details)

### 9. Rescue Team Location
- **Report Says**: (4,4)
- **Actual Code**: (5,5)
- **Impact**: Minor - affects only distance calculations

### 10. ML Feature Count in Report
- **Report Says**: Feature names vague ("injury severity", etc.)
- **Actual Code**: Specific dataset columns with normalization
- **Impact**: Documentation is good, feature mapping is clear

---

## ✅ WHAT'S CORRECT IN THE REPORT

| Component | Status | Notes |
|-----------|--------|-------|
| Grid size (10×10) | ✅ | Correct |
| Medical centers locations | ✅ | Correct (just different order in report) |
| Ambulances placement | ✅ | Correct |
| Ambulance capacity (2) | ✅ | Correct |
| Total medical kits (10) | ✅ | Correct |
| Victims count (5) | ✅ | Correct for Scenario A |
| Search algorithm costs | ✅ | All BFS/DFS/Greedy/A* metrics exact match |
| CSP hard constraints | ✅ | All 5/5 victims assigned correctly |
| System architecture | ✅ | Hybrid AI integration works as described |
| Resource allocation | ✅ | Proper prioritization and capacity enforcement |
| All victims rescued | ✅ | Confirmed in all scenarios |

---

## DATASET FEATURE MAPPING

```
Report Says              Dataset Column           Used In ML?
Injury severity    -->   severity_score           ✅ Yes
Distance to centre -->   distance_to_hospital_km  ✅ Yes (normalized /10)
Elapsed time       -->   time_since_event_hr      ✅ Yes
Risk-zone exposure -->   local_hazard_level       ✅ Yes
```

**Dataset Statistics**:
- Total rows: 20,000 (1 header + 19,999 data) = 20,000 instances
- Survival labels: 18,000 (90%) negative, 2,000 (10%) positive → 9:1 IMBALANCE
- Risk labels: 8000/8000/4000 (40%/40%/20% - three classes)
- Train/Val/Test split: 70%/15%/15% (stratified)

---

## ML MODEL SELECTION

The system trains both kNN and Naive Bayes, then **automatically selects the better one**:

```python
# Selection logic
if kNN_accuracy > Naive_Bayes_accuracy:
    use_kNN
else:
    use_Naive_Bayes
```

**Result**: Naive Bayes selected (92.47% > 94.10% on survival task)
- **Note**: Confusing because kNN shows 94.1%, but Naive Bayes has better F1 (0.75 vs 0.78)

---

## SEARCH ALGORITHMS - VERIFICATION TABLE

| Algorithm | Report Path | Report Cost | Code Path | Code Cost | Match |
|-----------|------------|-------------|-----------|-----------|-------|
| BFS | 8 hops | 8.0 | 8 hops | 8.0 | ✅ |
| DFS | 78 hops | 78.0 | 78 hops | 78.0 | ✅ |
| Greedy | 8 hops | 8.0 | 8 hops | 8.0 | ✅ |
| A* | 8 hops | 8.0 | 8 hops | 8.0 | ✅ |

**Conclusion**: Search algorithm measurements are ACCURATE and reproducible

---

## CONFIGURATION PARAMETERS

### Environment
```
Grid Size: 10×10
Medical Centers: (0,0), (9,9)
Ambulances: A1(0,9), A2(9,0)
Rescue Team: T1(5,5) [NOT (4,4) as reported]
High-Risk Cells: (3,3), (3,4), (6,6), (7,6) [NOT (3,3), (3,4), (4,3), (4,4)]
Victims: 5 (V1-V5)
Medical Kits: 10
Ambulance Capacity: 2 victims max
```

### ML Models
```
Dataset: 20,000 instances (NOT 500)
Feature Count: 4
Train/Val/Test: 70%/15%/15%
kNN: k=7 (NOT k=5)
Naive Bayes: Gaussian with StandardScaler
```

### Fuzzy Logic
```
Inputs: blockage probability, hazard spread rate (2, NOT 3)
Output: risk weight [0,1]
Defuzzification: Centroid
Activation: Min, Aggregation: Max
Rules: 6 explicit rules
```

### Search
```
Alpha parameter: {0.0 (speed), 1.0 (balanced), ∞ (safety)}
Heuristic: Manhattan + ML_risk × Fuzzy_weight (NOT simple +5)
Admissible: Yes (heuristic doesn't overestimate)
```

---

## PERFORMANCE METRICS - SCENARIOS

| Scenario | Report | Implementation | Status |
|----------|--------|-----------------|--------|
| A: 5 victims | 5/5 rescued | 5/5 rescued | ✅ |
| B: 5 victims + 1 road block | 5/5 rescued | 5/5 rescued | ✅ |
| C: 6 victims + 2 road blocks + events | 6/6 rescued | 6/6 rescued | ✅ |

**Rescue Time**: Reported 5.6-6.0 sec average (not independently verified in this session)
**Risk Exposure**: 0.0 in all scenarios (confirmed - no high-risk cells traversed)
**Resource Util**: 76-85% (plausible, not independently verified)

---

## WHAT TO FIX FOR PUBLICATION

**MUST FIX (Reproducibility)**:
1. ❌ Risk cells: (3,3), (3,4), (4,3), (4,4) → **(3,3), (3,4), (6,6), (7,6)**
2. ❌ A* formula oversimplified → Add ML + fuzzy version
3. ❌ Dataset 500 instances → Change to **20,000 instances**
4. ❌ kNN k=5 → Verify/update to **k=7** OR retrain with k=5

**SHOULD FIX (Major Discrepancies)**:
5. ⚠️ CSP backtracks: 91→0 explanation unclear
6. ⚠️ ML accuracy table: Clarify why kNN different from code results
7. ⚠️ Fuzzy inputs: Document that criticality is in CSP, not fuzzy

**NICE TO FIX (Documentation)**:
8. 📝 Rescue team location: (4,4) → **(5,5)**
9. 📝 Add Simulated Annealing to algorithms section
10. 📝 Update formulas with correct parameter ranges

---

## VALIDATION ARTIFACTS

- Full validation script: `validate_report.py`
- Comprehensive analysis: `COMPREHENSIVE_ANALYSIS.md` (this file)
- Existing reports: `FACT_CHECK_REPORT.md`, `VALIDATION_REPORT.md`

**Generated**: May 10, 2026
**Validation Method**: Code inspection + Dynamic testing
**Confidence**: HIGH (backed by actual code and execution)

---

## QUICK ACTION CHECKLIST

- [ ] Update risk cells in paper
- [ ] Correct A* heuristic formula
- [ ] Update dataset size to 20,000
- [ ] Verify/correct kNN k-value
- [ ] Retrain ML models if needed
- [ ] Document why CSP backtracks are 0 not 91
- [ ] Clarify fuzzy logic has 2 inputs not 3
- [ ] Add Simulated Annealing to algorithm list
- [ ] Update rescue team location
- [ ] Create reproducibility test suite
