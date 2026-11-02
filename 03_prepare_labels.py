import pandas as pd
import os

# ============================================================
# INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM
# STEP 3 - LABEL PREPARATION
# ============================================================

INPUT_FILE = "processed_data/combined_cleaned.parquet"
OUTPUT_FILE = "processed_data/binary_dataset.parquet"

print("=" * 70)
print("LABEL PREPARATION")
print("=" * 70)

# Load cleaned dataset
df = pd.read_parquet(INPUT_FILE)

print("\nOriginal dataset shape:", df.shape)

# ------------------------------------------------------------
# Create Binary Label
# ------------------------------------------------------------

df["Binary_Label"] = df["Label"].apply(
    lambda x: "BENIGN" if str(x).lower() == "benign" else "ATTACK"
)

# ------------------------------------------------------------
# Display distribution
# ------------------------------------------------------------

print("\nBinary Label Distribution:")
print(df["Binary_Label"].value_counts())

print("\nBinary Label Percentage:")
print(
    df["Binary_Label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# ------------------------------------------------------------
# Save dataset
# ------------------------------------------------------------

df.to_parquet(OUTPUT_FILE, index=False)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("LABEL PREPARATION COMPLETED")
print("=" * 70)