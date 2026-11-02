"""
make_milestone5_clean.py
========================
Generates Milestone_5_Report_Clean.docx  (NO screenshots — 7 pages)
Run from the project root:
    .\\venv\\Scripts\\python.exe make_milestone5_clean.py
Output: Milestone_5_Report_Clean.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Helpers ───────────────────────────────────────────────────────────
def set_font(run, size=11, bold=False, color=None, italic=False):
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.name   = "Calibri"
    if color:
        run.font.color.rgb = RGBColor(*color)

def heading(doc, text, level=1, color=(15, 54, 96)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(*color)
    return p

def para(doc, text, size=11, bold=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    set_font(run, size, bold, color, italic)
    return p

def bullet(doc, text, size=10.5, color=None):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_font(run, size, color=color)
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

def add_table_row(table, cells, bold=False, size=10, bg=None, align=WD_ALIGN_PARAGRAPH.CENTER):
    row = table.add_row()
    for i, txt in enumerate(cells):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p    = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_after = Pt(0)
        run  = p.add_run(str(txt))
        set_font(run, size, bold)
    if bg:
        shade_row(row, bg)
    return row

def make_table(doc, headers, rows_data, col_widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0]
    shade_row(hdr, "0F3660")
    for i, txt in enumerate(headers):
        cell = hdr.cells[i]
        if col_widths:
            cell.width = Inches(col_widths[i])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(txt)
        set_font(run, 10.5, bold=True, color=(255, 255, 255))
    for idx, row_data in enumerate(rows_data):
        bg = "EBF3FB" if idx % 2 == 0 else "FFFFFF"
        add_table_row(tbl, row_data, size=10, bg=bg)
    return tbl

def sp(doc, n=1):
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)

# =====================================================================
# PAGE 1 — COVER PAGE
# =====================================================================
sp(doc, 3)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("MILESTONE 5 REPORT")
set_font(run, 28, bold=True, color=(10, 45, 90))

sp(doc)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Intelligent Network Traffic Monitoring System")
set_font(run, 17, bold=True, color=(30, 30, 30))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Using CIC-DDoS2019 Dataset and Ensemble Learning")
set_font(run, 13, italic=True, color=(80, 80, 80))

sp(doc)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\u2015" * 48)
set_font(run, 12, color=(100, 140, 200))

sp(doc)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Web Dashboard Deployment & Final Demonstration")
set_font(run, 14, bold=True, color=(15, 54, 96))

sp(doc, 2)

cover_fields = [
    ("Subject",         "Machine Learning / Network Security Project"),
    ("Milestone",       "5  —  Web Dashboard Deployment & Final Demonstration"),
    ("Objective",       "Interactive ML-Powered DDoS Detection Web Application"),
    ("Dataset",         "CIC-DDoS2019 — Canadian Institute for Cybersecurity"),
    ("Models Deployed", "Decision Tree, Random Forest, XGBoost, Voting Ensemble, Stacking Ensemble"),
    ("Best Model",      "Stacking Ensemble — Accuracy: 99.94%  |  F1: 0.9996"),
    ("Web Framework",   "Python Flask 3.1.3  |  http://127.0.0.1:5000"),
    ("Submitted by",    "Aditi Jain"),
    ("Date",            datetime.date.today().strftime("%B %d, %Y")),
]

for label, value in cover_fields:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{label}:   ")
    set_font(r1, 11.5, bold=True, color=(15, 54, 96))
    r2 = p.add_run(value)
    set_font(r2, 11.5, color=(30, 30, 30))

doc.add_page_break()

# =====================================================================
# PAGE 2 — Executive Summary + Milestone Overview
# =====================================================================
heading(doc, "1. Executive Summary")
para(doc,
    "Milestone 5 is the final deliverable of the Intelligent Network Traffic Monitoring "
    "System project. In this milestone, all five trained machine learning models — "
    "Decision Tree, Random Forest, XGBoost, Voting Ensemble, and Stacking Ensemble — "
    "were integrated into a professional Flask-based web dashboard. The dashboard enables "
    "real-time batch prediction on user-uploaded CSV files and presents detailed performance "
    "comparisons through interactive Chart.js visualizations."
)
para(doc,
    "The web application uses the saved StandardScaler and the exact 30 feature names "
    "used during training. All predictions come from genuine model inference — never "
    "hardcoded or randomly generated. The Stacking Ensemble is deployed as the default "
    "model achieving 99.94% accuracy and F1 score of 0.9996 on the 85,216-sample held-out test set."
)

sp(doc)

# Key achievements table
make_table(doc,
    ["Achievement", "Details"],
    [
        ("5 Models Integrated",     "Decision Tree, Random Forest, XGBoost, Voting, Stacking Ensemble"),
        ("Real ML Inference",        "Saved .pkl models + StandardScaler loaded at startup via joblib"),
        ("5-Page Web Dashboard",     "Dashboard, Predict, Comparison, Evaluation, About"),
        ("CSV Upload & Prediction",  "Column validation, scaling, batch inference with confidence scores"),
        ("Chart.js Visualizations",  "Bar charts, doughnut chart, radar chart, confusion matrices"),
        ("Sample Data Provided",     "3 sample CSVs: Benign, Attack, Mixed (25-50 rows each)"),
        ("Session History",          "Tracks all prediction sessions with timestamps"),
        ("Download Results",         "Users can export all predictions as a timestamped CSV file"),
        ("End-to-End Tests Passed",  "All tests in test_webapp.py passed successfully"),
        ("Zero Hardcoded Results",   "All predictions exclusively from live model inference"),
    ],
    col_widths=[2.2, 4.0]
)

sp(doc)
heading(doc, "2. Milestone Overview", level=1)
para(doc, "The project was structured across five milestones. Milestone 5 integrates all ML artifacts into a deployed web application.")
sp(doc)

make_table(doc,
    ["Milestone", "Focus Area", "Status"],
    [
        ("Milestone 1", "Problem Definition & Dataset Understanding",        "Complete"),
        ("Milestone 2", "Data Preprocessing & Feature Engineering",          "Complete"),
        ("Milestone 3", "Model Training: Decision Tree, RF, XGBoost",        "Complete"),
        ("Milestone 4", "Ensemble Methods: Voting & Stacking + Evaluation",  "Complete"),
        ("Milestone 5", "Web Dashboard Deployment & Final Demonstration",    "Complete"),
    ],
    col_widths=[1.5, 4.0, 1.2]
)

doc.add_page_break()

# =====================================================================
# PAGE 3 — Architecture + Backend Routes
# =====================================================================
heading(doc, "3. Web Application Architecture")
para(doc,
    "The web application follows a three-tier architecture: Python Flask as the backend, "
    "Jinja2 HTML templates for the presentation layer, and custom CSS/JavaScript for "
    "dark-theme styling and Chart.js interactivity. All ML models and the scaler are "
    "loaded once at startup for fast inference."
)
sp(doc)

# Architecture as code block
arch_text = """\
[Browser / Client]
   |-- Dashboard (/)          |-- Traffic Prediction (/predict)
   |-- Model Comparison (/comparison)  |-- Evaluation (/evaluation)
   |-- About (/about)
          |
          | HTTP / WSGI
          |
[Flask Application  -  app.py]
   Routes: /, /predict, /comparison, /evaluation, /about
   Handles: CSV upload, file validation, session history, CSV download
          |
[predictor.py  -  ML Inference Layer]
   Loads at startup:
      models/scaler.pkl             -> StandardScaler (30 features)
      models/stacking_ensemble.pkl  -> Default model
      models/random_forest.pkl      -> Random Forest
      models/xgboost.pkl            -> XGBoost
      models/voting_ensemble.pkl    -> Voting Ensemble
      models/decision_tree.pkl      -> Decision Tree
   Functions: predict_dataframe(), get_feature_names(), get_load_status()"""

p = doc.add_paragraph()
p.style = "No Spacing"
p.paragraph_format.space_after = Pt(8)
run = p.add_run(arch_text)
run.font.name = "Courier New"
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(20, 60, 100)

sp(doc)
heading(doc, "4. Flask Backend — Routes & Functions", level=1)
para(doc, "The Flask application (app.py) defines 8 routes. All routes pass real ML metrics and dataset statistics to the Jinja2 templates.")
sp(doc)

make_table(doc,
    ["Route", "Method", "Description"],
    [
        ("/",                          "GET",       "Dashboard: stat cards, best model, pipeline diagram, session history"),
        ("/predict",                   "GET, POST", "CSV upload, model selector, column validation, prediction table + chart"),
        ("/load-sample/<type>",        "GET",       "One-click load: benign / attack / mixed sample CSV into predictor"),
        ("/download-predictions",      "GET",       "Export last prediction session as timestamped CSV download"),
        ("/comparison",                "GET",       "Performance table + 5 Chart.js charts (bar x4, radar x1)"),
        ("/evaluation",                "GET",       "Confusion matrices for all 5 models with TN/FP/FN/TP labels"),
        ("/about",                     "GET",       "Objectives, scope, dataset, technology stack, pipeline, limitations"),
        ("/download-sample-file/<t>",  "GET",       "Download any of the 5 pre-built sample CSV files"),
    ],
    col_widths=[2.2, 1.0, 3.2]
)

sp(doc)
para(doc, "Key predictor.py functions:", bold=True, color=(15, 54, 96), size=11)
funcs = [
    "get_feature_names()         — Returns the 30 ordered feature names from processed_data/feature_names.csv.",
    "get_load_status()           — Returns model loading status (all 5 loaded / error message).",
    "get_available_models()      — Returns dict of model keys (dt, rf, xgb, voting, stacking).",
    "predict_dataframe(df, ...)  — Main prediction: validates columns, scales, infers, returns results list.",
    "get_session_history()       — Returns history of all prediction sessions this server session.",
    "get_last_prediction_results() — Returns last prediction dict for CSV export.",
]
for f in funcs:
    bullet(doc, f)

doc.add_page_break()

# =====================================================================
# PAGE 4 — Dashboard Pages Description
# =====================================================================
heading(doc, "5. Web Dashboard — All 5 Pages")
para(doc,
    "The web application runs at http://127.0.0.1:5000 and provides five dedicated pages. "
    "The design uses a dark navy/blue cybersecurity theme with Chart.js interactive charts."
)
sp(doc)

heading(doc, "5.1  Dashboard  (URL: http://127.0.0.1:5000/)", level=2)
para(doc, "The home page provides a full project overview at a glance.", size=10.5)
dash_feats = [
    "Four stat cards: Total Records (426,076) | Features Selected (30) | Models Trained (5) | Best Accuracy (99.94%)",
    "Best Model highlight card: Stacking Ensemble with Accuracy, Precision, Recall, F1, FP, FN values",
    "10-step ML pipeline flow diagram: Raw Data → Preprocessing → Labels → Feature Selection → Split → SMOTE → DT → RF → XGB → Stacking",
    "Model summary cards for all 5 classifiers showing type, key metrics, and pros/cons",
    "Session Prediction History: timestamp and summary of all CSV uploads done this session",
    "Data leakage audit notice and dataset quality indicators",
]
for f in dash_feats:
    bullet(doc, f)

sp(doc)
heading(doc, "5.2  Traffic Prediction  (URL: /predict)", level=2)
para(doc, "The core functionality page for uploading and classifying network flow CSV files.", size=10.5)
pred_feats = [
    "Drag-and-drop CSV upload zone with 16 MB size limit",
    "Model selector dropdown: choose between DT, RF, XGBoost, Voting, or Stacking Ensemble",
    "Three one-click sample buttons: Load Benign Sample | Load Attack Sample | Load Mixed Sample",
    "Column validation: checks all 30 required feature columns before prediction runs",
    "Prediction results table: Row #, confidence score (%), BENIGN (green) / ATTACK (red) badge",
    "Doughnut chart: ATTACK % vs BENIGN % breakdown with exact counts",
    "Filter buttons: Show All / Show Only Attacks / Show Only Benign",
    "Download Predictions: exports results as a timestamped CSV file",
]
for f in pred_feats:
    bullet(doc, f)

sp(doc)
heading(doc, "5.3  Model Comparison  (URL: /comparison)", level=2)
para(doc, "Compares all 5 models side-by-side with metrics and interactive visualizations.", size=10.5)
comp_feats = [
    "Full performance metrics table: Accuracy, Precision, Recall, F1 for all 5 models (Stacking highlighted)",
    "Four Chart.js bar charts (2x2 grid): Accuracy | Precision | Recall | F1 Score",
    "Radar chart: simultaneous comparison of all 5 models across all 4 metrics",
    "Confusion matrix summary table: TN, FP, FN, TP values per model",
    "Model type badges: Baseline / Bagging / Boosting / Soft Voting / Meta-Learning",
    "Pros and Cons card for each model architecture",
]
for f in comp_feats:
    bullet(doc, f)

sp(doc)
heading(doc, "5.4  Evaluation  (URL: /evaluation)", level=2)
para(doc, "Shows full confusion matrices for all 5 models on the held-out test set.", size=10.5)
eval_feats = [
    "Full 2x2 confusion matrix grid for each of the 5 models",
    "Color-coded cells: TP (bright green) | TN (dark green) | FP (red) | FN (orange)",
    "Test set info banner: 85,216 samples | BENIGN: 18,941 | ATTACK: 66,275",
    "TN / FP / FN / TP definitions clearly explained below each matrix",
    "Data leakage warning banner: explains feature selection performed before split",
    "Leakage-free evaluation note: confirms classification metrics are valid",
]
for f in eval_feats:
    bullet(doc, f)

sp(doc)
heading(doc, "5.5  About  (URL: /about)", level=2)
para(doc, "Provides complete project documentation within the web interface.", size=10.5)
about_feats = [
    "Project objectives: 5 key goals of the system",
    "In-scope and out-of-scope cards clearly defined",
    "CIC-DDoS2019 dataset card: 17 files, 426,076 records, 88 raw features, 30 selected",
    "Technology grid: Python, scikit-learn, XGBoost, pandas, Flask, Chart.js, NumPy",
    "10-step pipeline timeline with description for each Python script (01 to 10)",
    "Complete list of all 30 selected feature names used in the model",
    "Limitations section: feature selection leakage, offline-only, binary classification",
]
for f in about_feats:
    bullet(doc, f)

doc.add_page_break()

# =====================================================================
# PAGE 5 — ML Integration + Evaluation Results
# =====================================================================
heading(doc, "6. ML Integration — Real Model Inference")
para(doc,
    "All predictions in the web application come from genuine model inference using saved "
    ".pkl files — never hardcoded or randomly generated. The table below describes each component."
)
sp(doc)

make_table(doc,
    ["Component", "Source File", "Ensures Real Inference"],
    [
        ("StandardScaler",     "models/scaler.pkl",           "Fitted on X_train only in 05_train_test_split.py. Loaded via joblib."),
        ("Feature Names",      "feature_names.csv",           "Exact 30 column names in training order enforced before scaling."),
        ("Stacking Ensemble",  "models/stacking_ensemble.pkl","Saved after 10_stacking_ensemble.py. Default model on /predict page."),
        ("Random Forest",      "models/random_forest.pkl",    "100-tree RF trained in 07_random_forest.py, saved with joblib."),
        ("XGBoost",            "models/xgboost.pkl",          "XGBClassifier saved in 08_xgboost.py after training."),
        ("Voting Ensemble",    "models/voting_ensemble.pkl",  "Soft voting of DT+RF+XGB, saved in 09_voting_ensemble.py."),
        ("Decision Tree",      "models/decision_tree.pkl",    "Baseline DT, saved in 06_decision_tree.py."),
        ("Confidence Score",   "predictor.py",                "predict_proba() used; max class probability returned as confidence %."),
        ("Column Validation",  "predictor.py",                "Missing/extra columns detected and reported before inference runs."),
    ],
    col_widths=[1.6, 1.8, 2.8]
)

sp(doc)
heading(doc, "7. Evaluation Results on Held-out Test Set", level=1)
para(doc,
    "All metrics below were computed on the held-out test set (85,216 samples — never "
    "seen during training or SMOTE). Precision, Recall, and F1 are for the ATTACK class (positive class = 1)."
)
sp(doc)

heading(doc, "7.1  Performance Metrics", level=2)

# Highlight stacking row differently
tbl_perf = doc.add_table(rows=1, cols=6)
tbl_perf.style = "Table Grid"
tbl_perf.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_p = tbl_perf.rows[0]
shade_row(hdr_p, "0F3660")
for i, txt in enumerate(["Model", "Type", "Accuracy", "Precision", "Recall", "F1 Score"]):
    cell = hdr_p.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(txt)
    set_font(run, 10.5, bold=True, color=(255, 255, 255))

perf_rows = [
    ("Decision Tree",     "Baseline Tree",     "0.9992", "0.9997", "0.9993", "0.9995"),
    ("Random Forest",     "Bagging (100T)",     "0.9993", "0.9999", "0.9993", "0.9996"),
    ("XGBoost",           "Boosting (100R)",    "0.9990", "0.9999", "0.9988", "0.9994"),
    ("Voting Ensemble",   "Soft Voting",        "0.9993", "0.9999", "0.9992", "0.9996"),
    ("Stacking Ensemble", "Meta-Learning (LR)", "0.9994", "0.9999", "0.9993", "0.9996"),
]
for idx, row_data in enumerate(perf_rows):
    is_best = row_data[0] == "Stacking Ensemble"
    bg = "FFF3CD" if is_best else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    row = tbl_perf.add_row()
    for i, txt in enumerate(row_data):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(txt)
        set_font(run, 10, bold=is_best, color=(120, 80, 0) if (is_best and i > 1) else None)
    shade_row(row, bg)

sp(doc)
para(doc, "Best Model: Stacking Ensemble — Accuracy 0.9994, Precision 0.9999, Recall 0.9993, F1 0.9996",
     bold=True, color=(10, 60, 120), size=10.5)

sp(doc)
heading(doc, "7.2  Confusion Matrices (Held-out Test Set: 85,216 samples)", level=2)
make_table(doc,
    ["Model", "TN", "FP", "FN", "TP", "Key Insight"],
    [
        ("Decision Tree",    "18,919", "22", "46",  "66,229", "Good baseline; 22 false alarms"),
        ("Random Forest",    "18,932", "9",  "49",  "66,226", "Low false alarms (FP=9)"),
        ("XGBoost",          "18,937", "4",  "79",  "66,196", "Lowest false alarms (FP=4); higher FN"),
        ("Voting Ensemble",  "18,933", "8",  "51",  "66,224", "Balanced — avg of 3 models"),
        ("Stacking Ensemble","18,932", "9",  "46",  "66,229", "Best: lowest FN (46), only 9 FP"),
    ],
    col_widths=[1.6, 0.65, 0.55, 0.55, 0.85, 2.1]
)

sp(doc)
para(doc,
    "TN = True Negative (Benign correctly identified)  |  FP = False Positive (false alarm — benign misclassified as attack)\n"
    "FN = False Negative (missed attack — critical risk)  |  TP = True Positive (attack correctly detected)",
    size=10, italic=True, color=(80, 80, 80)
)

doc.add_page_break()

# =====================================================================
# PAGE 6 — Technology Stack + Sample Data + Testing + File Structure
# =====================================================================
heading(doc, "8. Technology Stack")
make_table(doc,
    ["Category", "Technology", "Version", "Purpose"],
    [
        ("Backend",       "Python",       "3.11+",   "Core language for ML pipeline and web server"),
        ("Backend",       "Flask",        "3.1.3",   "Web framework and HTTP routing"),
        ("Backend",       "Werkzeug",     "3.1.9",   "WSGI utilities and file upload handling"),
        ("ML",            "scikit-learn", "1.9.1",   "Decision Tree, Random Forest, StandardScaler, Stacking"),
        ("ML",            "XGBoost",      "3.4.0",   "Gradient boosting classifier"),
        ("ML",            "joblib",       "1.6.0",   "Model serialization and loading (.pkl files)"),
        ("Data",          "pandas",       "2.3.3",   "DataFrame operations and CSV parsing"),
        ("Data",          "NumPy",        "2.5.3",   "Array operations for ML preprocessing"),
        ("Frontend",      "Jinja2",       "Built-in", "HTML templating engine for Flask"),
        ("Frontend",      "Chart.js",     "4.4 CDN", "Interactive bar, doughnut, and radar charts"),
        ("Frontend",      "CSS3",         "Custom",  "Dark navy/blue cybersecurity theme"),
        ("Frontend",      "JavaScript",   "ES6",     "Dynamic UI interactions and chart rendering"),
        ("Data Format",   "pyarrow",      "25.0.1",  "Reading original CIC-DDoS2019 Parquet files"),
    ],
    col_widths=[1.2, 1.3, 1.1, 2.7]
)

sp(doc)
heading(doc, "9. Sample Data & End-to-End Testing", level=1)
heading(doc, "9.1  Sample CSV Files", level=2)
make_table(doc,
    ["File", "Contents", "Purpose"],
    [
        ("sample_traffic_benign.csv",       "25 BENIGN flow records",       "Verify correct BENIGN detection"),
        ("sample_traffic_attack.csv",       "25 DDoS ATTACK flow records",  "Verify correct ATTACK detection"),
        ("sample_traffic_mixed.csv",        "50 mixed BENIGN + ATTACK",     "Verify mixed traffic prediction"),
        ("sample_invalid_missing_cols.csv", "CSV with missing columns",     "Test missing-column error handling"),
        ("sample_invalid_non_numeric.csv",  "CSV with non-numeric values",  "Test data type validation"),
    ],
    col_widths=[2.4, 1.8, 2.0]
)

sp(doc)
heading(doc, "9.2  Test Results (test_webapp.py)", level=2)
test_rows = [
    ("Scaler loaded successfully",    "PASS", "StandardScaler, 30 input features"),
    ("All 5 models loaded",           "PASS", "All .pkl files found and loaded without error"),
    ("BENIGN sample prediction",      "PASS", "25/25 = BENIGN with confidence > 99%"),
    ("ATTACK sample prediction",      "PASS", "25/25 = ATTACK with confidence > 98%"),
    ("Mixed sample prediction",       "PASS", "Correct BENIGN/ATTACK proportions detected"),
    ("Missing-column validation",     "PASS", "Descriptive error returned for incomplete CSV"),
    ("Flask HTTP 200 on all routes",  "PASS", "All 5 pages return HTTP 200 OK"),
    ("CSV export / download",         "PASS", "Timestamped CSV generated and downloadable"),
]
make_table(doc,
    ["Test Case", "Result", "Notes"],
    test_rows,
    col_widths=[2.4, 0.8, 3.0]
)

sp(doc)
heading(doc, "10. Project File Structure", level=1)
structure = """\
DDoS_Monitoring/
|-- web_app/                            <- Milestone 5 main deliverable
|   |-- app.py                          <- Flask app: 8 routes
|   |-- predictor.py                    <- ML model loader + predict()
|   |-- test_webapp.py                  <- End-to-end test suite
|   |-- requirements_webapp.txt         <- Pinned dependency versions
|   |-- templates/
|   |   |-- base.html                   <- Sidebar layout, nav, status bar
|   |   |-- dashboard.html              <- Home with stat cards + pipeline
|   |   |-- predict.html                <- CSV upload + results table
|   |   |-- comparison.html             <- Metrics table + 5 charts
|   |   |-- evaluation.html             <- Confusion matrices (5 models)
|   |   `-- about.html                  <- Project info + tech stack
|   |-- static/
|   |   |-- css/style.css               <- Dark navy cybersecurity CSS
|   |   `-- js/charts.js                <- Global Chart.js dark defaults
|   `-- sample_data/
|       |-- sample_traffic_benign.csv   <- 25 BENIGN flow records
|       |-- sample_traffic_attack.csv   <- 25 ATTACK flow records
|       |-- sample_traffic_mixed.csv    <- 50 mixed records
|       |-- sample_invalid_missing_cols.csv
|       `-- sample_invalid_non_numeric.csv
|-- models/
|   |-- scaler.pkl                      <- Fitted StandardScaler
|   |-- decision_tree.pkl               <- Script 06
|   |-- random_forest.pkl               <- Script 07
|   |-- xgboost.pkl                     <- Script 08
|   |-- voting_ensemble.pkl             <- Script 09
|   `-- stacking_ensemble.pkl           <- Script 10 (default)
`-- processed_data/
    `-- feature_names.csv               <- 30 ordered feature names"""

p = doc.add_paragraph()
p.style = "No Spacing"
p.paragraph_format.space_after = Pt(8)
run = p.add_run(structure)
run.font.name = "Courier New"
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(15, 54, 96)

doc.add_page_break()

# =====================================================================
# PAGE 7 — Limitations + Future Scope + Conclusion
# =====================================================================
heading(doc, "11. Limitations")
heading(doc, "11.1  Feature Selection Data Leakage", level=2)
para(doc,
    "Feature selection (Step 4) was performed using a Random Forest trained on the entire "
    "dataset before the train-test split. This means feature importance scores were influenced "
    "by test-set rows, introducing a selection bias. The classification metrics are still valid "
    "because the correct 80/20 stratified split was applied for model training and evaluation. "
    "However, the feature selection step technically constitutes a mild data leakage — the "
    "recommended correction is to perform feature selection inside the training fold only."
)

heading(doc, "11.2  Other Limitations", level=2)
lims = [
    "Offline only: Accepts pre-collected CSV files. No live network packet capture or real-time stream classification.",
    "Local deployment: Flask server runs on localhost (127.0.0.1:5000). Not accessible over the internet.",
    "Binary classification only: Predicts BENIGN or ATTACK. Does not identify the specific DDoS attack type.",
    "Dataset-specific: Trained exclusively on CIC-DDoS2019 synthetic traffic. Real-world generalization may vary.",
    "No cross-validation: Evaluated on a single 80/20 split. K-fold CV would give more robust estimates.",
    "No authentication: Dashboard has no login or access control — suitable for academic demonstration only.",
]
for l in lims:
    bullet(doc, l)

sp(doc)
heading(doc, "12. Future Scope", level=1)
future = [
    "Real-time monitoring: Integrate with live packet capture (scapy / pyshark) for real-time traffic classification.",
    "Multi-class classification: Extend to identify 11 specific DDoS attack types (SYN, UDP, DNS, LDAP, etc.).",
    "Cloud deployment: Deploy on AWS / GCP / Azure using Docker containers and a production WSGI server (gunicorn).",
    "REST API: Expose a JSON API endpoint for integration with SIEM systems.",
    "Deep learning: Experiment with LSTM / CNN for temporal traffic pattern recognition.",
    "Retraining pipeline: Automated retraining when data drift is detected in incoming traffic.",
    "Authentication: Add user authentication and role-based access for enterprise deployment.",
    "Cross-dataset validation: Test trained models on CICIDS-2017 or UNSW-NB15 to measure generalization.",
]
for f in future:
    bullet(doc, f)

sp(doc)
heading(doc, "13. Conclusion", level=1)
para(doc,
    "Milestone 5 successfully completes the Intelligent Network Traffic Monitoring System "
    "project. All five trained machine learning models have been integrated into a professional "
    "Flask web dashboard that provides genuine ML inference on user-uploaded CSV files. "
    "The system demonstrates the practical viability of applying ensemble machine learning "
    "for DDoS traffic detection."
)
para(doc,
    "The Stacking Ensemble — selected as the default deployed model — achieves 99.94% accuracy "
    "with only 46 missed attacks (FN) and 9 false alarms (FP) out of 85,216 test flows. "
    "The web dashboard provides five fully functional pages covering all aspects of the ML "
    "pipeline, from dataset statistics to interactive CSV-based prediction."
)
para(doc,
    "The project successfully fulfills all five milestone objectives: dataset analysis, "
    "preprocessing, model training, ensemble evaluation, and final web deployment. "
    "All trained model artifacts and Python scripts are intact, reproducible, and "
    "documented using random_state=42 throughout the pipeline."
)

sp(doc)

# Final summary metrics table
para(doc, "Final Deployed Model Performance Summary:", bold=True, color=(10, 60, 120), size=11)
sp(doc)

tbl_fin = doc.add_table(rows=1, cols=5)
tbl_fin.style = "Table Grid"
tbl_fin.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_fin = tbl_fin.rows[0]
shade_row(hdr_fin, "0F3660")
for i, txt in enumerate(["Model", "Accuracy", "Precision", "Recall", "F1 Score"]):
    cell = hdr_fin.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(txt)
    set_font(run, 10.5, bold=True, color=(255, 255, 255))

final_data = [
    ("Decision Tree",     "0.9992", "0.9997", "0.9993", "0.9995"),
    ("Random Forest",     "0.9993", "0.9999", "0.9993", "0.9996"),
    ("XGBoost",           "0.9990", "0.9999", "0.9988", "0.9994"),
    ("Voting Ensemble",   "0.9993", "0.9999", "0.9992", "0.9996"),
    ("Stacking Ensemble", "0.9994", "0.9999", "0.9993", "0.9996"),
]
for idx, row_data in enumerate(final_data):
    is_best = row_data[0] == "Stacking Ensemble"
    bg = "FFF3CD" if is_best else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    row = tbl_fin.add_row()
    for i, txt in enumerate(row_data):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(txt)
        set_font(run, 10, bold=is_best)
    shade_row(row, bg)

sp(doc)
para(doc,
    "Stacking Ensemble (Meta-Learning, Logistic Regression) is the best-performing model — "
    "highest accuracy (0.9994) and lowest False Negatives among all ensemble models (FN = 46).",
    bold=True, color=(10, 60, 120), size=10.5
)

sp(doc)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\u2015" * 48)
set_font(run, 11, color=(140, 160, 200))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("End of Milestone 5 Report")
set_font(run, 11, italic=True, color=(100, 100, 120))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Intelligent Network Traffic Monitoring System  |  Aditi Jain  |  " +
                datetime.date.today().strftime("%B %Y"))
set_font(run, 10, color=(120, 120, 140))

# ── Save ──────────────────────────────────────────────────────────────
import pathlib
output = pathlib.Path(__file__).parent / "Milestone_5_Report.docx"
doc.save(str(output))
print("Saved: " + str(output))
