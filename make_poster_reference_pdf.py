"""
make_poster_reference_pdf.py
Builds a visually striking, graph-heavy A3 Research Poster (PDF)
strictly following the user's reference template style.
Page: A3 Portrait (297mm x 420mm)
"""

import os
from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import simpleSplit

W, H = A3  # 841.89 x 1190.55 points

# Colors inspired by reference template
TEAL_HEADER   = HexColor("#1b5e6f")  # Deep academic teal
TEAL_DARK     = HexColor("#11424f")  # Dark teal
TEAL_LIGHT    = HexColor("#e8f4f7")  # Very light teal card background
BORDER_TEAL   = HexColor("#297e93")  # Card border teal
ACCENT_CYAN   = HexColor("#00acc1")  # Cyan accent
ACCENT_GOLD   = HexColor("#f57f17")  # Golden accent
ACCENT_GREEN  = HexColor("#2e7d32")  # Green for benign/positive
ACCENT_RED    = HexColor("#c62828")  # Red for attacks
CARD_BG       = HexColor("#ffffff")  # White card bg
PAGE_BG       = HexColor("#f4f7f9")  # Off-white/slate light background
TEXT_DARK     = HexColor("#212529")  # Dark charcoal text
TEXT_MUTED    = HexColor("#555555")  # Muted grey text

c = canvas.Canvas("Project_Poster_A3_Visual.pdf", pagesize=A3)
c.setTitle("Intelligent Network Traffic Monitoring System - Research Poster")

# 1. Page Background
c.setFillColor(PAGE_BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Helper: Card with optional header pill
def draw_card(x, y, w, h, title=None, fill_color=CARD_BG, border_color=BORDER_TEAL, lw=1.2, radius=4):
    c.setStrokeColor(border_color)
    c.setFillColor(fill_color)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    
    if title:
        # Title banner
        c.setFillColor(TEAL_HEADER)
        c.roundRect(x, y + h - 22, w, 22, radius, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x + 10, y + h - 16, title.upper())

# ─────────────────────────────────────────────────────────────────────
# 1. HEADER BANNER (Exact reference layout)
# ─────────────────────────────────────────────────────────────────────
header_h = 130
header_y = H - header_h - 10
margin = 16
c.setFillColor(TEAL_HEADER)
c.roundRect(margin, header_y, W - 2*margin, header_h, 6, fill=1, stroke=0)

# Left: University / Security Emblem Shield
c.setFillColor(white)
c.roundRect(margin + 12, header_y + 12, 100, header_h - 24, 6, fill=1, stroke=0)
c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(margin + 62, header_y + 80, "CSE DEPT")
c.setFont("Helvetica-Bold", 9)
c.drawCentredString(margin + 62, header_y + 64, "MITS GWALIOR")
c.setFont("Helvetica", 7.5)
c.setFillColor(TEXT_MUTED)
c.drawCentredString(margin + 62, header_y + 48, "Estd. 1957")
c.drawCentredString(margin + 62, header_y + 32, "Cybersecurity Lab")

# Right: QR Code Card
qr_w = 90
qr_x = W - margin - qr_w - 12
c.setFillColor(white)
c.roundRect(qr_x, header_y + 8, qr_w, header_h - 16, 6, fill=1, stroke=0)
c.drawImage("poster_assets/github_qr.png", qr_x + 10, header_y + 26, width=70, height=70)
c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 7)
c.drawCentredString(qr_x + 45, header_y + 14, "SCAN GITHUB REPO")

# Center: Title & Authors
center_x = margin + 125
center_w = qr_x - center_x - 15

c.setFillColor(white)
c.setFont("Helvetica-Bold", 23)
title = "Intelligent Network Traffic Monitoring System"
c.drawString(center_x, header_y + 86, title)

c.setFont("Helvetica-Bold", 13)
c.setFillColor(HexColor("#b2ebf2"))
sub = "DDoS Attack Detection & Real-Time Flow Classification Using Stacking Ensemble Learning"
c.drawString(center_x, header_y + 65, sub)

c.setFont("Helvetica-Bold", 11)
c.setFillColor(white)
c.drawString(center_x, header_y + 40, "Author: Aditi Jain")
c.setFont("Helvetica", 9.5)
c.setFillColor(HexColor("#e0f7fa"))
c.drawString(center_x, header_y + 22, "Department of Computer Science & Engineering, Madhav Institute of Technology & Science (MITS)")

# ─────────────────────────────────────────────────────────────────────
# 2. TOP SECTION: INTRODUCTION (Left) + METHODS / PIPELINE (Right)
# ─────────────────────────────────────────────────────────────────────
top_y = header_y - 12
row1_h = 168
row1_y = top_y - row1_h

intro_w = 270
methods_w = (W - 2*margin) - intro_w - 12
methods_x = margin + intro_w + 12

# Left: INTRODUCTION CARD
draw_card(margin, row1_y, intro_w, row1_h, title="Introduction")
iy = row1_y + row1_h - 32

intro_bullets = [
    ("DDoS Attacks Surge:", "Malicious traffic floods overwhelm servers, causing critical service downtime."),
    ("Rule-Based Failure:", "Traditional firewalls fail against dynamic, high-volume multi-vector DDoS."),
    ("Machine Learning Power:", "Supervised ML learns subtle, multi-dimensional traffic flow behaviors automatically.")
]

for title_b, text_b in intro_bullets:
    c.setFillColor(TEAL_HEADER)
    c.circle(margin + 14, iy - 3, 2.5, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(TEAL_DARK)
    c.drawString(margin + 22, iy, title_b)
    iy -= 11
    c.setFont("Helvetica", 7.8)
    c.setFillColor(TEXT_DARK)
    lines = simpleSplit(text_b, "Helvetica", 7.8, intro_w - 32)
    for line in lines:
        c.drawString(margin + 22, iy, line)
        iy -= 10
    iy -= 4

# Question / Hypothesis Callout Box
hyp_h = 36
c.setFillColor(HexColor("#e0f2f1"))
c.roundRect(margin + 8, row1_y + 8, intro_w - 16, hyp_h, 4, fill=1, stroke=1)
c.setFillColor(TEAL_HEADER)
c.setFont("Helvetica-Bold", 14)
c.drawString(margin + 14, row1_y + 20, "?")
c.setFont("Helvetica-Bold", 8)
c.drawString(margin + 28, row1_y + 27, "RESEARCH HYPOTHESIS:")
c.setFont("Helvetica-Oblique", 7.2)
c.setFillColor(TEXT_DARK)
c.drawString(margin + 28, row1_y + 17, "Can Stacking Ensemble minimize False Negatives")
c.drawString(margin + 28, row1_y + 9, "while preserving 99.9%+ classification accuracy?")

# Right: METHODS / PIPELINE (3-Step Chevron Flow matching reference)
draw_card(methods_x, row1_y, methods_w, row1_h, title="Methods & Experimental Workflow")

step_w = (methods_w - 24) / 3
step_y = row1_y + 10
step_h = row1_h - 40

steps_data = [
    ("STEP 1", "Data Engineering", [
        "17 CIC-DDoS2019 Parquet files",
        "426,076 Cleaned flow records",
        "Dropped nulls & duplicate rows",
        "Binary Labels: BENIGN (0), ATTACK (1)"
    ], HexColor("#e1f5fe")),
    ("STEP 2", "Feature Optimization", [
        "88 -> 30 Features (RF Importance)",
        "Stratified 80/20 train/test split",
        "StandardScaler fitted on train set",
        "SMOTE balanced 530,194 samples"
    ], HexColor("#e0f2f1")),
    ("STEP 3", "Ensemble & Inference", [
        "5 Models: DT, RF, XGB, Voting, Stacking",
        "Meta-Learner: Logistic Regression",
        "99.94% accuracy on held-out test set",
        "Flask Dashboard for CSV batch demo"
    ], HexColor("#fff8e1"))
]

for idx, (s_num, s_title, s_bullets, s_bg) in enumerate(steps_data):
    sx = methods_x + 8 + idx * (step_w + 4)
    c.setStrokeColor(BORDER_TEAL)
    c.setFillColor(s_bg)
    c.roundRect(sx, step_y, step_w, step_h, 4, fill=1, stroke=1)
    
    # Step header
    c.setFillColor(TEAL_HEADER)
    c.roundRect(sx + 6, step_y + step_h - 22, step_w - 12, 18, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(sx + step_w/2, step_y + step_h - 15, f"{s_num}: {s_title}")
    
    # Bullets
    by = step_y + step_h - 34
    for b_text in s_bullets:
        c.setFillColor(TEAL_DARK)
        c.circle(sx + 10, by - 2, 2, fill=1, stroke=0)
        c.setFont("Helvetica", 8)
        c.setFillColor(TEXT_DARK)
        c.drawString(sx + 16, by, b_text)
        by -= 16

# ─────────────────────────────────────────────────────────────────────
# 3. MIDDLE SECTION: RESULTS & VISUALIZATIONS (The Big Showcase)
# ─────────────────────────────────────────────────────────────────────
row2_top = row1_y - 12
row2_h = 490
row2_y = row2_top - row2_h

draw_card(margin, row2_y, W - 2*margin, row2_h, title="Results & System Performance Demonstration")

col3_w = (W - 2*margin - 24) / 3
col1_x = margin + 8
col2_x = col1_x + col3_w + 4
col3_x = col2_x + col3_w + 4
col_h = row2_h - 34
col_y = row2_y + 8

# ── SUB-COLUMN 1: Objective 1 - Feature Optimization ──
c.setStrokeColor(HexColor("#dcdcdc"))
c.setFillColor(white)
c.roundRect(col1_x, col_y, col3_w, col_h, 4, fill=1, stroke=1)

c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 10.5)
c.drawString(col1_x + 10, col_y + col_h - 18, "OBJECTIVE 1: Flow Feature Selection")
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_MUTED)
c.drawString(col1_x + 10, col_y + col_h - 30, "Random Forest importance ranking reduced 88 -> 30 features.")

# Feature importance chart
c.drawImage("poster_assets/feature_importance.png", col1_x + 6, col_y + col_h - 220, width=col3_w - 12, height=180)

c.setFont("Helvetica-Bold", 8)
c.setFillColor(TEAL_HEADER)
c.drawString(col1_x + 10, col_y + col_h - 232, "Figure 1. Relative Importance Score (Top 6 Selected Features)")

# Donut chart: Traffic distribution
c.drawImage("poster_assets/donut_distribution.png", col1_x + 20, col_y + 70, width=col3_w - 40, height=140)
c.setFont("Helvetica-Bold", 8)
c.drawString(col1_x + 10, col_y + 60, "Figure 2. CIC-DDoS2019 Cleaned Traffic Balance (426K flows)")

# Objective 1 concluding sentence
c.setFillColor(HexColor("#e8f5e9"))
c.roundRect(col1_x + 8, col_y + 8, col3_w - 16, 42, 3, fill=1, stroke=0)
c.setFillColor(HexColor("#2e7d32"))
c.setFont("Helvetica-Bold", 8)
c.drawString(col1_x + 14, col_y + 34, "> Concluding Outcome 1:")
c.setFont("Helvetica", 7.8)
c.setFillColor(TEXT_DARK)
c.drawString(col1_x + 14, col_y + 22, "Selecting top 30 features achieved 66% dimension reduction")
c.drawString(col1_x + 14, col_y + 12, "while retaining 100% predictive power and boosting speed.")

# ── SUB-COLUMN 2: Objective 2 - Monitoring Architecture (Central Brain equivalent) ──
c.setStrokeColor(HexColor("#dcdcdc"))
c.setFillColor(white)
c.roundRect(col2_x, col_y, col3_w, col_h, 4, fill=1, stroke=1)

c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 10.5)
c.drawString(col2_x + 10, col_y + col_h - 18, "OBJECTIVE 2: Detection Architecture")
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_MUTED)
c.drawString(col2_x + 10, col_y + col_h - 30, "Multi-tier ensemble processing & real-time classification.")

# Main Architecture Diagram
c.drawImage("poster_assets/architecture_diagram.png", col2_x + 6, col_y + col_h - 250, width=col3_w - 12, height=215)
c.setFont("Helvetica-Bold", 8)
c.setFillColor(TEAL_HEADER)
c.drawString(col2_x + 10, col_y + col_h - 262, "Figure 3. Intelligent Traffic Monitoring & Stacking Workflow")

# 3 Callout Cards matching reference
callouts = [
    ("1", "Base Learners Layer:", "DT, RF, and XGBoost evaluate incoming flow vectors simultaneously."),
    ("2", "Meta-Learner Engine:", "Logistic Regression weighs individual model outputs to minimize errors."),
    ("3", "Web Dashboard Inference:", "Flask application serves instant classification with confidence score.")
]

cy = col_y + col_h - 280
for c_num, c_title, c_desc in callouts:
    c.setFillColor(TEAL_HEADER)
    c.circle(col2_x + 16, cy - 2, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(col2_x + 16, cy - 5, c_num)
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(TEAL_DARK)
    c.drawString(col2_x + 30, cy, c_title)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(TEXT_DARK)
    lines = simpleSplit(c_desc, "Helvetica", 7.5, col3_w - 42)
    for line in lines:
        cy -= 10
        c.drawString(col2_x + 30, cy, line)
    cy -= 8

# Concluding Outcome 2
c.setFillColor(HexColor("#e3f2fd"))
c.roundRect(col2_x + 8, col_y + 8, col3_w - 16, 42, 3, fill=1, stroke=0)
c.setFillColor(HexColor("#1565c0"))
c.setFont("Helvetica-Bold", 8)
c.drawString(col2_x + 14, col_y + 34, "> Concluding Outcome 2:")
c.setFont("Helvetica", 7.8)
c.setFillColor(TEXT_DARK)
c.drawString(col2_x + 14, col_y + 22, "Stacking meta-learner dynamically resolves edge cases,")
c.drawString(col2_x + 14, col_y + 12, "eliminating single-model bias and providing robust inference.")

# ── SUB-COLUMN 3: Objective 3 - Performance Comparison ──
c.setStrokeColor(HexColor("#dcdcdc"))
c.setFillColor(white)
c.roundRect(col3_x, col_y, col3_w, col_h, 4, fill=1, stroke=1)

c.setFillColor(TEAL_DARK)
c.setFont("Helvetica-Bold", 10.5)
c.drawString(col3_x + 10, col_y + col_h - 18, "OBJECTIVE 3: Benchmark & Evaluation")
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_MUTED)
c.drawString(col3_x + 10, col_y + col_h - 30, "Testing across 85,216 unseen held-out network traffic flows.")

# Model comparison chart
c.drawImage("poster_assets/model_comparison.png", col3_x + 6, col_y + col_h - 220, width=col3_w - 12, height=180)
c.setFont("Helvetica-Bold", 8)
c.setFillColor(TEAL_HEADER)
c.drawString(col3_x + 10, col_y + col_h - 232, "Figure 4. Accuracy & F1-Score Comparison Across 5 Models")

# Confusion Matrix Heatmap
c.drawImage("poster_assets/confusion_matrix.png", col3_x + 14, col_y + 70, width=col3_w - 28, height=140)
c.setFont("Helvetica-Bold", 8)
c.drawString(col3_x + 10, col_y + 60, "Figure 5. Stacking Confusion Matrix (Test Size = 85,216 flows)")

# Concluding Outcome 3
c.setFillColor(HexColor("#fff3e0"))
c.roundRect(col3_x + 8, col_y + 8, col3_w - 16, 42, 3, fill=1, stroke=0)
c.setFillColor(HexColor("#e65100"))
c.setFont("Helvetica-Bold", 8)
c.drawString(col3_x + 14, col_y + 34, "> Concluding Outcome 3:")
c.setFont("Helvetica", 7.8)
c.setFillColor(TEXT_DARK)
c.drawString(col3_x + 14, col_y + 22, "Stacking Ensemble achieved lowest False Negatives (FN = 46)")
c.drawString(col3_x + 14, col_y + 12, "and only 9 False Positives out of 85,216 test traffic flows.")

# ─────────────────────────────────────────────────────────────────────
# 4. BOTTOM SECTION: DISCUSSION (Left) + CONCLUSION & REFERENCES (Right)
# ─────────────────────────────────────────────────────────────────────
row3_top = row2_y - 12
row3_h = 240
row3_y = row3_top - row3_h

# Left: DISCUSSION CARD
disc_w = 470
draw_card(margin, row3_y, disc_w, row3_h, title="Discussion & Key Study Findings")
dy = row3_y + row3_h - 34

# 3 Outcome Branch Blocks matching reference
branch_w = (disc_w - 32) / 3
branch_data = [
    ("99.94% Accuracy", "Highest score across 85,216 test flows", HexColor("#e8f5e9"), HexColor("#2e7d32")),
    ("FN = 46 (Lowest)", "Missed rate < 0.07%, high security", HexColor("#fff3e0"), HexColor("#e65100")),
    ("FP = 9 (Minimal)", "Only 9 false alarms in 18,941 normal", HexColor("#e1f5fe"), HexColor("#0277bd"))
]

for idx, (b_title, b_desc, b_bg, b_fg) in enumerate(branch_data):
    bx = margin + 10 + idx * (branch_w + 6)
    c.setStrokeColor(BORDER_TEAL)
    c.setFillColor(b_bg)
    c.roundRect(bx, dy - 42, branch_w, 46, 3, fill=1, stroke=1)
    c.setFillColor(b_fg)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(bx + branch_w/2, dy - 14, b_title)
    c.setFont("Helvetica", 7.2)
    c.setFillColor(TEXT_DARK)
    c.drawCentredString(bx + branch_w/2, dy - 30, b_desc)

dy -= 56

# Discussion Bullets
c.setFont("Helvetica-Bold", 8.5)
c.setFillColor(TEAL_DARK)
c.drawString(margin + 12, dy, "Cybersecurity Interpretation:")
dy -= 12
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_DARK)
c.drawString(margin + 12, dy, "* Minimizing False Negatives is critical: missing an active DDoS flood allows server crashes.")
dy -= 11
c.drawString(margin + 12, dy, "* High precision (FP=9) prevents blocking legitimate university or enterprise web users.")
dy -= 16

c.setFont("Helvetica-Bold", 8.5)
c.setFillColor(HexColor("#c62828"))
c.drawString(margin + 12, dy, "Study Limitations:")
dy -= 12
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_DARK)
c.drawString(margin + 12, dy, "* Offline flow processing only (no kernel packet capture / Scapy hook implemented).")
dy -= 11
c.drawString(margin + 12, dy, "* Binary classification only (identifies attack vs benign, not specific DDoS sub-type).")

# Right: CONCLUSION & REFERENCES CARD
conc_w = (W - 2*margin) - disc_w - 12
conc_x = margin + disc_w + 12
draw_card(conc_x, row3_y, conc_w, row3_h, title="Conclusion & Future Scope")
cy = row3_y + row3_h - 32

c.setFont("Helvetica-Bold", 8.5)
c.setFillColor(TEAL_DARK)
c.drawString(conc_x + 10, cy, "Summary of Findings:")
cy -= 12
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_DARK)
c.drawString(conc_x + 10, cy, "> Stacking Ensemble outperformed all individual base classifiers.")
cy -= 11
c.drawString(conc_x + 10, cy, "> SMOTE effectively resolved 78:22 class imbalance without test leakage.")
cy -= 16

c.setFont("Helvetica-Bold", 8.5)
c.setFillColor(TEAL_DARK)
c.drawString(conc_x + 10, cy, "Future Directions:")
cy -= 12
c.setFont("Helvetica", 8)
c.setFillColor(TEXT_DARK)
c.drawString(conc_x + 10, cy, "> Integration with Scapy/eBPF for live network packet interception.")
cy -= 11
c.drawString(conc_x + 10, cy, "> Multi-class extension to pinpoint 11 attack sub-types (SYN, UDP, etc.).")
cy -= 16

# Take-Home Message Callout
c.setFillColor(HexColor("#e0f2f1"))
c.roundRect(conc_x + 8, cy - 36, conc_w - 16, 42, 4, fill=1, stroke=1)
c.setFillColor(TEAL_HEADER)
c.setFont("Helvetica-Bold", 8.5)
c.drawString(conc_x + 14, cy - 10, "TAKE-HOME MESSAGE:")
c.setFont("Helvetica-Bold", 7.8)
c.setFillColor(TEXT_DARK)
c.drawString(conc_x + 14, cy - 22, "Ensemble meta-learning delivers optimal sensitivity and")
c.drawString(conc_x + 14, cy - 32, "reliability, making AI-driven network protection feasible.")

cy -= 46
# References section at bottom
c.setFont("Helvetica-Bold", 7.5)
c.setFillColor(TEAL_DARK)
c.drawString(conc_x + 10, cy, "References & Open Source Repository:")
cy -= 10
c.setFont("Helvetica", 6.8)
c.setFillColor(TEXT_MUTED)
c.drawString(conc_x + 10, cy, "[1] Sharafaldin et al., 'Developing Realistic DDoS Datasets' (CIC-DDoS2019).")
cy -= 9
c.drawString(conc_x + 10, cy, "[2] Pedregosa et al., 'Scikit-learn: Machine Learning in Python' (JMLR).")
cy -= 9
c.drawString(conc_x + 10, cy, "[3] GitHub: github.com/JainAditi123/Intelligent-Network-Traffic-Monitoring-System")

# ─────────────────────────────────────────────────────────────────────
# 5. FOOTER LINE
# ─────────────────────────────────────────────────────────────────────
c.setFont("Helvetica", 7.5)
c.setFillColor(TEXT_MUTED)
c.drawString(margin, 8, "Developed by Aditi Jain | Intelligent Network Traffic Monitoring System | Final Year CSE Capstone Demonstration | November 2026")
c.drawRightString(W - margin, 8, "Hosted at: http://127.0.0.1:5000 | Scikit-Learn | XGBoost | Flask | Parquet")

# Save PDF
c.save()
print("Saved Project_Poster_A3_Visual.pdf successfully!")
