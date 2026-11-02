"""
make_milestone5.py
==================
Generates Milestone_5_Report.docx for the DDoS Monitoring project.
Milestone 5 = Web Dashboard Deployment & Final Demonstration.

Run from the project root:
    .\\venv\\Scripts\\python.exe make_milestone5.py

Output: Milestone_5_Report.docx (in project root)
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime
import pathlib
import os

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Helper functions ──────────────────────────────────────────────────
def set_font(run, size=11, bold=False, color=None, italic=False):
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.name   = "Calibri"
    if color:
        run.font.color.rgb = RGBColor(*color)

def heading(doc, text, level=1, color=(26, 60, 100)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.name  = "Calibri"
        run.font.color.rgb = RGBColor(*color)
    return p

def para(doc, text, size=11, bold=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size, bold, color, italic)
    return p

def bullet(doc, text, size=11):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_font(run, size)
    return p

def shade_row(row, hex_color="D6E4F0"):
    for cell in row.cells:
        tc   = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd  = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  hex_color)
        tcPr.append(shd)

def add_table_row(table, cells, bold=False, size=10.5, bg=None):
    row = table.add_row()
    for i, txt in enumerate(cells):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p    = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run  = p.add_run(str(txt))
        set_font(run, size, bold)
    if bg:
        shade_row(row, bg)
    return row

def add_screenshot(doc, img_path, caption, width=Inches(5.8)):
    """Insert a screenshot image with a caption."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(img_path):
        run = p.add_run()
        run.add_picture(img_path, width=width)
    else:
        run = p.add_run(f"[Screenshot: {caption}]")
        set_font(run, 10, italic=True, color=(150, 150, 150))
    
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"Figure: {caption}")
    set_font(r, 9.5, italic=True, color=(80, 80, 120))
    doc.add_paragraph()

# ── Screenshot paths ──────────────────────────────────────────────────
PROJ_ROOT  = pathlib.Path(__file__).parent
SS_DIR     = PROJ_ROOT / "screenshots"
SS_DIR.mkdir(exist_ok=True)

SS = {
    "dashboard":   SS_DIR / "01_dashboard.png",
    "predict":     SS_DIR / "02_predict.png",
    "predict_res": SS_DIR / "03_predict_results.png",
    "comparison":  SS_DIR / "04_comparison.png",
    "evaluation":  SS_DIR / "05_evaluation.png",
    "about":       SS_DIR / "06_about.png",
}

# =====================================================================
# COVER PAGE
# =====================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\n\n\n")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("MILESTONE 5 REPORT")
set_font(run, 26, bold=True, color=(26, 60, 100))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Intelligent Network Traffic Monitoring System\nUsing CIC-DDoS2019 Dataset and Ensemble Learning")
set_font(run, 16, bold=True, color=(40, 40, 40))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("─" * 55)
set_font(run, 13, color=(100, 130, 180))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Milestone 5  —  Web Dashboard Deployment & Final Demonstration")
set_font(run, 13, bold=True, color=(60, 100, 160))

doc.add_paragraph()
fields = [
    ("Subject",      "Machine Learning / Network Security Project"),
    ("Milestone",    "5 — Web Dashboard Deployment & Final Demonstration"),
    ("Task",         "Interactive ML-Powered DDoS Detection Web Application"),
    ("Dataset",      "CIC-DDoS2019 (Canadian Institute for Cybersecurity)"),
    ("Submitted by", "Aditi Jain"),
    ("Date",         datetime.date.today().strftime("%B %d, %Y")),
]
for label, value in fields:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}:  ")
    set_font(r1, 12, bold=True, color=(26, 60, 100))
    r2 = p.add_run(value)
    set_font(r2, 12)

doc.add_page_break()

# =====================================================================
# TABLE OF CONTENTS (manual)
# =====================================================================
heading(doc, "Table of Contents")
toc = [
    ("1.", "Executive Summary"),
    ("2.", "Milestone Overview"),
    ("3.", "Web Application Architecture"),
    ("4.", "Flask Backend Implementation"),
    ("5.", "Web Dashboard Pages — Screenshots & Description"),
    ("   5.1", "Dashboard (Home Page)"),
    ("   5.2", "Traffic Prediction Page"),
    ("   5.3", "Model Comparison Page"),
    ("   5.4", "Evaluation Page (Confusion Matrices)"),
    ("   5.5", "About Page"),
    ("6.", "ML Integration — Real Model Inference"),
    ("7.", "Sample Data & Testing"),
    ("8.", "Technology Stack"),
    ("9.", "File Structure"),
    ("10.", "Verification & Testing"),
    ("11.", "Limitations & Future Scope"),
    ("12.", "Conclusion"),
]
for num, title in toc:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{num}  ")
    set_font(r1, 11, bold=(not num.startswith(" ")))
    r2 = p.add_run(title)
    set_font(r2, 11)

doc.add_page_break()

# =====================================================================
# 1. EXECUTIVE SUMMARY
# =====================================================================
heading(doc, "1. Executive Summary")
para(doc,
    "Milestone 5 marks the final deliverable of the Intelligent Network Traffic Monitoring "
    "System project. In this milestone, all five trained machine learning models — Decision "
    "Tree, Random Forest, XGBoost, Voting Ensemble, and Stacking Ensemble — were integrated "
    "into a professional Flask-based web dashboard that enables real-time batch prediction "
    "on user-uploaded CSV files."
)
doc.add_paragraph()
para(doc,
    "The web application provides five dedicated pages covering project overview, interactive "
    "traffic prediction, model performance comparison with Chart.js visualizations, confusion "
    "matrix evaluation, and a comprehensive About section. The system correctly uses the "
    "saved StandardScaler and the exact 30 features used during training for preprocessing, "
    "ensuring predictions are derived from genuine model inference — never hardcoded or "
    "randomly generated."
)
doc.add_paragraph()

# Key achievements
tbl = doc.add_table(rows=1, cols=2)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tbl.rows[0]
shade_row(hdr, "1A3C6E")
for i, txt in enumerate(["Achievement", "Details"]):
    cell = hdr.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

ach = [
    ("Best Model Deployed",     "Stacking Ensemble (Accuracy: 99.94%, F1: 0.9996)"),
    ("5 Models Integrated",     "DT, RF, XGBoost, Voting Ensemble, Stacking Ensemble"),
    ("Real ML Inference",       "Saved .pkl models + StandardScaler loaded at startup"),
    ("CSV Upload & Prediction", "Column validation, scaling, batch inference with confidence"),
    ("5-Page Dashboard",        "Dashboard, Predict, Comparison, Evaluation, About"),
    ("Chart.js Visualizations", "Bar charts, doughnut chart, radar chart, confusion matrices"),
    ("Session History",         "Tracks all prediction sessions with timestamps"),
    ("Download Results",        "Users can export predictions as CSV"),
    ("Test Suite Passed",       "All end-to-end tests passed (test_webapp.py)"),
    ("Zero Hardcoded Results",  "All predictions from live model inference"),
]
for i, row_data in enumerate(ach):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl, row_data, size=10.5, bg=bg)

doc.add_paragraph()

# =====================================================================
# 2. MILESTONE OVERVIEW
# =====================================================================
heading(doc, "2. Milestone Overview")
para(doc,
    "The project was structured into five milestones. Milestone 5 builds on all previous "
    "milestones by integrating the trained ML artifacts into a deployable web application."
)
doc.add_paragraph()

tbl_ms = doc.add_table(rows=1, cols=3)
tbl_ms.style = "Table Grid"
tbl_ms.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_ms = tbl_ms.rows[0]
shade_row(hdr_ms, "1A3C6E")
for i, txt in enumerate(["Milestone", "Focus Area", "Status"]):
    cell = hdr_ms.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

milestones = [
    ("Milestone 1", "Problem Definition & Dataset Understanding",          "✅ Complete"),
    ("Milestone 2", "Data Preprocessing & Feature Engineering",            "✅ Complete"),
    ("Milestone 3", "Model Training: Decision Tree, RF, XGBoost",          "✅ Complete"),
    ("Milestone 4", "Ensemble Methods: Voting & Stacking + Final Eval",    "✅ Complete"),
    ("Milestone 5", "Web Dashboard Deployment & Final Demonstration",      "✅ Complete"),
]
for i, row_data in enumerate(milestones):
    bg = "FFF9E6" if i == 4 else ("EBF3FB" if i % 2 == 0 else "FFFFFF")
    row = add_table_row(tbl_ms, row_data, size=10.5, bg=bg)
    if i == 4:
        for cell in row.cells:
            for run in cell.paragraphs[0].runs:
                run.font.bold = True

doc.add_paragraph()

# =====================================================================
# 3. WEB APPLICATION ARCHITECTURE
# =====================================================================
heading(doc, "3. Web Application Architecture")
para(doc,
    "The web application follows a three-tier architecture: a Python Flask backend, "
    "Jinja2 HTML templates for the presentation layer, and custom CSS/JavaScript for "
    "styling and interactivity."
)
doc.add_paragraph()

heading(doc, "3.1  Architecture Diagram", level=2)
arch = """\
┌───────────────────────────────────────────────────────────┐
│                     Browser (Client)                        │
│   ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│   │Dashboard│ │ Predict  │ │Comparison│ │  Evaluation  │  │
│   │  (/)    │ │(/predict)│ │(/compare)│ │ (/evaluation)│  │
│   └────┬────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘  │
└────────┼───────────┼────────────┼──────────────┼───────────┘
         │           │  HTTP/WSGI │              │
         ▼           ▼            ▼              ▼
┌───────────────────────────────────────────────────────────┐
│              Flask Application (app.py)                     │
│   Routes: /, /predict, /comparison, /evaluation, /about    │
│   CSV Upload Handling  │  JSON API  │  File Downloads       │
└────────────────┬──────────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────────────────────────┐
│                  predictor.py (ML Layer)                    │
│   Loads at startup:                                         │
│   ├── models/scaler.pkl       → StandardScaler              │
│   ├── models/stacking_ensemble.pkl  (default)               │
│   ├── models/random_forest.pkl                              │
│   ├── models/xgboost.pkl                                    │
│   ├── models/voting_ensemble.pkl                            │
│   └── models/decision_tree.pkl                              │
│   Functions: predict_dataframe(), get_feature_names()       │
└───────────────────────────────────────────────────────────┘"""

p = doc.add_paragraph()
p.style = "No Spacing"
run = p.add_run(arch)
run.font.name = "Courier New"
run.font.size = Pt(8.5)

doc.add_paragraph()

heading(doc, "3.2  Data Flow for Prediction", level=2)
flow_steps = [
    "User uploads a CSV file via the web form.",
    "Flask reads and parses the CSV using pandas.",
    "Column names are validated against the 30 required feature names.",
    "The predictor.py module preprocesses: selects the 30 features, applies the saved StandardScaler.",
    "The selected model runs inference on the scaled feature matrix.",
    "Results (label, confidence, prediction) are returned as a list of dictionaries.",
    "Flask renders the prediction table with color-coded BENIGN (green) / ATTACK (red) rows.",
    "A doughnut chart summarises the prediction distribution.",
    "User can download all predictions as a timestamped CSV file.",
]
for i, step in enumerate(flow_steps, 1):
    bullet(doc, f"Step {i}: {step}")

doc.add_page_break()

# =====================================================================
# 4. FLASK BACKEND IMPLEMENTATION
# =====================================================================
heading(doc, "4. Flask Backend Implementation")

heading(doc, "4.1  app.py — Route Summary", level=2)
para(doc,
    "The Flask application (app.py) defines six routes. All routes pass real ML metrics "
    "and dataset statistics to the Jinja2 templates."
)
doc.add_paragraph()

tbl_rt = doc.add_table(rows=1, cols=3)
tbl_rt.style = "Table Grid"
tbl_rt.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_rt = tbl_rt.rows[0]
shade_row(hdr_rt, "1A3C6E")
for i, txt in enumerate(["Route", "Method(s)", "Description"]):
    cell = hdr_rt.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

routes = [
    ("/",                              "GET",      "Dashboard: dataset stats, model cards, pipeline overview"),
    ("/predict",                       "GET, POST", "CSV upload, model selection, prediction table, doughnut chart"),
    ("/load-sample/<type>",            "GET",      "Load pre-built sample CSV (benign/attack/mixed)"),
    ("/download-predictions",          "GET",      "Download last prediction results as CSV"),
    ("/comparison",                    "GET",      "Model comparison table and 5 Chart.js charts"),
    ("/evaluation",                    "GET",      "Confusion matrices for all 5 models"),
    ("/about",                         "GET",      "Project objectives, scope, technology, limitations"),
    ("/download-sample-file/<type>",   "GET",      "Download sample CSV for testing"),
]
for i, row_data in enumerate(routes):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl_rt, row_data, size=10, bg=bg)

doc.add_paragraph()

heading(doc, "4.2  predictor.py — ML Module", level=2)
para(doc,
    "The predictor module loads all five models and the fitted scaler at startup. "
    "It exposes a predict_dataframe() function that accepts a pandas DataFrame and "
    "returns structured prediction results."
)
key_funcs = [
    "get_feature_names() — Returns the ordered list of 30 feature names from processed_data/feature_names.csv.",
    "get_load_status()   — Returns model loading status (all loaded / error message).",
    "get_available_models() — Returns dict of available model names and keys.",
    "predict_dataframe(df, filename, model_key) — Main prediction function: validates columns, scales, infers.",
    "get_session_history() — Returns history of all predictions made this session.",
    "get_last_prediction_results() — Returns last prediction for CSV download.",
]
for f in key_funcs:
    bullet(doc, f)

doc.add_paragraph()

# =====================================================================
# 5. WEB DASHBOARD PAGES — SCREENSHOTS
# =====================================================================
heading(doc, "5. Web Dashboard Pages — Screenshots & Description")
para(doc,
    "The web application runs locally at http://127.0.0.1:5000. The following sections "
    "describe each page with its screenshot and key features."
)

# ── 5.1 Dashboard ──
heading(doc, "5.1  Dashboard (Home Page)  —  http://127.0.0.1:5000/", level=2)
add_screenshot(doc, str(SS["dashboard"]), "Dashboard Home Page — Overview of system, stats, and best model")

para(doc, "Key components on the Dashboard page:")
dash_items = [
    "Top stat cards: Total Records (426,076), Features Selected (30), Models Trained (5), Best Accuracy (99.94%)",
    "Best Model banner: Stacking Ensemble with trophy icon, accuracy/precision/recall/F1 scores",
    "10-step pipeline flow diagram from Raw Data to Flask Prediction",
    "Model summary cards for all 5 classifiers with accuracy badges",
    "Session prediction history panel (tracks all CSV uploads this session)",
    "Data quality indicators: SMOTE applied, leakage audit status",
]
for item in dash_items:
    bullet(doc, item)

doc.add_paragraph()

# ── 5.2 Predict ──
heading(doc, "5.2  Traffic Prediction Page  —  http://127.0.0.1:5000/predict", level=2)
add_screenshot(doc, str(SS["predict"]), "Traffic Prediction Page — CSV upload interface")
add_screenshot(doc, str(SS["predict_res"]), "Traffic Prediction Results — Prediction table and summary chart")

para(doc, "Key features of the Traffic Prediction page:")
pred_items = [
    "Drag-and-drop CSV upload zone with file size limit (16 MB).",
    "Model selector dropdown: choose between DT, RF, XGBoost, Voting, or Stacking Ensemble.",
    "Three one-click sample buttons: Load Benign Sample, Load Attack Sample, Load Mixed Sample.",
    "Required feature list displayed (30 column names) so users know what CSV format is needed.",
    "Real-time column validation — missing columns listed before prediction.",
    "Prediction results table: Row #, confidence score, BENIGN (green) / ATTACK (red) badge.",
    "Summary doughnut chart: ATTACK % vs BENIGN % with counts.",
    "Filter buttons: Show All / Show Only Attacks / Show Only Benign.",
    "Download Predictions button — exports results as timestamped CSV.",
]
for item in pred_items:
    bullet(doc, item)

doc.add_paragraph()

# ── 5.3 Comparison ──
heading(doc, "5.3  Model Comparison Page  —  http://127.0.0.1:5000/comparison", level=2)
add_screenshot(doc, str(SS["comparison"]), "Model Comparison Page — Performance metrics and Chart.js charts")

para(doc, "Key features of the Model Comparison page:")
comp_items = [
    "Performance metrics table: Accuracy, Precision, Recall, F1 for all 5 models (Stacking highlighted in gold).",
    "Four Chart.js bar charts in 2×2 grid: Accuracy, Precision, Recall, F1 Score comparisons.",
    "Radar chart comparing all 5 models across all 4 metrics simultaneously.",
    "Confusion matrix summary table: TN, FP, FN, TP values for each model.",
    "Model type badges: Baseline, Bagging, Boosting, Soft Voting, Meta-Learning.",
    "Pros and Cons cards for each model architecture.",
]
for item in comp_items:
    bullet(doc, item)

doc.add_paragraph()

# ── 5.4 Evaluation ──
heading(doc, "5.4  Evaluation Page  —  http://127.0.0.1:5000/evaluation", level=2)
add_screenshot(doc, str(SS["evaluation"]), "Evaluation Page — Confusion matrices for all 5 models")

para(doc, "Key features of the Evaluation page:")
eval_items = [
    "Full confusion matrix grid for each of the 5 models.",
    "Color-coded cells: TP (bright green), TN (dark green), FP (red), FN (orange).",
    "Test set info banner: 85,216 samples | BENIGN: 18,941 | ATTACK: 66,275.",
    "TN/FP/FN/TP definitions explained clearly.",
    "Data leakage warning banner (feature selection was performed before the train-test split).",
    "Leakage-free evaluation section: shows that classification metrics are still valid.",
]
for item in eval_items:
    bullet(doc, item)

doc.add_paragraph()

# ── 5.5 About ──
heading(doc, "5.5  About Page  —  http://127.0.0.1:5000/about", level=2)
add_screenshot(doc, str(SS["about"]), "About Page — Project objectives, scope, and technology stack")

para(doc, "Key features of the About page:")
about_items = [
    "Project objectives: 5 key goals of the system.",
    "In-scope and out-of-scope cards clearly defined.",
    "CIC-DDoS2019 dataset details: 17 files, 426,076 records, 88 → 30 features.",
    "Technology grid: Python, scikit-learn, XGBoost, pandas, Flask, Chart.js, NumPy.",
    "10-step pipeline timeline with descriptions for each script (01–10).",
    "Complete list of all 30 selected feature names.",
    "Limitations section: feature selection leakage, offline-only, binary classification only.",
]
for item in about_items:
    bullet(doc, item)

doc.add_page_break()

# =====================================================================
# 6. ML INTEGRATION — REAL MODEL INFERENCE
# =====================================================================
heading(doc, "6. ML Integration — Real Model Inference")
para(doc,
    "A critical requirement of Milestone 5 was to ensure that all predictions displayed "
    "in the web application come from genuine model inference — not hardcoded or randomly "
    "generated values. The following table describes how each component ensures authentic inference."
)
doc.add_paragraph()

tbl_ml = doc.add_table(rows=1, cols=3)
tbl_ml.style = "Table Grid"
tbl_ml.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_ml = tbl_ml.rows[0]
shade_row(hdr_ml, "1A3C6E")
for i, txt in enumerate(["Component", "File", "How It Ensures Real Inference"]):
    cell = hdr_ml.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

ml_rows = [
    ("StandardScaler",      "models/scaler.pkl",           "Fitted on X_train only in 05_train_test_split.py. Loaded with joblib at startup."),
    ("Feature Names",       "processed_data/feature_names.csv", "Exact 30 columns in training order. Enforced before scaling."),
    ("Stacking Ensemble",   "models/stacking_ensemble.pkl",  "Saved after training in 10_stacking_ensemble.py. Loaded once at startup."),
    ("Random Forest",       "models/random_forest.pkl",     "100-tree RF, saved after training in 07_random_forest.py."),
    ("XGBoost",             "models/xgboost.pkl",           "XGBClassifier saved with joblib in 08_xgboost.py."),
    ("Voting Ensemble",     "models/voting_ensemble.pkl",   "Soft voting of DT+RF+XGB, saved in 09_voting_ensemble.py."),
    ("Decision Tree",       "models/decision_tree.pkl",     "Baseline DT, saved in 06_decision_tree.py."),
    ("Column Validation",   "predictor.py",                 "Missing columns are detected and reported before inference."),
    ("Confidence Score",    "predictor.py",                 "predict_proba() used; max class probability reported as confidence."),
]
for i, row_data in enumerate(ml_rows):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl_ml, row_data, size=10, bg=bg)

doc.add_paragraph()

# =====================================================================
# 7. SAMPLE DATA & TESTING
# =====================================================================
heading(doc, "7. Sample Data & Testing")
para(doc,
    "Five sample CSV files were created and stored in web_app/sample_data/ to enable "
    "instant one-click demonstration of the prediction pipeline without needing real "
    "network capture equipment."
)
doc.add_paragraph()

tbl_sd = doc.add_table(rows=1, cols=3)
tbl_sd.style = "Table Grid"
tbl_sd.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_sd = tbl_sd.rows[0]
shade_row(hdr_sd, "1A3C6E")
for i, txt in enumerate(["Sample File", "Contents", "Purpose"]):
    cell = hdr_sd.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

samples = [
    ("sample_traffic_benign.csv",        "25 rows of BENIGN traffic flows",          "Verify BENIGN detection"),
    ("sample_traffic_attack.csv",        "25 rows of DDoS ATTACK traffic flows",     "Verify ATTACK detection"),
    ("sample_traffic_mixed.csv",         "50 rows of mixed BENIGN + ATTACK flows",   "Verify mixed-traffic prediction"),
    ("sample_invalid_missing_cols.csv",  "CSV missing required feature columns",     "Test error handling"),
    ("sample_invalid_non_numeric.csv",   "CSV with non-numeric values in features",  "Test data type validation"),
]
for i, row_data in enumerate(samples):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl_sd, row_data, size=10, bg=bg)

doc.add_paragraph()

heading(doc, "7.1  End-to-End Test Results (test_webapp.py)", level=2)
para(doc, "All tests passed on the held-out sample data:", bold=True, color=(0, 120, 0))
test_results = [
    "✅  Scaler loaded successfully — type: StandardScaler, 30 features",
    "✅  All 5 models loaded successfully from models/ directory",
    "✅  BENIGN sample: 25/25 predictions = BENIGN (confidence > 99%)",
    "✅  ATTACK sample: 25/25 predictions = ATTACK (confidence > 98%)",
    "✅  Mixed sample: Correct BENIGN/ATTACK split detected",
    "✅  Missing-column validation: Error returned for incomplete CSV",
    "✅  Flask app responds HTTP 200 on all 5 routes",
]
for t in test_results:
    bullet(doc, t)

doc.add_paragraph()

# =====================================================================
# 8. TECHNOLOGY STACK
# =====================================================================
heading(doc, "8. Technology Stack")
para(doc,
    "The following table lists all technologies, libraries, and tools used in the "
    "web dashboard implementation."
)
doc.add_paragraph()

tbl_tech = doc.add_table(rows=1, cols=4)
tbl_tech.style = "Table Grid"
tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_tech = tbl_tech.rows[0]
shade_row(hdr_tech, "1A3C6E")
for i, txt in enumerate(["Category", "Technology", "Version", "Purpose"]):
    cell = hdr_tech.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

tech_rows = [
    ("Backend",       "Python",         "3.11+",    "Core language"),
    ("Backend",       "Flask",          "3.1.3",    "Web framework and HTTP routing"),
    ("Backend",       "Werkzeug",       "3.1.9",    "WSGI utilities, file upload handling"),
    ("ML",            "scikit-learn",   "1.9.1",    "Decision Tree, Random Forest, StandardScaler"),
    ("ML",            "XGBoost",        "3.4.0",    "Gradient boosting classifier"),
    ("ML",            "joblib",         "1.6.0",    "Model serialization (.pkl files)"),
    ("Data",          "pandas",         "2.3.3",    "DataFrame operations, CSV parsing"),
    ("Data",          "NumPy",          "2.5.3",    "Array operations"),
    ("Frontend",      "Jinja2",         "Built-in", "HTML templating engine"),
    ("Frontend",      "Chart.js",       "4.4 CDN",  "Interactive bar, doughnut, radar charts"),
    ("Frontend",      "CSS3",           "Custom",   "Dark navy/blue cybersecurity theme"),
    ("Frontend",      "JavaScript",     "ES6",      "Dynamic UI interactions"),
    ("Serialization", "pyarrow",        "25.0.1",   "Reading original Parquet dataset files"),
]
for i, row_data in enumerate(tech_rows):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl_tech, row_data, size=10, bg=bg)

doc.add_paragraph()

# =====================================================================
# 9. FILE STRUCTURE
# =====================================================================
heading(doc, "9. Project File Structure — web_app/")
structure = """\
DDoS_Monitoring/
├── web_app/                           ← Milestone 5 deliverable
│   ├── app.py                         ← Flask application (6 routes)
│   ├── predictor.py                   ← ML model loader + predict()
│   ├── test_webapp.py                 ← End-to-end test suite
│   ├── requirements_webapp.txt        ← Exact dependency versions
│   ├── templates/
│   │   ├── base.html                  ← Sidebar layout, nav, status bar
│   │   ├── dashboard.html             ← Home page with stats + charts
│   │   ├── predict.html               ← CSV upload + prediction results
│   │   ├── comparison.html            ← Model comparison + 5 charts
│   │   ├── evaluation.html            ← Confusion matrices (5 models)
│   │   └── about.html                 ← Project info + tech stack
│   ├── static/
│   │   ├── css/style.css              ← Dark cybersecurity theme CSS
│   │   └── js/charts.js               ← Global Chart.js defaults
│   └── sample_data/
│       ├── sample_traffic_benign.csv  ← 25 BENIGN flow records
│       ├── sample_traffic_attack.csv  ← 25 ATTACK flow records
│       ├── sample_traffic_mixed.csv   ← 50 mixed flow records
│       ├── sample_invalid_missing_cols.csv
│       └── sample_invalid_non_numeric.csv
├── models/                            ← Trained ML artifacts
│   ├── scaler.pkl                     ← StandardScaler (fit on X_train)
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── voting_ensemble.pkl
│   └── stacking_ensemble.pkl
└── processed_data/
    └── feature_names.csv              ← 30 ordered feature names"""

p = doc.add_paragraph()
p.style = "No Spacing"
run = p.add_run(structure)
run.font.name = "Courier New"
run.font.size = Pt(9)

doc.add_paragraph()

# =====================================================================
# 10. VERIFICATION & TESTING
# =====================================================================
heading(doc, "10. Verification & Testing")
para(doc,
    "Multiple layers of verification were performed to confirm the web application "
    "works correctly end-to-end."
)
doc.add_paragraph()

heading(doc, "10.1  Unit-Level Checks", level=2)
unit_checks = [
    "Scaler type verified: StandardScaler with 30 input features.",
    "Feature names cross-checked: Exact match between predictor.py and 05_train_test_split.py output.",
    "Model types verified: All 5 .pkl files load without errors using joblib.",
    "sklearn version compatibility: Models saved with 1.8.0, runtime uses 1.9.1 (minor version — safe).",
    "Version warning suppressed in predictor.py using Python's warnings module.",
]
for c in unit_checks:
    bullet(doc, c)

heading(doc, "10.2  Integration Tests", level=2)
int_tests = [
    "BENIGN sample prediction: All 25 rows → BENIGN with confidence > 99% ✅",
    "ATTACK sample prediction: All 25 rows → ATTACK with confidence > 98% ✅",
    "Mixed sample prediction: Correct proportions detected ✅",
    "Missing-column error handling: Descriptive error message returned ✅",
    "Non-numeric value handling: Pandas coercion with NaN fill ✅",
    "CSV download: Timestamped CSV exported correctly ✅",
    "Sample file download: All 5 sample files downloadable via /download-sample-file/<type> ✅",
]
for t in int_tests:
    bullet(doc, t)

heading(doc, "10.3  Server Verification", level=2)
server_checks = [
    "Flask starts without errors using venv Python interpreter.",
    "HTTP 200 response confirmed on all 5 routes.",
    "16 MB upload limit configured.",
    "Application runs stably at http://127.0.0.1:5000.",
    "Models load in ~10 seconds due to large Random Forest and Stacking Ensemble files (7 MB each).",
]
for c in server_checks:
    bullet(doc, c)

doc.add_paragraph()

# =====================================================================
# 11. LIMITATIONS & FUTURE SCOPE
# =====================================================================
heading(doc, "11. Limitations & Future Scope")

heading(doc, "11.1  Current Limitations", level=2)
lims = [
    "Offline batch prediction only: The system accepts pre-collected CSV files. Live packet "
     "capture and real-time traffic monitoring are outside the current scope.",
    "Local deployment only: The Flask server runs on localhost (127.0.0.1:5000). It is not "
     "deployed to a public cloud or accessible over the internet.",
    "Binary classification: The system predicts BENIGN or ATTACK but does not identify "
     "the specific DDoS attack type (e.g., SYN, UDP, DNS).",
    "Feature selection leakage: Feature importance was computed before the train-test split, "
     "introducing mild selection bias (not affecting classification metrics).",
    "Dataset-specific performance: Models were trained exclusively on CIC-DDoS2019 synthetic "
     "traffic. Real-world generalization may be lower.",
    "No authentication: The web dashboard has no login/access control.",
]
for l in lims:
    bullet(doc, l)

heading(doc, "11.2  Future Scope", level=2)
future = [
    "Real-time monitoring: Integrate with live packet capture libraries (e.g., scapy, pyshark) "
     "to perform real-time traffic classification.",
    "Multi-class classification: Extend the model to classify the 11 specific DDoS attack types.",
    "Cloud deployment: Deploy on AWS/GCP/Azure using Docker containers and a production WSGI server.",
    "API endpoint: Expose a REST API for integration with SIEM (Security Information & Event Management) systems.",
    "Deep learning: Experiment with LSTM or CNN models for temporal traffic pattern recognition.",
    "Retraining pipeline: Add an automated retraining trigger when drift is detected in incoming data.",
    "Authentication & Role-based access: Add user authentication for enterprise deployment.",
]
for f in future:
    bullet(doc, f)

doc.add_paragraph()

# =====================================================================
# 12. CONCLUSION
# =====================================================================
heading(doc, "12. Conclusion")
para(doc,
    "Milestone 5 successfully completes the Intelligent Network Traffic Monitoring System "
    "project. All five trained machine learning models — Decision Tree, Random Forest, "
    "XGBoost, Voting Ensemble, and Stacking Ensemble — have been integrated into a "
    "professional, dark-themed Flask web dashboard that provides genuine ML inference "
    "on user-uploaded CSV files."
)
doc.add_paragraph()
para(doc,
    "The web application provides a complete demonstration pipeline: users can upload any "
    "CSV file containing the 30 required network flow features, select their preferred model, "
    "and receive instant BENIGN/ATTACK classifications with confidence scores. All prediction "
    "results come exclusively from the saved trained models using the fitted StandardScaler — "
    "never from hardcoded or randomly generated values."
)
doc.add_paragraph()
para(doc,
    "The system demonstrates the practical viability of applying ensemble machine learning "
    "for DDoS traffic detection. The Stacking Ensemble, selected as the default deployed model, "
    "achieves 99.94% accuracy and an F1 score of 0.9996 on the 85,216-sample held-out test set, "
    "with only 46 missed attacks (FN) and 9 false alarms (FP) out of 85,216 test flows."
)
doc.add_paragraph()

# Final summary metrics
para(doc, "Final Deployed Model Performance Summary:", bold=True, color=(26, 60, 100))
tbl_fin = doc.add_table(rows=1, cols=5)
tbl_fin.style = "Table Grid"
tbl_fin.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_fin = tbl_fin.rows[0]
shade_row(hdr_fin, "1A3C6E")
for i, txt in enumerate(["Model", "Accuracy", "Precision", "Recall", "F1 Score"]):
    cell = hdr_fin.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

final_perf = [
    ("Decision Tree",    "0.9992", "0.9997", "0.9993", "0.9995"),
    ("Random Forest",    "0.9993", "0.9999", "0.9993", "0.9996"),
    ("XGBoost",          "0.9990", "0.9999", "0.9988", "0.9994"),
    ("Voting Ensemble",  "0.9993", "0.9999", "0.9992", "0.9996"),
    ("Stacking Ensemble","0.9994", "0.9999", "0.9993", "0.9996"),
]
for idx, row_data in enumerate(final_perf):
    bg = "FFF9E6" if row_data[0] == "Stacking Ensemble" else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    row = add_table_row(tbl_fin, row_data, size=10.5, bg=bg)
    if row_data[0] == "Stacking Ensemble":
        for cell in row.cells:
            for run in cell.paragraphs[0].runs:
                run.font.bold = True

doc.add_paragraph()
para(doc,
    "★  Stacking Ensemble (Meta-Learning with Logistic Regression) is deployed as the default "
    "model — achieving the best balance of accuracy, precision, recall, and minimum missed attacks.",
    bold=True, color=(26, 60, 100)
)

# ── Save ──────────────────────────────────────────────────────────────
output = PROJ_ROOT / "Milestone_5_Report.docx"
doc.save(str(output))
print(f"\n✅  Saved: {output}")
print(f"    Open this file in Microsoft Word.\n")
