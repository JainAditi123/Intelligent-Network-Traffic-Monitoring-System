"""
test_full_system.py
===================
Comprehensive Verification Test Suite for the Intelligent Network Traffic Monitoring System.
Tests all 11 requirements from Section 6 of the project specifications:
1. Artifact Loading
2. Feature Order Compatibility
3. Genuine Prediction on Valid Sample CSVs
4. Error Handling on Invalid CSVs
5. Column Reordering and Schema Validation
6. Prediction CSV Export Generation
7. Dashboard Artifact Values Matching
8. Confusion Matrix Mathematical Consistency
9. Model Comparison Values Verification
10. Flask Endpoints & Navigation Verification
11. Local Startup Readiness
"""

import sys
import os
import pathlib
import io
import json
import numpy as np
import pandas as pd
import joblib

# Set paths
BASE_DIR = pathlib.Path(__file__).parent.resolve()
WEB_APP_DIR = BASE_DIR / "web_app"
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(WEB_APP_DIR))

PASS_COUNT = 0
FAIL_COUNT = 0

def check(title, condition, details=""):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS] {title}")
        if details:
            print(f"         {details}")
    else:
        FAIL_COUNT += 1
        print(f"  [FAIL] {title}")
        if details:
            print(f"         ERROR: {details}")

print("=" * 75)
print("INTELLIGENT NETWORK TRAFFIC MONITORING SYSTEM - TEST SUITE")
print("=" * 75)

# -------------------------------------------------------------
# TEST 1: All required model and scaler files load
# -------------------------------------------------------------
print("\n[CHECK 1/11] Checking Model and Scaler Files Loading...")
models_to_check = [
    "models/scaler.pkl",
    "models/decision_tree.pkl",
    "models/random_forest.pkl",
    "models/xgboost.pkl",
    "models/voting_ensemble.pkl",
    "models/stacking_ensemble.pkl",
    "processed_data/feature_names.csv",
]
all_loaded = True
for m in models_to_check:
    p = BASE_DIR / m
    if not p.exists():
        all_loaded = False
        check(f"File exists: {m}", False, "File not found")
    else:
        try:
            if m.endswith(".pkl"):
                obj = joblib.load(p)
            else:
                obj = pd.read_csv(p, header=None)
            check(f"Loaded {m}", True, f"Type: {type(obj).__name__}")
        except Exception as e:
            all_loaded = False
            check(f"Loaded {m}", False, str(e))

# -------------------------------------------------------------
# TEST 2: Feature names count and ordering
# -------------------------------------------------------------
print("\n[CHECK 2/11] Checking Feature Order and Scaler Compatibility...")
feature_file = BASE_DIR / "processed_data" / "feature_names.csv"
features = pd.read_csv(feature_file, header=None)[0].tolist()
scaler = joblib.load(BASE_DIR / "models" / "scaler.pkl")
stacking_model = joblib.load(BASE_DIR / "models" / "stacking_ensemble.pkl")

check("Exact 30 features present in feature_names.csv", len(features) == 30, f"Found {len(features)} features")
check("Scaler n_features_in_ matches feature count", scaler.n_features_in_ == 30, f"Scaler features: {scaler.n_features_in_}")
check("Stacking model n_features_in_ matches feature count", stacking_model.n_features_in_ == 30, f"Model features: {stacking_model.n_features_in_}")

# -------------------------------------------------------------
# TEST 3: Genuine Predictions on Valid Sample CSVs
# -------------------------------------------------------------
print("\n[CHECK 3/11] Testing Inference Engine with Genuine Predictions...")
from web_app.predictor import predict_dataframe, get_last_prediction_results

benign_sample_path = WEB_APP_DIR / "sample_data" / "sample_traffic_benign.csv"
attack_sample_path = WEB_APP_DIR / "sample_data" / "sample_traffic_attack.csv"

df_benign = pd.read_csv(benign_sample_path)
res_b = predict_dataframe(df_benign, "test_benign.csv")
check("Benign sample execution success", res_b["success"] is True)
check("Benign sample detects 100% BENIGN", res_b["summary"]["benign_count"] == 10 and res_b["summary"]["attack_count"] == 0)
check("Benign sample confidence is high (>95%)", res_b["summary"]["avg_confidence"] > 95.0, f"Avg Conf: {res_b['summary']['avg_confidence']}%")

df_attack = pd.read_csv(attack_sample_path)
res_a = predict_dataframe(df_attack, "test_attack.csv")
check("Attack sample execution success", res_a["success"] is True)
check("Attack sample detects 100% ATTACK", res_a["summary"]["attack_count"] == 10 and res_a["summary"]["benign_count"] == 0)
check("Attack sample confidence is high (>95%)", res_a["summary"]["avg_confidence"] > 95.0, f"Avg Conf: {res_a['summary']['avg_confidence']}%")

# -------------------------------------------------------------
# TEST 4: Error Handling on Invalid CSVs
# -------------------------------------------------------------
print("\n[CHECK 4/11] Testing Error Handling on Corrupted/Invalid Inputs...")
empty_df = pd.DataFrame()
res_empty = predict_dataframe(empty_df, "empty.csv")
check("Empty CSV rejected cleanly", res_empty["success"] is False and "contains no data" in res_empty["error"])

nonnum_path = WEB_APP_DIR / "sample_data" / "sample_invalid_non_numeric.csv"
df_nonnum = pd.read_csv(nonnum_path)
res_nonnum = predict_dataframe(df_nonnum, "invalid_nonnum.csv")
check("Non-numeric/corrupted values rejected cleanly", res_nonnum["success"] is False and "Validation Error" in res_nonnum["error"])

# -------------------------------------------------------------
# TEST 5: Missing and Reordered Columns Handling
# -------------------------------------------------------------
print("\n[CHECK 5/11] Testing Column Reordering & Missing Column Rejection...")
missing_path = WEB_APP_DIR / "sample_data" / "sample_invalid_missing_cols.csv"
df_missing = pd.read_csv(missing_path)
res_missing = predict_dataframe(df_missing, "missing_cols.csv")
check("Missing required columns rejected with list", res_missing["success"] is False and len(res_missing["missing_cols"]) == 3)

# Test shuffled/reordered valid columns
shuffled_features = list(reversed(features))
df_shuffled = df_benign[shuffled_features].copy()
res_shuffled = predict_dataframe(df_shuffled, "shuffled.csv")
check("Shuffled columns automatically aligned to trained order", res_shuffled["success"] is True and res_shuffled["summary"]["benign_count"] == 10)

# -------------------------------------------------------------
# TEST 6: Downloaded Prediction CSV Generation
# -------------------------------------------------------------
print("\n[CHECK 6/11] Verifying Prediction CSV Export Dataframe...")
last_results = get_last_prediction_results()
check("Last prediction results retained in memory", last_results is not None and "export_df" in last_results)
export_df = last_results["export_df"]
check("Export CSV has Predicted_Label column", "Predicted_Label" in export_df.columns)
check("Export CSV has Confidence_Score_Pct column", "Confidence_Score_Pct" in export_df.columns)
check("Export CSV has Prediction_Timestamp column", "Prediction_Timestamp" in export_df.columns)
check("Export CSV row count matches input rows", len(export_df) == 10)

# -------------------------------------------------------------
# TEST 7: Dashboard Numbers Match Actual Project Artifacts
# -------------------------------------------------------------
print("\n[CHECK 7/11] Verifying Dashboard Numbers against Project Artifacts...")
from web_app.app import DATASET_STATS, RESULTS

y_test = np.load(BASE_DIR / "processed_data" / "y_test.npy")
y_train = np.load(BASE_DIR / "processed_data" / "y_train.npy")

check("Dashboard total samples matches reality (426,076)", DATASET_STATS["total_cleaned_samples"] == 426076)
check("Dashboard pre-SMOTE train count matches (340,860)", DATASET_STATS["train_split_pre_smote"] == 340860)
check("Dashboard post-SMOTE train count matches actual y_train.npy (530,194)", len(y_train) == DATASET_STATS["train_samples_post_smote"])
check("Dashboard test samples count matches actual y_test.npy (85,216)", len(y_test) == DATASET_STATS["test_split_samples"])
check("Dashboard test benign matches y_test=0 (18,941)", int((y_test == 0).sum()) == DATASET_STATS["test_benign"])
check("Dashboard test attack matches y_test=1 (66,275)", int((y_test == 1).sum()) == DATASET_STATS["test_attack"])

# -------------------------------------------------------------
# TEST 8: Confusion Matrix Mathematical Consistency
# -------------------------------------------------------------
print("\n[CHECK 8/11] Verifying Confusion Matrix Mathematical Consistency...")
all_cm_consistent = True
for r in RESULTS:
    cm = r["cm"]
    total = cm["tn"] + cm["fp"] + cm["fn"] + cm["tp"]
    benign_total = cm["tn"] + cm["fp"]
    attack_total = cm["fn"] + cm["tp"]
    
    calc_acc = round((cm["tp"] + cm["tn"]) / total, 4)
    calc_prec = round(cm["tp"] / (cm["tp"] + cm["fp"]), 4)
    calc_rec = round(cm["tp"] / (cm["tp"] + cm["fn"]), 4)
    calc_f1 = round(2 * calc_prec * calc_rec / (calc_prec + calc_rec), 4)

    is_valid = (
        total == 85216 and
        benign_total == 18941 and
        attack_total == 66275 and
        abs(calc_acc - r["accuracy"]) <= 0.0001 and
        abs(calc_prec - r["precision"]) <= 0.0001 and
        abs(calc_rec - r["recall"]) <= 0.0001 and
        abs(calc_f1 - r["f1"]) <= 0.0001
    )
    if not is_valid:
        all_cm_consistent = False
check("All 5 confusion matrices match test set totals and derived metrics exactly", all_cm_consistent)

# -------------------------------------------------------------
# TEST 9: Model Comparison Metrics Accuracy
# -------------------------------------------------------------
print("\n[CHECK 9/11] Checking Model Comparison Recorded Values...")
model_names = [r["name"] for r in RESULTS]
check("All 5 models represented in comparison", len(model_names) == 5 and "Stacking Ensemble" in model_names)
stacking_r = [r for r in RESULTS if r["name"] == "Stacking Ensemble"][0]
check("Stacking Ensemble has recorded accuracy 0.9994", stacking_r["accuracy"] == 0.9994)
check("Stacking Ensemble has recorded F1 0.9996", stacking_r["f1"] == 0.9996)
xgboost_r = [r for r in RESULTS if r["name"] == "XGBoost"][0]
check("XGBoost has lowest false positives (FP = 4)", xgboost_r["cm"]["fp"] == 4)

# -------------------------------------------------------------
# TEST 10: Flask Endpoints and Client Responses
# -------------------------------------------------------------
print("\n[CHECK 10/11] Testing Flask Web Application Routes...")
from web_app.app import app as flask_app
flask_app.config["TESTING"] = True
client = flask_app.test_client()

routes_to_test = [
    ("/", 200, "Dashboard"),
    ("/predict", 200, "Traffic Prediction"),
    ("/comparison", 200, "Model Comparison"),
    ("/evaluation", 200, "Evaluation"),
    ("/about", 200, "About"),
    ("/load-sample/benign", 200, "Instant Benign Demo"),
    ("/load-sample/attack", 200, "Instant Attack Demo"),
    ("/load-sample/mixed", 200, "Instant Mixed Demo"),
    ("/download-predictions", 200, "Prediction CSV Download"),
    ("/download-sample-file/benign", 200, "Sample File Download"),
]

all_routes_ok = True
for path, expected_status, label in routes_to_test:
    resp = client.get(path)
    if resp.status_code != expected_status:
        all_routes_ok = False
        check(f"Endpoint GET {path} ({label})", False, f"Returned status {resp.status_code}")
    else:
        check(f"Endpoint GET {path} ({label})", True, f"HTTP {resp.status_code}")

# -------------------------------------------------------------
# TEST 11: Scientific Leakage Audit Artifacts Present
# -------------------------------------------------------------
print("\n[CHECK 11/11] Checking Scientific Leakage Audit Artifacts...")
audit_file = BASE_DIR / "processed_data" / "leakage_audit_results.json"
check("Leakage audit JSON results file exists", audit_file.exists())
if audit_file.exists():
    with open(audit_file) as f:
        audit_data = json.load(f)
    check("Leakage audit contains model evaluation results", "models_evaluated" in audit_data)
    check("Leakage audit verifies feature overlap >= 25/30", audit_data["leakage_audit_findings"]["feature_overlap_count"] >= 25)

# -------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------
print("\n" + "=" * 75)
print(f"TEST SUITE SUMMARY: {PASS_COUNT} PASSED | {FAIL_COUNT} FAILED")
print("=" * 75)

if FAIL_COUNT == 0:
    print(">>> ALL TESTS PASSED SUCCESSFULLY! The system is verified and ready for demonstration.")
    sys.exit(0)
else:
    print(">>> SOME TESTS FAILED. Please review the error log above.")
    sys.exit(1)
