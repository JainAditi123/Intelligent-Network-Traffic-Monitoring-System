"""
app.py  —  Flask Web Application for Intelligent Network Traffic Monitoring
===========================================================================
Run from web_app/ directory:
    python app.py
Then open http://127.0.0.1:5000
"""

import io
import os
import sys
import json
import pathlib
import datetime
import pandas as pd
from flask import (
    Flask, render_template, request, jsonify, redirect, url_for, send_file, Response
)

# Ensure web_app directory is on sys.path regardless of execution root
_WEB_APP_DIR = os.path.dirname(os.path.abspath(__file__))
if _WEB_APP_DIR not in sys.path:
    sys.path.insert(0, _WEB_APP_DIR)

from predictor import (
    get_feature_names,
    get_load_status,
    get_available_models,
    predict_dataframe,
    get_session_history,
    get_last_prediction_results
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024   # 16 MB max upload
app.secret_key = "ddos-monitoring-system-secret-key"

# ── Base paths ──
_APP_DIR = pathlib.Path(__file__).parent.resolve()
_PROJECT_DIR = _APP_DIR.parent
_SAMPLE_DIR = _APP_DIR / "sample_data"
_AUDIT_FILE = _PROJECT_DIR / "processed_data" / "leakage_audit_results.json"

# ── Load leakage audit results if available ──
LEAKAGE_AUDIT = None
if _AUDIT_FILE.exists():
    try:
        with open(_AUDIT_FILE, "r") as f:
            LEAKAGE_AUDIT = json.load(f)
    except Exception:
        LEAKAGE_AUDIT = None

# ── Context processor for global status across all templates ──
@app.context_processor
def inject_global_status():
    return {
        "load_status": get_load_status(),
        "available_models": get_available_models()
    }

# ── Recorded Experiment Results (5 Models on Held-out Test Set) ──
RESULTS = [
    {
        "name": "Decision Tree",
        "accuracy":  0.9992,
        "precision": 0.9997,
        "recall":    0.9993,
        "f1":        0.9995,
        "cm": {"tn": 18919, "fp": 22, "fn": 46, "tp": 66229},
        "icon": "🌳",
        "type": "Single Tree (Baseline)",
        "color": "#4e9af1",
        "pros": "Highly interpretable; fast training and inference.",
        "cons": "Susceptible to high variance and overfitting.",
    },
    {
        "name": "Random Forest",
        "accuracy":  0.9993,
        "precision": 0.9999,
        "recall":    0.9993,
        "f1":        0.9996,
        "cm": {"tn": 18932, "fp": 9, "fn": 49, "tp": 66226},
        "icon": "🌲",
        "type": "Bagging Ensemble (100 Trees)",
        "color": "#00d4aa",
        "pros": "Significantly reduces variance via random feature subspacing.",
        "cons": "Larger model size (7 MB); slower training than single tree.",
    },
    {
        "name": "XGBoost",
        "accuracy":  0.9990,
        "precision": 0.9999,
        "recall":    0.9988,
        "f1":        0.9994,
        "cm": {"tn": 18937, "fp": 4, "fn": 79, "tp": 66196},
        "icon": "⚡",
        "type": "Gradient Boosting (100 Estimators)",
        "color": "#f4a261",
        "pros": "Lowest False Positives (FP=4); very few false alarms.",
        "cons": "Slightly higher False Negatives (FN=79) than Stacking.",
    },
    {
        "name": "Voting Ensemble",
        "accuracy":  0.9993,
        "precision": 0.9999,
        "recall":    0.9992,
        "f1":        0.9996,
        "cm": {"tn": 18933, "fp": 8, "fn": 51, "tp": 66224},
        "icon": "🗳️",
        "type": "Soft Voting (DT + RF + XGB)",
        "color": "#a78bfa",
        "pros": "Averages class probabilities across diverse architectures.",
        "cons": "Assigns equal weight to all models regardless of strengths.",
    },
    {
        "name": "Stacking Ensemble",
        "accuracy":  0.9994,
        "precision": 0.9999,
        "recall":    0.9993,
        "f1":        0.9996,
        "cm": {"tn": 18932, "fp": 9, "fn": 46, "tp": 66229},
        "icon": "🏆",
        "type": "Meta-Learning (Logistic Regression)",
        "color": "#f72585",
        "pros": "Highest accuracy & lowest False Negatives among ensembles (FN=46).",
        "cons": "Most complex architecture; requires 2-level inference.",
    },
]

# ── Real Verified Dataset Statistics ──
DATASET_STATS = {
    "total_cleaned_samples": 426076,
    "parquet_files":         17,
    "selected_features":     30,
    "attack_types_count":    11,
    
    # Pre-SMOTE Split
    "train_split_pre_smote": 340860,
    "test_split_samples":    85216,
    
    # Class breakdown in Cleaned Dataset (Overall)
    "cleaned_benign": 94704,
    "cleaned_attack": 331372,
    "cleaned_benign_pct": 22.2,
    "cleaned_attack_pct": 77.8,
    
    # Training Split Pre-SMOTE (80%)
    "train_benign_pre_smote": 75763,
    "train_attack_pre_smote": 265097,
    
    # Training Split Post-SMOTE (Balanced)
    "train_samples_post_smote": 530194,
    "train_benign_post_smote":  265097,
    "train_attack_post_smote":  265097,
    
    # Held-out Test Split (20% - never seen in training or SMOTE)
    "test_benign": 18941,
    "test_attack": 66275,
    "test_benign_pct": 22.2,
    "test_attack_pct": 77.8,
}


# ── Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    history = get_session_history()
    return render_template(
        "dashboard.html",
        results=RESULTS,
        stats=DATASET_STATS,
        best=RESULTS[-1],
        session_history=history,
        audit=LEAKAGE_AUDIT
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    feature_names = get_feature_names()
    filter_type = request.args.get("filter", "all").lower()
    selected_model = request.args.get("model", "stacking").lower()
    
    context = {
        "feature_names": feature_names,
        "records": None,
        "displayed_records": None,
        "summary": None,
        "error": None,
        "missing_cols": [],
        "filename": None,
        "num_rows": None,
        "filter_type": filter_type,
        "selected_model": selected_model,
        "session_history": get_session_history(),
    }

    if request.method == "POST":
        selected_model = request.form.get("model_select", "stacking").lower()
        context["selected_model"] = selected_model

        file = request.files.get("csv_file")
        if not file or file.filename == "":
            context["error"] = "No file selected. Please choose a valid network flow CSV file."
            return render_template("predict.html", **context)

        if not file.filename.lower().endswith(".csv"):
            context["error"] = "Invalid file type. Only standard CSV (.csv) files are supported."
            return render_template("predict.html", **context)

        try:
            content = file.read().decode("utf-8", errors="replace")
            df = pd.read_csv(io.StringIO(content))
        except Exception as e:
            context["error"] = f"Unable to parse CSV file: {str(e)}"
            return render_template("predict.html", **context)

        if df.empty:
            context["error"] = "The uploaded CSV file contains no rows."
            return render_template("predict.html", **context)

        # Run prediction engine
        res = predict_dataframe(df, filename=file.filename, model_key=selected_model)
        
        context["filename"] = file.filename
        context["num_rows"] = len(df)
        context["missing_cols"] = res.get("missing_cols", [])
        
        if not res.get("success", False):
            context["error"] = res.get("error", "An unknown error occurred during prediction.")
            return render_template("predict.html", **context)

        all_records = res.get("records", [])
        context["records"] = all_records
        context["summary"] = res.get("summary", {})
        
        # Apply filter
        if filter_type == "attack":
            context["displayed_records"] = [r for r in all_records if r["is_attack"]]
        elif filter_type == "benign":
            context["displayed_records"] = [r for r in all_records if not r["is_attack"]]
        else:
            context["displayed_records"] = all_records

    return render_template("predict.html", **context)


@app.route("/load-sample/<sample_type>")
def load_sample(sample_type):
    """Directly loads a sample dataset for instant one-click demonstration."""
    filename_map = {
        "benign": "sample_traffic_benign.csv",
        "attack": "sample_traffic_attack.csv",
        "mixed":  "sample_traffic_mixed.csv"
    }
    
    fname = filename_map.get(sample_type)
    if not fname:
        return redirect(url_for("predict"))
        
    sample_path = _SAMPLE_DIR / fname
    if not sample_path.exists():
        return redirect(url_for("predict"))
        
    selected_model = request.args.get("model", "stacking").lower()
    df = pd.read_csv(sample_path)
    res = predict_dataframe(df, filename=fname, model_key=selected_model)
    
    feature_names = get_feature_names()
    context = {
        "feature_names": feature_names,
        "records": res.get("records", []),
        "displayed_records": res.get("records", []),
        "summary": res.get("summary", {}),
        "error": res.get("error"),
        "missing_cols": res.get("missing_cols", []),
        "filename": fname,
        "num_rows": len(df),
        "filter_type": "all",
        "selected_model": selected_model,
        "session_history": get_session_history(),
    }
    return render_template("predict.html", **context)


@app.route("/download-predictions")
def download_predictions():
    """Generates and downloads a CSV of the latest prediction results."""
    last_res = get_last_prediction_results()
    if not last_res or "export_df" not in last_res:
        return "No recent prediction results available to download.", 404

    export_df = last_res["export_df"]
    buffer = io.StringIO()
    export_df.to_csv(buffer, index=False)
    buffer.seek(0)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_name = f"ddos_predictions_{ts}.csv"
    
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={download_name}"}
    )


@app.route("/download-sample-file/<sample_type>")
def download_sample_file(sample_type):
    """Allows users to download pre-configured sample CSV files."""
    filename_map = {
        "benign": "sample_traffic_benign.csv",
        "attack": "sample_traffic_attack.csv",
        "mixed":  "sample_traffic_mixed.csv",
        "missing": "sample_invalid_missing_cols.csv",
        "nonnumeric": "sample_invalid_non_numeric.csv"
    }
    fname = filename_map.get(sample_type)
    if not fname:
        return "Sample not found", 404
    
    sample_path = _SAMPLE_DIR / fname
    if not sample_path.exists():
        return "Sample file missing", 404
        
    return send_file(sample_path, as_attachment=True, download_name=fname)


@app.route("/comparison")
def comparison():
    return render_template("comparison.html", results=RESULTS, audit=LEAKAGE_AUDIT)


@app.route("/evaluation")
def evaluation():
    return render_template("evaluation.html", results=RESULTS, stats=DATASET_STATS, audit=LEAKAGE_AUDIT)


@app.route("/about")
def about():
    features = get_feature_names()
    return render_template("about.html", features=features, stats=DATASET_STATS, audit=LEAKAGE_AUDIT)


# ── Launch ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print(" Intelligent Network Traffic Monitoring System")
    print(" Running at: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, host="127.0.0.1", port=5000)
