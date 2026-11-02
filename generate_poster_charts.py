"""
generate_poster_charts.py
Generates high-resolution graphical assets for the A3 Research Poster:
1. Feature Importance Horizontal Bar Chart
2. Model Comparison Bar Chart (Accuracy & F1)
3. Dataset Donut Chart (Traffic Class Distribution)
4. Confusion Matrix Heatmap
5. Network Architecture Flow Diagram
6. GitHub QR Code
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "poster_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Common styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
TEAL_PRIMARY = '#1f5f73'
TEAL_DARK = '#143e4b'
TEAL_LIGHT = '#3b8b9b'
ACCENT_BLUE = '#2575fc'
CORAL_ACCENT = '#e65c53'
GREEN_ACCENT = '#2ca02c'
BG_LIGHT = '#f8fafd'

# 1. Feature Importance Horizontal Bar Chart
def create_feature_importance():
    fig, ax = plt.subplots(figsize=(4.8, 2.7), dpi=300)
    features = [
        "Protocol",
        "Flow IAT Mean",
        "Bwd Pkt Len Max",
        "Fwd Pkt Len Mean",
        "Fwd Pkt Len Max",
        "Flow Duration"
    ]
    scores = [0.08, 0.12, 0.16, 0.19, 0.22, 0.23]
    
    colors = ['#8fc1cc', '#6baab8', '#4993a4', '#2d7c90', '#1f5f73', '#143e4b']
    bars = ax.barh(features, scores, color=colors, height=0.6, edgecolor='none')
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.005, bar.get_y() + bar.get_height()/2, f'{w:.2f}',
                ha='left', va='center', fontsize=9, fontweight='bold', color='#143e4b')
        
    ax.set_xlim(0, 0.28)
    ax.set_xlabel('Relative Importance Score', fontsize=9, fontweight='bold', color='#333333')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(colors='#333333', labelsize=8.5)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor(BG_LIGHT)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'feature_importance.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# 2. Model Comparison Bar Chart
def create_model_comparison():
    fig, ax = plt.subplots(figsize=(5.0, 2.7), dpi=300)
    models = ['Decision\nTree', 'Random\nForest', 'XGBoost', 'Voting\nEnsemble', 'Stacking\n(Best)']
    accuracy = [99.92, 99.93, 99.90, 99.93, 99.94]
    f1_score = [99.95, 99.96, 99.94, 99.96, 99.96]
    
    x = np.arange(len(models))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, accuracy, width, label='Accuracy (%)', color='#2d7c90', edgecolor='white', linewidth=1)
    rects2 = ax.bar(x + width/2, f1_score, width, label='F1-Score (%)', color='#e67e22', edgecolor='white', linewidth=1)
    
    ax.set_ylim(99.85, 100.0)
    ax.set_ylabel('Score (%)', fontsize=9, fontweight='bold', color='#333333')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=8, fontweight='bold')
    ax.legend(loc='lower left', fontsize=8, frameon=True, facecolor='white', framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(colors='#333333', labelsize=8)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor(BG_LIGHT)
    
    # Annotate best model
    ax.annotate('99.94%', xy=(4 - width/2, 99.94), xytext=(4 - width/2 - 0.2, 99.97),
                arrowprops=dict(arrowstyle="->", color='#143e4b', lw=1.2),
                fontsize=8, fontweight='bold', color='#143e4b')
    
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'model_comparison.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# 3. Donut Chart: Traffic Distribution
def create_donut_distribution():
    fig, ax = plt.subplots(figsize=(3.4, 2.7), dpi=300)
    sizes = [78, 22]
    labels = ['DDoS Attack\n(78%)', 'Benign\n(22%)']
    colors = ['#d9534f', '#2ca02c']
    
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.0f%%', startangle=140,
        colors=colors, pctdistance=0.72,
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2),
        textprops=dict(color='#222222', fontsize=8, fontweight='bold')
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_weight('bold')
        
    ax.text(0, 0, 'CIC-DDoS\n2019', ha='center', va='center', fontsize=9, fontweight='bold', color='#1f5f73')
    fig.patch.set_facecolor(BG_LIGHT)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'donut_distribution.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# 4. Confusion Matrix Heatmap
def create_confusion_matrix():
    fig, ax = plt.subplots(figsize=(3.6, 2.7), dpi=300)
    # Matrix data: [[TN, FP], [FN, TP]]
    matrix = np.array([[18932, 9], [46, 66229]])
    
    # Custom colored blocks
    cmap = plt.cm.Blues
    im = ax.imshow([[0.2, 0.9], [0.85, 0.1]], cmap=plt.cm.coolwarm_r, alpha=0.15)
    
    labels = [
        [f"TN = 18,932\n(Benign OK)", f"FP = 9\n(False Alarm)"],
        [f"FN = 46\n(Missed)", f"TP = 66,229\n(Detected)"]
    ]
    colors_text = [
        ['#155724', '#721c24'],
        ['#856404', '#155724']
    ]
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Pred Benign', 'Pred Attack'], fontsize=8.5, fontweight='bold', color='#143e4b')
    ax.set_yticklabels(['Actual Benign', 'Actual Attack'], fontsize=8.5, fontweight='bold', color='#143e4b')
    
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j], ha="center", va="center",
                    color=colors_text[i][j], fontsize=8.5, fontweight="bold")
            
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor(BG_LIGHT)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'confusion_matrix.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# 5. Network Security Architecture Infographic
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(5.5, 3.4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # 1. Incoming traffic
    box_props = dict(boxstyle="round,pad=0.3", fc="#eef4f8", ec="#2d7c90", lw=1.5)
    alert_box = dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#d32f2f", lw=1.5)
    benign_box = dict(boxstyle="round,pad=0.3", fc="#e8f5e9", ec="#388e3c", lw=1.5)
    model_box = dict(boxstyle="round,pad=0.3", fc="#e0f2f1", ec="#00796b", lw=1.5)
    meta_box = dict(boxstyle="round,pad=0.35", fc="#fff8e1", ec="#f57f17", lw=2)
    dash_box = dict(boxstyle="round,pad=0.3", fc="#e8eaf6", ec="#3f51b5", lw=1.5)
    
    ax.text(1.2, 4.5, "Incoming Traffic\n(CIC-DDoS2019)", ha="center", va="center", bbox=box_props, fontsize=8, fontweight='bold', color='#143e4b')
    ax.text(1.2, 2.0, "30 Selected\nFeatures + Scaler", ha="center", va="center", bbox=box_props, fontsize=8, fontweight='bold', color='#143e4b')
    ax.annotate('', xy=(1.2, 2.7), xytext=(1.2, 3.8), arrowprops=dict(arrowstyle="->", color="#2d7c90", lw=2))
    
    # Base Models
    ax.text(4.2, 4.8, "Decision Tree (DT)", ha="center", va="center", bbox=model_box, fontsize=7.5, fontweight='bold', color='#004d40')
    ax.text(4.2, 3.8, "Random Forest (RF)", ha="center", va="center", bbox=model_box, fontsize=7.5, fontweight='bold', color='#004d40')
    ax.text(4.2, 2.8, "XGBoost Classifier", ha="center", va="center", bbox=model_box, fontsize=7.5, fontweight='bold', color='#004d40')
    ax.text(4.2, 1.8, "Voting Ensemble", ha="center", va="center", bbox=model_box, fontsize=7.5, fontweight='bold', color='#004d40')
    
    # Connect features to base models
    for y_pos in [4.8, 3.8, 2.8, 1.8]:
        ax.annotate('', xy=(3.0, y_pos), xytext=(2.2, 2.0), arrowprops=dict(arrowstyle="->", color="#4db6ac", lw=1.2))
        
    # Meta Learner Stacking
    ax.text(6.8, 3.3, "Stacking Ensemble\nMeta-Learner\n(Logistic Regression)", ha="center", va="center", bbox=meta_box, fontsize=8, fontweight='bold', color='#b78103')
    for y_pos in [4.8, 3.8, 2.8, 1.8]:
        ax.annotate('', xy=(5.8, 3.3), xytext=(5.1, y_pos), arrowprops=dict(arrowstyle="->", color="#f57f17", lw=1.2))
        
    # Output to Dashboard & Alert
    ax.text(9.0, 4.5, "ATTACK Detected\n(Confidence: 99.9%)", ha="center", va="center", bbox=alert_box, fontsize=7.5, fontweight='bold', color='#c62828')
    ax.text(9.0, 2.1, "BENIGN Traffic\n(Flow Passed)", ha="center", va="center", bbox=benign_box, fontsize=7.5, fontweight='bold', color='#2e7d32')
    ax.annotate('', xy=(8.1, 4.5), xytext=(7.8, 3.5), arrowprops=dict(arrowstyle="->", color="#d32f2f", lw=1.5))
    ax.annotate('', xy=(8.1, 2.1), xytext=(7.8, 3.1), arrowprops=dict(arrowstyle="->", color="#388e3c", lw=1.5))
    
    fig.patch.set_facecolor(BG_LIGHT)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, 'architecture_diagram.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# 6. QR Code to GitHub
def create_qr_code():
    url = "https://github.com/JainAditi123/Intelligent-Network-Traffic-Monitoring-System"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#143e4b", back_color="white")
    img.save(os.path.join(ASSETS_DIR, 'github_qr.png'))

if __name__ == '__main__':
    print("Generating poster visual assets...")
    create_feature_importance()
    create_model_comparison()
    create_donut_distribution()
    create_confusion_matrix()
    create_architecture_diagram()
    create_qr_code()
    print("All assets generated successfully in poster_assets/")
