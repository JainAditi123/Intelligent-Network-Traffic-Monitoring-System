import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# ============================================================
# INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM
# STEP 5 - TRAIN / TEST SPLIT + SMOTE
# ============================================================

INPUT_FILE = "processed_data/feature_selected_dataset.parquet"

print("=" * 70)
print("TRAIN / TEST SPLIT AND CLASS BALANCING")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

df = pd.read_parquet(INPUT_FILE)

print("\nDataset shape:", df.shape)

# ------------------------------------------------------------
# 2. Separate features and target
# ------------------------------------------------------------

feature_columns = [
    col for col in df.columns
    if col not in ["Label", "Binary_Label"]
]

X = df[feature_columns]
y = df["Binary_Label"]

print("Number of features:", X.shape[1])

# ------------------------------------------------------------
# 3. Convert to numeric
# ------------------------------------------------------------

X = X.apply(pd.to_numeric, errors="coerce")

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

# ------------------------------------------------------------
# 4. Encode target
# ------------------------------------------------------------

y = y.map({
    "BENIGN": 0,
    "ATTACK": 1
})

print("\nTarget classes:")
print("0 = BENIGN")
print("1 = ATTACK")

# ------------------------------------------------------------
# 5. Original class distribution
# ------------------------------------------------------------

print("\nOriginal class distribution:")
print(y.value_counts())

# ------------------------------------------------------------
# 6. Train/Test Split
# ------------------------------------------------------------

print("\nCreating 80/20 stratified split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])

print("\nTraining distribution BEFORE SMOTE:")
print(y_train.value_counts())

print("\nTesting distribution:")
print(y_test.value_counts())

# ------------------------------------------------------------
# 7. Feature Scaling
# ------------------------------------------------------------

print("\nApplying StandardScaler...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------
# Save the fitted scaler so it can be reused at inference time
# without needing to re-fit on new data.
# Load later with: scaler = joblib.load("models/scaler.pkl")
# ----------------------------------------------------------

import joblib as _joblib

os.makedirs("models", exist_ok=True)

_joblib.dump(scaler, "models/scaler.pkl")

print("Scaler saved to models/scaler.pkl")

# ------------------------------------------------------------
# 8. SMOTE - TRAINING DATA ONLY
# ------------------------------------------------------------

print("\nApplying SMOTE to training data...")

smote = SMOTE(
    random_state=42
)

X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("\nTraining distribution AFTER SMOTE:")
print(pd.Series(y_train_balanced).value_counts())

# ------------------------------------------------------------
# 9. Create processed_data directory
# ------------------------------------------------------------

os.makedirs("processed_data", exist_ok=True)

# ------------------------------------------------------------
# 10. Save arrays
# ------------------------------------------------------------

np.save(
    "processed_data/X_train.npy",
    X_train_balanced
)

np.save(
    "processed_data/X_test.npy",
    X_test_scaled
)

np.save(
    "processed_data/y_train.npy",
    y_train_balanced
)

np.save(
    "processed_data/y_test.npy",
    y_test
)

# Save feature names (header=False avoids a spurious '0' column header row)
pd.Series(feature_columns).to_csv(
    "processed_data/feature_names.csv",
    index=False,
    header=False
)

print("\nSaved files:")
print("processed_data/X_train.npy")
print("processed_data/X_test.npy")
print("processed_data/y_train.npy")
print("processed_data/y_test.npy")
print("processed_data/feature_names.csv")

print("\n" + "=" * 70)
print("TRAIN / TEST PREPARATION COMPLETED")
print("=" * 70)