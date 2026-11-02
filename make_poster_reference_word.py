"""
make_poster_reference_word.py
Generates an editable Microsoft Word (.docx) version of the
visually rich A3 Research Poster with charts and diagram embedded.
Page: A3 Portrait (297mm x 420mm)
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Mm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# Page Setup: A3 Portrait
for sec in doc.sections:
    sec.page_width = Mm(297)
    sec.page_height = Mm(420)
    sec.top_margin = Mm(8)
    sec.bottom_margin = Mm(8)
    sec.left_margin = Mm(10)
    sec.right_margin = Mm(10)

# Remove default empty paragraph
for para in doc.paragraphs:
    p = para._element
    p.getparent().remove(p)

# Helpers
def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=1, bottom=1, left=2, right=2):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val * 20))
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    for old in tcPr.findall(qn("w:tcMar")):
        tcPr.remove(old)
    tcPr.append(tcMar)

def set_cell_border(cell, color="297E93", sz=6):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        tcBd.append(el)
    for old in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(old)
    tcPr.append(tcBd)

def no_border_cell(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        tcBd.append(el)
    for old in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(old)
    tcPr.append(tcBd)

def add_run(p, text, size=9, bold=False, color="212529", italic=False, font_name="Arial"):
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font_name
    run.font.color.rgb = RGBColor.from_string(color)
    return run

def section_banner(cell, text, bg="1B5E6F", fg="FFFFFF"):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), bg)
    pPr.append(shd)
    add_run(p, f"  {text}  ", size=9.5, bold=True, color=fg)

# 1. HEADER TABLE (3 columns: Logo / Title / QR)
header_tbl = doc.add_table(rows=1, cols=3)
header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
no_border_cell(header_tbl.rows[0].cells[0])
no_border_cell(header_tbl.rows[0].cells[1])
no_border_cell(header_tbl.rows[0].cells[2])

# Left: Logo
c_logo = header_tbl.rows[0].cells[0]
c_logo.width = Mm(35)
set_cell_bg(c_logo, "1B5E6F")
set_cell_margins(c_logo, 4, 4, 4, 4)
c_logo.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p = c_logo.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, "CSE DEPT\nMITS GWALIOR\nEstd. 1957\nCybersecurity Lab", size=9, bold=True, color="FFFFFF")

# Middle: Title
c_title = header_tbl.rows[0].cells[1]
c_title.width = Mm(205)
set_cell_bg(c_title, "1B5E6F")
set_cell_margins(c_title, 4, 4, 4, 4)
c_title.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p = c_title.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
add_run(p, "Intelligent Network Traffic Monitoring System\n", size=20, bold=True, color="FFFFFF")
add_run(p, "DDoS Attack Detection & Real-Time Flow Classification Using Stacking Ensemble Learning\n", size=11, bold=True, color="B2EBF2")
add_run(p, "Author: Aditi Jain   |   Department of CSE, Madhav Institute of Technology & Science (MITS)", size=9.5, bold=False, color="E0F7FA")

# Right: QR
c_qr = header_tbl.rows[0].cells[2]
c_qr.width = Mm(35)
set_cell_bg(c_qr, "1B5E6F")
set_cell_margins(c_qr, 3, 3, 3, 3)
c_qr.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p = c_qr.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(1)
run = p.add_run()
run.add_picture("poster_assets/github_qr.png", width=Inches(1.0))
p2 = c_qr.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p2, "SCAN GITHUB REPO", size=7, bold=True, color="FFFFFF")

# Spacer
p_sp = doc.add_paragraph()
p_sp.paragraph_format.space_before = Pt(3)
p_sp.paragraph_format.space_after = Pt(3)

# 2. ROW 1: INTRODUCTION (Left) + METHODS (Right)
r1_tbl = doc.add_table(rows=1, cols=2)
r1_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
c_intro = r1_tbl.rows[0].cells[0]
c_intro.width = Mm(90)
set_cell_bg(c_intro, "FFFFFF")
set_cell_border(c_intro, color="297E93", sz=6)
set_cell_margins(c_intro, 3, 3, 4, 4)

section_banner(c_intro, "INTRODUCTION")
p = c_intro.add_paragraph()
p.paragraph_format.space_after = Pt(2)
add_run(p, "• DDoS Attacks Surge: ", size=8, bold=True, color="1B5E6F")
add_run(p, "Malicious traffic floods overwhelm servers, causing critical service downtime.\n", size=7.8, color="333333")
add_run(p, "• Rule-Based Failure: ", size=8, bold=True, color="1B5E6F")
add_run(p, "Traditional firewalls fail against dynamic, high-volume multi-vector DDoS.\n", size=7.8, color="333333")
add_run(p, "• Machine Learning Power: ", size=8, bold=True, color="1B5E6F")
add_run(p, "Supervised ML learns subtle, multi-dimensional flow behaviors automatically.", size=7.8, color="333333")

p_hyp = c_intro.add_paragraph()
p_hyp.paragraph_format.space_before = Pt(3)
pPr = p_hyp._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "E0F2F1")
pPr.append(shd)
add_run(p_hyp, " ? RESEARCH HYPOTHESIS:\n", size=8, bold=True, color="1B5E6F")
add_run(p_hyp, " Can Stacking Ensemble minimize False Negatives while keeping 99.9%+ accuracy?", size=7.5, italic=True, color="212529")

# Methods
c_methods = r1_tbl.rows[0].cells[1]
c_methods.width = Mm(185)
set_cell_bg(c_methods, "FFFFFF")
set_cell_border(c_methods, color="297E93", sz=6)
set_cell_margins(c_methods, 3, 3, 4, 4)

section_banner(c_methods, "METHODS & EXPERIMENTAL WORKFLOW")

# Inside Methods: 3 steps mini-table
m_steps = c_methods.add_table(rows=1, cols=3)
no_border_cell(m_steps.rows[0].cells[0])
no_border_cell(m_steps.rows[0].cells[1])
no_border_cell(m_steps.rows[0].cells[2])

steps_content = [
    ("STEP 1: Data Prep", "E1F5FE", [
        "17 CIC-DDoS Parquet files",
        "426,076 Cleaned records",
        "Dropped nulls & duplicates",
        "Labels: BENIGN(0), ATTACK(1)"
    ]),
    ("STEP 2: Features", "E0F2F1", [
        "88 -> 30 Features (RF)",
        "80/20 train/test split",
        "StandardScaler on train set",
        "SMOTE: 530,194 samples"
    ]),
    ("STEP 3: Models", "FFF8E1", [
        "5 Models: DT, RF, XGB, Voting, Stacking",
        "Meta-Learner: Log. Reg.",
        "99.94% accuracy test set",
        "Flask Dashboard demo"
    ])
]

for idx, (st_name, st_bg, st_lines) in enumerate(steps_content):
    c_st = m_steps.rows[0].cells[idx]
    c_st.width = Mm(60)
    set_cell_bg(c_st, st_bg)
    set_cell_border(c_st, color="297E93", sz=4)
    set_cell_margins(c_st, 2, 2, 3, 3)
    p_st = c_st.add_paragraph()
    p_st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_st.paragraph_format.space_after = Pt(2)
    add_run(p_st, st_name, size=8.5, bold=True, color="1B5E6F")
    for line in st_lines:
        p_l = c_st.add_paragraph()
        p_l.paragraph_format.space_after = Pt(1)
        add_run(p_l, f"• {line}", size=7.5, color="333333")

# Spacer
p_sp2 = doc.add_paragraph()
p_sp2.paragraph_format.space_before = Pt(3)
p_sp2.paragraph_format.space_after = Pt(3)

# 3. ROW 2: RESULTS (3 Columns with charts embedded)
r2_banner = doc.add_paragraph()
r2_banner.paragraph_format.space_after = Pt(3)
pPr = r2_banner._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "1B5E6F")
pPr.append(shd)
add_run(r2_banner, "  RESULTS & SYSTEM PERFORMANCE DEMONSTRATION  ", size=10, bold=True, color="FFFFFF")

r2_tbl = doc.add_table(rows=1, cols=3)
r2_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

# Col 1: Objective 1
c_obj1 = r2_tbl.rows[0].cells[0]
c_obj1.width = Mm(91)
set_cell_bg(c_obj1, "FFFFFF")
set_cell_border(c_obj1, color="297E93", sz=4)
set_cell_margins(c_obj1, 3, 3, 3, 3)

p = c_obj1.add_paragraph()
p.paragraph_format.space_after = Pt(1)
add_run(p, "OBJECTIVE 1: Flow Feature Selection\n", size=9, bold=True, color="1B5E6F")
add_run(p, "Random Forest importance ranking reduced 88 -> 30 features.", size=7.5, color="555555")

p_img1 = c_obj1.add_paragraph()
p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img1.paragraph_format.space_after = Pt(1)
run = p_img1.add_run()
run.add_picture("poster_assets/feature_importance.png", width=Inches(3.3))
p_c1 = c_obj1.add_paragraph()
p_c1.paragraph_format.space_after = Pt(3)
add_run(p_c1, "Figure 1. Relative Importance Score (Top 6 Features)", size=7.5, bold=True, color="1B5E6F")

p_img2 = c_obj1.add_paragraph()
p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img2.paragraph_format.space_after = Pt(1)
run2 = p_img2.add_run()
run2.add_picture("poster_assets/donut_distribution.png", width=Inches(2.5))
p_c2 = c_obj1.add_paragraph()
p_c2.paragraph_format.space_after = Pt(3)
add_run(p_c2, "Figure 2. CIC-DDoS2019 Cleaned Traffic Balance", size=7.5, bold=True, color="1B5E6F")

p_out1 = c_obj1.add_paragraph()
pPr = p_out1._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "E8F5E9")
pPr.append(shd)
add_run(p_out1, "> Concluding Outcome 1:\nSelecting top 30 features achieved 66% dimension reduction with zero metric loss.", size=7.5, bold=True, color="2E7D32")

# Col 2: Objective 2
c_obj2 = r2_tbl.rows[0].cells[1]
c_obj2.width = Mm(91)
set_cell_bg(c_obj2, "FFFFFF")
set_cell_border(c_obj2, color="297E93", sz=4)
set_cell_margins(c_obj2, 3, 3, 3, 3)

p = c_obj2.add_paragraph()
p.paragraph_format.space_after = Pt(1)
add_run(p, "OBJECTIVE 2: Detection Architecture\n", size=9, bold=True, color="1B5E6F")
add_run(p, "Multi-tier ensemble processing & real-time classification.", size=7.5, color="555555")

p_img3 = c_obj2.add_paragraph()
p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img3.paragraph_format.space_after = Pt(1)
run3 = p_img3.add_run()
run3.add_picture("poster_assets/architecture_diagram.png", width=Inches(3.3))
p_c3 = c_obj2.add_paragraph()
p_c3.paragraph_format.space_after = Pt(3)
add_run(p_c3, "Figure 3. Intelligent Monitoring & Stacking Architecture", size=7.5, bold=True, color="1B5E6F")

# 3 Callouts
callouts = [
    ("1. Base Learners:", "DT, RF, and XGBoost evaluate incoming flows."),
    ("2. Meta-Learner:", "Logistic Regression weighs individual models to minimize errors."),
    ("3. Web Dashboard:", "Flask serves live prediction with calibrated confidence.")
]
for c_hdr, c_txt in callouts:
    p_cl = c_obj2.add_paragraph()
    p_cl.paragraph_format.space_after = Pt(1)
    add_run(p_cl, f"• {c_hdr} ", size=7.8, bold=True, color="1B5E6F")
    add_run(p_cl, c_txt, size=7.5, color="333333")

p_out2 = c_obj2.add_paragraph()
p_out2.paragraph_format.space_before = Pt(3)
pPr = p_out2._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "E3F2FD")
pPr.append(shd)
add_run(p_out2, "> Concluding Outcome 2:\nStacking meta-learner dynamically resolves edge cases, eliminating single-model bias.", size=7.5, bold=True, color="1565C0")

# Col 3: Objective 3
c_obj3 = r2_tbl.rows[0].cells[2]
c_obj3.width = Mm(91)
set_cell_bg(c_obj3, "FFFFFF")
set_cell_border(c_obj3, color="297E93", sz=4)
set_cell_margins(c_obj3, 3, 3, 3, 3)

p = c_obj3.add_paragraph()
p.paragraph_format.space_after = Pt(1)
add_run(p, "OBJECTIVE 3: Benchmark & Evaluation\n", size=9, bold=True, color="1B5E6F")
add_run(p, "Testing across 85,216 unseen held-out network traffic flows.", size=7.5, color="555555")

p_img4 = c_obj3.add_paragraph()
p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img4.paragraph_format.space_after = Pt(1)
run4 = p_img4.add_run()
run4.add_picture("poster_assets/model_comparison.png", width=Inches(3.3))
p_c4 = c_obj3.add_paragraph()
p_c4.paragraph_format.space_after = Pt(3)
add_run(p_c4, "Figure 4. Accuracy & F1-Score Across 5 Models", size=7.5, bold=True, color="1B5E6F")

p_img5 = c_obj3.add_paragraph()
p_img5.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_img5.paragraph_format.space_after = Pt(1)
run5 = p_img5.add_run()
run5.add_picture("poster_assets/confusion_matrix.png", width=Inches(2.5))
p_c5 = c_obj3.add_paragraph()
p_c5.paragraph_format.space_after = Pt(3)
add_run(p_c5, "Figure 5. Stacking Confusion Matrix (Test = 85,216 flows)", size=7.5, bold=True, color="1B5E6F")

p_out3 = c_obj3.add_paragraph()
pPr = p_out3._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "FFF3E0")
pPr.append(shd)
add_run(p_out3, "> Concluding Outcome 3:\nStacking Ensemble achieved lowest False Negatives (FN = 46) and only 9 False Positives.", size=7.5, bold=True, color="E65100")

# Spacer
p_sp3 = doc.add_paragraph()
p_sp3.paragraph_format.space_before = Pt(3)
p_sp3.paragraph_format.space_after = Pt(3)

# 4. ROW 3: DISCUSSION (Left) + CONCLUSION (Right)
r3_tbl = doc.add_table(rows=1, cols=2)
r3_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

c_disc = r3_tbl.rows[0].cells[0]
c_disc.width = Mm(150)
set_cell_bg(c_disc, "FFFFFF")
set_cell_border(c_disc, color="297E93", sz=4)
set_cell_margins(c_disc, 3, 3, 4, 4)

section_banner(c_disc, "DISCUSSION & KEY STUDY FINDINGS")
# Badges inside discussion
p_b = c_disc.add_paragraph()
p_b.paragraph_format.space_after = Pt(2)
add_run(p_b, "[99.94% Accuracy] ", size=8, bold=True, color="2E7D32")
add_run(p_b, "Highest test accuracy.   ", size=7.5, color="333333")
add_run(p_b, "[FN = 46] ", size=8, bold=True, color="E65100")
add_run(p_b, "Missed rate < 0.07%.   ", size=7.5, color="333333")
add_run(p_b, "[FP = 9] ", size=8, bold=True, color="0277BD")
add_run(p_b, "Minimal false alarms.", size=7.5, color="333333")

p_d1 = c_disc.add_paragraph()
p_d1.paragraph_format.space_after = Pt(1)
add_run(p_d1, "• Security Interpretation: ", size=8, bold=True, color="1B5E6F")
add_run(p_d1, "Minimizing False Negatives is critical: missing an active DDoS flood allows server crashes, while FP=9 avoids blocking legitimate users.", size=7.5, color="333333")

p_d2 = c_disc.add_paragraph()
p_d2.paragraph_format.space_after = Pt(1)
add_run(p_d2, "• Limitations: ", size=8, bold=True, color="C62828")
add_run(p_d2, "Offline flow analysis (no live packet capture / Scapy hook); binary classification (attack vs benign).", size=7.5, color="333333")

# Conclusion
c_conc = r3_tbl.rows[0].cells[1]
c_conc.width = Mm(125)
set_cell_bg(c_conc, "FFFFFF")
set_cell_border(c_conc, color="297E93", sz=4)
set_cell_margins(c_conc, 3, 3, 4, 4)

section_banner(c_conc, "CONCLUSION & REFERENCES")
p_c1 = c_conc.add_paragraph()
p_c1.paragraph_format.space_after = Pt(1)
add_run(p_c1, "• Summary: ", size=8, bold=True, color="1B5E6F")
add_run(p_c1, "Stacking Ensemble outperformed base classifiers; SMOTE fixed 78:22 imbalance.\n", size=7.5, color="333333")
add_run(p_c1, "• Future Directions: ", size=8, bold=True, color="1B5E6F")
add_run(p_c1, "Live packet sniffing via Scapy and 11-class multi-label DDoS classification.", size=7.5, color="333333")

p_tm = c_conc.add_paragraph()
p_tm.paragraph_format.space_before = Pt(2)
p_tm.paragraph_format.space_after = Pt(2)
pPr = p_tm._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "E0F2F1")
pPr.append(shd)
add_run(p_tm, "TAKE-HOME MESSAGE:\nEnsemble meta-learning delivers robust, high-accuracy threat classification suitable for modern network security pipelines.", size=7.5, bold=True, color="1B5E6F")

p_ref = c_conc.add_paragraph()
p_ref.paragraph_format.space_after = Pt(0)
add_run(p_ref, "[1] Sharafaldin et al. (CIC-DDoS2019)  |  [2] Pedregosa et al. (Scikit-Learn)\n[3] GitHub: github.com/JainAditi123/Intelligent-Network-Traffic-Monitoring-System", size=6.8, color="777777")

# Save document
out_path = "Project_Poster_A3_Visual.docx"
doc.save(out_path)
print(f"Saved {out_path} successfully!")
