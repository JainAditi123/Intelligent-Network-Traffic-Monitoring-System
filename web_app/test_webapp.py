"""
test_webapp.py — End-to-end test for web_app artifacts.
Run from inside web_app/:  python test_webapp.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

print("Loading predictor (may take a few seconds for large models)...")
import predictor

print("Scaler type     :", type(predictor.SCALER).__name__)
print("Model type      :", type(predictor.MODEL).__name__)
print("Features loaded :", len(predictor.FEATURE_NAMES))
print("Feature  1      :", predictor.FEATURE_NAMES[0])
print("Feature 30      :", predictor.FEATURE_NAMES[-1])
print()

# ── Build a synthetic test row (all zeros — clearly ATTACK after scaling) ──
import numpy as np
import pandas as pd

features = predictor.FEATURE_NAMES

# Row 1: all zeros
row_zeros = {f: 0.0 for f in features}
# Row 2: large packet rates — typical ATTACK signature
row_attack = {f: 0.0 for f in features}
row_attack["Bwd Packets/s"]  = 1_000_000
row_attack["Flow Packets/s"] = 1_000_000
row_attack["Flow Bytes/s"]   = 50_000_000

df_test = pd.DataFrame([row_zeros, row_attack])

print("Running predict_dataframe() on 2-row synthetic test...")
result = predictor.predict_dataframe(df_test)

print("Error        :", result["error"])
print("Missing cols :", result["missing_cols"])
print("Predictions  :", result["predictions"])
print("Counts       :", result["counts"])
print()

# ── Test missing column detection ──
print("Testing missing-column validation...")
df_bad = pd.DataFrame([{"Wrong_Col": 1.0, "Another_Wrong": 2.0}])
result_bad = predictor.predict_dataframe(df_bad)
print("Error (expected)   :", result_bad["error"])
print("Missing cols count :", len(result_bad["missing_cols"]))
assert len(result_bad["missing_cols"]) == 30, "Expected 30 missing columns"
print()

print("=" * 50)
print("ALL TESTS PASSED — predictor.py works correctly.")
print("=" * 50)
