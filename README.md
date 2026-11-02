# Develop Intelligent Network Traffic Monitoring System
### Using CIC-DDoS2019 Dataset and Ensemble Learning Architectures

---

## 1. Project Overview

This project implements a complete, reproducible machine learning pipeline and interactive web monitoring system for **binary network traffic classification** — distinguishing between normal user traffic (**BENIGN**) and Distributed Denial-of-Service attacks (**ATTACK**).

It leverages the benchmark **CIC-DDoS2019 dataset** (Canadian Institute for Cybersecurity) across 17 Apache Parquet files covering 11 DDoS attack scenarios. The system evaluates five distinct machine learning paradigms, demonstrating how ensemble meta-learning (Stacking) achieves superior sensitivity (lowest missed attacks) compared to individual classifiers.

An interactive **Flask web dashboard** is included to allow batch traffic analysis, instant demonstration benchmarks, schema validation, calibrated confidence scoring, and CSV prediction export.

---

## 2. Project Scope & Boundaries

| Category | In Scope (Implemented) | Out of Scope (Planned Future Scope) |
|---|---|---|
| **Classification** | Binary classification (`BENIGN` vs. `ATTACK`) | Attack-family classification (e.g. DNS vs SYN) |
| **Data Processing** | Batch flow records in Parquet / CSV format | Live kernel packet capture (libpcap / Scapy) |
| **Mitigation** | Threat detection & confidence scoring | Active firewall packet dropping / eBPF filtering |
| **Models** | DT, Random Forest, XGBoost, Voting, Stacking | Deep learning (RNN, LSTM, Transformers) |
| **Deployment** | Local WSGI / Flask local development | Distributed Kubernetes multi-cloud streaming |

---

## 3. Dataset Specifications (CIC-DDoS2019)

- **Source:** Canadian Institute for Cybersecurity (University of New Brunswick)
- **Format:** Apache Parquet (17 files)
- **Total Cleaned Records:** **426,076** network flows
- **Feature Count:** Reduced from 88 raw flow features to **30 selected features** via Random Forest feature importance.
- **Attack Types Included (11):** DNS, LDAP, MSSQL, NetBIOS, NTP, Portmap, SNMP, SYN, TFTP, UDP, UDPLag.

### Verified Dataset Partitions

```
Total Cleaned Dataset: 426,076 flows (94,704 BENIGN [22.2%] / 331,372 ATTACK [77.8%])
│
├── Training Split (80% Stratified): 340,860 flows
│   ├── Pre-SMOTE Distribution: 75,763 BENIGN (22.2%) / 265,097 ATTACK (77.8%)
│   └── Post-SMOTE Distribution: 265,097 BENIGN (50.0%) / 265,097 ATTACK (50.0%) -> Total 530,194 flows
│
└── Held-out Test Split (20% Stratified): 85,216 flows
    └── Test Distribution: 18,941 BENIGN (22.2%) / 66,275 ATTACK (77.8%)
```

---

## 4. The 30 Selected Features

The 30 selected features represent statistical summaries of bidirectional network flows:

1. `Fwd Packet Length Min`
2. `Bwd Packets/s`
3. `Total Backward Packets`
4. `Packet Length Max`
5. `Bwd Header Length`
6. `Bwd IAT Total`
7. `Fwd Packets Length Total`
8. `URG Flag Count`
9. `Init Fwd Win Bytes`
10. `Bwd IAT Min`
11. `Down/Up Ratio`
12. `Bwd IAT Mean`
13. `Flow Packets/s`
14. `Fwd Packet Length Max`
15. `Bwd IAT Max`
16. `Flow IAT Mean`
17. `ACK Flag Count`
18. `Init Bwd Win Bytes`
19. `Protocol`
20. `Flow IAT Max`
21. `Flow IAT Std`
22. `Idle Std`
23. `Bwd Packet Length Mean`
24. `Fwd Act Data Packets`
25. `Bwd Packet Length Max`
26. `Flow Duration`
27. `Flow Bytes/s`
28. `Fwd PSH Flags`
29. `Packet Length Variance`
30. `Total Fwd Packets`

---

## 5. Model Architectures & Performance Comparison

All models were evaluated on the **held-out test set (85,216 samples)**. **Positive Class = ATTACK (1)**.

| Model | Architecture | Accuracy | Precision | Recall | F1-Score | FP (False Alarms) | FN (Missed Attacks) |
|---|---|---|---|---|---|---|---|
| **Decision Tree** | Single Recursive Tree (Baseline) | 0.9992 | 0.9997 | 0.9993 | 0.9995 | 22 | 46 |
| **Random Forest** | Bagging (100 Trees, Random Features) | 0.9993 | 0.9999 | 0.9993 | 0.9996 | 9 | 49 |
| **XGBoost** | Gradient Boosting (100 Estimators) | 0.9990 | 0.9999 | 0.9988 | 0.9994 | **4 (Lowest)** | 79 |
| **Voting Ensemble**| Soft Voting (DT + RF + XGBoost) | 0.9993 | 0.9999 | 0.9992 | 0.9996 | 8 | 51 |
| **Stacking Ensemble**| Level-1 Meta-Learning (LogReg Meta) | **0.9994**| **0.9999**| **0.9993**| **0.9996**| 9 | **46 (Lowest)** |

### Confusion Matrix Ground Truth (85,216 Test Samples)
- Actual BENIGN (Class 0): 18,941 samples ($TN + FP$)
- Actual ATTACK (Class 1): 66,275 samples ($FN + TP$)

```
Stacking Ensemble Confusion Matrix:
               Predicted BENIGN    Predicted ATTACK
Actual BENIGN       18,932 (TN)            9 (FP)   -> 99.95% Benign Specificity
Actual ATTACK           46 (FN)       66,229 (TP)   -> 99.93% Attack Recall
```

---

## 6. Scientific Data Leakage Audit

### Audit Context
In the original baseline workflow (`04_feature_selection.py`), feature selection was computed on the entire dataset (426,076 records) before the 80/20 train-test split (`05_train_test_split.py`). This introduces a mild selection bias.

### Audit Implementation (`leakage_free_evaluation.py`)
To evaluate the impact of this leakage scientifically, a separate audit script was developed:
1. Stratified 80/20 split was executed **first**, completely isolating the 85,216 test flows.
2. Constant removal, correlation pruning, and Random Forest feature ranking were fitted **strictly on the 340,860 training samples only**.
3. `StandardScaler` was fitted strictly on training data.
4. Models were re-evaluated on the untouched test partition.

### Audit Findings
- **27 out of 30 top features (90.0%)** selected by the training set alone were **identical** to the baseline feature set.
- Model performance under strict leakage-free conditions remained above **99.84%** (Decision Tree: 0.9992, Random Forest: 0.9991, XGBoost: 0.9984).
- **Conclusion:** The high detection accuracy is primarily driven by the distinct statistical signatures of DDoS floods in the CIC-DDoS2019 dataset rather than artificial selection leakage.

---

## 7. Folder Structure

```
DDoS_Monitoring/
│
├── 01_dataset_analysis.py       # Inspect 17 raw parquet files
├── 02_preprocessing.py          # Concatenate and clean raw files
├── 03_prepare_labels.py         # Generate binary classification labels
├── 04_feature_selection.py      # Top 30 feature importance ranking
├── 05_train_test_split.py       # 80/20 split, StandardScaler, SMOTE balancing
├── 06_decision_tree.py          # Train & evaluate Decision Tree baseline
├── 07_random_forest.py          # Train & evaluate Random Forest ensemble
├── 08_xgboost.py                # Train & evaluate XGBoost ensemble
├── 09_voting_ensemble.py        # Train & evaluate Soft Voting ensemble
├── 10_stacking_ensemble.py      # Train & evaluate Stacking meta-learner
│
├── leakage_free_evaluation.py   # Independent leakage audit pipeline
├── test_full_system.py          # 11-category system verification suite
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
│
├── models/                      # Saved production model artifacts
│   ├── scaler.pkl               # Fitted StandardScaler (30 features)
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── voting_ensemble.pkl
│   └── stacking_ensemble.pkl
│
├── processed_data/              # Saved dataset arrays & schema
│   ├── feature_names.csv        # 30 feature schema
│   ├── X_train.npy / X_test.npy # Scaled & SMOTE numpy arrays
│   ├── y_train.npy / y_test.npy # Label numpy arrays
│   └── leakage_audit_results.json
│
└── web_app/                     # Flask Web Application
    ├── app.py                   # Web routes and API endpoints
    ├── predictor.py             # Inference engine, validation & probabilities
    ├── sample_data/             # Pre-extracted test CSV samples
    │   ├── sample_traffic_benign.csv
    │   ├── sample_traffic_attack.csv
    │   └── sample_traffic_mixed.csv
    ├── static/                  # Dark cybersecurity CSS & Chart.js
    └── templates/               # HTML5 Jinja2 Templates (5 Pages)
```

---

## 8. Setup & Execution Instructions (Windows PowerShell)

### Step 1: Clone & Environment Activation
```powershell
cd "C:\Users\ADITI JAIN\OneDrive\Desktop\DDoS_Monitoring"

# Activate existing virtual environment
.\venv\Scripts\Activate.ps1

# (Optional) Install dependencies if needed
pip install -r requirements.txt
```

### Step 2: Run Full System Verification Suite
```powershell
python test_full_system.py
```
*Expected Output: `TEST SUITE SUMMARY: 49 PASSED | 0 FAILED`.*

### Step 3: Run the Web Dashboard
```powershell
cd web_app
..\venv\Scripts\python.exe app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 9. Teacher Demonstration & Viva Guide

### How to Demonstrate to Your Professor in 3 Minutes:
1. **Show Dashboard (`/`):** Point out the verified sample counts (426,076 total, 340,860 pre-SMOTE vs. 530,194 post-SMOTE balanced, 85,216 test).
2. **Show Traffic Prediction (`/predict`):** Click **"⚡ Run Benign Test"** & show 100% normal classification with 99.9% confidence. Then click **"⚡ Run Attack Test"** & show 100% attack detection with critical threat status. Click **"📥 Download Predictions CSV"** to demonstrate real file generation.
3. **Show Model Comparison (`/comparison`):** Explain the trade-off table: Stacking has highest recall (FN=46), while XGBoost has lowest false alarms (FP=4).
4. **Show Evaluation (`/evaluation`):** Show the confusion matrices and explain the security significance of False Negatives vs. False Positives.
5. **Show Scientific Rigor (`/comparison` bottom):** Show the Leakage Audit table, explaining that you independently audited the pipeline with `leakage_free_evaluation.py` to verify that performance holds even when feature selection is restricted to training data.

### Top Viva Questions & Answers:
- **Q: Why use Stacking instead of just Voting?**  
  *A:* Soft Voting gives equal weight to all models. Stacking uses a Level-1 Logistic Regression meta-learner that learns optimal weights based on out-of-fold predictions, minimizing missed attacks.
- **Q: Why did you use SMOTE?**  
  *A:* The raw dataset had an imbalanced class distribution (22% Benign vs 78% Attack). Without balancing, models could bias towards the majority attack class. SMOTE balanced the training set to 50/50 without altering the test distribution.
- **Q: Does feature selection data leakage invalidate your 99.9% score?**  
  *A:* No. While the initial pipeline computed RF importance across the dataset, our dedicated audit (`leakage_free_evaluation.py`) proved that 27 of 30 features are identical when restricted strictly to training data, maintaining >99.84% accuracy.
