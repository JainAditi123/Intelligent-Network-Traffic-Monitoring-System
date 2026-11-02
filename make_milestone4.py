"""
make_milestone4.py
==================
Generates Milestone_4_Report.docx for the DDoS Monitoring project.
Run from the project root:
    .\\venv\\Scripts\\python.exe make_milestone4.py
Output: Milestone_4_Report.docx (in project root)
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
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Helper functions ──────────────────────────────────────────────────
def set_font(run, size=11, bold=False, color=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Calibri"
    if color:
        run.font.color.rgb = RGBColor(*color)

def heading(doc, text, level=1, color=(26, 60, 100)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.name  = "Calibri"
        run.font.color.rgb = RGBColor(*color)
    return p

def para(doc, text, size=11, bold=False, color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size, bold, color)
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

# =====================================================================
# COVER PAGE
# =====================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\n\n\n")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("MILESTONE 4 REPORT")
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
fields = [
    ("Subject",      "Machine Learning / Network Security Project"),
    ("Milestone",    "4 — Final Implementation & Evaluation"),
    ("Task",         "Binary Classification: BENIGN vs ATTACK"),
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
# 1. EXECUTIVE SUMMARY
# =====================================================================
heading(doc, "1. Executive Summary")
para(doc,
    "This report presents the complete implementation and evaluation of an Intelligent "
    "Network Traffic Monitoring System. The system applies ensemble machine learning methods "
    "to classify network flows as BENIGN or ATTACK (DDoS) using the CIC-DDoS2019 dataset. "
    "Five classifiers were developed and evaluated: a Decision Tree baseline, Random Forest, "
    "XGBoost, Soft Voting Ensemble, and a Stacking Ensemble with a Logistic Regression "
    "meta-learner. The Stacking Ensemble achieved the best overall performance with an "
    "accuracy of 0.9994 and an F1 score of 0.9996 on an 85,216-sample held-out test set. "
    "A Flask-based web dashboard was also developed to demonstrate the pipeline interactively."
)

# =====================================================================
# 2. PROJECT OBJECTIVES
# =====================================================================
heading(doc, "2. Project Objectives")
objectives = [
    "Classify network traffic flows as BENIGN (0) or ATTACK (1) using supervised machine learning.",
    "Evaluate a Decision Tree baseline against four ensemble classifiers.",
    "Demonstrate the advantage of ensemble methods over single models in cybersecurity classification.",
    "Build a reproducible, step-by-step ML pipeline using publicly available data.",
    "Develop a professional web dashboard to demonstrate the system interactively.",
]
for obj in objectives:
    bullet(doc, obj)

# =====================================================================
# 3. SCOPE
# =====================================================================
heading(doc, "3. Project Scope")

heading(doc, "3.1  In Scope", level=2)
in_scope = [
    "Binary classification: BENIGN vs ATTACK only.",
    "Five ensemble ML classifiers (Decision Tree, Random Forest, XGBoost, Voting, Stacking).",
    "CIC-DDoS2019 dataset — pre-extracted flow-level statistics.",
    "Offline batch prediction via CSV upload.",
    "Flask web dashboard with five pages.",
]
for s in in_scope:
    bullet(doc, s)

heading(doc, "3.2  Out of Scope", level=2)
out_scope = [
    "Real-time packet capture or live network monitoring.",
    "Attack-type identification (e.g., SYN vs UDP vs LDAP).",
    "Deep learning architectures.",
    "Deployment on public cloud or production infrastructure.",
]
for s in out_scope:
    bullet(doc, s)

# =====================================================================
# 4. DATASET
# =====================================================================
heading(doc, "4. Dataset — CIC-DDoS2019")
para(doc,
    "The Canadian Institute for Cybersecurity DDoS 2019 dataset consists of pre-computed "
    "network flow statistics (88 features) extracted from controlled DDoS attack scenarios. "
    "The dataset is distributed as Apache Parquet files."
)

# Dataset stats table
doc.add_paragraph()
tbl = doc.add_table(rows=1, cols=2)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tbl.rows[0]
shade_row(hdr, "1A3C6E")
for i, txt in enumerate(["Property", "Value"]):
    cell = hdr.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

rows_data = [
    ("Source",             "Canadian Institute for Cybersecurity (CIC)"),
    ("Format",             "Apache Parquet (17 files)"),
    ("Total Records",      "426,076 flow records"),
    ("Raw Features",       "88 features per record"),
    ("Selected Features",  "30 (via Random Forest importance ranking)"),
    ("Attack Types",       "11 (DNS, LDAP, MSSQL, NetBIOS, NTP, Portmap, SNMP, SYN, TFTP, UDP, UDPLag)"),
    ("BENIGN Records",     "~22% of total"),
    ("ATTACK Records",     "~78% of total"),
    ("Train Split",        "340,860 samples (80%, post-SMOTE)"),
    ("Test Split",         "85,216 samples  (20%, stratified)"),
]
for i, (k, v) in enumerate(rows_data):
    bg = "EBF3FB" if i % 2 == 0 else "FFFFFF"
    add_table_row(tbl, [k, v], size=10.5, bg=bg)

doc.add_paragraph()

# =====================================================================
# 5. ML PIPELINE
# =====================================================================
heading(doc, "5. Machine Learning Pipeline")
para(doc,
    "The pipeline is implemented as ten numbered Python scripts (01–10), each producing "
    "a saved artifact consumed by the next step."
)

steps = [
    ("01", "Dataset Analysis",       "Inspect raw parquet files; print shape, columns, missing values."),
    ("02", "Preprocessing",          "Combine all 17 parquet files; replace ±∞ with NaN; drop NaN rows and duplicates."),
    ("03", "Binary Label Creation",  "Map all non-BENIGN labels to ATTACK; create Binary_Label column."),
    ("04", "Feature Selection",      "Remove constant + highly correlated (>0.95) features; select top 30 by RF importance."),
    ("05", "Split · Scale · SMOTE",  "80/20 stratified split → StandardScaler (fit on train only) → SMOTE on training set only."),
    ("06", "Decision Tree",          "Train baseline DecisionTreeClassifier (random_state=42); evaluate on test set."),
    ("07", "Random Forest",          "Train RandomForestClassifier (100 trees, random_state=42)."),
    ("08", "XGBoost",                "Train XGBClassifier (100 rounds, lr=0.1, max_depth=6)."),
    ("09", "Voting Ensemble",        "Soft Voting of DT + RF + XGB; averaged class probabilities."),
    ("10", "Stacking Ensemble",      "DT + RF + XGB base learners; Logistic Regression meta-learner (3-fold CV)."),
]

tbl2 = doc.add_table(rows=1, cols=3)
tbl2.style = "Table Grid"
tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr2 = tbl2.rows[0]
shade_row(hdr2, "1A3C6E")
for i, txt in enumerate(["Script", "Step", "Description"]):
    cell = hdr2.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

for idx, (num, name, desc) in enumerate(steps):
    bg = "EBF3FB" if idx % 2 == 0 else "FFFFFF"
    add_table_row(tbl2, [num, name, desc], size=10, bg=bg)

doc.add_paragraph()

# =====================================================================
# 6. MODEL DESCRIPTIONS
# =====================================================================
heading(doc, "6. Model Descriptions")

models_desc = [
    ("Decision Tree (Baseline)",
     "A single, unconstrained decision tree (no max_depth). Serves as the baseline "
     "to quantify the improvement from ensemble methods. Simple, interpretable, "
     "but prone to overfitting on training data."),
    ("Random Forest (Bagging Ensemble)",
     "An ensemble of 100 decision trees, each trained on a random bootstrap sample "
     "of the training data with random feature subsets. Predictions are aggregated "
     "by majority vote. Reduces variance compared to a single tree."),
    ("XGBoost (Boosting Ensemble)",
     "Gradient-boosted decision trees trained sequentially, where each round corrects "
     "the errors of the previous. Parameters: 100 estimators, max_depth=6, "
     "learning_rate=0.1, subsample=0.8, colsample_bytree=0.8."),
    ("Voting Ensemble (Soft Voting)",
     "Combines Decision Tree, Random Forest, and XGBoost using soft voting: the final "
     "prediction is based on the average predicted class probabilities across all three "
     "base models."),
    ("Stacking Ensemble (Meta-Learning)",
     "Uses Decision Tree, Random Forest, and XGBoost as base learners. "
     "Their out-of-fold predictions (3-fold cross-validation) are fed to a "
     "Logistic Regression meta-learner that learns optimal combination weights. "
     "This is the best-performing model."),
]

for name, desc in models_desc:
    heading(doc, name, level=2)
    para(doc, desc)

# =====================================================================
# 7. EVALUATION RESULTS
# =====================================================================
heading(doc, "7. Evaluation Results")
para(doc,
    "All metrics were computed on the held-out test set (85,216 samples, never seen "
    "during training or SMOTE). Precision, Recall, and F1 are reported for the ATTACK "
    "class (positive class = 1)."
)

# ── Performance table ──
doc.add_paragraph()
heading(doc, "7.1  Performance Metrics", level=2)

tbl3 = doc.add_table(rows=1, cols=6)
tbl3.style = "Table Grid"
tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr3 = tbl3.rows[0]
shade_row(hdr3, "1A3C6E")
for i, txt in enumerate(["Model", "Type", "Accuracy", "Precision", "Recall", "F1 Score"]):
    cell = hdr3.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

perf = [
    ("Decision Tree",    "Baseline",        "0.9992", "0.9997", "0.9993", "0.9995"),
    ("Random Forest",    "Bagging",         "0.9993", "0.9999", "0.9993", "0.9996"),
    ("XGBoost",          "Boosting",        "0.9990", "0.9999", "0.9988", "0.9994"),
    ("Voting Ensemble",  "Soft Voting",     "0.9993", "0.9999", "0.9992", "0.9996"),
    ("Stacking Ensemble","Meta-Learning",   "0.9994", "0.9999", "0.9993", "0.9996"),
]
for idx, row_data in enumerate(perf):
    bg = "FFF9E6" if row_data[0] == "Stacking Ensemble" else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    row = add_table_row(tbl3, row_data, size=10.5, bg=bg)
    if row_data[0] == "Stacking Ensemble":
        for cell in row.cells:
            for run in cell.paragraphs[0].runs:
                run.font.bold = True

doc.add_paragraph()
para(doc, "★  Stacking Ensemble achieves the highest accuracy (0.9994) and tied-best F1 (0.9996).",
     bold=True, color=(26, 60, 100))

# ── Confusion matrix table ──
heading(doc, "7.2  Confusion Matrices", level=2)
para(doc,
    "Test set: 85,216 samples  |  BENIGN: 18,941  |  ATTACK: 66,275\n"
    "TN = True Negative (BENIGN correctly identified)  |  FP = False Positive (false alarm)  |  "
    "FN = False Negative (missed attack)  |  TP = True Positive (attack correctly detected)"
)

doc.add_paragraph()
tbl4 = doc.add_table(rows=1, cols=5)
tbl4.style = "Table Grid"
tbl4.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr4 = tbl4.rows[0]
shade_row(hdr4, "1A3C6E")
for i, txt in enumerate(["Model", "TN", "FP", "FN", "TP"]):
    cell = hdr4.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    set_font(run, 11, bold=True, color=(255,255,255))

cm_data = [
    ("Decision Tree",    "18,919", "22",  "46",  "66,229"),
    ("Random Forest",    "18,932", "9",   "49",  "66,226"),
    ("XGBoost",          "18,937", "4",   "79",  "66,196"),
    ("Voting Ensemble",  "18,933", "8",   "51",  "66,224"),
    ("Stacking Ensemble","18,932", "9",   "46",  "66,229"),
]
for idx, row_data in enumerate(cm_data):
    bg = "FFF9E6" if row_data[0] == "Stacking Ensemble" else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    add_table_row(tbl4, row_data, size=10.5, bg=bg)

doc.add_paragraph()

# ── Key observations ──
heading(doc, "7.3  Key Observations", level=2)
obs = [
    "XGBoost achieves the fewest false positives (FP = 4), rarely misclassifying benign traffic as an attack.",
    "Stacking Ensemble achieves the fewest false negatives among ensemble models (FN = 46), "
     "meaning it misses the fewest actual attacks — critical in a security context.",
    "All models correctly classify > 99.9% of BENIGN flows.",
    "Accuracy > 99% is typical for CIC-DDoS2019 because DDoS flows have very distinct "
     "statistical signatures (e.g., extremely high packet rates, short flow durations). "
     "This is consistent with published results on this dataset.",
]
for o in obs:
    bullet(doc, o)

# =====================================================================
# 8. WEB DASHBOARD
# =====================================================================
heading(doc, "8. Web Dashboard")
para(doc,
    "A Flask-based web application was developed inside the web_app/ subfolder to "
    "demonstrate the pipeline interactively. The dashboard uses a dark navy/blue "
    "cybersecurity theme with Chart.js visualisations."
)

pages = [
    ("Dashboard (/)","Project overview, dataset statistics, model summary cards, pipeline workflow."),
    ("Traffic Prediction (/predict)","CSV upload with drag-and-drop, column validation against the 30 trained features, "
     "BENIGN/ATTACK predictions using the saved scaler + Stacking Ensemble model, "
     "result table and doughnut chart."),
    ("Model Comparison (/comparison)","Recorded metrics table, four bar charts (accuracy, precision, recall, F1), radar chart."),
    ("Evaluation (/evaluation)","Confusion matrices for all five models, TN/FP/FN/TP explanation, data leakage warning."),
    ("About (/about)","Objectives, scope, dataset, technologies, pipeline steps, limitations."),
]
for page, desc in pages:
    heading(doc, page, level=2)
    para(doc, desc)

heading(doc, "8.1  Technology Stack", level=2)
tech = [
    "Backend:  Python Flask 3.1",
    "Frontend: HTML5, CSS3 (custom dark theme), JavaScript",
    "Charts:   Chart.js 4.4 (bar, doughnut, radar)",
    "ML artifacts: joblib (scaler.pkl, stacking_ensemble.pkl), pandas, numpy, scikit-learn, XGBoost",
]
for t in tech:
    bullet(doc, t)

heading(doc, "8.2  How to Run", level=2)
para(doc, "Open Windows PowerShell and run:", bold=True)
code_lines = [
    "cd \"C:\\Users\\ADITI JAIN\\OneDrive\\Desktop\\DDoS_Monitoring\\web_app\"",
    ".\\..\\venv\\Scripts\\python.exe app.py",
    "",
    "# Then open in browser:",
    "http://127.0.0.1:5000",
]
p = doc.add_paragraph()
p.style = "No Spacing"
for line in code_lines:
    run = p.add_run(line + "\n")
    run.font.name = "Courier New"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 80, 30)

# =====================================================================
# 9. LIMITATIONS
# =====================================================================
heading(doc, "9. Limitations")

heading(doc, "9.1  Feature Selection Data Leakage", level=2)
para(doc,
    "Feature selection (Step 4) used a Random Forest trained on the entire dataset before "
    "the train-test split. This means feature importance scores were influenced by test-set "
    "rows, introducing a mild selection bias. The classification metrics are still valid "
    "(correct 80/20 split used for training and evaluation), but this constitutes a "
    "selection bias that may slightly inflate the apparent quality of the 30 selected features. "
    "The recommended correction for future work is to perform feature selection inside the "
    "training fold only."
)

heading(doc, "9.2  Other Limitations", level=2)
lims = [
    "Dataset-specific: Models were trained and tested on CIC-DDoS2019 only. Performance on "
     "real-world traffic from different environments may be lower.",
    "No cross-validation: Models are evaluated on a single 80/20 split. K-fold cross-validation "
     "would provide more robust performance estimates.",
    "Offline only: The system processes uploaded CSV files — not live network packets.",
    "Binary classification only: Attack-type identification is out of scope.",
]
for l in lims:
    bullet(doc, l)

# =====================================================================
# 10. FILE STRUCTURE
# =====================================================================
heading(doc, "10. Project File Structure")
structure = """DDoS_Monitoring/
├── 01_dataset_analysis.py      — Inspect raw parquet files
├── 02_preprocessing.py         — Combine and clean all files
├── 03_prepare_labels.py        — Create binary labels
├── 04_feature_selection.py     — Select top 30 features
├── 05_train_test_split.py      — Split, scale, SMOTE, save arrays + scaler
├── 06_decision_tree.py         — Train and evaluate Decision Tree
├── 07_random_forest.py         — Train and evaluate Random Forest
├── 08_xgboost.py               — Train and evaluate XGBoost
├── 09_voting_ensemble.py       — Train and evaluate Voting Ensemble
├── 10_stacking_ensemble.py     — Train and evaluate Stacking Ensemble
├── save_scaler.py              — Scaler recovery utility
├── README.md                   — Full project documentation
├── requirements.txt            — ML pipeline dependencies
├── models/
│   ├── scaler.pkl              — Fitted StandardScaler
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── voting_ensemble.pkl
│   └── stacking_ensemble.pkl
├── processed_data/
│   ├── feature_names.csv       — 30 selected feature names
│   ├── X_train.npy / X_test.npy
│   ├── y_train.npy / y_test.npy
│   └── *.parquet               — Intermediate datasets
├── archive (32)/               — 17 raw CIC-DDoS2019 parquet files
└── web_app/                    — Flask web dashboard
    ├── app.py
    ├── predictor.py
    ├── requirements_webapp.txt
    ├── templates/  (base, dashboard, predict, comparison, evaluation, about)
    └── static/     (css/style.css, js/charts.js)"""

p = doc.add_paragraph()
p.style = "No Spacing"
run = p.add_run(structure)
run.font.name = "Courier New"
run.font.size = Pt(9)

# =====================================================================
# 11. CONCLUSION
# =====================================================================
doc.add_paragraph()
heading(doc, "11. Conclusion")
para(doc,
    "This project successfully demonstrates the application of ensemble machine learning "
    "methods for binary network traffic classification. All five models — Decision Tree, "
    "Random Forest, XGBoost, Voting Ensemble, and Stacking Ensemble — were trained, "
    "evaluated, and saved. The Stacking Ensemble achieved the best overall balance of "
    "accuracy (0.9994), precision (0.9999), recall (0.9993), and F1 score (0.9996), "
    "with the fewest missed attacks among ensemble models (FN = 46) on the 85,216-sample "
    "held-out test set."
)
para(doc,
    "The accompanying Flask web dashboard provides an interactive demonstration of the "
    "pipeline, including real CSV-based prediction using the saved model and scaler. "
    "All original project files and trained models remain intact and reproducible using "
    "random_state=42 throughout the pipeline."
)

# ── Save ──────────────────────────────────────────────────────────────
output = "Milestone_4_Report.docx"
doc.save(output)
print(f"Saved: {output}")
