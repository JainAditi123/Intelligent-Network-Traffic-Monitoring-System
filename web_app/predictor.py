"""
predictor.py
============
Inference Engine for the Intelligent Network Traffic Monitoring System.
Loads all 5 trained models (Decision Tree, Random Forest, XGBoost, Voting, Stacking)
and the fitted StandardScaler. Performs strict schema validation, input preview,
calibrated probability estimation, latency tracking, and session analysis logging.
"""

import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=".*InconsistentVersionWarning.*"
)

import os
import io
import time
import datetime
import pathlib
import numpy as np
import pandas as pd
import joblib

# ── Paths relative to project root ──
_BASE      = pathlib.Path(__file__).parent.parent.resolve()
_MODELS_DIR = _BASE / "models"
_SCALER    = _MODELS_DIR / "scaler.pkl"
_FEATURES  = _BASE / "processed_data" / "feature_names.csv"

_MODEL_FILES = {
    "stacking":      _MODELS_DIR / "stacking_ensemble.pkl",
    "voting":        _MODELS_DIR / "voting_ensemble.pkl",
    "random_forest": _MODELS_DIR / "random_forest.pkl",
    "xgboost":       _MODELS_DIR / "xgboost.pkl",
    "decision_tree": _MODELS_DIR / "decision_tree.pkl",
}

_MODEL_LABELS = {
    "stacking":      "Stacking Ensemble (Recommended)",
    "voting":        "Voting Ensemble (Soft Voting)",
    "random_forest": "Random Forest (Bagging)",
    "xgboost":       "XGBoost (Gradient Boosting)",
    "decision_tree": "Decision Tree (Baseline)",
}

# ── Global Artifact Registry & Load Status ──
LOAD_STATUS = {
    "success": False,
    "models_loaded": {},
    "scaler_loaded": False,
    "features_loaded": False,
    "error_message": None,
    "status_text": "Initializing..."
}

SCALER = None
MODELS = {}
FEATURE_NAMES = []
SESSION_HISTORY = []
LAST_PREDICTION_RESULTS = None


def _initialize_artifacts():
    global SCALER, MODELS, FEATURE_NAMES, LOAD_STATUS
    try:
        # 1. Feature schema
        if not _FEATURES.exists():
            raise FileNotFoundError(f"Missing required feature schema: {_FEATURES}")
        FEATURE_NAMES = pd.read_csv(_FEATURES, header=None)[0].tolist()
        if len(FEATURE_NAMES) != 30:
            raise ValueError(f"Expected 30 features in schema, found {len(FEATURE_NAMES)}")
        LOAD_STATUS["features_loaded"] = True

        # 2. Fitted StandardScaler
        if not _SCALER.exists():
            raise FileNotFoundError(f"Missing fitted scaler: {_SCALER}")
        SCALER = joblib.load(_SCALER)
        if SCALER.n_features_in_ != 30:
            raise ValueError(f"StandardScaler expects {SCALER.n_features_in_} features, expected 30")
        LOAD_STATUS["scaler_loaded"] = True

        # 3. Load all 5 models
        for key, path in _MODEL_FILES.items():
            if not path.exists():
                raise FileNotFoundError(f"Missing model artifact: {path}")
            model = joblib.load(path)
            if model.n_features_in_ != 30:
                raise ValueError(f"Model {key} expects {model.n_features_in_} features, expected 30")
            MODELS[key] = model
            LOAD_STATUS["models_loaded"][key] = _MODEL_LABELS[key]

        LOAD_STATUS["success"] = True
        LOAD_STATUS["status_text"] = "5 Models & Scaler Loaded"
        LOAD_STATUS["error_message"] = None

    except Exception as e:
        LOAD_STATUS["success"] = False
        LOAD_STATUS["error_message"] = str(e)
        LOAD_STATUS["status_text"] = f"Artifact Error: {str(e)}"
        print(f"[ERROR] Failed to load artifacts: {e}")

_initialize_artifacts()


def get_load_status():
    """Return health status of models and scaler."""
    return dict(LOAD_STATUS)


def get_available_models():
    """Return dict of available model keys and user-friendly labels."""
    return dict(_MODEL_LABELS)


def get_feature_names():
    """Return ordered list of 30 required feature names."""
    return list(FEATURE_NAMES)


def get_session_history():
    """Return past analysis sessions in reverse chronological order."""
    return list(reversed(SESSION_HISTORY))


def get_last_prediction_results():
    """Return the most recent prediction results for export."""
    return LAST_PREDICTION_RESULTS


def predict_dataframe(df: pd.DataFrame, filename: str = "uploaded_traffic.csv", model_key: str = "stacking"):
    """
    Validate, preprocess, and predict on an uploaded DataFrame.
    
    Strict validation rules:
    - Rejects missing required columns (does NOT invent features).
    - Checks for invalid, non-numeric, or missing values in required columns.
    - Strictly maps to the exact 30 features in trained order.
    - Applies fitted StandardScaler.
    - Computes real predictions (BENIGN / ATTACK) and calibrated confidence scores
      via the selected model's probability output.
    - Tracks precise inference latency.
    """
    global LAST_PREDICTION_RESULTS
    t_start = time.perf_counter()

    if not LOAD_STATUS["success"]:
        return {
            "success": False,
            "error": f"Backend Error: ML models or scaler are not loaded. {LOAD_STATUS['error_message']}",
            "missing_cols": [],
            "records": [],
            "summary": {}
        }

    if df is None or df.empty:
        return {
            "success": False,
            "error": "The uploaded CSV file contains no data rows.",
            "missing_cols": [],
            "records": [],
            "summary": {}
        }

    # Normalize model selection
    if model_key not in MODELS:
        model_key = "stacking"
    active_model = MODELS[model_key]
    model_name = _MODEL_LABELS[model_key]

    # Strip column whitespaces
    df.columns = df.columns.str.strip()

    # 1. Check for missing required columns
    missing_cols = [c for c in FEATURE_NAMES if c not in df.columns]
    if missing_cols:
        return {
            "success": False,
            "error": (
                f"Feature Schema Mismatch: {len(missing_cols)} of 30 required columns are missing. "
                "The system requires flow statistical features matching the CIC-DDoS2019 dataset schema."
            ),
            "missing_cols": missing_cols,
            "records": [],
            "summary": {}
        }

    # 2. Extract only the 30 features in the exact trained order
    X_raw = df[FEATURE_NAMES].copy()

    # 3. Validate numeric integrity: reject invalid non-numeric/null values
    X_numeric = X_raw.apply(pd.to_numeric, errors="coerce")
    
    nan_mask = X_numeric.isna()
    inf_mask = np.isinf(X_numeric.to_numpy(dtype=float)) if not nan_mask.all().all() else np.zeros(X_numeric.shape, dtype=bool)
    invalid_mask = nan_mask | inf_mask
    
    invalid_cell_count = int(invalid_mask.sum().sum())
    invalid_rows_count = int(invalid_mask.any(axis=1).sum())
    
    if invalid_cell_count > 0:
        bad_cols = [col for col in FEATURE_NAMES if invalid_mask[col].sum() > 0]
        return {
            "success": False,
            "error": (
                f"Data Validation Error: Found {invalid_cell_count} invalid (missing, null, or non-numeric) value(s) "
                f"across {invalid_rows_count} row(s) in column(s): {', '.join(bad_cols[:5])}"
                f"{' and more...' if len(bad_cols) > 5 else ''}. "
                "Rule: Real ML inference requires complete numeric feature values without synthetic substitution."
            ),
            "missing_cols": [],
            "records": [],
            "summary": {}
        }

    # 4. Scale using the fitted StandardScaler (never refit)
    try:
        X_scaled = SCALER.transform(X_numeric)
    except Exception as e:
        return {
            "success": False,
            "error": f"Preprocessing Error during feature scaling: {str(e)}",
            "missing_cols": [],
            "records": [],
            "summary": {}
        }

    # 5. Predict using the selected ML model
    try:
        y_pred = active_model.predict(X_scaled)
        has_proba = hasattr(active_model, "predict_proba")
        y_proba = active_model.predict_proba(X_scaled) if has_proba else None
    except Exception as e:
        return {
            "success": False,
            "error": f"Model Inference Error: {str(e)}",
            "missing_cols": [],
            "records": [],
            "summary": {}
        }

    # Measure exact inference elapsed time
    elapsed_sec = time.perf_counter() - t_start
    processing_time_ms = round(elapsed_sec * 1000.0, 2)
    time_display = f"{processing_time_ms:.1f} ms" if processing_time_ms < 1000 else f"{elapsed_sec:.2f} s"

    # 6. Assemble individual row records with real confidence scores and input preview
    records = []
    total_records = len(df)
    benign_count = int((y_pred == 0).sum())
    attack_count = int((y_pred == 1).sum())
    
    benign_pct = round((benign_count / total_records) * 100.0, 1) if total_records > 0 else 0.0
    attack_pct = round((attack_count / total_records) * 100.0, 1) if total_records > 0 else 0.0

    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    confidences = []
    for i in range(total_records):
        pred_int = int(y_pred[i])
        pred_label = "BENIGN" if pred_int == 0 else "ATTACK"
        
        if y_proba is not None:
            prob_benign = float(y_proba[i][0])
            prob_attack = float(y_proba[i][1])
            conf_score = prob_attack if pred_int == 1 else prob_benign
        else:
            prob_benign = 1.0 if pred_int == 0 else 0.0
            prob_attack = 1.0 if pred_int == 1 else 0.0
            conf_score = 1.0

        conf_pct = round(conf_score * 100.0, 2)
        confidences.append(conf_pct)

        # Contextual input feature preview
        duration = float(X_numeric.iloc[i].get("Flow Duration", 0))
        flow_pkts = float(X_numeric.iloc[i].get("Flow Packets/s", 0))
        flow_bytes = float(X_numeric.iloc[i].get("Flow Bytes/s", 0))
        protocol = int(X_numeric.iloc[i].get("Protocol", 0))
        pkt_len_max = float(X_numeric.iloc[i].get("Packet Length Max", 0))
        fwd_pkts = float(X_numeric.iloc[i].get("Total Fwd Packets", 0))
        bwd_pkts = float(X_numeric.iloc[i].get("Total Backward Packets", 0))

        records.append({
            "row_id": i + 1,
            "prediction": pred_label,
            "is_attack": (pred_int == 1),
            "confidence": conf_pct,
            "benign_prob": round(prob_benign * 100.0, 2),
            "attack_prob": round(prob_attack * 100.0, 2),
            "flow_duration": duration,
            "flow_packets_s": round(flow_pkts, 2),
            "flow_bytes_s": round(flow_bytes, 2),
            "protocol": protocol,
            "packet_length_max": pkt_len_max,
            "fwd_pkts": int(fwd_pkts),
            "bwd_pkts": int(bwd_pkts),
        })

    # Threat assessment level
    if attack_pct == 0.0:
        threat_level = "NORMAL"
        threat_color = "#00d4aa"
        threat_badge = "Normal Traffic"
    elif attack_pct < 15.0:
        threat_level = "LOW"
        threat_color = "#4e9af1"
        threat_badge = "Low Suspicious Activity"
    elif attack_pct < 50.0:
        threat_level = "ELEVATED"
        threat_color = "#f4a261"
        threat_badge = "Elevated Threat"
    else:
        threat_level = "CRITICAL"
        threat_color = "#f72585"
        threat_badge = "Critical Attack Detected"

    avg_conf = round(float(np.mean(confidences)), 2) if confidences else 0.0

    summary = {
        "filename": filename,
        "timestamp": timestamp_str,
        "model_key": model_key,
        "model_name": model_name,
        "total_records": total_records,
        "benign_count": benign_count,
        "attack_count": attack_count,
        "benign_pct": benign_pct,
        "attack_pct": attack_pct,
        "avg_confidence": avg_conf,
        "threat_level": threat_level,
        "threat_color": threat_color,
        "threat_badge": threat_badge,
        "processing_time": time_display,
        "processing_time_ms": processing_time_ms,
    }

    # Store in session history
    session_item = {
        "id": len(SESSION_HISTORY) + 1,
        "timestamp": timestamp_str,
        "filename": filename,
        "model_name": model_name,
        "total_flows": total_records,
        "benign_count": benign_count,
        "attack_count": attack_count,
        "attack_pct": attack_pct,
        "threat_level": threat_level,
        "processing_time": time_display,
    }
    SESSION_HISTORY.append(session_item)
    if len(SESSION_HISTORY) > 20:
        SESSION_HISTORY.pop(0)

    # Save export dataframe in memory
    export_df = df.copy()
    export_df["Predicted_Label"] = [r["prediction"] for r in records]
    export_df["Confidence_Score_Pct"] = [r["confidence"] for r in records]
    export_df["Attack_Probability_Pct"] = [r["attack_prob"] for r in records]
    export_df["Classifier_Model"] = model_name
    export_df["Prediction_Timestamp"] = timestamp_str
    
    LAST_PREDICTION_RESULTS = {
        "summary": summary,
        "export_df": export_df
    }

    return {
        "success": True,
        "error": None,
        "missing_cols": [],
        "records": records,
        "summary": summary,
    }
