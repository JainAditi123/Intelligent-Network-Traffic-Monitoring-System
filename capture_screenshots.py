"""
capture_screenshots.py (v2)
===========================
Creates professional-looking placeholder screenshots for the 
DDoS Monitoring web dashboard pages using PIL.

Run from the project root:
    .\\venv\\Scripts\\python.exe capture_screenshots.py
"""

import pathlib
import sys

PROJ_ROOT = pathlib.Path(__file__).parent
SS_DIR    = PROJ_ROOT / "screenshots"
SS_DIR.mkdir(exist_ok=True)

BASE_URL = "http://127.0.0.1:5000"

pages_info = [
    ("01_dashboard.png",     "/",               "DASHBOARD — HOME",         "System overview, dataset stats, model summary cards, pipeline"),
    ("02_predict.png",       "/predict",        "TRAFFIC PREDICTION",       "CSV upload interface with drag-and-drop and model selector"),
    ("03_predict_results.png","/load-sample/mixed","PREDICTION RESULTS",    "Mixed traffic predictions: BENIGN (green) + ATTACK (red) rows"),
    ("04_comparison.png",    "/comparison",     "MODEL COMPARISON",         "Performance metrics table + 5 Chart.js charts (bar + radar)"),
    ("05_evaluation.png",    "/evaluation",     "CONFUSION MATRICES",       "TN/FP/FN/TP matrices for all 5 trained models"),
    ("06_about.png",         "/about",          "ABOUT THE PROJECT",        "Objectives, dataset, technology stack, pipeline steps"),
]

def create_screenshot(fname, path, title, description, live_page_html=None):
    try:
        from PIL import Image, ImageDraw
        
        W, H = 1280, 720
        
        # Colors
        BG_DARK    = (10, 22, 40)       # #0a1628
        SIDEBAR_BG = (8, 18, 32)        # #08121f
        ACCENT     = (78, 154, 241)     # #4e9af1
        TEAL       = (0, 212, 170)      # #00d4aa
        CARD_BG    = (14, 30, 58)       # #0e1e3a
        TEXT_LIGHT = (143, 163, 184)    # #8fa3b8
        WHITE      = (255, 255, 255)
        GREEN      = (0, 212, 170)
        RED        = (247, 37, 133)
        ORANGE     = (244, 162, 97)
        PURPLE     = (167, 139, 250)
        GOLD       = (255, 213, 79)

        img  = Image.new("RGB", (W, H), BG_DARK)
        draw = ImageDraw.Draw(img)

        # ── Sidebar ──
        draw.rectangle([0, 0, 220, H], fill=SIDEBAR_BG)
        draw.rectangle([220, 0, 223, H], fill=ACCENT)

        # Logo
        draw.ellipse([20, 18, 56, 54], outline=ACCENT, width=2)
        draw.text((38, 36), "S", fill=ACCENT, anchor="mm")
        draw.text((75, 28), "DDoS", fill=WHITE, anchor="lm")
        draw.text((75, 44), "Monitor", fill=TEXT_LIGHT, anchor="lm")

        # Nav links
        nav_items = [
            ("Dashboard",         "/",           ACCENT  if "DASH" in title else TEXT_LIGHT),
            ("Traffic Prediction","/predict",    ACCENT  if "PRED" in title else TEXT_LIGHT),
            ("Model Comparison",  "/comparison", ACCENT  if "COMP" in title else TEXT_LIGHT),
            ("Evaluation",        "/evaluation", ACCENT  if "CONF" in title or "EVAL" in title else TEXT_LIGHT),
            ("About",             "/about",      ACCENT  if "ABOUT" in title else TEXT_LIGHT),
        ]
        y_nav = 100
        for nav_label, nav_path, nav_color in nav_items:
            if nav_color == ACCENT:
                draw.rectangle([0, y_nav - 12, 220, y_nav + 16], fill=(20, 50, 90))
                draw.rectangle([0, y_nav - 12, 4, y_nav + 16], fill=ACCENT)
            draw.text((30, y_nav), nav_label, fill=nav_color, anchor="lm")
            y_nav += 46

        # Status indicator
        draw.ellipse([20, H-32, 30, H-22], fill=GREEN)
        draw.text((38, H-27), "5 Models Loaded", fill=TEXT_LIGHT, anchor="lm")

        # ── Top bar ──
        draw.rectangle([224, 0, W, 54], fill=CARD_BG)
        draw.line([224, 54, W, 54], fill=(20, 40, 80), width=1)
        draw.text((244, 28), title, fill=WHITE, anchor="lm")
        draw.text((W-20, 28), "http://127.0.0.1:5000" + path, fill=TEXT_LIGHT, anchor="rm")

        # ── Main content area ──
        content_x = 240
        content_y = 76

        if "DASH" in title:
            # Stat cards
            stats = [
                ("426,076",  "Total Records",    ACCENT),
                ("30",       "Features",         TEAL),
                ("5",        "Models Trained",   ORANGE),
                ("99.94%",   "Best Accuracy",    GREEN),
            ]
            cx = content_x + 10
            for val, label, color in stats:
                draw.rounded_rectangle([cx, content_y, cx+190, content_y+80], radius=8, fill=CARD_BG)
                draw.rounded_rectangle([cx, content_y, cx+190, content_y+5], radius=4, fill=color)
                draw.text((cx+95, content_y+35), val, fill=color, anchor="mm")
                draw.text((cx+95, content_y+60), label, fill=TEXT_LIGHT, anchor="mm")
                cx += 205

            # Pipeline diagram
            py = content_y + 110
            draw.text((content_x+10, py), "10-Step ML Pipeline", fill=ACCENT, anchor="lm")
            pipeline = ["Raw Data","Preprocess","Labels","Features","Split+Scale","SMOTE","DT","RF","XGB","Stack"]
            px = content_x + 10
            py2 = py + 30
            for i, step in enumerate(pipeline):
                draw.rounded_rectangle([px, py2, px+95, py2+36], radius=5, fill=(20, 50, 90))
                draw.text((px+48, py2+18), step, fill=WHITE, anchor="mm")
                if i < len(pipeline)-1:
                    draw.text((px+100, py2+18), "->", fill=ACCENT, anchor="mm")
                px += 108

            # Best model card
            bm_y = py2 + 60
            draw.rounded_rectangle([content_x+10, bm_y, content_x+580, bm_y+100], radius=8, fill=(20, 40, 90))
            draw.text((content_x+20, bm_y+18), "Best Model: Stacking Ensemble", fill=GOLD, anchor="lm")
            draw.text((content_x+20, bm_y+45), "Accuracy: 0.9994  |  F1: 0.9996  |  FN: 46  |  FP: 9", fill=WHITE, anchor="lm")
            draw.text((content_x+20, bm_y+72), "Meta-Learning (Logistic Regression) | test: 85,216 samples", fill=TEXT_LIGHT, anchor="lm")

        elif "PRED" in title and "RESULT" not in title:
            # Upload zone
            uy = content_y + 20
            draw.rounded_rectangle([content_x+20, uy, W-30, uy+180], radius=12,
                                    outline=ACCENT, width=2)
            draw.text(((content_x+20+W-30)//2, uy+70), "Drag & Drop CSV File Here", fill=ACCENT, anchor="mm")
            draw.text(((content_x+20+W-30)//2, uy+100), "or click to browse", fill=TEXT_LIGHT, anchor="mm")
            draw.text(((content_x+20+W-30)//2, uy+135), "Required: 30 network flow feature columns", fill=TEXT_LIGHT, anchor="mm")
            # Sample buttons
            bx = content_x + 20
            by = uy + 200
            for btn_label, btn_color in [("Load Benign Sample", GREEN), ("Load Attack Sample", RED), ("Load Mixed Sample", ORANGE)]:
                draw.rounded_rectangle([bx, by, bx+220, by+36], radius=6, fill=btn_color)
                draw.text((bx+110, by+18), btn_label, fill=(0,0,0), anchor="mm")
                bx += 235
            # Model selector
            draw.text((content_x+20, by+60), "Selected Model:", fill=TEXT_LIGHT, anchor="lm")
            draw.rounded_rectangle([content_x+160, by+46, content_x+420, by+76], radius=5, fill=CARD_BG, outline=ACCENT, width=1)
            draw.text((content_x+290, by+61), "Stacking Ensemble (Default)", fill=WHITE, anchor="mm")

        elif "RESULT" in title:
            # Results table header
            cols = [("Row","#"), ("Flow Duration","sec"), ("Fwd Pkts","count"), ("Protocol","type"), ("Confidence","%"), ("Prediction","class")]
            cy = content_y + 10
            draw.rectangle([content_x+10, cy, W-20, cy+32], fill=(20, 50, 90))
            cx_t = content_x + 20
            for col_name, _ in cols:
                draw.text((cx_t, cy+16), col_name, fill=ACCENT, anchor="lm")
                cx_t += (W - content_x - 40) // len(cols)
            
            rows_data = [
                ("1", "0.000123", "45", "TCP",  "99.2%", "BENIGN",  GREEN),
                ("2", "0.002341", "892","UDP",  "98.7%", "ATTACK",  RED),
                ("3", "0.000089", "12", "TCP",  "99.8%", "BENIGN",  GREEN),
                ("4", "0.001876", "654","UDP",  "97.3%", "ATTACK",  RED),
                ("5", "0.000201", "28", "ICMP", "99.1%", "BENIGN",  GREEN),
                ("6", "0.003421", "987","UDP",  "99.5%", "ATTACK",  RED),
                ("7", "0.000156", "19", "TCP",  "98.9%", "BENIGN",  GREEN),
                ("8", "0.002109", "743","UDP",  "98.1%", "ATTACK",  RED),
            ]
            row_y = cy + 32
            for i, (r, dur, pkts, proto, conf, pred, pred_color) in enumerate(rows_data):
                bg = (12, 26, 48) if i % 2 == 0 else CARD_BG
                draw.rectangle([content_x+10, row_y, W-20, row_y+30], fill=bg)
                vals = [r, dur, pkts, proto, conf, ""]
                cx_t = content_x + 20
                for v in vals:
                    draw.text((cx_t, row_y+15), v, fill=WHITE, anchor="lm")
                    cx_t += (W - content_x - 40) // len(cols)
                # Prediction badge
                badge_x = cx_t - (W - content_x - 40) // len(cols) + 10
                draw.rounded_rectangle([badge_x-5, row_y+5, badge_x+80, row_y+25], radius=4, fill=pred_color)
                draw.text((badge_x+37, row_y+15), pred, fill=(0,0,0), anchor="mm")
                row_y += 30
            
            # Summary
            sy = row_y + 20
            draw.rounded_rectangle([content_x+10, sy, content_x+200, sy+60], radius=8, fill=CARD_BG)
            draw.text((content_x+20, sy+20), "Total: 50 flows", fill=WHITE, anchor="lm")
            draw.text((content_x+20, sy+44), "ATTACK: 25 (50%)  BENIGN: 25 (50%)", fill=TEXT_LIGHT, anchor="lm")

        elif "COMP" in title:
            # Metrics table
            cy = content_y + 10
            models_m = [("Decision Tree","0.9992","0.9997","0.9993","0.9995"),
                        ("Random Forest","0.9993","0.9999","0.9993","0.9996"),
                        ("XGBoost","0.9990","0.9999","0.9988","0.9994"),
                        ("Voting Ensemble","0.9993","0.9999","0.9992","0.9996"),
                        ("Stacking Ensemble","0.9994","0.9999","0.9993","0.9996"),]
            hdrs = ["Model","Accuracy","Precision","Recall","F1"]
            col_w = (W - content_x - 40) // len(hdrs)
            draw.rectangle([content_x+10, cy, W-20, cy+28], fill=(20, 50, 90))
            for i, h in enumerate(hdrs):
                draw.text((content_x+20 + i*col_w, cy+14), h, fill=ACCENT, anchor="lm")
            cy += 28
            colors_m = [ACCENT, TEAL, ORANGE, PURPLE, RED]
            for mi, (mname, *vals) in enumerate(models_m):
                bg = (20, 50, 90) if mname == "Stacking Ensemble" else (CARD_BG if mi%2==0 else BG_DARK)
                draw.rectangle([content_x+10, cy, W-20, cy+26], fill=bg)
                all_vals = [mname] + vals
                for i, v in enumerate(all_vals):
                    c = colors_m[mi] if i == 0 else WHITE
                    draw.text((content_x+20 + i*col_w, cy+13), v, fill=c, anchor="lm")
                cy += 26
            
            # Mini bar charts placeholder
            cy += 20
            chart_w = (W - content_x - 60) // 2
            chart_data = [("Accuracy", [0.9992,0.9993,0.999,0.9993,0.9994]),
                          ("F1 Score", [0.9995,0.9996,0.9994,0.9996,0.9996])]
            cx_c = content_x + 10
            for chart_name, chart_vals in chart_data:
                draw.rounded_rectangle([cx_c, cy, cx_c+chart_w, cy+130], radius=6, fill=CARD_BG)
                draw.text((cx_c+chart_w//2, cy+16), chart_name, fill=WHITE, anchor="mm")
                bar_w = (chart_w-30)//(len(chart_vals)+1)
                bx_c = cx_c + 20
                for i, (v, c) in enumerate(zip(chart_vals, colors_m)):
                    bh = int((v - 0.998) * 100000)
                    draw.rectangle([bx_c, cy+120-bh, bx_c+bar_w-4, cy+120], fill=c)
                    bx_c += bar_w
                cx_c += chart_w + 20

        elif "CONF" in title or "EVAL" in title:
            # Confusion matrices
            cm_data = [
                ("Decision Tree",    18919, 22, 46, 66229),
                ("Random Forest",    18932, 9,  49, 66226),
                ("XGBoost",          18937, 4,  79, 66196),
                ("Voting Ensemble",  18933, 8,  51, 66224),
                ("Stacking Ensemble",18932, 9,  46, 66229),
            ]
            mx = content_x + 20
            my = content_y + 20
            cell_w, cell_h = 95, 55
            for mi, (mname, tn, fp, fn, tp) in enumerate(cm_data):
                if mi == 3:
                    mx = content_x + 20 + 2 * (cell_w*2+30)
                    my = content_y + 20
                label_color = GOLD if mname == "Stacking Ensemble" else TEXT_LIGHT
                draw.text((mx + cell_w, my - 10), mname, fill=label_color, anchor="mm")
                # 2x2 grid
                for r, (val, bg_c, label) in enumerate([
                    (tn, (0,90,60),   f"TN={tn:,}"),
                    (fp, (120,20,40), f"FP={fp}"),
                    (fn, (120,60,0),  f"FN={fn}"),
                    (tp, (0,130,80),  f"TP={tp:,}"),
                ]):
                    row_r = r // 2
                    col_r = r % 2
                    x1 = mx + col_r * cell_w
                    y1 = my + row_r * cell_h
                    draw.rectangle([x1, y1, x1+cell_w-2, y1+cell_h-2], fill=bg_c)
                    draw.text((x1+cell_w//2, y1+cell_h//2), label, fill=WHITE, anchor="mm")
                
                mx += cell_w*2 + 30
                if mi == 1:
                    mx += cell_w*2 + 30
                if mi == 2:
                    mx = content_x + 20 + (cell_w*2+30)
                    my = content_y + cell_h*2 + 60

        elif "ABOUT" in title:
            # Tech stack grid
            tech_items = [
                ("Python 3.11", ACCENT), ("scikit-learn 1.9", TEAL), ("XGBoost 3.4", ORANGE),
                ("Flask 3.1", PURPLE), ("Chart.js 4.4", RED), ("pandas 2.3", GREEN),
                ("NumPy 2.5", GOLD), ("joblib 1.6", ACCENT), ("pyarrow 25.0", TEAL),
            ]
            tx = content_x + 10
            ty = content_y + 30
            draw.text((content_x+20, content_y+10), "Technology Stack", fill=WHITE, anchor="lm")
            for i, (tech, tc) in enumerate(tech_items):
                if i > 0 and i % 3 == 0:
                    tx = content_x + 10
                    ty += 56
                draw.rounded_rectangle([tx, ty, tx+175, ty+44], radius=6, fill=CARD_BG)
                draw.rounded_rectangle([tx, ty, tx+175, ty+4], radius=3, fill=tc)
                draw.text((tx+88, ty+26), tech, fill=WHITE, anchor="mm")
                tx += 190
            
            # Pipeline steps
            py_a = ty + 70
            draw.text((content_x+20, py_a), "10-Step Pipeline", fill=WHITE, anchor="lm")
            steps_a = ["01 Dataset Analysis","02 Preprocessing","03 Labels","04 Features",
                       "05 Split+SMOTE","06 Decision Tree","07 Random Forest","08 XGBoost","09 Voting","10 Stacking"]
            sx = content_x + 10
            sy_a = py_a + 30
            for i, step in enumerate(steps_a[:5]):
                draw.rounded_rectangle([sx, sy_a, sx+192, sy_a+34], radius=5, fill=CARD_BG)
                draw.text((sx+10, sy_a+17), step, fill=ACCENT, anchor="lm")
                sx += 205
            sx = content_x + 10
            for step in steps_a[5:]:
                draw.rounded_rectangle([sx, sy_a+46, sx+192, sy_a+80], radius=5, fill=CARD_BG)
                draw.text((sx+10, sy_a+63), step, fill=TEAL, anchor="lm")
                sx += 205

        # ── Status bar at bottom ──
        draw.rectangle([224, H-36, W, H], fill=CARD_BG)
        draw.line([224, H-36, W, H-36], fill=(20,40,80), width=1)
        draw.text((244, H-18), "Flask 3.1.3  |  scikit-learn 1.9.1  |  XGBoost 3.4.0  |  CIC-DDoS2019 Dataset", 
                  fill=TEXT_LIGHT, anchor="lm")
        draw.text((W-20, H-18), "http://127.0.0.1:5000" + path, fill=ACCENT, anchor="rm")

        out = SS_DIR / fname
        img.save(str(out))
        print(f"  Saved: {out.name}")
        return True

    except Exception as e:
        print(f"  ERROR creating {fname}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*60)
    print("  Creating Dashboard Screenshots")
    print("="*60)
    
    ok = 0
    for fname, path, title, desc in pages_info:
        if create_screenshot(fname, path, title, desc):
            ok += 1
    
    print(f"\nDone. {ok}/{len(pages_info)} screenshots created in: {SS_DIR}")
