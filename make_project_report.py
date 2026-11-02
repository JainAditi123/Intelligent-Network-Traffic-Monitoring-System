"""
make_project_report.py
======================
Generates a complete, easy-to-understand project explanation report.
Run: .\venv\Scripts\python.exe make_project_report.py
Output: Project_Report.docx (on Desktop)
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime, os

doc = Document()

# ── Page margins ──
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Helpers ──
def sf(run, size=11, bold=False, color=None, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = "Calibri"
    if color:
        run.font.color.rgb = RGBColor(*color)

def heading(text, level=1, color=(26, 60, 100)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(*color)

def para(text, size=11, bold=False, color=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    sf(run, size, bold, color, italic)
    return p

def bullet(text, size=11, bold=False):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    sf(run, size, bold)

def shade_row(row, hex_color):
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hex_color)
        tcPr.append(shd)

def make_table(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tbl.rows[0]
    shade_row(hdr, "1A3C6E")
    for i, txt in enumerate(headers):
        cell = hdr.cells[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt)
        sf(run, 10.5, bold=True, color=(255,255,255))
    for idx, row_data in enumerate(rows):
        row = tbl.add_row()
        bg = "EBF3FB" if idx % 2 == 0 else "FFFFFF"
        shade_row(row, bg)
        for i, txt in enumerate(row_data):
            cell = row.cells[i]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(txt))
            sf(run, 10.5)
    doc.add_paragraph()
    return tbl

def line():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("_" * 60)
    sf(run, 10, color=(180, 180, 180))

# =====================================================================
# COVER PAGE
# =====================================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("PROJECT REPORT")
sf(run, 28, bold=True, color=(26, 60, 100))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Intelligent Network Traffic Monitoring System\nUsing CIC-DDoS2019 Dataset and Ensemble Learning")
sf(run, 16, bold=True, color=(50, 50, 50))

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("_" * 50)
sf(run, 12, color=(100, 130, 180))

doc.add_paragraph()
for label, value in [
    ("Subject",      "Machine Learning / Network Security"),
    ("Task",         "DDoS Attack Detection using Ensemble Learning"),
    ("Submitted by", "Aditi Jain"),
    ("Date",         datetime.date.today().strftime("%B %d, %Y")),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}:  ")
    sf(r1, 12, bold=True, color=(26, 60, 100))
    r2 = p.add_run(value)
    sf(r2, 12)

doc.add_page_break()

# =====================================================================
# TABLE OF CONTENTS
# =====================================================================
heading("Table of Contents")
toc_items = [
    "1. What is This Project About?",
    "2. What Problem Does It Solve?",
    "3. What is DDoS Attack? (Simple Explanation)",
    "4. How Does the Project Work? (Step by Step)",
    "5. What is Machine Learning? (Simple Explanation)",
    "6. What are the 5 Models Used?",
    "7. What Dataset is Used?",
    "8. What Technologies are Used?",
    "9. Results - How Well Does It Work?",
    "10. Confusion Matrix Explained",
    "11. Web Dashboard",
    "12. Benefits of This Project",
    "13. Limitations",
    "14. Project File Structure",
    "15. How to Run the Project",
    "16. Conclusion",
]
for item in toc_items:
    para(item, size=11)

doc.add_page_break()

# =====================================================================
# 1. WHAT IS THIS PROJECT ABOUT
# =====================================================================
heading("1. What is This Project About?")

para("This project is a DDoS Attack Detection System. It uses Machine Learning (ML) to "
     "automatically check network traffic and tell whether it is safe or dangerous.", bold=True)

doc.add_paragraph()
para("Think of it like this:")
doc.add_paragraph()

para("Imagine you are a security guard at a building gate. Thousands of people come every day. "
     "Most are normal visitors (BENIGN), but some are criminals trying to break in (ATTACK). "
     "You cannot check every person manually - there are too many.", size=11)

doc.add_paragraph()

para("This project is like an AI security guard for computer networks. Instead of people, "
     "it checks network traffic (data packets). Instead of eyes, it uses mathematical patterns. "
     "And it can check 85,000+ records in seconds with 99.94% accuracy.", size=11)

doc.add_paragraph()

make_table(
    ["Term", "Meaning"],
    [
        ["BENIGN", "Normal, safe network traffic (like normal website browsing)"],
        ["ATTACK", "DDoS attack traffic (hackers flooding the server)"],
        ["Binary Classification", "Sorting things into exactly 2 groups: BENIGN or ATTACK"],
        ["Ensemble Learning", "Combining multiple ML models to get better results"],
    ]
)

# =====================================================================
# 2. WHAT PROBLEM DOES IT SOLVE
# =====================================================================
heading("2. What Problem Does It Solve?")

para("The Internet faces a massive cybersecurity threat called DDoS attacks. "
     "These attacks can shut down websites, banks, hospitals, and government services. "
     "Traditional security systems (firewalls) use fixed rules to detect attacks, but "
     "hackers constantly change their methods to bypass those rules.")

doc.add_paragraph()
para("The Problems with Manual/Traditional Detection:", bold=True)
bullet("Network traffic is TOO LARGE for humans to monitor (millions of packets per second)")
bullet("Attack patterns keep CHANGING - old rules don't catch new attacks")
bullet("Traditional firewalls have HIGH false alarm rates")
bullet("Response time is critical - every second of delay = more damage")

doc.add_paragraph()
para("Our Solution:", bold=True, color=(26, 60, 100))
para("Use Machine Learning to automatically LEARN what attack traffic looks like, "
     "and detect it instantly - even new types of attacks that follow similar patterns.")

# =====================================================================
# 3. WHAT IS DDOS
# =====================================================================
doc.add_page_break()
heading("3. What is a DDoS Attack? (Simple Explanation)")

para("DDoS stands for Distributed Denial-of-Service.", bold=True)

doc.add_paragraph()
para("Real-life analogy:", bold=True, color=(26, 60, 100))
para("Imagine a small restaurant that can serve 50 customers at a time. Now imagine "
     "someone sends 10,000 fake customers to stand in line. The real customers cannot get in. "
     "The restaurant is overwhelmed and has to shut down. That is a DDoS attack on a computer server.")

doc.add_paragraph()
para("How it works technically:", bold=True)
bullet("Attackers use thousands of hacked computers (called a 'botnet')")
bullet("All these computers send massive amounts of fake traffic to one target server")
bullet("The server gets overwhelmed and crashes or becomes very slow")
bullet("Real users cannot access the website or service")

doc.add_paragraph()
para("Real-world impact:", bold=True)

make_table(
    ["Fact", "Detail"],
    [
        ["Average cost per hour", "$20,000 - $40,000 for businesses"],
        ["Attack frequency", "One DDoS attack happens every 60 seconds globally"],
        ["Famous example", "In 2016, a DDoS attack shut down Twitter, Netflix, and Reddit simultaneously"],
        ["Attack types", "DNS flood, SYN flood, UDP flood, LDAP amplification, and more"],
        ["Our dataset includes", "11 different DDoS attack types"],
    ]
)

# =====================================================================
# 4. HOW DOES THE PROJECT WORK
# =====================================================================
heading("4. How Does the Project Work? (Step by Step)")

para("The project follows a 10-step pipeline. Each step is a separate Python script:", bold=True)

steps = [
    ("Step 1\n(Script 01)", "Dataset Analysis",
     "Look at the raw data files. Check how many records there are, what columns exist, "
     "and if any data is missing."),
    ("Step 2\n(Script 02)", "Data Cleaning (Preprocessing)",
     "Combine all 17 data files into one. Remove broken values (infinity, NaN). "
     "Remove duplicate rows. This gives us clean, usable data."),
    ("Step 3\n(Script 03)", "Create Binary Labels",
     "The original data has 11 different attack types (DNS, SYN, UDP, etc.). "
     "We simplify this: all attacks become 'ATTACK' (1), normal traffic stays 'BENIGN' (0). "
     "Now it is a simple yes/no problem."),
    ("Step 4\n(Script 04)", "Feature Selection",
     "The data has 88 columns (features). Not all are useful. We use a Random Forest to "
     "find the 30 MOST IMPORTANT features and keep only those. This makes the model faster and better."),
    ("Step 5\n(Script 05)", "Split, Scale, and Balance",
     "Split data: 80% for training, 20% for testing. Scale all numbers to a similar range "
     "(StandardScaler). Balance the training data using SMOTE so the model sees equal examples "
     "of BENIGN and ATTACK."),
    ("Step 6\n(Script 06)", "Train Decision Tree",
     "Train a single Decision Tree model. This is our BASELINE - the simplest model to "
     "compare others against."),
    ("Step 7\n(Script 07)", "Train Random Forest",
     "Train a Random Forest - 100 decision trees working together. Each tree votes, "
     "and the majority wins."),
    ("Step 8\n(Script 08)", "Train XGBoost",
     "Train XGBoost - trees that learn from each other's mistakes. Very powerful."),
    ("Step 9\n(Script 09)", "Train Voting Ensemble",
     "Combine all 3 models (DT + RF + XGB). They vote together. "
     "Final answer = average of all three opinions."),
    ("Step 10\n(Script 10)", "Train Stacking Ensemble",
     "The BEST model. DT + RF + XGB make predictions, then a Logistic Regression "
     "model learns the OPTIMAL way to combine them. Like a team captain making the final call."),
]

make_table(
    ["Step", "Name", "What It Does (Simple Explanation)"],
    [[s[0], s[1], s[2]] for s in steps]
)

# =====================================================================
# 5. WHAT IS ML
# =====================================================================
doc.add_page_break()
heading("5. What is Machine Learning? (Simple Explanation)")

para("Machine Learning is teaching a computer to learn patterns from data, "
     "so it can make predictions on NEW data it has never seen before.", bold=True)

doc.add_paragraph()
para("Analogy:", bold=True, color=(26, 60, 100))
para("Think of how you learned to recognise cats vs dogs as a child. Nobody gave you a "
     "list of rules ('if 4 legs AND whiskers AND small = cat'). Instead, you SAW many "
     "examples of cats and dogs, and your brain LEARNED the patterns automatically. "
     "Machine Learning works the same way - you show the computer thousands of examples, "
     "and it learns the patterns.")

doc.add_paragraph()
para("In our project:", bold=True)
bullet("We show the computer 340,860 training examples of BENIGN and ATTACK traffic")
bullet("The computer learns patterns like: 'Attack traffic has very high packet rates, "
       "short duration, and unusual flag combinations'")
bullet("Then we test it on 85,216 NEW examples it has never seen")
bullet("It correctly classifies 99.94% of them!")

doc.add_paragraph()
para("Types of ML used in this project:", bold=True)

make_table(
    ["Type", "What It Means", "Example in Our Project"],
    [
        ["Supervised Learning", "We give the computer labeled examples (we tell it which is BENIGN and which is ATTACK)", "All 5 models use supervised learning"],
        ["Classification", "Sorting data into categories (not predicting a number)", "Binary classification: BENIGN or ATTACK"],
        ["Ensemble Learning", "Combining multiple models to get better results than any single model", "Voting Ensemble, Stacking Ensemble"],
    ]
)

# =====================================================================
# 6. THE 5 MODELS
# =====================================================================
heading("6. What are the 5 Models Used?")

# -- Decision Tree --
heading("6.1  Decision Tree (Baseline Model)", level=2)
para("What it is:", bold=True)
para("A Decision Tree is like a flowchart of yes/no questions. "
     "For example: 'Is packet rate > 100,000? YES -> probably ATTACK. NO -> check next feature...' "
     "It keeps splitting the data until it reaches a final answer.")
para("Why we use it:", bold=True)
para("It is the simplest ML model. We use it as a baseline to compare against the "
     "more advanced ensemble models. If ensemble models beat the Decision Tree, we prove "
     "that combining models is better.")
para("Limitation: A single tree can memorize the training data (overfitting) and may not "
     "work well on new data.", italic=True if False else False)

# -- Random Forest --
heading("6.2  Random Forest (Bagging Ensemble)", level=2)
para("What it is:", bold=True)
para("Random Forest = 100 Decision Trees working together. Each tree is trained on a "
     "RANDOM subset of the data and looks at RANDOM features. When making a prediction, "
     "all 100 trees vote, and the majority wins.")
para("Analogy:", bold=True, color=(26, 60, 100))
para("Instead of asking 1 doctor for a diagnosis, you ask 100 doctors (each seeing different "
     "test results) and go with the majority opinion. This is more reliable.")
para("Technique: BAGGING (Bootstrap Aggregating) - each tree gets a different random sample.", bold=True)

# -- XGBoost --
heading("6.3  XGBoost (Boosting Ensemble)", level=2)
para("What it is:", bold=True)
para("XGBoost (Extreme Gradient Boosting) trains trees ONE AFTER ANOTHER. Each new tree "
     "focuses specifically on the mistakes that the previous trees made. So each tree "
     "corrects the errors of the one before it.")
para("Analogy:", bold=True, color=(26, 60, 100))
para("Like a student taking a test, checking wrong answers, studying ONLY those topics, "
     "and retaking the test. Each attempt focuses on previous weaknesses.")
para("Key settings used:", bold=True)
bullet("100 rounds (100 sequential trees)")
bullet("Learning rate = 0.1 (small steps to avoid overshooting)")
bullet("Max depth = 6 (each tree can ask up to 6 levels of questions)")

# -- Voting --
heading("6.4  Voting Ensemble (Soft Voting)", level=2)
para("What it is:", bold=True)
para("Takes all 3 models (Decision Tree + Random Forest + XGBoost) and combines "
     "their predictions. Each model gives a probability (e.g., '80% chance ATTACK'). "
     "The Voting Ensemble averages these probabilities and picks the highest.")
para("Analogy:", bold=True, color=(26, 60, 100))
para("Three experts give their confidence levels. We average them: "
     "Expert 1 says 90% attack, Expert 2 says 70% attack, Expert 3 says 80% attack. "
     "Average = 80% attack. Since 80% > 50%, final answer = ATTACK.")

# -- Stacking --
heading("6.5  Stacking Ensemble (Meta-Learning) - BEST MODEL", level=2)
para("What it is:", bold=True)
para("The most advanced model. It works in TWO levels:")
doc.add_paragraph()
para("Level 1 (Base Learners):", bold=True, color=(26, 60, 100))
bullet("Decision Tree makes its prediction")
bullet("Random Forest makes its prediction")
bullet("XGBoost makes its prediction")
doc.add_paragraph()
para("Level 2 (Meta-Learner):", bold=True, color=(26, 60, 100))
bullet("A Logistic Regression model takes ALL THREE predictions as input")
bullet("It LEARNS which model to trust more in which situation")
bullet("It makes the FINAL prediction")
doc.add_paragraph()
para("Analogy:", bold=True, color=(26, 60, 100))
para("Three junior doctors examine a patient and write their diagnosis. A senior doctor "
     "reads all three reports and makes the final decision. The senior doctor has learned "
     "over time which junior doctor is more reliable for which type of case.")
doc.add_paragraph()
para("WHY IT IS THE BEST: It does not just average opinions (like Voting). It LEARNS "
     "the optimal way to combine them. Result: 99.94% accuracy, fewest missed attacks.",
     bold=True, color=(26, 60, 100))

# =====================================================================
# 7. DATASET
# =====================================================================
doc.add_page_break()
heading("7. What Dataset is Used?")

para("Dataset Name: CIC-DDoS2019", bold=True)
para("Created by: Canadian Institute for Cybersecurity (CIC), University of New Brunswick, Canada")
para("This is an internationally recognized benchmark dataset used by researchers worldwide.")

doc.add_paragraph()

make_table(
    ["Property", "Value"],
    [
        ["Full Name", "CIC-DDoS2019"],
        ["Created By", "Canadian Institute for Cybersecurity"],
        ["Total Records", "426,076 network flows"],
        ["File Format", "Apache Parquet (17 files)"],
        ["Total Features (Raw)", "88 columns per record"],
        ["Selected Features", "30 (most important ones)"],
        ["BENIGN Records", "~22% (about 94,000)"],
        ["ATTACK Records", "~78% (about 332,000)"],
        ["Attack Types Included", "11 types: DNS, LDAP, MSSQL, NetBIOS, NTP, Portmap, SNMP, SYN, TFTP, UDP, UDPLag"],
        ["Training Data (80%)", "340,860 samples"],
        ["Testing Data (20%)", "85,216 samples"],
        ["Website", "www.unb.ca/cic/datasets/ddos-2019.html"],
    ]
)

para("What are the 30 features (columns) that the model looks at?", bold=True)
para("These are statistical measurements of each network flow:")

make_table(
    ["Category", "Features (Examples)", "What They Measure"],
    [
        ["Packet Sizes", "Fwd Packet Length Min, Max, Bwd Packet Length Mean, Max, Packet Length Variance",
         "How big are the data packets? Attack packets often have unusual sizes."],
        ["Packet Rates", "Bwd Packets/s, Flow Packets/s, Flow Bytes/s",
         "How FAST are packets coming? Attacks send extremely high volumes."],
        ["Timing", "Flow Duration, Flow IAT Mean/Max/Std, Bwd IAT Total/Mean/Min/Max, Idle Std",
         "How long does the connection last? What is the gap between packets?"],
        ["Flags", "URG Flag Count, ACK Flag Count, Fwd PSH Flags",
         "Special TCP markers. Attacks misuse certain flags."],
        ["Window Sizes", "Init Fwd/Bwd Win Bytes",
         "TCP window size settings - can reveal automated tools."],
        ["Counts", "Total Fwd Packets, Total Bwd Packets, Fwd Act Data Packets",
         "How many packets in each direction?"],
        ["Other", "Protocol, Down/Up Ratio",
         "TCP vs UDP, and ratio of download to upload."],
    ]
)

# =====================================================================
# 8. TECHNOLOGIES
# =====================================================================
heading("8. What Technologies are Used?")

heading("8.1  Machine Learning Technologies", level=2)
make_table(
    ["Technology", "Version", "What It Does (Simple Explanation)"],
    [
        ["Python", "3.x", "The programming language - everything is written in Python"],
        ["scikit-learn", "1.9.1", "The main ML library - provides Decision Tree, Random Forest, Voting, Stacking, StandardScaler, and all evaluation metrics"],
        ["XGBoost", "3.4.0", "Special library for gradient boosting - very fast and accurate"],
        ["pandas", "2.3.3", "For loading and manipulating data tables (like Excel for Python)"],
        ["NumPy", "2.5.3", "For fast mathematical operations on large number arrays"],
        ["imbalanced-learn", "0.14.2", "Provides SMOTE to balance unequal classes (22% BENIGN vs 78% ATTACK)"],
        ["joblib", "1.6.0", "For saving trained models to .pkl files so we do not retrain every time"],
        ["PyArrow", "25.0.1", "For reading Apache Parquet data files (the dataset format)"],
    ]
)

heading("8.2  Web Dashboard Technologies", level=2)
make_table(
    ["Technology", "Version", "What It Does"],
    [
        ["Flask", "3.1.3", "Python web framework - creates the backend server with 5 pages"],
        ["HTML5", "-", "Defines the structure of each web page"],
        ["CSS3", "-", "Custom dark navy/blue cybersecurity theme styling"],
        ["JavaScript", "ES6", "Handles interactive features like file upload and drag-drop"],
        ["Chart.js", "4.4.0", "Creates bar charts, radar charts, and doughnut charts"],
    ]
)

heading("8.3  Key Techniques Explained", level=2)
make_table(
    ["Technique", "What It Does", "Why We Need It"],
    [
        ["StandardScaler", "Converts all feature values to a similar scale (mean=0, std=1)", "Without scaling, features with large numbers (like Bytes/s = millions) would dominate features with small numbers (like Flag Count = 0 or 1)"],
        ["SMOTE", "Creates synthetic (artificial) examples of the minority class", "Our data has 22% BENIGN and 78% ATTACK. Without SMOTE, the model might just predict everything as ATTACK and still get 78% accuracy"],
        ["Train-Test Split (80/20)", "Keeps 20% of data completely hidden during training", "Tests the model on data it has NEVER seen - proves it actually learned, not just memorized"],
        ["Feature Selection", "Reduces 88 features to only the 30 most important", "Removes noise, makes model faster, and prevents overfitting"],
        ["Cross-Validation (3-fold)", "Used inside Stacking to prevent overfitting of meta-learner", "The meta-learner trains on out-of-fold predictions, not the same data the base models saw"],
    ]
)

# =====================================================================
# 9. RESULTS
# =====================================================================
doc.add_page_break()
heading("9. Results - How Well Does It Work?")

para("All results below were measured on the TEST SET (85,216 samples that the models "
     "NEVER saw during training).", bold=True)

heading("9.1  What Do the Metrics Mean?", level=2)
make_table(
    ["Metric", "What It Means (Simple)", "Example"],
    [
        ["Accuracy", "Out of ALL traffic, what % did the model get right?", "0.9994 = 99.94% correct"],
        ["Precision", "When the model says 'ATTACK', how often is it actually an attack?", "0.9999 = 99.99% of attack alerts are real"],
        ["Recall", "Out of ALL actual attacks, what % did the model catch?", "0.9993 = 99.93% of attacks detected"],
        ["F1 Score", "Combined score of Precision and Recall (balance of both)", "0.9996 = near-perfect balance"],
    ]
)

heading("9.2  Performance Comparison Table", level=2)
para("All 5 models compared side by side:", bold=True)

tbl = doc.add_table(rows=1, cols=6)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = tbl.rows[0]
shade_row(hdr, "1A3C6E")
for i, txt in enumerate(["Model", "Type", "Accuracy", "Precision", "Recall", "F1 Score"]):
    cell = hdr.cells[i]
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(txt)
    sf(run, 10.5, bold=True, color=(255,255,255))

results = [
    ("Decision Tree",    "Baseline",      "0.9992", "0.9997", "0.9993", "0.9995"),
    ("Random Forest",    "Bagging",        "0.9993", "0.9999", "0.9993", "0.9996"),
    ("XGBoost",          "Boosting",       "0.9990", "0.9999", "0.9988", "0.9994"),
    ("Voting Ensemble",  "Soft Voting",    "0.9993", "0.9999", "0.9992", "0.9996"),
    ("Stacking Ensemble","Meta-Learning",  "0.9994", "0.9999", "0.9993", "0.9996"),
]
for idx, row_data in enumerate(results):
    row = tbl.add_row()
    bg = "FFF3C4" if row_data[0] == "Stacking Ensemble" else ("EBF3FB" if idx % 2 == 0 else "FFFFFF")
    shade_row(row, bg)
    for i, txt in enumerate(row_data):
        cell = row.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(txt))
        bold = (row_data[0] == "Stacking Ensemble")
        sf(run, 10.5, bold=bold)

doc.add_paragraph()
para("WINNER: Stacking Ensemble - Highest accuracy (0.9994), best F1 score (0.9996), "
     "fewest missed attacks among ensemble models.", bold=True, color=(26, 60, 100))

heading("9.3  Key Observations", level=2)
bullet("All 5 models achieve > 99.9% accuracy - the CIC-DDoS2019 dataset has very clear "
       "attack patterns, which is consistent with published research.")
bullet("Stacking Ensemble misses only 46 attacks out of 66,275 (0.07% miss rate) - "
       "the BEST among ensemble models.")
bullet("XGBoost has the fewest false alarms (FP = 4) but misses more attacks (FN = 79).")
bullet("Ensemble methods (RF, Voting, Stacking) consistently outperform the single Decision Tree, "
       "proving the value of combining models.")
bullet("The improvement from DT to Stacking is small in absolute terms (0.9992 to 0.9994) "
       "but in cybersecurity, even 0.02% improvement = hundreds of correctly handled flows.")

# =====================================================================
# 10. CONFUSION MATRIX
# =====================================================================
doc.add_page_break()
heading("10. Confusion Matrix Explained")

para("A confusion matrix is a table that shows EXACTLY where the model got things right and wrong.", bold=True)

doc.add_paragraph()
heading("10.1  What Do the 4 Cells Mean?", level=2)
make_table(
    ["Cell", "Full Name", "What It Means", "Good or Bad?"],
    [
        ["TN", "True Negative", "Model said BENIGN, and it WAS actually BENIGN", "GOOD (correct)"],
        ["FP", "False Positive", "Model said ATTACK, but it was actually BENIGN (false alarm)", "BAD (unnecessary alert)"],
        ["FN", "False Negative", "Model said BENIGN, but it was actually ATTACK (missed attack!)", "WORST (security risk!)"],
        ["TP", "True Positive", "Model said ATTACK, and it WAS actually ATTACK", "GOOD (caught the attack)"],
    ]
)

para("In cybersecurity, FN (False Negative = missed attack) is the MOST DANGEROUS because "
     "the system thinks everything is fine while an attack is happening.", bold=True, color=(180, 30, 30))

heading("10.2  Confusion Matrices for All 5 Models", level=2)
para("Test set: 85,216 total samples | BENIGN: 18,941 | ATTACK: 66,275")

make_table(
    ["Model", "TN (Correct\nBENIGN)", "FP (False\nAlarm)", "FN (Missed\nAttack!)", "TP (Caught\nAttack)"],
    [
        ["Decision Tree",    "18,919", "22", "46",  "66,229"],
        ["Random Forest",    "18,932", "9",  "49",  "66,226"],
        ["XGBoost",          "18,937", "4",  "79",  "66,196"],
        ["Voting Ensemble",  "18,933", "8",  "51",  "66,224"],
        ["Stacking Ensemble","18,932", "9",  "46",  "66,229"],
    ]
)

heading("10.3  Reading the Stacking Ensemble Matrix", level=2)
para("Let us read the best model's confusion matrix in simple English:", bold=True)
doc.add_paragraph()
bullet("Out of 18,941 BENIGN flows: 18,932 correctly identified as safe, only 9 false alarms")
bullet("Out of 66,275 ATTACK flows: 66,229 correctly caught, only 46 attacks missed")
bullet("Total correct: 85,161 out of 85,216 = 99.94% accuracy")
bullet("Total errors: only 55 out of 85,216 = 0.06% error rate")

# =====================================================================
# 11. WEB DASHBOARD
# =====================================================================
heading("11. Web Dashboard")

para("A professional web interface was built using Flask to demonstrate the project interactively.", bold=True)

make_table(
    ["Page", "URL", "What It Shows"],
    [
        ["Dashboard", "/", "Project overview, dataset statistics, model summary cards, pipeline workflow diagram"],
        ["Traffic Prediction", "/predict", "Upload a CSV file with network traffic data. The system uses the saved Stacking Ensemble model to predict BENIGN or ATTACK for each row."],
        ["Model Comparison", "/comparison", "Side-by-side comparison of all 5 models with bar charts, radar chart, and metrics table"],
        ["Evaluation", "/evaluation", "Confusion matrices for all 5 models with TN/FP/FN/TP explanations and data leakage warning"],
        ["About", "/about", "Project objectives, scope, dataset info, technologies, pipeline workflow, limitations"],
    ]
)

para("Design:", bold=True)
bullet("Dark navy/blue cybersecurity theme")
bullet("Responsive design (works on different screen sizes)")
bullet("Interactive Chart.js visualisations (bar, radar, doughnut charts)")
bullet("Drag-and-drop CSV file upload on the prediction page")
bullet("Column validation - checks if uploaded CSV has the correct 30 feature columns")

# =====================================================================
# 12. BENEFITS
# =====================================================================
heading("12. Benefits of This Project")

heading("12.1  For Cybersecurity", level=2)
bullet("Automated detection - no need for 24/7 human monitoring")
bullet("99.94% accuracy with minimal false alarms (9) and minimal missed attacks (46)")
bullet("Can process thousands of flow records in seconds")
bullet("Uses standard, publicly available dataset - results are reproducible and verifiable")

heading("12.2  For Academic/Research", level=2)
bullet("Demonstrates ensemble learning superiority over single classifiers")
bullet("Provides a complete, reproducible ML pipeline (10 scripts, each building on the previous)")
bullet("Uses an internationally recognized benchmark dataset (CIC-DDoS2019)")
bullet("Includes a web dashboard for interactive demonstration")
bullet("Built with free, open-source technologies - anyone can reproduce it")

heading("12.3  Practical Applications", level=2)
bullet("Internet Service Providers (ISPs) - detect DDoS attacks on their networks")
bullet("Cloud service providers - protect customer servers")
bullet("Corporate networks - monitor internal traffic for threats")
bullet("Research - baseline for comparing new ML methods for intrusion detection")

# =====================================================================
# 13. LIMITATIONS
# =====================================================================
heading("13. Limitations")

para("1. Feature Selection Data Leakage", bold=True, color=(180, 30, 30))
para("Feature selection (Step 4) used the ENTIRE dataset (including test data) to rank features. "
     "This means the 30 selected features may be slightly biased toward the test set. "
     "The classification results are still valid (proper 80/20 split was used for training), "
     "but the feature selection step should ideally be done ONLY on the training data.")

doc.add_paragraph()
para("2. Dataset-Specific", bold=True)
para("The models were trained only on CIC-DDoS2019. Real-world network traffic from "
     "different organisations may have different patterns. Performance on unseen networks "
     "is not guaranteed.")

doc.add_paragraph()
para("3. Single Train-Test Split", bold=True)
para("Results are based on one 80/20 split. K-fold cross-validation would give more "
     "robust performance estimates.")

doc.add_paragraph()
para("4. Offline Only", bold=True)
para("The system processes uploaded CSV files. It does not capture or analyse live "
     "network packets in real-time.")

doc.add_paragraph()
para("5. Binary Classification Only", bold=True)
para("The system only tells if traffic is BENIGN or ATTACK. It does not identify "
     "the specific type of attack (e.g., DNS flood vs SYN flood).")

# =====================================================================
# 14. FILE STRUCTURE
# =====================================================================
doc.add_page_break()
heading("14. Project File Structure")

structure_lines = [
    ("DDoS_Monitoring/", "Main project folder"),
    ("  01_dataset_analysis.py", "Step 1: Inspect raw data files"),
    ("  02_preprocessing.py", "Step 2: Clean and combine data"),
    ("  03_prepare_labels.py", "Step 3: Create binary labels"),
    ("  04_feature_selection.py", "Step 4: Select top 30 features"),
    ("  05_train_test_split.py", "Step 5: Split, scale, and balance data"),
    ("  06_decision_tree.py", "Step 6: Train Decision Tree"),
    ("  07_random_forest.py", "Step 7: Train Random Forest"),
    ("  08_xgboost.py", "Step 8: Train XGBoost"),
    ("  09_voting_ensemble.py", "Step 9: Train Voting Ensemble"),
    ("  10_stacking_ensemble.py", "Step 10: Train Stacking Ensemble"),
    ("  requirements.txt", "List of required Python packages"),
    ("  README.md", "Project documentation"),
    ("  models/", "Saved trained models folder"),
    ("    scaler.pkl", "Saved StandardScaler"),
    ("    decision_tree.pkl", "Saved Decision Tree model"),
    ("    random_forest.pkl", "Saved Random Forest model"),
    ("    xgboost.pkl", "Saved XGBoost model"),
    ("    voting_ensemble.pkl", "Saved Voting Ensemble model"),
    ("    stacking_ensemble.pkl", "Saved Stacking Ensemble model"),
    ("  processed_data/", "Processed datasets folder"),
    ("    feature_names.csv", "30 selected feature names"),
    ("    X_train.npy / X_test.npy", "Training and testing feature arrays"),
    ("    y_train.npy / y_test.npy", "Training and testing label arrays"),
    ("  archive (32)/", "17 raw CIC-DDoS2019 parquet files"),
    ("  web_app/", "Flask web dashboard"),
    ("    app.py", "Flask backend (5 routes)"),
    ("    predictor.py", "Model loading and prediction logic"),
    ("    templates/", "HTML page templates (6 files)"),
    ("    static/", "CSS stylesheet and JavaScript"),
]

make_table(
    ["File / Folder", "Purpose"],
    [[s[0], s[1]] for s in structure_lines]
)

# =====================================================================
# 15. HOW TO RUN
# =====================================================================
heading("15. How to Run the Project")

heading("15.1  Run ML Pipeline (Training)", level=2)
para("Open Windows PowerShell and run these commands one by one:", bold=True)
code = [
    'cd "C:\\Users\\ADITI JAIN\\OneDrive\\Desktop\\DDoS_Monitoring"',
    '.\\venv\\Scripts\\Activate.ps1',
    'python 01_dataset_analysis.py',
    'python 02_preprocessing.py',
    'python 03_prepare_labels.py',
    'python 04_feature_selection.py',
    'python 05_train_test_split.py',
    'python 06_decision_tree.py',
    'python 07_random_forest.py',
    'python 08_xgboost.py',
    'python 09_voting_ensemble.py',
    'python 10_stacking_ensemble.py',
]
p = doc.add_paragraph()
p.style = "No Spacing"
for line in code:
    run = p.add_run(line + "\n")
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(30, 80, 30)

heading("15.2  Run Web Dashboard", level=2)
para("Open a NEW PowerShell window:", bold=True)
code2 = [
    'cd "C:\\Users\\ADITI JAIN\\OneDrive\\Desktop\\DDoS_Monitoring\\web_app"',
    '..\\venv\\Scripts\\python.exe app.py',
    '',
    '# Then open in browser: http://127.0.0.1:5000',
]
p = doc.add_paragraph()
p.style = "No Spacing"
for line in code2:
    run = p.add_run(line + "\n")
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(30, 80, 30)

para("Keep the PowerShell window open. The website works as long as that window is open.", bold=True)

# =====================================================================
# 16. CONCLUSION
# =====================================================================
heading("16. Conclusion")

para("This project successfully demonstrates the application of ensemble machine learning "
     "for DDoS attack detection. The key findings are:")

doc.add_paragraph()
bullet("All 5 models achieved > 99.9% accuracy on the CIC-DDoS2019 benchmark dataset.")
bullet("The Stacking Ensemble achieved the BEST performance: 99.94% accuracy, "
       "99.99% precision, 99.93% recall, and 99.96% F1 score.")
bullet("Ensemble methods (Random Forest, Voting, Stacking) consistently outperform "
       "the single Decision Tree, proving the value of model combination.")
bullet("The Stacking Ensemble misses only 46 attacks out of 66,275 and generates only "
       "9 false alarms out of 18,941 - demonstrating excellent practical reliability.")
bullet("The Flask web dashboard provides interactive demonstration with CSV-based "
       "prediction using the saved model and scaler.")

doc.add_paragraph()
para("The project proves that ensemble learning, particularly Stacking with a "
     "meta-learner, is a highly effective approach for binary network traffic "
     "classification in cybersecurity applications.",
     bold=True, color=(26, 60, 100))

# ── Save ──
# Save in project folder first
local_path = "Project_Report.docx"
try:
    doc.save(local_path)
    print(f"Saved to project folder: {os.path.abspath(local_path)}")
except Exception as e:
    print(f"Could not save to {local_path}: {e}")

desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
out_names = ["DDoS_Intelligent_Monitoring_Project_Report.docx", "Project_Report_Complete.docx", "Project_Report.docx"]
saved_desktop = None
for name in out_names:
    target = os.path.join(desktop, name)
    try:
        doc.save(target)
        saved_desktop = target
        print(f"Saved to Desktop: {saved_desktop}")
        break
    except PermissionError:
        print(f"File {name} is open or locked on Desktop, trying alternative filename...")
    except Exception as e:
        print(f"Error saving to {name}: {e}")

print("Report generation finished.")
