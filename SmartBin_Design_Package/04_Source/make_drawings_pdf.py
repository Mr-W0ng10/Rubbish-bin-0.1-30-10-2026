# -*- coding: utf-8 -*-
"""Build an A3 landscape drawings pack PDF from the PNG figures."""
import os, sys
from PIL import Image, ImageDraw, ImageOps
sys.path.insert(0, os.path.dirname(__file__))
from draw_lib import font, GREEN, WHITE, INK, MUTED, ORANGE

def fnt(size, bold=False):
    return font(size, bold=bold, zh=True)


BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DRAW = os.path.join(BASE, "02_Drawings")
OUT = os.path.join(BASE, "02_Drawings", "SmartBin_Drawings_A3.pdf")

W, H = 2480, 1754  # A3 landscape at 150 dpi
M = 80
pages = []

def new_page():
    return Image.new("RGB", (W, H), "white")

def caption(d, text, sub=""):
    f = fnt(28, bold=True)
    f2 = fnt(20)
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, H - 105), text, font=f, fill=INK)
    if sub:
        tw2 = d.textlength(sub, font=f2)
        d.text(((W - tw2) / 2, H - 65), sub, font=f2, fill=MUTED)

def add_figure(filename, title, sub=""):
    path = os.path.join(DRAW, filename)
    if not os.path.exists(path):
        return
    page = new_page()
    d = ImageDraw.Draw(page)
    im = Image.open(path).convert("RGB")
    box_w, box_h = W - 2 * M, H - 2 * M - 100
    im = ImageOps.contain(im, (box_w, box_h), Image.LANCZOS)
    x = (W - im.width) // 2
    y = M
    page.paste(im, (x, y))
    d.rectangle((x - 1, y - 1, x + im.width, y + im.height), outline=(200, 206, 210), width=2)
    caption(d, title, sub)
    pages.append(page)

# Cover
cover = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cover)
d.rectangle((0, 0, W, 260), fill=GREEN)
d.text((M, 55), "SMART WASTE SORTING BIN", font=fnt(64, bold=True), fill=WHITE)
d.text((M, 145), "A3 DRAWINGS PACK  ·  智能分類垃圾桶 A3 圖紙", font=fnt(34, bold=True), fill=(216, 232, 177))
d.text((M, 215), "Version 1.0  ·  29 October 2026  ·  Dimensions in mm", font=fnt(24), fill=WHITE)
d.text((M, 330), "Contents", font=fnt(34, bold=True), fill=GREEN)
items = [
    ("Fig. 01", "System architecture  ·  系統架構"),
    ("Fig. 02", "Front section & sensor locations  ·  正視剖面與感測器位置"),
    ("Fig. 03", "Top view: bins, spout & sensors  ·  俯視圖"),
    ("Fig. 04", "Exploded assembly  ·  爆炸圖"),
    ("Fig. 05", "Detail A: weigh hopper, door & sensors  ·  詳圖 A"),
    ("Fig. 06", "One sort cycle  ·  一次分類流程"),
    ("Fig. 07", "Power distribution & safety wiring  ·  電源與安全接線"),
    ("Fig. 08", "ESP32 connection map  ·  ESP32 接線圖"),
    ("Fig. 09", "Control state machine  ·  控制狀態機"),
]
y = 390
for a, b in items:
    d.text((M, y), a, font=fnt(26, bold=True), fill=ORANGE)
    d.text((M + 160, y), b, font=fnt(26), fill=INK)
    y += 58
d.text((M, H - 210), "Print at A3 (420 × 297 mm), landscape. Do not scale to fit A4; dimensions become unreadable.", font=fnt(24), fill=(176, 58, 58))
d.text((M, H - 160), "The text tables in the design package are the authoritative build data. Verify all dimensions on the built frame before drilling.", font=fnt(20), fill=MUTED)
pages.append(cover)

add_figure("fig01_system_architecture.png", "Fig. 01  System architecture", "Sensors and actuators around the ESP32; vision/app/data on the Raspberry Pi.")
add_figure("fig02_cross_section.png", "Fig. 02  Front section & sensor locations", "Section A-A; nominal dimensions in mm.")
add_figure("fig03_top_view.png", "Fig. 03  Top view: bins, spout & sensors", "2 × 2 bins, 80 × 80 mm corner notches, 150 mm bearing.")
add_figure("fig04_exploded.png", "Fig. 04  Exploded assembly", "Build from the base up; test the drawer, hopper and spout before final assembly.")
add_figure("fig05_hopper_detail.png", "Fig. 05  Detail A: weigh hopper, door & sensors", "Load cells, door, moisture pad, metal coil, funnel and bearing.")
add_figure("fig06_sort_sequence.png", "Fig. 06  One sort cycle: 6–9 seconds", "Load, sense, decide/rotate, drop, confirm/home.")
add_figure("fig07_power_wiring.png", "Fig. 07  Power distribution & safety wiring", "12 V SELV; e-stop cuts the actuator bus; Pi/ESP32 stay alive for logging.")
add_figure("fig08_connection_map.png", "Fig. 08  ESP32 connection map", "Logical map; use the pin table in Section 5.3 as the authoritative schedule.")
add_figure("fig09_state_machine.png", "Fig. 09  Control state machine", "The Pi decides; the ESP32 executes only after validating interlocks and a target bin.")

pages[0].save(OUT, "PDF", resolution=150.0, save_all=True, append_images=pages[1:])
print("saved", OUT, "pages", len(pages), "size MB", round(os.path.getsize(OUT) / 1048576, 2))
