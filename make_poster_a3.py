"""
make_poster_a3.py
=================
Generates  Project_Poster_A3.pdf  — A3 portrait (297mm x 420mm)
Professional cybersecurity dark-theme poster.
Run:  .\\venv\\Scripts\\python.exe make_poster_a3.py
"""

from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import simpleSplit
import math

# ── Palette ──────────────────────────────────────────────────────────
BG          = HexColor("#0a1628")   # very dark navy
HEADER_BG   = HexColor("#0d2044")   # slightly lighter navy
CARD_BG     = HexColor("#112244")   # card background
ACCENT      = HexColor("#1e88e5")   # electric blue
ACCENT2     = HexColor("#00e5ff")   # cyan
GREEN       = HexColor("#00e676")   # bright green (BENIGN)
RED         = HexColor("#ff1744")   # red (ATTACK)
GOLD        = HexColor("#ffd600")   # gold for best model
TEXT_MAIN   = HexColor("#e8f0fe")   # near-white text
TEXT_SUB    = HexColor("#90caf9")   # lighter blue text
TEXT_DARK   = HexColor("#b0bec5")   # grey text
DIVIDER     = HexColor("#1a3a6e")   # subtle divider

W, H = A3  # 297mm x 420mm in points (841.89 x 1190.55)

# ── Canvas ───────────────────────────────────────────────────────────
c = canvas.Canvas("Project_Poster_A3.pdf", pagesize=A3)
c.setTitle("Intelligent Network Traffic Monitoring System - Project Poster")

# ─────────────────────────────────────────────────────────────────────
# BACKGROUND
# ─────────────────────────────────────────────────────────────────────
c.setFillColor(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Subtle grid lines
c.setStrokeColor(DIVIDER)
c.setLineWidth(0.3)
for x in range(0, int(W)+1, 40):
    c.line(x, 0, x, H)
for y in range(0, int(H)+1, 40):
    c.line(0, y, W, y)

# ─────────────────────────────────────────────────────────────────────
# HEADER BAND
# ─────────────────────────────────────────────────────────────────────
header_h = 145
c.setFillColor(HEADER_BG)
c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)

# Blue accent bar top
c.setFillColor(ACCENT)
c.rect(0, H - 6, W, 6, fill=1, stroke=0)

# Cyan accent bar bottom of header
c.setFillColor(ACCENT2)
c.rect(0, H - header_h, W, 3, fill=1, stroke=0)

# Top-left institution tag
c.setFillColor(ACCENT2)
c.setFont("Helvetica-Bold", 10)
c.drawString(28, H - 28, "THIRD YEAR CSE PROJECT  |  MACHINE LEARNING & CYBERSECURITY")

# Main title
c.setFillColor(TEXT_MAIN)
c.setFont("Helvetica-Bold", 34)
title = "Intelligent Network Traffic Monitoring System"
c.drawCentredString(W / 2, H - 68, title)

# Subtitle
c.setFillColor(ACCENT2)
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(W / 2, H - 93, "DDoS Attack Detection using Ensemble Machine Learning  |  CIC-DDoS2019 Dataset")

# Author + Date line
c.setFillColor(TEXT_SUB)
c.setFont("Helvetica", 12)
c.drawCentredString(W / 2, H - 118, "Aditi Jain     |     Python  •  scikit-learn  •  XGBoost  •  Flask     |     November 2026")

# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────
MARGIN  = 22
COL_GAP = 14
NCOLS   = 3
col_w   = (W - 2*MARGIN - (NCOLS-1)*COL_GAP) / NCOLS
col_x   = [MARGIN + i*(col_w + COL_GAP) for i in range(NCOLS)]

body_top    = H - header_h - 14
body_bottom = 52  # footer height

def card(cx, cy, cw, ch, bg=CARD_BG, border=ACCENT, radius=6):
    c.setStrokeColor(border)
    c.setFillColor(bg)
    c.setLineWidth(1.2)
    c.roundRect(cx, cy, cw, ch, radius, fill=1, stroke=1)

def section_title(cx, cy, cw, txt, bg=ACCENT, fg=white, size=12):
    c.setFillColor(bg)
    c.roundRect(cx, cy - 20, cw, 22, 4, fill=1, stroke=0)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(cx + cw/2, cy - 13, txt)
    return cy - 26

def wrap_text(cx, cy, cw, txt, font="Helvetica", size=9.5, color=TEXT_MAIN,
              leading=13, indent=0):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = simpleSplit(txt, font, size, cw - indent*2)
    for line in lines:
        c.drawString(cx + indent, cy, line)
        cy -= leading
    return cy

def bullet_item(cx, cy, cw, txt, dot_color=ACCENT2, size=9.5, indent=14):
    c.setFillColor(dot_color)
    c.circle(cx + 5, cy + 3, 3, fill=1, stroke=0)
    c.setFillColor(TEXT_MAIN)
    c.setFont("Helvetica", size)
    lines = simpleSplit(txt, "Helvetica", size, cw - indent - 6)
    for i, line in enumerate(lines):
        c.drawString(cx + indent, cy, line)
        cy -= 12
    return cy - 2

def metric_badge(cx, cy, label, value, val_color=ACCENT2, w=95, h=52):
    card(cx, cy, w, h, bg=HexColor("#0d1f3c"), border=ACCENT)
    c.setFillColor(val_color)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(cx + w/2, cy + 28, value)
    c.setFillColor(TEXT_SUB)
    c.setFont("Helvetica", 8)
    c.drawCentredString(cx + w/2, cy + 12, label)

def h_line(cx, cy, cw, color=DIVIDER, lw=0.8):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(cx, cy, cx+cw, cy)

# ─────────────────────────────────────────────────────────────────────
# ── COLUMN 1  (left)
# ─────────────────────────────────────────────────────────────────────
x1 = col_x[0]
y  = body_top

# ── CARD 1A: Problem Statement ─────────────────────────────────────
card_h = 160
card(x1, y - card_h, col_w, card_h)
y2 = section_title(x1+6, y - 4, col_w-12, "  PROBLEM STATEMENT")
y2 -= 4
y2 = wrap_text(x1+10, y2, col_w-12,
    "Distributed Denial-of-Service (DDoS) attacks flood network servers with "
    "malicious traffic, rendering services unavailable. Traditional rule-based "
    "firewalls fail against modern, high-volume, multi-vector attacks.",
    size=9, leading=12)
y2 -= 4
y2 = bullet_item(x1+6, y2, col_w-12, "Over 17 million DDoS attacks occur globally every year", size=9)
y2 = bullet_item(x1+6, y2, col_w-12, "Attack traffic mimics legitimate patterns — hard to detect", size=9)
y2 = bullet_item(x1+6, y2, col_w-12, "Manual analysis cannot scale to Gbps network speeds", size=9)
y2 = bullet_item(x1+6, y2, col_w-12, "ML can learn statistical traffic patterns automatically", size=9)
y -= card_h + 12

# ── CARD 1B: Dataset ───────────────────────────────────────────────
card_h = 162
card(x1, y - card_h, col_w, card_h)
y2 = section_title(x1+6, y - 4, col_w-12, "  DATASET: CIC-DDoS2019")
y2 -= 4
y2 = wrap_text(x1+10, y2, col_w-12,
    "Canadian Institute for Cybersecurity benchmark dataset captured on "
    "a realistic network testbed. Contains labelled benign and 11 DDoS attack types.",
    size=9, leading=12)
y2 -= 6

ds_items = [
    ("Source Files",  "17 Parquet files"),
    ("Raw Records",   "500,000+"),
    ("After Cleaning","426,076 rows"),
    ("Raw Features",  "88 columns"),
    ("Selected Feat.","30 best features"),
    ("Train Set",     "340,860 rows  (80%)"),
    ("Post-SMOTE",    "530,194 rows  (balanced)"),
    ("Test Set",      "85,216 rows  (20%, held-out)"),
    ("Attack Types",  "SYN, UDP, DNS, LDAP, MSSQL, NTP..."),
]
for label, val in ds_items:
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(ACCENT2)
    c.drawString(x1+10, y2, label + ":")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(TEXT_MAIN)
    c.drawString(x1+92, y2, val)
    y2 -= 12

y -= card_h + 12

# ── CARD 1C: Preprocessing Pipeline ───────────────────────────────
card_h = 192
card(x1, y - card_h, col_w, card_h)
y2 = section_title(x1+6, y - 4, col_w-12, "  PREPROCESSING PIPELINE")
y2 -= 5

steps = [
    ("01", "Load 17 Parquet files with pyarrow"),
    ("02", "Drop null / infinite / duplicate rows"),
    ("03", "Binary labels: BENIGN=0, ATTACK=1"),
    ("04", "Feature selection: 88 -> 30 features\n     (RandomForest importance + correlation)"),
    ("05", "80/20 stratified train-test split"),
    ("06", "StandardScaler on X_train only"),
    ("07", "SMOTE on training set only\n     (balance classes 50%-50%)"),
]
for num, desc in steps:
    # Step circle
    c.setFillColor(ACCENT)
    c.circle(x1+14, y2+3, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x1+14, y2, num)
    # Text
    lines = simpleSplit(desc, "Helvetica", 8.8, col_w - 36)
    c.setFillColor(TEXT_MAIN)
    for i, line in enumerate(lines):
        c.setFont("Helvetica", 8.8)
        c.drawString(x1+28, y2 - i*11, line)
    # Arrow
    if num != "07":
        c.setFillColor(ACCENT2)
        c.setFont("Helvetica", 8)
        c.drawString(x1+10, y2 - len(lines)*11 + 2, "v")
    y2 -= len(lines)*11 + 5

y -= card_h + 12

# remaining col 1 height => fill with key features card
remaining = y - body_bottom - 12
card_h = remaining
card(x1, body_bottom, col_w, card_h)
y2 = section_title(x1+6, y - 4, col_w-12, "  30 SELECTED FEATURES (TOP 12)")
y2 -= 5
top12 = [
    "Flow Duration",           "Fwd Packet Length Max",
    "Fwd Packet Length Mean",  "Bwd Packet Length Max",
    "Fwd Packets/s",           "Bwd Packets/s",
    "Flow IAT Mean",           "Flow IAT Max",
    "Fwd Header Length",       "Fwd IAT Total",
    "Packet Length Mean",      "Protocol",
]
for feat in top12:
    y2 = bullet_item(x1+6, y2, col_w-12, feat, dot_color=GREEN, size=8.8, indent=12)

# ─────────────────────────────────────────────────────────────────────
# ── COLUMN 2  (middle)
# ─────────────────────────────────────────────────────────────────────
x2 = col_x[1]
y  = body_top

# ── CARD 2A: 5 Models Overview ─────────────────────────────────────
card_h = 220
card(x2, y - card_h, col_w, card_h)
y2 = section_title(x2+6, y - 4, col_w-12, "  5 MODELS TRAINED", bg=HexColor("#1a237e"))
y2 -= 5

models = [
    ("Decision Tree",     "Baseline",           "0.9992", ACCENT2),
    ("Random Forest",     "Bagging (100 trees)", "0.9993", ACCENT),
    ("XGBoost",           "Boosting (100 rounds)","0.9990", HexColor("#ab47bc")),
    ("Voting Ensemble",   "Soft voting DT+RF+XGB","0.9993", HexColor("#26a69a")),
    ("Stacking Ensemble", "Meta-Learning (LR)",  "0.9994", GOLD),
]
for mname, mtype, acc, mcol in models:
    # Model colour bar
    c.setFillColor(mcol)
    c.rect(x2+8, y2-2, 5, 16, fill=1, stroke=0)
    # Name
    c.setFillColor(mcol)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x2+18, y2+8, mname)
    # Type
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica", 8)
    c.drawString(x2+18, y2-1, mtype)
    # Accuracy
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(x2+col_w-10, y2+8, "Acc: " + acc)
    h_line(x2+8, y2-8, col_w-16, color=DIVIDER)
    y2 -= 30

# Best model label
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 8.5)
c.drawCentredString(x2+col_w/2, y2+6,
    "BEST MODEL: Stacking Ensemble  |  Accuracy 99.94%  |  F1: 0.9996")
y -= card_h + 12

# ── CARD 2B: Performance Metrics Table ────────────────────────────
card_h = 178
card(x2, y - card_h, col_w, card_h)
y2 = section_title(x2+6, y - 4, col_w-12, "  PERFORMANCE METRICS (TEST SET: 85,216 SAMPLES)")
y2 -= 8

headers  = ["Model",        "Accuracy", "Precision", "Recall", "F1"]
col_ws   = [92, 50, 54, 46, 44]
data = [
    ("Decision Tree",    "99.92%", "99.97%", "99.93%", "99.95%"),
    ("Random Forest",    "99.93%", "99.99%", "99.93%", "99.96%"),
    ("XGBoost",          "99.90%", "99.99%", "99.88%", "99.94%"),
    ("Voting Ensemble",  "99.93%", "99.99%", "99.92%", "99.96%"),
    ("Stacking Ens.",    "99.94%", "99.99%", "99.93%", "99.96%"),
]
# Header row
rx = x2+8
c.setFillColor(ACCENT)
c.rect(rx, y2-14, sum(col_ws), 16, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 8.5)
hx = rx
for i, (hdr, cw_) in enumerate(zip(headers, col_ws)):
    c.drawCentredString(hx + cw_/2, y2-9, hdr)
    hx += cw_
y2 -= 16

for ridx, (mname, acc, prec, rec, f1) in enumerate(data):
    is_best = "Stacking" in mname
    row_bg = HexColor("#162840") if ridx%2==0 else HexColor("#0e1f38")
    if is_best:
        row_bg = HexColor("#1a2a00")
    c.setFillColor(row_bg)
    c.rect(rx, y2-13, sum(col_ws), 15, fill=1, stroke=0)
    vals = [mname, acc, prec, rec, f1]
    hx = rx
    for i, (val, cw_) in enumerate(zip(vals, col_ws)):
        col_ = GOLD if is_best else (TEXT_MAIN if i==0 else GREEN)
        c.setFillColor(col_)
        c.setFont("Helvetica-Bold" if (is_best or i==0) else "Helvetica", 8.2)
        c.drawCentredString(hx+cw_/2, y2-9, val)
        hx += cw_
    # thin border
    c.setStrokeColor(DIVIDER)
    c.setLineWidth(0.4)
    c.rect(rx, y2-13, sum(col_ws), 15, fill=0, stroke=1)
    y2 -= 15

y -= card_h + 12

# ── CARD 2C: Confusion Matrix Summary ─────────────────────────────
card_h = 150
card(x2, y - card_h, col_w, card_h)
y2 = section_title(x2+6, y - 4, col_w-12, "  CONFUSION MATRIX (STACKING ENSEMBLE — BEST)", bg=HexColor("#1b0000"))
y2 -= 10

# Draw a big 2x2 matrix visually
mx = x2 + 30
my = y2 - 90
cell_w, cell_h = 90, 38

cells = [
    ("True Negative (TN)", "18,932", HexColor("#1b4332"), "Benign correctly\nidentified"),
    ("False Positive (FP)",    "9",    HexColor("#7b0000"), "False alarm\n(benign -> attack)"),
    ("False Negative (FN)",   "46",   HexColor("#7c4700"), "Missed attack!\n(critical risk)"),
    ("True Positive (TP)",  "66,229", HexColor("#145a32"), "Attack correctly\ndetected"),
]
for i, (lbl, val, bg, desc) in enumerate(cells):
    cx_ = mx + (i % 2) * (cell_w+4)
    cy_ = my + (1 - i//2) * (cell_h+4)
    c.setFillColor(bg)
    c.roundRect(cx_, cy_, cell_w, cell_h, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(cx_+cell_w/2, cy_+22, val)
    c.setFillColor(HexColor("#dddddd"))
    c.setFont("Helvetica", 7)
    c.drawCentredString(cx_+cell_w/2, cy_+10, lbl)

# Labels
c.setFillColor(TEXT_SUB)
c.setFont("Helvetica-Bold", 8)
c.drawCentredString(mx+cell_w/2,    my + 2*cell_h+16, "Predicted BENIGN")
c.drawCentredString(mx+cell_w+4+cell_w/2, my + 2*cell_h+16, "Predicted ATTACK")

# right text block
rx2 = mx + 2*cell_w + 20
ry2 = my + 2*cell_h + 10
c.setFillColor(TEXT_DARK)
c.setFont("Helvetica", 8)
notes = ["Test size: 85,216", "Benign:  18,941", "Attack:  66,275", "", "FP=9 (false alarms)",
         "FN=46 (missed attacks)"]
for note in notes:
    c.drawString(rx2, ry2, note)
    ry2 -= 11

y -= card_h + 12

# remaining col2 -> why ensemble
remaining = y - body_bottom - 12
card_h = remaining
card(x2, body_bottom, col_w, card_h)
y2 = section_title(x2+6, y-4, col_w-12, "  WHY ENSEMBLE LEARNING?", bg=HexColor("#0d3d0d"))
y2 -= 5
ens_points = [
    "Single models are prone to overfitting specific patterns",
    "Voting combines DT + RF + XGBoost — reduces individual bias",
    "Stacking uses meta-learner (Logistic Regression) to optimally weight base model predictions",
    "Ensemble achieves lowest FN (46) — fewest missed attacks",
    "Bagging (RF): reduces variance by averaging 100 trees",
    "Boosting (XGBoost): corrects errors of previous trees sequentially",
    "Meta-Learning: learns WHEN to trust each base model",
]
for pt in ens_points:
    y2 = bullet_item(x2+6, y2, col_w-12, pt, dot_color=GOLD, size=9)


# ─────────────────────────────────────────────────────────────────────
# ── COLUMN 3  (right)
# ─────────────────────────────────────────────────────────────────────
x3 = col_x[2]
y  = body_top

# ── CARD 3A: 4 Big Metric Badges ───────────────────────────────────
card_h = 110
card(x3, y - card_h, col_w, card_h)
y2 = section_title(x3+6, y-4, col_w-12, "  KEY RESULTS AT A GLANCE", bg=HexColor("#0d3b2e"))

badges = [
    ("Total Records",   "426,076",  TEXT_MAIN),
    ("Features Used",   "30",       ACCENT2),
    ("Models Trained",  "5",        ACCENT),
    ("Best Accuracy",   "99.94%",   GREEN),
]
bx = x3 + 10
for label, val, vcol in badges:
    metric_badge(bx, y - card_h + 10, label, val, val_color=vcol, w=col_w/4 - 6, h=56)
    bx += col_w/4 + 2

y -= card_h + 12

# ── CARD 3B: Web Dashboard ─────────────────────────────────────────
card_h = 198
card(x3, y - card_h, col_w, card_h)
y2 = section_title(x3+6, y-4, col_w-12, "  FLASK WEB DASHBOARD", bg=HexColor("#1a0050"))
y2 -= 4

c.setFillColor(ACCENT2)
c.setFont("Helvetica-Bold", 9)
c.drawString(x3+10, y2, "URL:  http://127.0.0.1:5000")
y2 -= 16

pages = [
    ("Dashboard",        "Stat cards, 10-step pipeline flow, best model summary"),
    ("Traffic Prediction","CSV upload -> real ML inference -> BENIGN/ATTACK table"),
    ("Model Comparison", "Side-by-side metrics, bar charts, radar chart"),
    ("Evaluation",       "Confusion matrices for all 5 models"),
    ("About",            "Dataset, pipeline, tech stack, limitations"),
]
for pname, pdesc in pages:
    c.setFillColor(ACCENT)
    c.roundRect(x3+8, y2-2, 8, 10, 2, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(x3+21, y2+6, pname)
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica", 8.3)
    lines = simpleSplit(pdesc, "Helvetica", 8.3, col_w-26)
    for line in lines:
        c.drawString(x3+21, y2-3, line)
        y2 -= 11
    y2 -= 10

y2 -= 3
c.setFillColor(GREEN)
c.setFont("Helvetica-Bold", 8.5)
c.drawString(x3+10, y2, "Real ML Inference | No hardcoded results | CSV Download supported")

y -= card_h + 12

# ── CARD 3C: Technology Stack ──────────────────────────────────────
card_h = 135
card(x3, y - card_h, col_w, card_h)
y2 = section_title(x3+6, y-4, col_w-12, "  TECHNOLOGY STACK", bg=HexColor("#1a2000"))
y2 -= 6

tech = [
    ("Python 3.11",       "Core language"),
    ("scikit-learn 1.9",  "DT, RF, Stacking, StandardScaler"),
    ("XGBoost 3.4",       "Gradient boosting"),
    ("pandas / NumPy",    "Data processing"),
    ("imbalanced-learn",  "SMOTE oversampling"),
    ("Flask 3.1.3",       "Web framework"),
    ("Chart.js 4.4",      "Interactive charts"),
    ("joblib 1.6",        "Model serialization (.pkl)"),
]
for tname, tdesc in tech:
    c.setFillColor(ACCENT2)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x3+10, y2, tname)
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica", 8.2)
    c.drawString(x3+115, y2, tdesc)
    y2 -= 12

y -= card_h + 12

# ── CARD 3D: Results Highlights & Impact ──────────────────────────
card_h = 148
card(x3, y - card_h, col_w, card_h)
y2 = section_title(x3+6, y-4, col_w-12, "  RESULTS & IMPACT", bg=HexColor("#3d0000"))
y2 -= 5

highlights = [
    "Stacking Ensemble achieves 99.94% accuracy on 85,216 test samples",
    "Only 9 false positives — reduces unnecessary blocking of legitimate users",
    "Only 46 missed attacks (FN) — critical for security reliability",
    "SMOTE resolved 78%-22% class imbalance without touching test data",
    "30 features selected from 88 — improves speed with no accuracy loss",
    "CSV-based demo: teacher can upload any 30-feature network flow file",
    "Prediction confidence from model.predict_proba() — scientifically valid",
]
for h in highlights:
    y2 = bullet_item(x3+6, y2, col_w-12, h, dot_color=GOLD, size=9)

y -= card_h + 12

# remaining col3 -> limitations + future
remaining = y - body_bottom - 12
card_h = remaining
card(x3, body_bottom, col_w, card_h)
y2 = section_title(x3+6, y-4, col_w-12, "  LIMITATIONS & FUTURE SCOPE", bg=HexColor("#3d2000"))
y2 -= 5

c.setFillColor(RED)
c.setFont("Helvetica-Bold", 8.5)
c.drawString(x3+10, y2, "Current Limitations:")
y2 -= 13
lims = [
    "Offline only — no live packet capture",
    "Binary classification (not multi-class)",
    "Feature selection performed pre-split (mild leakage)",
    "Tested only on CIC-DDoS2019 dataset",
]
for l in lims:
    y2 = bullet_item(x3+6, y2, col_w-12, l, dot_color=RED, size=8.8)

y2 -= 5
c.setFillColor(GREEN)
c.setFont("Helvetica-Bold", 8.5)
c.drawString(x3+10, y2, "Future Scope:")
y2 -= 13
fut = [
    "Integrate with scapy for live packet capture",
    "Extend to 11-class multi-label DDoS classification",
    "Deploy on cloud (AWS/GCP) with Docker + gunicorn",
    "Add auto-retraining pipeline for data drift detection",
]
for f in fut:
    y2 = bullet_item(x3+6, y2, col_w-12, f, dot_color=GREEN, size=8.8)


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
c.setFillColor(HEADER_BG)
c.rect(0, 0, W, 46, fill=1, stroke=0)

c.setFillColor(ACCENT)
c.rect(0, 46, W, 2, fill=1, stroke=0)

c.setFillColor(TEXT_MAIN)
c.setFont("Helvetica-Bold", 10)
c.drawCentredString(W/2, 28, "Intelligent Network Traffic Monitoring System  —  DDoS Detection using Ensemble Machine Learning")

c.setFillColor(TEXT_SUB)
c.setFont("Helvetica", 9)
c.drawString(MARGIN, 12, "Dataset: CIC-DDoS2019  |  5 Models: Decision Tree, Random Forest, XGBoost, Voting Ensemble, Stacking Ensemble")
c.drawRightString(W - MARGIN, 12, "Submitted by: Aditi Jain  |  November 2026  |  http://127.0.0.1:5000")

# ─────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────
c.save()
print("Poster saved: Project_Poster_A3.pdf")
