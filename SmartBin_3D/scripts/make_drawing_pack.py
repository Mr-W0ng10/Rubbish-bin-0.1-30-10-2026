# -*- coding: utf-8 -*-
"""Create a 4-page A3 v2 concept drawing pack from current renders."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
R = os.path.join(BASE, "renders")
OUT = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_Design_Package\02_Drawings\SmartBin_Drawings_A3_v2.pdf"
W, H = 3307, 2339  # A3 landscape @ 200 dpi
GREEN = (31, 78, 69)
INK = (30, 40, 50)
MUTED = (90, 103, 120)
LIGHT = (247, 249, 247)
ORANGE = (217, 130, 43)

pages = []
F = r"C:\Windows\Fonts\msjh.ttc"
FB = lambda s: ImageFont.truetype(F, s)
FT = lambda s: ImageFont.truetype(F, s)


def new_page(title, subtitle):
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 150], fill=GREEN)
    d.text((70, 28), title, font=FT(58), fill="white")
    d.text((70, 98), subtitle, font=FB(26), fill=(216, 232, 177))
    d.text((W - 420, 54), "V2 / HK$1,000", font=FB(30), fill="white")
    return im, d


def footer(d, page):
    d.line([(70, H - 70), (W - 70, H - 70)], fill=(210, 218, 214), width=2)
    d.text((70, H - 58), "Concept / visualisation model — not manufacturing CAD. Verify purchased parts before cutting.", font=FB(19), fill=MUTED)
    d.text((W - 220, H - 58), f"{page} / 4", font=FB(20), fill=MUTED)


def paste(im, path, box):
    img = Image.open(path).convert("RGB")
    x, y, w, h = box
    img.thumbnail((w, h), Image.LANCZOS)
    im.paste(img, (x + (w - img.width) // 2, y + (h - img.height) // 2))


def table(d, x, y, rows, widths, size=24, header=True):
    yy = y
    for i, row in enumerate(rows):
        xx = x
        for j, cell in enumerate(row):
            if header and i == 0:
                d.rectangle([xx, yy, xx + widths[j], yy + 46], fill=(226, 238, 232))
                f = FB(size + 2)
            else:
                f = FB(size)
            d.text((xx + 12, yy + 10), str(cell), font=f, fill=INK)
            d.line([(xx, yy), (xx, yy + 46)], fill=(210, 218, 214), width=1)
            xx += widths[j]
        d.line([(x, yy + 46), (x + sum(widths), yy + 46)], fill=(210, 218, 214), width=1)
        yy += 46
    d.rectangle([x, y, x + sum(widths), yy], outline=(210, 218, 214), width=2)


# page 1: cover / dimensions
im, d = new_page("SMART WASTE SORTING BIN", "Standalone ESP32-S3-CAM · MobileNetV2 · sensor fusion · 4 streams")
paste(im, os.path.join(R, "01_hero.png"), (60, 200, 1550, 1950))
d.text((1680, 230), "Design intent", font=FT(44), fill=GREEN)
rows = [
    ["Item", "Value"],
    ["Overall", "420 × 420 × 900 mm"],
    ["Bins", "4 × 170 × 170 × 300 mm (8.7 L)"],
    ["Total capacity", "approx. 34.7 L"],
    ["Platform", "220 × 180 mm; 180 × 140 mm door"],
    ["Funnel / spout", "220 × 200 → 75 mm; 75 mm elbow"],
    ["Max item", "500 mL bottle / 330 mL can; <=0.5 kg"],
    ["Cycle", "6–10 s"],
    ["BOM", "HK$866"],
    ["Total incl. 15%", "approx. HK$996"],
]
table(d, 1680, 300, rows, [430, 900], size=26)
d.text((1680, 880), "No laptop / no cloud / no agent", font=FT(38), fill=ORANGE)
d.text((1680, 940), "ESP32-S3-CAM runs MobileNetV2 0.35/0.5 at 96–128 px, INT8.\nSensor fusion: camera + 5 kg load cell + moisture + IR.\nWiFi AP and OLED are for status only.", font=FB(25), fill=INK, spacing=8)
footer(d, 1)
pages.append(im.copy())

# page 2: cutaway
im, d = new_page("INTERNAL STRUCTURE", "Fixed platform · trapdoor · single load cell · NEMA 17 spout")
paste(im, os.path.join(R, "07_internal_labeled.png"), (60, 190, W - 120, H - 250))
footer(d, 2)
pages.append(im.copy())

# page 3: top view + layout
im, d = new_page("TOP VIEW / BIN LAYOUT", "2 × 2 bins, no corner notches; spout rotates above bin tops")
paste(im, os.path.join(R, "03_top_internal.png"), (60, 190, 1700, 1750))
d.text((1800, 220), "Bin layout", font=FT(42), fill=GREEN)
table(d, 1800, 290, [
    ["Bin", "Centre (mm)", "Colour"],
    ["1 Plastic", "(-100, -100)", "Blue"],
    ["2 Metal", "(+100, -100)", "Yellow"],
    ["3 Wet", "(-100, +100)", "Green"],
    ["4 Other", "(+100, +100)", "Grey"],
], [420, 500, 300], size=25)
d.text((1800, 600), "Sensors", font=FT(42), fill=GREEN)
table(d, 1800, 670, [
    ["Device", "Location"],
    ["ESP32-S3-CAM", "Lid underside"],
    ["IR beam", "Hopper mouth"],
    ["Load cell", "Under platform"],
    ["Moisture pad", "On trapdoor"],
    ["4 × IR full", "Mid-frame / bin"],
    ["Home switch", "Beside spout"],
    ["OLED / SD", "Front / camera"],
], [520, 600], size=24)
footer(d, 3)
pages.append(im.copy())

# page 4: mechanism + electronics
im, d = new_page("MECHANISM / ELECTRONICS", "NEMA 17 + 3:1 GT2 · MG996R trapdoor · ESP32-S3-CAM electronics bay")
paste(im, os.path.join(R, "05_detail.png"), (60, 190, 1550, 1650))
paste(im, os.path.join(R, "08_electronics_labeled.png"), (1600, 190, W - 100, 1200))
d.text((1600, 1260), "Key checks", font=FT(38), fill=GREEN)
for i, line in enumerate([
    "1. Spout torque: 1.35 N·m available vs ~0.34 N·m required.",
    "2. Trapdoor: MG996R + spring; item <=0.5 kg.",
    "3. Clearance: 225 mm tray-to-lid; upright 500 mL bottle.",
    "4. On-device model: MobileNetV2 0.35/0.5, INT8.",
    "5. Build frame/bins first; fit platform/door before lid.",
]):
    d.text((1600, 1320 + i * 62), line, font=FB(25), fill=INK)
footer(d, 4)
pages.append(im.copy())

pages[0].save(OUT, "PDF", resolution=200, save_all=True, append_images=pages[1:])
print("saved", OUT, "pages", len(pages))
