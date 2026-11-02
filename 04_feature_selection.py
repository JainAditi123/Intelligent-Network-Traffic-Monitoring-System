import pandas as pd
import numpy as np
import os
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier

# ============================================================
# INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM
# STEP 4 - FEATURE SELECTION
# ============================================================

INPUT_FILE = "processed_data/binary_dataset.parquet"

print("=" * 70)
print("FEATURE SELECTION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

df = pd.read_parquet(INPUT_FILE)

print("\nDataset shape:", df.shape)

# ------------------------------------------------------------
# 2. Separate features and target
# ------------------------------------------------------------

X = df.drop(columns=["Label", "Binary_Label"])
y = df["Binary_Label"]

print("\nOriginal number of features:", X.shape[1])

# ------------------------------------------------------------
# 3. Convert all features to numeric
# ------------------------------------------------------------

X = X.apply(pd.to_numeric, errors="coerce")

# Replace infinity
X = X.replace([np.inf, -np.inf], np.nan)

# Fill missing values
X = X.fillna(0)

# ------------------------------------------------------------
# 4. Remove constant features
# ------------------------------------------------------------

constant_features = [
    col for col in X.columns
    if X[col].nunique() <= 1
]

print("\nConstant features found:", len(constant_features))

if constant_features:
    print("\nRemoving:")
    for col in constant_features:
        print("-", col)

    X = X.drop(columns=constant_features)

print("\nFeatures after constant removal:", X.shape[1])

# ------------------------------------------------------------
# 5. Correlation-based feature removal
# ------------------------------------------------------------

print("\nCalculating correlation matrix...")

correlation_matrix = X.corr().abs()

upper_triangle = correlation_matrix.where(
    np.triu(
        np.ones(correlation_matrix.shape),
        k=1
    ).astype(bool)
)

high_correlation_features = [
    column
    for column in upper_triangle.columns
    if any(upper_triangle[column] > 0.95)
]

print(
    "\nHighly correlated features:",
    len(high_correlation_features)
)

if high_correlation_features:
    print("\nRemoving highly correlated features:")

    for col in high_correlation_features:
        print("-", col)

    X = X.drop(columns=high_correlation_features)

print("\nFeatures after correlation removal:", X.shape[1])

# ------------------------------------------------------------
# 6. Random Forest Feature Importance
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RANDOM FOREST FEATURE IMPORTANCE")
print("=" * 70)

# Convert target to numeric
y_numeric = y.map({
    "BENIGN": 0,
    "ATTACK": 1
})

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

print("\nTraining Random Forest for feature importance...")

rf.fit(X, y_numeric)

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 30 Features:\n")

print(
    importance.head(30).to_string(index=False)
)

# ------------------------------------------------------------
# 7. Select top features
# ------------------------------------------------------------

TOP_N = 30

selected_features = importance.head(TOP_N)["Feature"].tolist()

print("\n" + "=" * 70)
print(f"SELECTED TOP {TOP_N} FEATURES")
print("=" * 70)

for i, feature in enumerate(selected_features, start=1):
    print(f"{i:02d}. {feature}")

# ------------------------------------------------------------
# 8. Create final dataset
# ------------------------------------------------------------

final_df = df[selected_features + ["Label", "Binary_Label"]]

print("\nFinal dataset shape:", final_df.shape)

# ------------------------------------------------------------
# 9. Save feature-selected dataset
# ------------------------------------------------------------

output_file = "processed_data/feature_selected_dataset.parquet"

final_df.to_parquet(
    output_file,
    index=False
)

print("\nSaved file:")
print(output_file)

print("\n" + "=" * 70)
print("FEATURE SELECTION COMPLETED")
print("=" * 70)