"""
make_poster_word.py
===================
Generates  Project_Poster_A3.docx  — A3 Portrait (297mm x 420mm)
Table-based layout — fully editable in Microsoft Word.
Run: .\\venv\\Scripts\\python.exe make_poster_word.py
"""

from docx import Document
from docx.shared import Pt, RGBColor, Mm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ════════════════════════════════════════════════════════
#  PAGE SETUP  — A3 Portrait  297 x 420 mm
# ════════════════════════════════════════════════════════
for sec in doc.sections:
    sec.page_width  = Mm(297)
    sec.page_height = Mm(420)
    sec.top_margin    = Mm(10)
    sec.bottom_margin = Mm(10)
    sec.left_margin   = Mm(10)
    sec.right_margin  = Mm(10)

# Remove default empty paragraph
for para in doc.paragraphs:
    p = para._element
    p.getparent().remove(p)

# ════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ════════════════════════════════════════════════════════
C_DARK_BG   = "0A1628"   # very dark navy
C_HEADER    = "0D2044"   # header bg
C_CARD      = "112244"   # card bg
C_ACCENT    = "1E88E5"   # electric blue
C_CYAN      = "00BCD4"   # cyan
C_GREEN     = "00C853"   # green (BENIGN)
C_RED       = "FF1744"   # red (ATTACK)
C_GOLD      = "FFB300"   # gold (best model)
C_WHITE     = "FFFFFF"
C_OFFWHITE  = "E8F0FE"
C_LIGHTBLUE = "90CAF9"
C_GREY      = "B0BEC5"
C_DARK_CARD = "0D1F3C"
C_TEAL      = "00897B"
C_PURPLE    = "7B1FA2"

# ════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=1, bottom=1, left=2, right=2):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom),
                      ("left", left), ("right", right)]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"),    str(val * 20))   # twips
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    for old in tcPr.findall(qn("w:tcMar")):
        tcPr.remove(old)
    tcPr.append(tcMar)

def set_cell_border(cell, color="1E88E5", sz=6):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"),   "single")
        el.set(qn("w:sz"),    str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        tcBd.append(el)
    for old in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(old)
    tcPr.append(tcBd)

def no_border_cell(cell):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"),  "0")
        el.set(qn("w:space"),"0")
        el.set(qn("w:color"),"auto")
        tcBd.append(el)
    for old in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(old)
    tcPr.append(tcBd)

def no_space_para(cell_or_doc):
    """Clear all paragraphs from a cell and return fresh para."""
    for p in list(cell_or_doc.paragraphs):
        el = p._element
        el.getparent().remove(el)
    return cell_or_doc.add_paragraph()

def add_run(para, text, size=10, bold=False, color=C_WHITE,
            italic=False, font_name="Calibri"):
    run = para.add_run(text)
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.name   = font_name
    run.font.color.rgb = RGBColor.from_string(color)
    return run

def cell_para(cell, text, size=10, bold=False, color=C_WHITE,
              align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0,
              space_after=2, italic=False):
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = Pt(size + 2)
    add_run(p, text, size=size, bold=bold, color=color, italic=italic)
    return p

def section_head(cell, text, bg=C_ACCENT, fg=C_WHITE, size=10):
    """Coloured heading bar inside a cell."""
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.line_spacing = Pt(size + 4)
    # simulate filled heading with shading via paragraph shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  bg)
    pPr.append(shd)
    add_run(p, f"  {text}  ", size=size, bold=True, color=fg)
    return p

def bullet_line(cell, text, size=8.5, color=C_OFFWHITE, dot="•"):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.line_spacing = Pt(size + 2)
    p.paragraph_format.left_indent  = Mm(3)
    add_run(p, dot + "  ", size=size, bold=True, color=C_CYAN)
    add_run(p, text, size=size, color=color)
    return p

def kv_line(cell, key, val, ksize=8.5, vsize=8.5,
            kcolor=C_CYAN, vcolor=C_OFFWHITE):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.line_spacing = Pt(ksize + 2)
    add_run(p, key + ":  ", size=ksize, bold=True,  color=kcolor)
    add_run(p, val,         size=vsize, bold=False, color=vcolor)
    return p

def divider_line(cell, color=C_ACCENT):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "4")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), color)
    pBdr.append(bot)
    pPr.append(pBdr)

def set_row_height(row, height_mm):
    tr   = row._tr
    trPr = tr.get_or_add_trPr()
    for old in trPr.findall(qn("w:trHeight")):
        trPr.remove(old)
    trH = OxmlElement("w:trHeight")
    trH.set(qn("w:val"),   str(int(height_mm * 56.69)))
    trH.set(qn("w:hRule"), "atLeast")
    trPr.append(trH)

def merge_row(row):
    """Merge all cells in a row."""
    row.cells[0].merge(row.cells[-1])

def set_col_width(cell, width_mm):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:tcW")):
        tcPr.remove(old)
    tcW = OxmlElement("w:tcW")
    tcW.set(qn("w:w"),    str(int(width_mm * 56.69)))
    tcW.set(qn("w:type"), "dxa")
    tcPr.append(tcW)

def no_table_border(table):
    tbl  = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    tblBd = OxmlElement("w:tblBorders")
    for side in ["top","left","bottom","right","insideH","insideV"]:
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"),  "none")
        el.set(qn("w:sz"),   "0")
        el.set(qn("w:space"),"0")
        el.set(qn("w:color"),"auto")
        tblBd.append(el)
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    tblPr.append(tblBd)

# ════════════════════════════════════════════════════════
# USABLE WIDTHS
# Page = 297mm, margins = 10mm each side → usable = 277mm
# 3 equal columns with 3mm gaps: (277 - 6) / 3 = 90.3mm ≈ 90mm
# ════════════════════════════════════════════════════════
PW   = 277   # usable page width mm
COL  = 90    # each column mm
GAP  = 3     # gap between columns mm
# Adjust so 3 cols + 2 gaps = PW: 90*3 + 3*2 = 276 ≈ 277 ✓

# ════════════════════════════════════════════════════════
# MAIN OUTER TABLE  (1 col, full width — rows stacked)
# We'll use a single-column outer table for each band,
# and a 3-column table for the body.
# ════════════════════════════════════════════════════════

def add_band(doc, rows=1, cols=1):
    t = doc.add_table(rows=rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    no_table_border(t)
    return t

# ════════════════════════════════════════════════════════
#  ① HEADER BAND
# ════════════════════════════════════════════════════════
ht = add_band(doc, rows=3, cols=1)

# Row 0 — top accent bar
r0 = ht.rows[0]
set_row_height(r0, 4)
c0 = r0.cells[0]
set_col_width(c0, PW)
set_cell_bg(c0, C_ACCENT)
no_border_cell(c0)
set_cell_margins(c0, 0, 0, 0, 0)
p = no_space_para(c0)
p.paragraph_format.space_after = Pt(0)

# Row 1 — main header
r1 = ht.rows[1]
set_row_height(r1, 32)
c1 = r1.cells[0]
set_col_width(c1, PW)
set_cell_bg(c1, C_HEADER)
no_border_cell(c1)
set_cell_margins(c1, 4, 2, 8, 8)
c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

p_tag = c1.add_paragraph()
p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tag.paragraph_format.space_after = Pt(2)
p_tag.paragraph_format.line_spacing = Pt(12)
add_run(p_tag, "THIRD YEAR CSE PROJECT  |  MACHINE LEARNING & CYBERSECURITY",
        size=9, bold=True, color=C_CYAN)

p_title = c1.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(2)
p_title.paragraph_format.line_spacing = Pt(26)
add_run(p_title,
        "Intelligent Network Traffic Monitoring System",
        size=22, bold=True, color=C_OFFWHITE)

p_sub = c1.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(2)
p_sub.paragraph_format.line_spacing = Pt(14)
add_run(p_sub,
        "DDoS Attack Detection using Ensemble Machine Learning  |  CIC-DDoS2019 Dataset",
        size=11, bold=False, color=C_LIGHTBLUE)

p_auth = c1.add_paragraph()
p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_auth.paragraph_format.space_after = Pt(0)
p_auth.paragraph_format.line_spacing = Pt(13)
add_run(p_auth,
        "Aditi Jain     |     Python  •  scikit-learn  •  XGBoost  •  Flask     |     November 2026",
        size=9, italic=True, color=C_GREY)

# Row 2 — bottom cyan bar
r2 = ht.rows[2]
set_row_height(r2, 3)
c2 = r2.cells[0]
set_col_width(c2, PW)
set_cell_bg(c2, C_CYAN)
no_border_cell(c2)
set_cell_margins(c2, 0, 0, 0, 0)
p = no_space_para(c2)
p.paragraph_format.space_after = Pt(0)

# ════════════════════════════════════════════════════════
#  ② STATS BADGES ROW
# ════════════════════════════════════════════════════════
st = add_band(doc, rows=1, cols=4)
set_row_height(st.rows[0], 20)

badges = [
    ("426,076", "Total Records Cleaned",      C_LIGHTBLUE, C_DARK_CARD),
    ("30",      "Features Selected (88→30)",  C_CYAN,      C_DARK_CARD),
    ("5",       "ML Models Trained",          C_ACCENT,    C_DARK_CARD),
    ("99.94%",  "Best Model Accuracy",        C_GREEN,     "102800"),
]
badge_w = PW / 4

for i, (val, lbl, vcol, bg) in enumerate(badges):
    cell = st.rows[0].cells[i]
    set_col_width(cell, badge_w - 1)
    set_cell_bg(cell, bg)
    no_border_cell(cell)
    set_cell_margins(cell, 3, 3, 4, 4)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    p_val = cell.add_paragraph()
    p_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_val.paragraph_format.space_after = Pt(0)
    p_val.paragraph_format.line_spacing = Pt(20)
    add_run(p_val, val, size=16, bold=True, color=vcol)

    p_lbl = cell.add_paragraph()
    p_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl.paragraph_format.space_after = Pt(0)
    p_lbl.paragraph_format.line_spacing = Pt(10)
    add_run(p_lbl, lbl, size=7.5, bold=False, color=C_GREY)

# ════════════════════════════════════════════════════════
#  ③ BODY — 3 COLUMNS
# ════════════════════════════════════════════════════════
bt = add_band(doc, rows=1, cols=3)
set_row_height(bt.rows[0], 270)

col_cells = bt.rows[0].cells
for ci, cell in enumerate(col_cells):
    set_col_width(cell, COL)
    set_cell_bg(cell, C_DARK_BG)
    set_cell_margins(cell, 2, 2, 3, 3)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    # Thin blue border between columns
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBd = OxmlElement("w:tcBorders")
    sides = {"left": C_ACCENT if ci > 0 else "none",
             "right": C_ACCENT if ci < 2 else "none",
             "top": "none", "bottom": "none"}
    for side, sc in sides.items():
        el = OxmlElement(f"w:{side}")
        if sc == "none":
            el.set(qn("w:val"), "none")
        else:
            el.set(qn("w:val"),   "single")
            el.set(qn("w:sz"),    "4")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), sc)
        tcBd.append(el)
    for old in tcPr.findall(qn("w:tcBorders")):
        tcPr.remove(old)
    tcPr.append(tcBd)

# ── COLUMN 1 : Left ──────────────────────────────────────────────
L = col_cells[0]

section_head(L, "PROBLEM STATEMENT", bg=C_ACCENT)
cell_para(L, "DDoS (Distributed Denial-of-Service) attacks flood network servers "
             "with massive fake traffic, crashing services. Traditional firewalls "
             "fail against modern multi-vector attacks.",
          size=8.5, color=C_OFFWHITE, space_after=2)
bullet_line(L, "17 million+ DDoS attacks occur globally each year")
bullet_line(L, "Attack traffic mimics legitimate patterns — hard to detect")
bullet_line(L, "Manual analysis cannot scale to Gbps network speeds")
bullet_line(L, "ML learns statistical traffic patterns automatically")

divider_line(L)

section_head(L, "DATASET: CIC-DDoS2019", bg="1A237E")
kv_line(L, "Source Files",   "17 Parquet files")
kv_line(L, "After Cleaning", "426,076 rows")
kv_line(L, "Raw Features",   "88 columns")
kv_line(L, "Selected Feat.", "30 best features")
kv_line(L, "Train Set",      "340,860 rows (80%)")
kv_line(L, "Post-SMOTE",     "530,194 rows (balanced)")
kv_line(L, "Test Set",       "85,216 rows (20%, held-out)")
kv_line(L, "Attack Types",   "SYN, UDP, DNS, LDAP, MSSQL, NTP…")

divider_line(L)

section_head(L, "PREPROCESSING PIPELINE", bg="0D3B2E")
steps = [
    ("01", "Load 17 Parquet files via pyarrow"),
    ("02", "Drop null / infinite / duplicate rows"),
    ("03", "Binary labels: BENIGN=0, ATTACK=1"),
    ("04", "Feature selection 88→30 (RF importance + correlation)"),
    ("05", "80/20 stratified train-test split"),
    ("06", "StandardScaler fitted on X_train only"),
    ("07", "SMOTE on training set (balance 50-50%)"),
]
for num, desc in steps:
    p = L.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.line_spacing = Pt(11)
    add_run(p, f"[{num}] ", size=8.5, bold=True, color=C_ACCENT)
    add_run(p, desc,         size=8.5, color=C_OFFWHITE)

divider_line(L)

section_head(L, "30 SELECTED FEATURES (TOP 12)", bg="1B0050")
feats = [
    "Flow Duration",          "Fwd Packet Length Max",
    "Fwd Packet Length Mean", "Bwd Packet Length Max",
    "Fwd Packets/s",          "Bwd Packets/s",
    "Flow IAT Mean",          "Flow IAT Max",
    "Fwd Header Length",      "Fwd IAT Total",
    "Packet Length Mean",     "Protocol",
]
for f in feats:
    bullet_line(L, f, size=8, dot="›", color=C_LIGHTBLUE)

# ── COLUMN 2 : Middle ────────────────────────────────────────────
M = col_cells[1]

section_head(M, "5 MODELS TRAINED", bg="1A237E")
models = [
    ("Decision Tree",     "Baseline classifier",       "99.92%", C_LIGHTBLUE),
    ("Random Forest",     "Bagging — 100 trees",       "99.93%", C_ACCENT),
    ("XGBoost",           "Boosting — 100 rounds",     "99.90%", "AB47BC"),
    ("Voting Ensemble",   "Soft voting DT+RF+XGB",     "99.93%", C_TEAL),
    ("Stacking Ensemble", "Meta-Learning (Log. Reg.)", "99.94%", C_GOLD),
]
for mname, mtype, acc, mc in models:
    p = M.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(0)
    p.paragraph_format.line_spacing = Pt(12)
    add_run(p, f"■ {mname}  ", size=9, bold=True,  color=mc)
    add_run(p, f"({mtype})",   size=8, bold=False, color=C_GREY)
    p2 = M.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after  = Pt(3)
    p2.paragraph_format.line_spacing = Pt(11)
    p2.paragraph_format.left_indent  = Mm(3)
    add_run(p2, f"Accuracy: {acc}", size=8.5, bold=True, color=C_GREEN)

p_best = M.add_paragraph()
p_best.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_best.paragraph_format.space_before = Pt(1)
p_best.paragraph_format.space_after  = Pt(3)
p_best.paragraph_format.line_spacing = Pt(12)
pPr = p_best._p.get_or_add_pPr()
shd = OxmlElement("w:shd")
shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
shd.set(qn("w:fill"), "332200")
pPr.append(shd)
add_run(p_best, "BEST MODEL: Stacking Ensemble | Accuracy 99.94% | F1: 0.9996",
        size=8.5, bold=True, color=C_GOLD)

divider_line(M)

section_head(M, "PERFORMANCE METRICS (TEST: 85,216 SAMPLES)", bg="1B0000")

# metrics table inside cell
mt = M.add_table(rows=1, cols=5)
no_table_border(mt)
mt_headers = ["Model", "Acc", "Prec", "Recall", "F1"]
mt_widths   = [34, 13, 13, 14, 13]
hr = mt.rows[0]
for i, (hdr, w) in enumerate(zip(mt_headers, mt_widths)):
    cell_ = hr.cells[i]
    set_col_width(cell_, w)
    set_cell_bg(cell_, C_ACCENT)
    set_cell_margins(cell_, 1, 1, 1, 1)
    p_ = cell_.add_paragraph()
    p_.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_.paragraph_format.space_after = Pt(0)
    p_.paragraph_format.line_spacing = Pt(10)
    add_run(p_, hdr, size=7.5, bold=True, color=C_WHITE)

perf_data = [
    ("Decision Tree",    "99.92%", "99.97%", "99.93%", "99.95%", "162535"),
    ("Random Forest",    "99.93%", "99.99%", "99.93%", "99.96%", "0D1F3C"),
    ("XGBoost",          "99.90%", "99.99%", "99.88%", "99.94%", "162535"),
    ("Voting Ensemble",  "99.93%", "99.99%", "99.92%", "99.96%", "0D1F3C"),
    ("Stacking Ens. ★",  "99.94%", "99.99%", "99.93%", "99.96%", "332200"),
]
for mname, acc, prec, rec, f1, rowbg in perf_data:
    is_best = "★" in mname
    mr = mt.add_row()
    for i, (val, w) in enumerate(zip([mname, acc, prec, rec, f1], mt_widths)):
        cell_ = mr.cells[i]
        set_col_width(cell_, w)
        set_cell_bg(cell_, rowbg)
        set_cell_margins(cell_, 1, 1, 1, 1)
        p_ = cell_.add_paragraph()
        p_.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_.paragraph_format.space_after = Pt(0)
        p_.paragraph_format.line_spacing = Pt(10)
        col_ = C_GOLD if is_best else (C_OFFWHITE if i == 0 else C_GREEN)
        add_run(p_, val, size=7.5, bold=is_best, color=col_)

divider_line(M)

section_head(M, "CONFUSION MATRIX — STACKING ENSEMBLE", bg="3D0000")

# 2x2 matrix using a mini table
cm_tbl = M.add_table(rows=2, cols=2)
no_table_border(cm_tbl)
cm_data = [
    ("TN = 18,932\nBenign correctly ID'd",  "1B4332", "FP = 9\nFalse alarm",       "7B0000"),
    ("FN = 46\nMissed attack (risk!)",       "7C4700", "TP = 66,229\nAttack detected","145A32"),
]
cm_labels = [("Predicted BENIGN", "Predicted ATTACK"), ("", "")]
for ri, row_data in enumerate(cm_data):
    for ci in range(2):
        cell_ = cm_tbl.rows[ri].cells[ci]
        set_col_width(cell_, 43)
        set_cell_bg(cell_, row_data[ci*2 + 1])
        set_cell_margins(cell_, 2, 2, 2, 2)
        cell_.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p_ = cell_.add_paragraph()
        p_.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_.paragraph_format.space_after = Pt(0)
        p_.paragraph_format.line_spacing = Pt(14)
        txt = row_data[ci*2]
        lines = txt.split("\n")
        add_run(p_, lines[0], size=11, bold=True,  color=C_WHITE)
        if len(lines) > 1:
            add_run(p_, "\n" + lines[1], size=7.5, bold=False, color="DDDDDD")

divider_line(M)

section_head(M, "WHY ENSEMBLE LEARNING?", bg="0D3D0D")
ens_pts = [
    "Voting: DT+RF+XGB combined → reduces individual bias",
    "Stacking: meta-learner learns WHEN to trust each model",
    "Bagging (RF): 100 trees → reduces variance",
    "Boosting (XGB): corrects errors of previous learners",
    "Best FN=46 — fewest missed attacks across all models",
]
for pt in ens_pts:
    bullet_line(M, pt, size=8, dot="★", color=C_OFFWHITE)

# ── COLUMN 3 : Right ─────────────────────────────────────────────
R = col_cells[2]

section_head(R, "FLASK WEB DASHBOARD", bg="1A0050")
p_url = R.add_paragraph()
p_url.paragraph_format.space_after = Pt(3)
p_url.paragraph_format.line_spacing = Pt(12)
add_run(p_url, "URL:  http://127.0.0.1:5000", size=9, bold=True, color=C_CYAN)

pages_data = [
    ("Dashboard",         "Stat cards, 10-step ML pipeline, best model summary"),
    ("Traffic Prediction","CSV upload → real ML inference → BENIGN/ATTACK results"),
    ("Model Comparison",  "Side-by-side metrics, bar charts, radar chart"),
    ("Evaluation",        "Confusion matrices for all 5 trained models"),
    ("About",             "Dataset info, pipeline steps, tech stack, limitations"),
]
for pname, pdesc in pages_data:
    p_ = R.add_paragraph()
    p_.paragraph_format.space_before = Pt(1)
    p_.paragraph_format.space_after  = Pt(0)
    p_.paragraph_format.line_spacing = Pt(12)
    add_run(p_, f"◆ {pname}:  ", size=9, bold=True,  color=C_ACCENT)
    add_run(p_, pdesc,           size=8.5, bold=False, color=C_OFFWHITE)

p_note = R.add_paragraph()
p_note.paragraph_format.space_before = Pt(3)
p_note.paragraph_format.space_after  = Pt(2)
p_note.paragraph_format.line_spacing = Pt(11)
add_run(p_note, "Real ML Inference | No hardcoded results | CSV Download supported",
        size=8, bold=True, color=C_GREEN)

divider_line(R)

section_head(R, "TECHNOLOGY STACK", bg="1A2000")
tech_data = [
    ("Python 3.11",      "Core language"),
    ("scikit-learn 1.9", "DT, RF, Stacking, StandardScaler"),
    ("XGBoost 3.4",      "Gradient boosting classifier"),
    ("pandas / NumPy",   "Data processing and arrays"),
    ("imbalanced-learn", "SMOTE oversampling"),
    ("Flask 3.1.3",      "Web framework + HTTP routing"),
    ("Chart.js 4.4",     "Interactive charts (CDN)"),
    ("joblib 1.6",       "Model serialization (.pkl)"),
    ("pyarrow 25.0",     "Reading Parquet dataset files"),
]
for tname, tdesc in tech_data:
    kv_line(R, tname, tdesc, ksize=8.5, vsize=8.5)

divider_line(R)

section_head(R, "KEY RESULTS & IMPACT", bg="3D0000")
results = [
    "Stacking Ensemble: 99.94% accuracy on 85,216 test flows",
    "Only 9 false positives — minimal disruption to legitimate users",
    "Only 46 missed attacks — high security reliability",
    "SMOTE fixed 78-22% class imbalance without touching test data",
    "Features reduced from 88 to 30 — faster without accuracy loss",
    "predict_proba() used for scientifically valid confidence scores",
]
for r in results:
    bullet_line(R, r, size=8, dot="●", color=C_OFFWHITE)

divider_line(R)

section_head(R, "LIMITATIONS", bg="7C0000")
lims = [
    "Offline only — no live network packet capture",
    "Binary classification only (not 11-class multi-label)",
    "Feature selection done pre-split (mild data leakage note)",
    "Tested on CIC-DDoS2019 only — real-world generalization TBD",
]
for l in lims:
    bullet_line(R, l, size=8, dot="!", color=C_OFFWHITE)

divider_line(R, color=C_GREEN)

section_head(R, "FUTURE SCOPE", bg="0D3D0D")
fut = [
    "Live packet capture via scapy / pyshark library",
    "11-class multi-label DDoS type classification",
    "Cloud deployment: Docker + gunicorn + AWS/GCP",
    "REST API for SIEM system integration",
    "K-fold cross-validation for robust evaluation",
    "Auto-retraining on data drift detection",
]
for f in fut:
    bullet_line(R, f, size=8, dot="→", color=C_OFFWHITE)

# ════════════════════════════════════════════════════════
#  ④ FOOTER BAND
# ════════════════════════════════════════════════════════
ft = add_band(doc, rows=2, cols=1)

# Top divider
r_div = ft.rows[0]
set_row_height(r_div, 3)
c_div = r_div.cells[0]
set_col_width(c_div, PW)
set_cell_bg(c_div, C_ACCENT)
no_border_cell(c_div)
set_cell_margins(c_div, 0, 0, 0, 0)
p = no_space_para(c_div)
p.paragraph_format.space_after = Pt(0)

# Footer text
r_ft = ft.rows[1]
set_row_height(r_ft, 14)
c_ft = r_ft.cells[0]
set_col_width(c_ft, PW)
set_cell_bg(c_ft, C_HEADER)
no_border_cell(c_ft)
set_cell_margins(c_ft, 2, 2, 8, 8)
c_ft.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

p_f1 = c_ft.add_paragraph()
p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_f1.paragraph_format.space_after = Pt(1)
p_f1.paragraph_format.line_spacing = Pt(13)
add_run(p_f1,
    "Intelligent Network Traffic Monitoring System  —  DDoS Detection using Ensemble Machine Learning",
    size=9.5, bold=True, color=C_OFFWHITE)

p_f2 = c_ft.add_paragraph()
p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_f2.paragraph_format.space_after = Pt(0)
p_f2.paragraph_format.line_spacing = Pt(11)
add_run(p_f2,
    "Models: Decision Tree • Random Forest • XGBoost • Voting Ensemble • Stacking Ensemble     |     Submitted by: Aditi Jain  |  November 2026",
    size=8.5, color=C_GREY)

# ════════════════════════════════════════════════════════
#  SAVE
# ════════════════════════════════════════════════════════
out = "Project_Poster_A3.docx"
doc.save(out)
print(f"Poster saved: {out}")
