import pandas as pd
import os

DATASET_PATH = "archive (32)"

print("=" * 60)
print("INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM")
print("=" * 60)

files = os.listdir(DATASET_PATH)

parquet_files = [f for f in files if f.endswith(".parquet")]

print("\nTotal Parquet files:", len(parquet_files))

print("\nFiles:")
for file in parquet_files:
    print("-", file)

print("\n" + "=" * 60)
print("READING FIRST FILE")
print("=" * 60)

first_file = os.path.join(DATASET_PATH, parquet_files[0])

df = pd.read_parquet(first_file)

print("\nFile:", parquet_files[0])
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn names:")
for col in df.columns:
    print(col)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())