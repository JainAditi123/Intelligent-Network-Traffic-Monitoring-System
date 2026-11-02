import pandas as pd
import os
import numpy as np

# ============================================================
# INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM
# STEP 2 - DATASET PREPROCESSING
# ============================================================

DATASET_PATH = "archive (32)"

print("=" * 70)
print("DATASET PREPROCESSING")
print("=" * 70)


# ------------------------------------------------------------
# 1. Get all parquet files
# ------------------------------------------------------------

files = [
    f for f in os.listdir(DATASET_PATH)
    if f.endswith(".parquet")
]

print("\nTotal files found:", len(files))


# ------------------------------------------------------------
# 2. Read all parquet files
# ------------------------------------------------------------

dataframes = []

for file in files:

    path = os.path.join(DATASET_PATH, file)

    print(f"\nReading: {file}")

    df_temp = pd.read_parquet(path)

    print("Rows:", len(df_temp))
    print("Columns:", len(df_temp.columns))

    dataframes.append(df_temp)


# ------------------------------------------------------------
# 3. Combine all files
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMBINING DATASETS")
print("=" * 70)

df = pd.concat(dataframes, ignore_index=True)

print("\nCombined dataset shape:")
print(df.shape)


# ------------------------------------------------------------
# 4. Clean column names
# ------------------------------------------------------------

df.columns = df.columns.str.strip()

print("\nColumn names cleaned.")


# ------------------------------------------------------------
# 5. Replace infinite values
# ------------------------------------------------------------

print("\nChecking infinite values...")

numeric_columns = df.select_dtypes(include=np.number).columns

df[numeric_columns] = df[numeric_columns].replace(
    [np.inf, -np.inf],
    np.nan
)


# ------------------------------------------------------------
# 6. Missing value check
# ------------------------------------------------------------

missing_values = df.isnull().sum().sum()

print("Total missing values:", missing_values)


# ------------------------------------------------------------
# 7. Remove missing values
# ------------------------------------------------------------

if missing_values > 0:

    print("Removing missing values...")

    df.dropna(inplace=True)

else:

    print("No missing values found.")


# ------------------------------------------------------------
# 8. Remove duplicate rows
# ------------------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate rows:", duplicates)

if duplicates > 0:

    df.drop_duplicates(inplace=True)

    print("Duplicate rows removed.")

else:

    print("No duplicate rows found.")


# ------------------------------------------------------------
# 9. Check labels
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LABEL DISTRIBUTION")
print("=" * 70)

print(df["Label"].value_counts())


# ------------------------------------------------------------
# 10. Display percentage distribution
# ------------------------------------------------------------

print("\nLabel percentage:")

label_percentage = (
    df["Label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(label_percentage)


# ------------------------------------------------------------
# 11. Final dataset information
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL DATASET")
print("=" * 70)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFinal labels:")
print(df["Label"].unique())


# ------------------------------------------------------------
# 12. Save cleaned dataset
# ------------------------------------------------------------

os.makedirs("processed_data", exist_ok=True)

output_file = "processed_data/combined_cleaned.parquet"

df.to_parquet(output_file, index=False)

print("\nCleaned dataset saved at:")
print(output_file)

print("\n" + "=" * 70)
print("PREPROCESSING COMPLETED")
print("=" * 70)