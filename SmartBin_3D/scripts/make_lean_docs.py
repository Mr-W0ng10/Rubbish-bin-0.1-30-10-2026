# -*- coding: utf-8 -*-
"""Build concise EN/ZH HK$1,000 design briefs (DOCX + PDF source)."""
import os, sys
from pathlib import Path
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
sys.path.insert(0, r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_Design_Package\04_Source")
import make_docx as MD

BASE = Path(r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D")
OUT = BASE / "docs"
OUT.mkdir(exist_ok=True)
REND = BASE / "renders"
MD.DRAW = REND

GREEN = MD.GREEN
INK = MD.INK
MUTED = MD.MUTED
RED = MD.RED
WHITE = MD.WHITE


def cover(doc, lang):
    t = doc.add_table(rows=1, cols=1)
    t.autofit = False
    t.columns[0].width = Mm(166)
    cell = t.cell(0, 0)
    cell.width = Mm(166)
    MD.shade(cell, "1F4E45")
    MD.cell_margins(cell, 7, 7, 7, 7)
    MD.set_row_height(t.rows[0], 40)
    p = cell.paragraphs[0]
    r = p.add_run("SMART WASTE SORTING BIN" if lang == "en" else "智能分類垃圾桶")
    MD.set_run_font(r, size=24, bold=True, color=WHITE)
    p2 = cell.add_paragraph()
    r = p2.add_run("HK$1,000 LEAN PROTOTYPE  ·  VERSION 2.0" if lang == "en" else "HK$1,000 精簡原型  ·  版本 2.0")
    MD.set_run_font(r, size=12, bold=True, color=RGBColor(0xD8, 0xE8, 0xB1))

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    r = p.add_run("Standalone edge AI: ESP32-S3-CAM + MobileNetV2 + sensor fusion" if lang == "en" else "Standalone edge AI：ESP32-S3-CAM＋MobileNetV2＋感測器融合")
    MD.set_run_font(r, size=16, bold=True, color=GREEN)

    p = doc.add_paragraph()
    r = p.add_run("420 × 420 × 900 mm  ·  4 × 8.7 L  ·  BOM HK$866  ·  total ≈ HK$996" if lang == "en"
                  else "420 × 420 × 900 mm  ·  4 × 8.7 L  ·  BOM HK$866  ·  總計約 HK$996")
    MD.set_run_font(r, size=10, color=MUTED)

    img = REND / "00_overview.png"
    if img.exists():
        doc.add_picture(str(img), width=Mm(162))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.paragraphs[-1].paragraph_format.space_after = Pt(2)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    r = p.add_run("Standalone: no laptop, no cloud, no agent. MobileNetV2 runs on the ESP32-S3-CAM; WiFi AP is only for optional phone monitoring." if lang == "en"
                  else "Standalone：不需要 laptop、不需要雲端、不需要 agent。MobileNetV2 在 ESP32-S3-CAM 上跑；WiFi AP 只給手機可選監看。")
    MD.set_run_font(r, size=8.5, color=RED, italic=True)


def build(lang):
    files = []
    doc = Document()
    MD.setup_document(doc, lang)
    for r in doc.sections[0].header.paragraphs[0].runs:
        if "v1.0" in r.text:
            r.text = "v2.0"
    cover(doc, lang)
    doc.add_page_break()

    if lang == "en":
        MD.add_heading(doc, "1. Why this version is feasible", 1, lang)
        MD.add_paragraph(doc, "The previous HK$1,000 sketch used a 28BYJ-48 stepper and a tilting load-cell tray. Both are marginal: the 28BYJ-48 has only ~0.033 N·m, and a tilting tray side-loads the load cell. This version fixes both.", lang)
        MD.add_bullet(doc, "NEMA 17 (0.45 N·m) with 3:1 GT2 belt gives 1.35 N·m at the spout; required ≈ 0.34 N·m. Safety factor ≈ 4.", lang)
        MD.add_bullet(doc, "Fixed weigh platform + small trapdoor: the 5 kg load cell never carries the servo or door side-load. The MG996R only pulls the door; a spring closes it.", lang)
        MD.add_bullet(doc, "Top clearance is 225 mm (tray 635 mm, lid underside 860 mm), enough for an upright 500 mL bottle (~200 mm).", lang)
        MD.add_bullet(doc, "Four standard 170 × 170 × 300 mm bins, no corner notches; spout rotates above the bins.", lang)
        MD.add_bullet(doc, "12 V 3 A adapter + 5 V buck: no Li-ion pack, no charging risk, no BMS cost.", lang)
        MD.add_paragraph(doc, "Edge AI: ESP32-S3-CAM (8 MB PSRAM, 16 MB flash) runs MobileNetV2 0.35/0.5 at 96–128 px, INT8. MobileNetV2 1.0 at 224 px is too slow/large for this board; use transfer learning on the 0.35/0.5 backbone and fuse camera + weight + moisture + IR. No laptop, cloud or agent is used at run time.", lang)

        MD.add_heading(doc, "2. Dimensions and capacity", 1, lang)
        MD.add_table(doc, [
            ["Item", "Value"],
            ["Overall", "420 W × 420 D × 900 H mm"],
            ["Bins", "4 × 170 × 170 × 300 mm; ≈ 8.7 L each"],
            ["Total capacity", "≈ 34.7 L"],
            ["Weigh platform", "220 × 180 mm fixed frame; 180 × 140 mm trapdoor"],
            ["Funnel / spout", "220 × 200 → 75 mm; 75 mm elbow, outlet radius 100 mm"],
            ["Max item", "≈ 500 mL bottle / 330 mL can; ≤ 0.5 kg"],
            ["Cycle time", "≈ 6–10 s"],
            ["Target accuracy", "≥ 80–85% on a 50-item local dataset"],
        ], lang, font_size=8.5, widths=[44, 122])

        MD.add_heading(doc, "3. Internal structure", 1, lang)
        MD.add_figure(doc, "07_internal_labeled.png", "Figure 1. Internal structure: fixed platform, trapdoor, load cell, servo, funnel, NEMA 17 spout drive, bins, IR sensors and MCU bay.", 180, lang)
        MD.add_paragraph(doc, "The load path is deliberate: item → trapdoor → fixed platform → single 5 kg load cell → mid-frame. The servo and hinge are mounted on the platform frame, not on the load cell. When the trapdoor opens, the item falls through the funnel and the rotating spout into the selected bin. The spring closes the door when power is removed.", lang)
        MD.add_callout(doc, "Why the trapdoor matters", "A tilting tray changes the load-cell geometry and adds side-load. The fixed platform keeps weighing repeatable; the trapdoor only moves after the weight is recorded. This is the main mechanical fix for feasibility.", lang)

        MD.add_heading(doc, "4. Sensors and MCU locations", 1, lang)
        MD.add_figure(doc, "08_electronics_labeled.png", "Figure 2. Electronics bay: ESP32, HX711, A4988, USB link and wiring.", 175, lang)
        MD.add_table(doc, [
            ["Device", "Location", "Interface"],
            ["ESP32-S3-CAM", "Lid underside, looking down", "On-device inference"],
            ["IR safety beam", "Hopper mouth", "GPIO"],
            ["5 kg load cell", "Under fixed platform", "HX711"],
            ["Moisture pad", "On trapdoor", "ADC / ESP32"],
            ["Metal coil", "Under platform (fixed)", "Digital"],
            ["4 × IR bin-full", "Mid-frame above each bin", "GPIO"],
            ["NEMA 17 + A4988", "Right of spout / base", "STEP/DIR/EN"],
            ["MG996R", "Platform side", "PWM"],
            ["ESP32-S3 / HX711 / A4988", "Base electronics bay", "—"],
            ["Home switch", "Beside spout", "GPIO"],
            ["OLED 0.96\"", "Front panel", "I2C"],
            ["microSD", "ESP32-S3-CAM / base", "SPI"],
            ["12 V 3 A + 5 V buck", "Base, rear", "Power"],
        ], lang, font_size=7.8, widths=[40, 70, 56])

        MD.add_heading(doc, "5. BOM (HKD)", 1, lang)
        MD.add_table(doc, [
            ["Item", "Qty", "Unit", "Total"],
            ["ESP32-S3-CAM", "1", "120", "120"],
            ["OLED 0.96\"", "1", "20", "20"],
            ["microSD 16 GB", "1", "15", "15"],
            ["5 kg load cell + HX711", "1", "35", "35"],
            ["NEMA 17 stepper", "1", "75", "75"],
            ["A4988 driver", "1", "18", "18"],
            ["MG996R servo", "1", "35", "35"],
            ["IR break-beam", "1", "15", "15"],
            ["Capacitive moisture", "1", "15", "15"],
            ["4 × IR bin-full", "4", "5", "20"],
            ["Microswitches", "3", "3", "9"],
            ["12 V 3 A adapter", "1", "45", "45"],
            ["5 V 3 A buck", "1", "18", "18"],
            ["Plywood / acrylic", "1", "160", "160"],
            ["3D-printed brackets", "1", "45", "45"],
            ["Bins (reused)", "4", "9", "36"],
            ["Hinges / screws / feet", "1", "60", "60"],
            ["Wire / connectors", "1", "45", "45"],
            ["Labels / tape", "1", "20", "20"],
            ["Misc / spare", "1", "15", "15"],
            ["Subtotal", "", "", "866"],
            ["15% contingency", "", "", "130"],
            ["TOTAL", "", "", "≈ 996"],
        ], lang, font_size=7.5, widths=[90, 18, 24, 34])

        MD.add_heading(doc, "6. Operation", 1, lang)
        if (REND / "09_storyboard_5.png").exists():
            MD.add_figure(doc, "09_storyboard_5.png", "Figure 3. Operation storyboard: throw, close/scan, rotate, drop, done.", 180, lang)
        MD.add_num(doc, "1. Lid is open; the bottle is thrown in and lands on the closed trapdoor.", lang)
        MD.add_num(doc, "2. Lid closes; ESP32-S3-CAM captures, MobileNetV2 runs on-board; weight/moisture/IR are fused.", lang)
        MD.add_num(doc, "3. The on-board classifier picks a bin; the ESP32 rotates the spout.", lang)
        MD.add_num(doc, "4. MG996R opens the trapdoor; the item falls through funnel and spout.", lang)
        MD.add_num(doc, "5. Spring closes the door; spout homes; app records the event.", lang)

        MD.add_heading(doc, "7. Build and test notes", 1, lang)
        MD.add_bullet(doc, "Build the bin frame and 2 × 2 bins first; fit the platform and trapdoor before the lid.", lang)
        MD.add_bullet(doc, "Bench-test NEMA 17 + A4988 at 0.8 A, 1/8 microstep, 3:1 belt; home switch repeatability ±2 steps.", lang)
        MD.add_bullet(doc, "Calibrate the 5 kg cell with 0/100/500/1000 g; place the item within 60 mm of platform centre.", lang)
        MD.add_bullet(doc, "Test 20 dry cycles, then 20 real items, then wet waste. Record jam rate, cycle time, accuracy.", lang)
        MD.add_bullet(doc, "Never run with the lid or bin drawer open; keep the 12 V fuse and e-stop.", lang)

        MD.add_heading(doc, "8. Limitations", 1, lang)
        MD.add_bullet(doc, "Standalone edge AI, but not full MobileNetV2: 0.35/0.5 at 96–128 px INT8; accuracy must be validated on your own 4-class dataset.", lang)
        MD.add_bullet(doc, "Single load cell: off-centre items can add ±5–10 g error.", lang)
        MD.add_bullet(doc, "IR bin-full sensors are fixed-height switches, not continuous level sensors.", lang)
        MD.add_bullet(doc, "DIY metal coil is confirmatory; transparent plastic vs glass remains hard.", lang)
        MD.add_bullet(doc, "Blender model is a concept/visualisation mesh, not a manufacturing CAD file.", lang)
    else:
        MD.add_heading(doc, "1. 為何這個版本可行", 1, lang)
        MD.add_paragraph(doc, "之前的 HK$1,000 草稿用 28BYJ-48 步進和會傾斜的負重盤。兩者都勉強：28BYJ-48 只有約 0.033 N·m；傾斜盤會給負重感測器側向力。這版把兩者都改掉。", lang)
        MD.add_bullet(doc, "NEMA 17（0.45 N·m）＋3:1 GT2 皮帶，滑槽端 1.35 N·m；需要約 0.34 N·m，安全係數約 4。", lang)
        MD.add_bullet(doc, "固定稱重平台＋小活門：5 kg 負重感測器不承受伺服或門的側向力。MG996R 只拉開活門，彈簧關回。", lang)
        MD.add_bullet(doc, "頂部淨空 225 mm（平台 635 mm，蓋底 860 mm），可放直立的 500 mL 樽（約 200 mm）。", lang)
        MD.add_bullet(doc, "四個標準 170 × 170 × 300 mm 桶，不用切角；滑槽在桶頂上方旋轉。", lang)
        MD.add_bullet(doc, "12 V 3 A 適配器＋5 V 降壓：不用鋰電池、BMS、充電器。", lang)
        MD.add_paragraph(doc, "Edge AI：ESP32-S3-CAM（8 MB PSRAM、16 MB flash）跑 MobileNetV2 0.35/0.5、96–128 px、INT8。完整的 MobileNetV2 1.0／224 px 對這塊板太大太慢；用 0.35/0.5 backbone 做 transfer learning，再把鏡頭＋重量＋濕度＋IR 融合。運行時不需要 laptop、雲端或 agent。", lang)

        MD.add_heading(doc, "2. 尺寸與容量", 1, lang)
        MD.add_table(doc, [
            ["項目", "數值"],
            ["整體", "420 闊 × 420 深 × 900 高 mm"],
            ["四個桶", "4 × 170 × 170 × 300 mm；每個約 8.7 L"],
            ["總容量", "約 34.7 L"],
            ["稱重平台", "220 × 180 mm 固定外框；180 × 140 mm 活門"],
            ["漏斗／滑槽", "220 × 200 → 75 mm；75 mm 彎頭，出口半徑 100 mm"],
            ["最大物件", "約 500 mL 樽／330 mL 罐；≤0.5 kg"],
            ["分類時間", "約 6–10 秒"],
            ["目標準確率", "50 件本地資料集 ≥80–85%"],
        ], lang, font_size=8.5, widths=[44, 122])

        MD.add_heading(doc, "3. 內部結構", 1, lang)
        MD.add_figure(doc, "07_internal_labeled.png", "圖 1. 內部結構：固定平台、活門、負重、伺服、漏斗、NEMA 17 滑槽驅動、四個桶、IR 與電子倉。", 180, lang)
        MD.add_paragraph(doc, "受力路徑是刻意設計的：物件 → 活門 → 固定平台 → 單個 5 kg 負重感測器 → 中框。伺服和鉸鏈裝在平台框架，不壓在負重感測器上。活門打開後，物件經漏斗和旋轉滑槽落入選定桶。停電時彈簧關門。", lang)
        MD.add_callout(doc, "為何用活門", "傾斜盤會改變負重幾何，還加入側向力。固定平台令稱重可重複；活門只在記錄重量之後才動。這是可行性最重要的機械修正。", lang)

        MD.add_heading(doc, "4. 感測器與 MCU 位置", 1, lang)
        MD.add_figure(doc, "08_electronics_labeled.png", "圖 2. 電子倉：ESP32、HX711、A4988、USB 與接線。", 175, lang)
        MD.add_table(doc, [
            ["裝置", "位置", "介面"],
            ["ESP32-S3-CAM", "蓋底，向下看", "板上推論"],
            ["IR 對射", "料斗口", "GPIO"],
            ["5 kg 負重", "固定平台下", "HX711"],
            ["濕度墊", "活門上", "ADC／ESP32"],
            ["金屬線圈", "平台下（固定）", "數位"],
            ["4 × IR 滿度", "中框，每個桶上方", "GPIO"],
            ["NEMA 17 + A4988", "滑槽右側／底部", "STEP/DIR/EN"],
            ["MG996R", "平台側", "PWM"],
            ["ESP32-S3／HX711／A4988", "底部電子倉", "—"],
            ["原點開關", "滑槽旁", "GPIO"],
            ["OLED 0.96\"", "前面板", "I2C"],
            ["microSD", "ESP32-S3-CAM／底部", "SPI"],
            ["12 V 3 A＋5 V 降壓", "底部後方", "電源"],
        ], lang, font_size=7.8, widths=[40, 70, 56])

        MD.add_heading(doc, "5. 成本（HKD）", 1, lang)
        MD.add_table(doc, [
            ["項目", "數量", "單價", "小計"],
            ["ESP32-S3-CAM", "1", "120", "120"],
            ["OLED 0.96\"", "1", "20", "20"],
            ["microSD 16 GB", "1", "15", "15"],
            ["5 kg 負重＋HX711", "1", "35", "35"],
            ["NEMA 17 步進", "1", "75", "75"],
            ["A4988 驅動", "1", "18", "18"],
            ["MG996R 伺服", "1", "35", "35"],
            ["IR 對射", "1", "15", "15"],
            ["電容濕度", "1", "15", "15"],
            ["4 × IR 滿度", "4", "5", "20"],
            ["微動開關", "3", "3", "9"],
            ["12 V 3 A 適配器", "1", "45", "45"],
            ["5 V 3 A 降壓", "1", "18", "18"],
            ["夾板／亞克力", "1", "160", "160"],
            ["3D 打印支架", "1", "45", "45"],
            ["四個桶（重用）", "4", "9", "36"],
            ["鉸鏈／螺絲／腳", "1", "60", "60"],
            ["線材／接頭", "1", "45", "45"],
            ["標籤／膠帶", "1", "20", "20"],
            ["雜項／備件", "1", "15", "15"],
            ["小計", "", "", "866"],
            ["15% 應急", "", "", "130"],
            ["總計", "", "", "≈ 996"],
        ], lang, font_size=7.5, widths=[90, 18, 24, 34])

        MD.add_heading(doc, "6. 操作流程", 1, lang)
        if (REND / "09_storyboard_5.png").exists():
            MD.add_figure(doc, "09_storyboard_5.png", "圖 3. 操作分鏡：投放、關蓋／掃描、旋轉、落料、完成。", 180, lang)
        MD.add_num(doc, "1. 蓋打開；膠樽由上方投入，落在關閉的活門上。", lang)
        MD.add_num(doc, "2. 關蓋；ESP32-S3-CAM 拍攝，MobileNetV2 在板子上推論；重量／濕度／IR 融合。", lang)
        MD.add_num(doc, "3. 板上分類器選桶；ESP32 把滑槽轉到目標桶。", lang)
        MD.add_num(doc, "4. MG996R 拉開活門；物件經漏斗、滑槽落入桶。", lang)
        MD.add_num(doc, "5. 彈簧關門；滑槽回原點；App 記錄。", lang)

        MD.add_heading(doc, "7. 製作與測試", 1, lang)
        MD.add_bullet(doc, "先做桶架和 2 × 2 桶；裝平台和活門，最後才裝蓋。", lang)
        MD.add_bullet(doc, "NEMA 17＋A4988 用 0.8 A、1/8 微步、3:1 皮帶；原點重複性 ±2 步。", lang)
        MD.add_bullet(doc, "5 kg 負重用 0／100／500／1000 g 校正；物件放平台中心 60 mm 內。", lang)
        MD.add_bullet(doc, "先 20 次空機、再 20 件真實垃圾、最後濕垃圾；記錄卡料率、時間、準確率。", lang)
        MD.add_bullet(doc, "蓋或抽屜打開時不得動作；保留 12 V 保險絲和急停。", lang)

        MD.add_heading(doc, "8. 限制", 1, lang)
        MD.add_bullet(doc, "Standalone edge AI，但不是完整 MobileNetV2：0.35/0.5、96–128 px INT8；4 類準確率要用自己的 dataset 驗證。", lang)
        MD.add_bullet(doc, "單個負重感測器：物件偏心會有 ±5–10 g 誤差。", lang)
        MD.add_bullet(doc, "IR 滿度是固定高度開關，不是連續液位。", lang)
        MD.add_bullet(doc, "DIY 金屬線圈只作確認；透明膠 vs 玻璃仍難。", lang)
        MD.add_bullet(doc, "Blender 模型是概念／視覺 mesh，不是制造 CAD。", lang)

    name = "Smart_Waste_Sorting_Bin_HK1000_Design_EN.docx" if lang == "en" else "智能分類垃圾桶_HK1000_設計方案_ZH-Hant.docx"
    out = OUT / name
    doc.save(out)
    print("saved", out)
    return out


if __name__ == "__main__":
    build("en")
    build("zh")
