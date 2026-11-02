import numpy as np
import os
import joblib

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("=" * 70)
print("XGBOOST - BOOSTING ENSEMBLE MODEL")
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
# 2. CREATE XGBOOST MODEL
# --------------------------------------------------

print("\nCreating XGBoost model...")

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    eval_metric="logloss"
)

print("Number of boosting rounds:", 100)

# --------------------------------------------------
# 3. TRAIN MODEL
# --------------------------------------------------

print("\nTraining XGBoost...")

model.fit(X_train, y_train)

print("XGBoost training completed!")

# --------------------------------------------------
# 4. MAKE PREDICTIONS
# --------------------------------------------------

print("\nMaking predictions on test data...")

y_pred = model.predict(X_test)

# --------------------------------------------------
# 5. CALCULATE METRICS
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
print("XGBOOST RESULTS")
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

model_path = "models/xgboost.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully:")
print(model_path)

print("\n" + "=" * 70)
print("XGBOOST TRAINING COMPLETED")
print("=" * 70)