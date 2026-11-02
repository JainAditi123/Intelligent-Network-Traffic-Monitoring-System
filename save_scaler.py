"""
save_scaler.py — One-time scaler recovery utility
==================================================
The StandardScaler was fit during Step 5 (05_train_test_split.py) but was
not originally saved to disk. This script recovers the identical scaler
by repeating the exact same deterministic steps (same random_state=42,
same stratify=y) on the already-processed feature-selected dataset.

IMPORTANT:
  - This does NOT overwrite X_train.npy, X_test.npy, y_train.npy,
    or y_test.npy.
  - SMOTE is NOT re-run.
  - The saved scaler is mathematically identical to the one used during
    the original training, because the split and scaler fit are fully
    deterministic (random_state=42, same input data).

Usage:
    python save_scaler.py

Output:
    models/scaler.pkl
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "processed_data/feature_selected_dataset.parquet"

print("=" * 70)
print("SCALER RECOVERY UTILITY")
print("=" * 70)

# ----------------------------------------------------------------
# 1. Load the feature-selected dataset (same input as Step 5)
# ----------------------------------------------------------------

print("\nLoading feature-selected dataset...")

df = pd.read_parquet(INPUT_FILE)

print("Dataset shape:", df.shape)

# ----------------------------------------------------------------
# 2. Separate features and target (identical to Step 5)
# ----------------------------------------------------------------

feature_columns = [
    col for col in df.columns
    if col not in ["Label", "Binary_Label"]
]

X = df[feature_columns]
y = df["Binary_Label"]

# ----------------------------------------------------------------
# 3. Convert to numeric and clean (identical to Step 5)
# ----------------------------------------------------------------

X = X.apply(pd.to_numeric, errors="coerce")
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

# ----------------------------------------------------------------
# 4. Encode target (identical to Step 5)
# ----------------------------------------------------------------

y = y.map({"BENIGN": 0, "ATTACK": 1})

# ----------------------------------------------------------------
# 5. Recreate the identical 80/20 stratified split (random_state=42)
# ----------------------------------------------------------------

print("\nRecreating 80/20 stratified split (random_state=42)...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples :", X_train.shape[0])
print("Testing samples  :", X_test.shape[0])

# ----------------------------------------------------------------
# 6. Fit StandardScaler on X_train ONLY (identical to Step 5)
# ----------------------------------------------------------------

print("\nFitting StandardScaler on training data only...")

scaler = StandardScaler()
scaler.fit(X_train)

print("Scaler fitted.")
print("Feature means (first 5):", scaler.mean_[:5].round(4))

# ----------------------------------------------------------------
# 7. Save scaler
# ----------------------------------------------------------------

os.makedirs("models", exist_ok=True)

scaler_path = "models/scaler.pkl"
joblib.dump(scaler, scaler_path)

print(f"\nScaler saved to: {scaler_path}")

# ----------------------------------------------------------------
# 8. Quick sanity check — verify test array is consistent
# ----------------------------------------------------------------

print("\nRunning sanity check against saved X_test.npy...")

X_test_scaled = scaler.transform(X_test)
X_test_saved  = np.load("processed_data/X_test.npy")

max_diff = np.max(np.abs(X_test_scaled - X_test_saved))
print(f"Max absolute difference vs saved X_test.npy: {max_diff:.8f}")

if max_diff < 1e-6:
    print("[PASS] Scaler is IDENTICAL to the one used during original training.")
else:
    print("[WARN] Small numerical difference detected (> 1e-6).")
    print("   This may indicate the input dataset was modified since training.")

print("\n" + "=" * 70)
print("SCALER RECOVERY COMPLETED")
print("=" * 70)
print("""
HOW TO USE THE SAVED SCALER FOR INFERENCE:

    import joblib
    import numpy as np

    # Load scaler and model
    scaler = joblib.load("models/scaler.pkl")
    model  = joblib.load("models/stacking_ensemble.pkl")  # or any model

    # Scale new data (same 30 features, same order as feature_names.csv)
    X_new_scaled = scaler.transform(X_new)

    # Predict: 0 = BENIGN, 1 = ATTACK
    predictions = model.predict(X_new_scaled)
""")
