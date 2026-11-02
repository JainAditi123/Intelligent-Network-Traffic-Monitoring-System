import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("=" * 70)
print("RANDOM FOREST - ENSEMBLE MODEL")
print("=" * 70)

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

print("\nLoading prepared data...")

X_train = np.load("processed_data/X_train.npy")
X_test = np.load("processed_data/X_test.npy")
y_train = np.load("processed_data/y_train.npy")
y_test = np.load("processed_data/y_test.npy")

print("X_train shape:", X_train.shape)
print("X_test shape :", X_test.shape)

# --------------------------------------------------
# 2. CREATE RANDOM FOREST
# --------------------------------------------------

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("Number of trees:", 100)

# --------------------------------------------------
# 3. TRAIN MODEL
# --------------------------------------------------

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

print("Random Forest training completed!")

# --------------------------------------------------
# 4. PREDICTIONS
# --------------------------------------------------

print("\nMaking predictions on test data...")

y_pred = model.predict(X_test)

# --------------------------------------------------
# 5. METRICS
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

# --------------------------------------------------
# 6. DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("RANDOM FOREST RESULTS")
print("=" * 70)

print(f"\nAccuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

# --------------------------------------------------
# 7. CONFUSION MATRIX
# --------------------------------------------------

print("\nConfusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)

print("\nClass labels:")
print("0 = BENIGN")
print("1 = ATTACK")

# --------------------------------------------------
# 8. CLASSIFICATION REPORT
# --------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["BENIGN", "ATTACK"],
        zero_division=0
    )
)

# --------------------------------------------------
# 9. SAVE MODEL
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

model_path = "models/random_forest.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully:")
print(model_path)

print("\n" + "=" * 70)
print("RANDOM FOREST TRAINING COMPLETED")
print("=" * 70)