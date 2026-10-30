# -*- coding: utf-8 -*-
"""Detail, sequence, power and state-machine figures."""
import os, math, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from draw_lib import *
from make_diagrams import header, footer

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_Drawings"))
os.makedirs(OUT, exist_ok=True)


def hopper_detail():
    c = Canvas(2400, 1450, PAPER)
    header(c, "Detail A: weigh hopper, door & sensors", "詳圖 A：稱重料斗、門與感測器（mm）", "Fig. 05")
    S = 5.0
    ox, oy = 120, 1320

    def X(x): return ox + x * S
    def Y(z): return oy - (z - 470) * S

    # hopper body crop 620-710
    c.rect((X(50), Y(710), X(430), Y(620)), fill=(252, 252, 251), outline=INK, width=3)
    c.rect((X(70), Y(710), X(410), Y(642)), fill=(247, 247, 244), outline=LINE, width=1)
    c.line([(X(50), Y(710)), (X(430), Y(710))], fill=INK, width=2, dash=(8, 6))
    c.text((X(240), Y(716)), "to hopper top 至料斗頂", size=9, fill=MUTED, anchor="ma")
    # walls
    c.rect((X(50), Y(710), X(70), Y(620)), fill=(225, 232, 228), outline=INK, width=2)
    c.rect((X(410), Y(710), X(430), Y(620)), fill=(225, 232, 228), outline=INK, width=2)
    # door
    c.rect((X(85), Y(642), X(395), Y(625)), fill=(222, 231, 226), outline=INK, width=3)
    c.text((X(105), Y(646)), "HOPPER DOOR  料斗門", size=11, fill=INK, bold=True)
    c.ellipse((X(75), Y(642), X(89), Y(628)), fill=INK, outline=None)
    # gasket
    c.line([(X(90), Y(643)), (X(390), Y(643))], fill=BLUE, width=3)
    # moisture pad
    c.rect((X(150), Y(644), X(330), Y(638)), fill=(180, 210, 230), outline=BLUE, width=3)
    c.text((X(240), Y(652)), "MOISTURE PAD  濕度墊", size=8, fill=BLUE, anchor="mm", bold=True)
    # metal coil
    c.arc((X(160), Y(625), X(320), Y(585)), 0, 180, fill=ORANGE, width=6)
    c.text((X(240), Y(578)), "METAL COIL  金屬線圈", size=9, fill=ORANGE, anchor="mm", bold=True)
    # funnel
    c.polygon([(X(90), Y(625)), (X(390), Y(625)), (X(295), Y(490)), (X(185), Y(490))],
              fill=(232, 239, 234), outline=INK, width=3)
    c.text((X(240), Y(560)), "FUNNEL  漏斗", size=12, fill=INK, anchor="mm", bold=True)
    c.text((X(240), Y(538)), "280 inlet → 110 outlet", size=9, fill=MUTED, anchor="mm")
    # bearing and spout
    c.rect((X(185), Y(490), X(295), Y(478)), fill=(208, 217, 212), outline=INK, width=2)
    c.text((X(240), Y(484)), "BEARING", size=7, fill=INK, anchor="mm", bold=True)
    c.polygon([(X(190), Y(478)), (X(290), Y(478)), (X(370), Y(505)), (X(310), Y(515))],
              fill=(225, 235, 230), outline=ORANGE, width=2)
    # load cells
    for x in (90, 350):
        c.rect((X(x), Y(620), X(x + 40), Y(600)), fill=YELLOW, outline=INK, width=2)
        c.text((X(x + 20), Y(610)), "LC", size=10, fill=INK, anchor="mm", bold=True)
    c.rect((X(60), Y(630), X(420), Y(620)), fill=(213, 221, 217), outline=INK, width=2)
    c.text((X(240), Y(596)), "4 × 5 kg load cells  負重感測器", size=9, fill=ORANGE, anchor="ma", bold=True)
    # servo
    c.rect((X(400), Y(710), X(445), Y(660)), fill=(230, 230, 230), outline=INK, width=2)
    c.text((X(423), Y(685)), "SERVO", size=7, fill=INK, anchor="mm", bold=True)
    c.line([(X(400), Y(670)), (X(395), Y(635))], fill=INK, width=3)
    # spring
    c.line([(X(370), Y(640)), (X(340), Y(612))], fill=RED, width=3)
    c.text((X(360), Y(606)), "spring", size=8, fill=RED)
    # item
    c.rect((X(195), Y(675), X(245), Y(645)), fill=(160, 200, 225), outline=BLUE, width=2, radius=8)
    c.rect((X(212), Y(688), X(228), Y(675)), fill=(160, 200, 225), outline=BLUE, width=2)
    c.text((X(220), Y(700)), "item ≤ 1.5 kg", size=8, fill=BLUE, anchor="ma", bold=True)
    # dimensions
    dim_h(c, X(70), X(410), Y(710) + 18, "320 internal", color=BLUE, size=12)
    dim_h(c, X(85), X(395), Y(625) + 38, "290 door", color=MUTED, size=11)
    dim_h(c, X(185), X(295), Y(490) + 28, "110 outlet", color=ORANGE, size=11)
    dim_h(c, X(185), X(295), Y(478) + 55, "150 bearing", color=ORANGE, size=11)
    dim_v(c, Y(620), Y(600), X(50) - 28, "20", color=ORANGE, size=10)
    dim_v(c, Y(642), Y(625), X(430) + 28, "17 door", color=MUTED, size=10)

    # callouts
    items = [
        ("A", "Door gasket: closed-cell silicone; wipe clean.", 1960, 220, (392, 642)),
        ("B", "Moisture pad under 1.5 mm HDPE; replaceable.", 1960, 310, (330, 640)),
        ("C", "Inductive coil fixed to mid-frame; never on load cells.", 1960, 400, (320, 605)),
        ("D", "Funnel 59° walls; smooth joints; 110 mm outlet.", 1960, 490, (300, 560)),
        ("E", "Spout bearing + 3:1 belt; home at 45°.", 1960, 580, (295, 484)),
        ("F", "Servo outside hopper; spring closes on power loss.", 1960, 670, (445, 685)),
    ]
    for tag, txt, x, y, (tx, tz) in items:
        c.ellipse((x, y, x + 28, y + 28), fill=ORANGE, outline=None)
        c.text((x + 14, y + 14), tag, size=13, fill=WHITE, anchor="mm", bold=True)
        c.line([(x, y + 14), (X(tx), Y(tz))], fill=ORANGE, width=1, dash=(4, 4))
        c.textbox((x + 38, y - 2), txt, size=12, fill=INK, maxw=390)

    # notes
    c.rect((1940, 780, 2340, 1210), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((1958, 795), "WHY THIS DETAIL MATTERS", size=13, fill=GREEN, bold=True)
    notes = [
        "•  The hopper floats on four load cells; no pipe or cable",
        "   should bypass the cells or the weight will drift.",
        "•  The door hinge is on the hopper; its mass is tared.",
        "•  The coil and ToF sensors are fixed to the frame.",
        "•  A spring closes the door if power is lost; the servo",
        "   only pulls it open.",
        "•  Dry-run with rice; check the gasket seal.",
    ]
    yy = 825
    for n in notes:
        c.text((1958, yy), n, size=11, fill=INK)
        yy += 27
    c.text((1940, 1230), "DETAIL SCALE 5:1 ON A3", size=11, fill=MUTED, bold=True)

    footer(c, "Detail A scale approximately 5:1 at A3. Confirm fit on the built hopper before cutting the liner.")
    c.save(os.path.join(OUT, "fig05_hopper_detail.png"))


def sequence():
    c = Canvas(2400, 1250, PAPER)
    header(c, "One sort cycle: 6-9 seconds", "一次分類流程：6-9 秒", "Fig. 06")
    panel_w = 440
    top = 180
    h = 760
    titles = ["1  LOAD", "2  SENSE", "3  DECIDE + ROTATE", "4  DROP", "5  CONFIRM + HOME"]
    times = ["0-2 s", "2-3 s", "3-4 s", "4-5 s", "5-7 s"]
    for i in range(5):
        x = 60 + i * (panel_w + 30)
        c.rect((x, top, x + panel_w, top + h), fill=WHITE, outline=GREY, width=2, radius=12)
        c.text((x + 20, top + 15), titles[i], size=17, fill=GREEN, bold=True)
        c.text((x + panel_w - 20, top + 18), times[i], size=14, fill=ORANGE, anchor="ra", bold=True)
        # simple bin outline
        bx1, bx2 = x + 70, x + panel_w - 70
        by1, by2 = top + 80, top + 620
        c.rect((bx1, by1, bx2, by2), fill=(250, 251, 250), outline=INK, width=2)
        # layer lines
        c.line([(bx1, by1 + 170), (bx2, by1 + 170)], fill=LINE, width=1)
        c.line([(bx1, by1 + 260), (bx2, by1 + 260)], fill=LINE, width=1)
        # bins
        for j in range(4):
            xx = bx1 + 20 + (j % 2) * 120
            yy = by1 + 290 + (j // 2) * 120
            fill = [BLUE_2, (250, 235, 190), (210, 235, 214), (230, 232, 234)][j]
            c.rect((xx, yy, xx + 95, yy + 95), fill=fill, outline=INK, width=1)
        # hopper
        hx1, hx2 = bx1 + 45, bx2 - 45
        hy1, hy2 = by1 + 55, by1 + 160
        c.rect((hx1, hy1, hx2, hy2), fill=(245, 247, 244), outline=INK, width=2)
        # camera
        c.rect((x + panel_w / 2 - 14, by1 + 20, x + panel_w / 2 + 14, by1 + 45), fill=INK, outline=None)
        c.ellipse((x + panel_w / 2 - 18, by1 + 40, x + panel_w / 2 + 18, by1 + 70), fill=None, outline=YELLOW, width=3)
        # spout
        c.line([(x + panel_w / 2, by1 + 260), (x + panel_w / 2, by1 + 290)], fill=ORANGE, width=6)
        # per-panel action
        if i == 0:
            c.line([(bx1 + 20, by1 + 55), (bx1 + 20, by1 + 10)], fill=INK, width=3)
            c.line([(bx1 + 20, by1 + 10), (bx1 + 55, by1 + 10)], fill=INK, width=3)
            c.arrow((bx1 + 100, by1 + 10), (bx1 + 100, by1 + 80), fill=ORANGE, width=4, head=12)
            c.text((bx1 + 110, by1 + 30), "place item", size=12, fill=ORANGE)
        elif i == 1:
            # camera rays
            for dx in (-45, 0, 45):
                c.line([(x + panel_w / 2, by1 + 65), (x + panel_w / 2 + dx, by1 + 150)], fill=BLUE, width=2, dash=(4, 4))
            c.text((bx1 + 12, by1 + 185), "weight 128 g", size=12, fill=ORANGE, bold=True)
            c.text((bx1 + 12, by1 + 205), "moisture 0.12", size=12, fill=BLUE)
            c.text((bx1 + 12, by1 + 225), "metal: no", size=12, fill=MUTED)
        elif i == 2:
            c.arrow((x + panel_w / 2, by1 + 250), (bx2 - 55, by1 + 300), fill=ORANGE, width=5, head=14)
            c.text((bx1 + 12, by1 + 190), "class: metal", size=13, fill=GREEN, bold=True)
            c.text((bx1 + 12, by1 + 212), "confidence 0.91", size=12, fill=MUTED)
            c.text((bx1 + 12, by1 + 234), "target: BIN 2", size=12, fill=ORANGE, bold=True)
        elif i == 3:
            c.line([(x + panel_w / 2 - 35, by1 + 160), (x + panel_w / 2 + 35, by1 + 160)], fill=INK, width=5)
            c.arrow((x + panel_w / 2, by1 + 165), (x + panel_w / 2, by1 + 300), fill=ORANGE, width=4, head=12)
            c.text((bx1 + 12, by1 + 185), "door opens 70°", size=12, fill=ORANGE, bold=True)
            c.text((bx1 + 12, by1 + 207), "drop confirmed", size=12, fill=GREEN)
        else:
            c.line([(x + panel_w / 2 - 35, by1 + 160), (x + panel_w / 2 + 35, by1 + 160)], fill=INK, width=5)
            c.text((bx1 + 12, by1 + 185), "door closed", size=12, fill=GREEN, bold=True)
            c.text((bx1 + 12, by1 + 207), "spout home 45°", size=12, fill=ORANGE)
            c.text((bx1 + 12, by1 + 229), "bin level +1", size=12, fill=BLUE)
            c.text((x + panel_w / 2, by1 + 350), "✓", size=48, fill=GREEN, anchor="mm", bold=True)
        # bottom note
        notes = [
            "Lid closes; item sits on the hopper door.",
            "Load cells tare; camera captures 3 frames.",
            "Pi classifies; ESP32 rotates spout to bin.",
            "Door opens; item falls through funnel and spout.",
            "Drop beam confirms; close, home, log, update app.",
        ]
        c.textbox((x + 20, top + 650), notes[i], size=13, fill=MUTED, maxw=panel_w - 40)
    footer(c, "Timing excludes user loading time. The critical path is classification + spout rotation.")
    c.save(os.path.join(OUT, "fig06_sort_sequence.png"))


def power_wiring():
    c = Canvas(2400, 1800, PAPER)
    header(c, "Power distribution & safety wiring", "電源分配與安全接線", "Fig. 07")

    def box(x1, y1, x2, y2, title, sub="", fill=WHITE, outline=INK, tcol=INK):
        c.rect((x1, y1, x2, y2), fill=fill, outline=outline, width=2, radius=10)
        c.text((x1 + 14, y1 + 10), title, size=19, fill=tcol, bold=True)
        if sub:
            c.text((x1 + 14, y1 + 36), sub, size=13, fill=MUTED)

    # battery / input
    box(80, 160, 430, 300, "12 V 6 Ah Li-ion", "3S2P · BMS · 12.6 V charger", fill=(255, 247, 235), outline=ORANGE)
    box(470, 160, 700, 300, "5 A fuse", "within 150 mm of +", fill=(255, 240, 240), outline=RED)
    box(740, 160, 980, 300, "Main switch", "10 A, keyed", fill=WHITE)
    box(1020, 160, 1280, 300, "E-stop", "NC · cuts actuator bus", fill=(255, 240, 240), outline=RED)
    # 12V bus
    c.line([(430, 230), (470, 230)], fill=RED, width=5)
    c.line([(700, 230), (740, 230)], fill=RED, width=5)
    c.line([(980, 230), (1020, 230)], fill=RED, width=5)
    c.line([(1280, 230), (2260, 230)], fill=RED, width=5)
    c.text((1500, 205), "12 V ACTUATOR BUS", size=15, fill=RED, bold=True)
    # branches
    branches = [
        (1450, "A4988 + NEMA 17", "12 V · 0.8 A · 100 µF", ORANGE),
        (1720, "LED ring", "12 V · 0.25 A · MOSFET", YELLOW),
        (1990, "Spare 12 V", "vibration / fan", MUTED),
    ]
    for x, t, s, col in branches:
        c.line([(x, 230), (x, 330)], fill=RED, width=4)
        box(x - 100, 330, x + 100, 430, t, s, fill=WHITE, outline=col)
    # buck converters
    bucks = [
        (500, "Buck 1: 5 V 5 A", "Raspberry Pi + USB hub", BLUE, 520, 560),
        (800, "Buck 2: 5 V 3 A", "ESP32 + sensors + LED bar", GREEN_2, 560, 610),
        (1100, "Buck 3: 6 V 5 A", "Servo only · 1000 µF", ORANGE, 600, 660),
    ]
    for x, t, s, col, y1, y2 in bucks:
        c.line([(x + 100, 230), (x + 100, y1 - 30)], fill=RED, width=4)
        box(x, y1, x + 300, y2, t, s, fill=(245, 250, 252) if col == BLUE else WHITE, outline=col)
    # loads
    box(430, 760, 760, 900, "Raspberry Pi Zero 2 W", "5 V · 1.2 A peak · USB-C", fill=BLUE_2, outline=BLUE)
    box(800, 760, 1080, 900, "USB camera", "5 V · 0.2 A · UVC · USB data", fill=BLUE_2, outline=BLUE)
    box(1120, 760, 1450, 900, "ESP32 DevKit", "5 V · 0.25 A · 3.3 V sensors", fill=(255, 250, 244), outline=ORANGE)
    box(1490, 760, 1770, 900, "Servo DS3225MG", "6 V · 2 A peak · 1000 µF", fill=(255, 247, 235), outline=ORANGE)
    # power arrows
    c.arrow((650, 560), (600, 760), fill=BLUE, width=4, head=12)
    c.text((610, 690), "5 V", size=13, fill=BLUE, bold=True)
    c.arrow((950, 610), (1280, 760), fill=GREEN_2, width=4, head=12)
    c.text((1040, 690), "5 V", size=13, fill=GREEN_2, bold=True)
    c.arrow((1250, 660), (1630, 760), fill=ORANGE, width=4, head=12)
    c.text((1430, 700), "6 V", size=13, fill=ORANGE, bold=True)
    # Pi USB powers and talks to the camera
    c.arrow((760, 830), (800, 830), fill=BLUE, width=4, head=10)
    c.text((780, 842), "USB 5 V + data", size=10, fill=BLUE, anchor="ma")
    # ground bus
    c.line([(120, 1050), (2260, 1050)], fill=BLACK, width=5)
    c.text((130, 1025), "STAR GROUND BUS  (one point at the power board)", size=15, fill=BLACK, bold=True)
    for x in (590, 950, 1280, 1630):
        c.line([(x, 900), (x, 1050)], fill=BLACK, width=3)
    # notes
    c.rect((80, 1120, 1160, 1450), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((100, 1135), "WIRING RULES", size=17, fill=GREEN, bold=True)
    rules = [
        "•  Fuse the battery positive within 150 mm of the pack.",
        "•  The e-stop cuts 12 V to stepper, servo and LED; Pi/ESP32 stay on 5 V.",
        "•  Use separate bucks for Pi, servo and ESP32; do not daisy-chain.",
        "•  Servo supply: 1000 µF electrolytic + 100 nF ceramic at the connector.",
        "•  A4988: 100 µF across VMOT/GND; set Vref = 0.64 V (0.8 A).",
        "•  Load-cell cable is shielded; shield grounded at HX711 only.",
        "•  Keep stepper and servo cables away from HX711 and I2C; cross at 90°.",
        "•  All connectors keyed and labelled; strain-relieve every cable.",
    ]
    yy = 1170
    for r in rules:
        c.text((100, yy), r, size=13, fill=INK)
        yy += 30
    # wire gauge table
    c.rect((1200, 1120, 2260, 1450), fill=(240, 248, 241), outline=GREEN_2, width=1, radius=8)
    c.text((1220, 1135), "WIRE GAUGE / COLOUR", size=17, fill=GREEN, bold=True)
    rows = [
        ("12 V battery / motor", "18 AWG red / black", "5 A fuse"),
        ("5 V Pi / ESP32", "20 AWG red / black", "3 A buck"),
        ("6 V servo", "20 AWG orange / black", "5 A buck"),
        ("Signal / I2C", "22-24 AWG twisted pair", "keep < 500 mm"),
        ("Load cell", "4-core shielded", "shield one end"),
        ("Earth / frame", "18 AWG green", "star point"),
    ]
    for i, (a, b, d) in enumerate(rows):
        y = 1175 + i * 40
        c.text((1220, y), a, size=12, fill=INK, bold=True)
        c.text((1500, y), b, size=12, fill=MUTED)
        c.text((1880, y), d, size=12, fill=GREEN)
    # warning
    c.rect((80, 1490, 2260, 1610), fill=(255, 240, 240), outline=RED, width=2, radius=8)
    c.text((100, 1503), "SAFETY", size=15, fill=RED, bold=True)
    c.text((180, 1505), "Never charge a Li-ion pack unattended inside the bin. Use a certified pack with BMS; charge outside the enclosure.", size=13, fill=INK)
    c.text((180, 1535), "The prototype uses 12 V SELV only. Do not route mains into the bin. Keep liquids away from the electronics bay.", size=13, fill=INK)
    c.text((180, 1565), "Fit a 5 A fuse, a main switch and a mushroom e-stop. Label the e-stop “STOP MOTION / 停止動作”.", size=13, fill=INK)
    footer(c, "Block diagram, not a full schematic. The pin-level connection map is Fig. 08; the terminal schedule is in Section 5.7.")
    c.save(os.path.join(OUT, "fig07_power_wiring.png"))


def connection_map():
    c = Canvas(2400, 1800, PAPER)
    header(c, "ESP32 connection map", "ESP32 接線圖（邏輯）", "Fig. 08")
    # central board
    bx1, by1, bx2, by2 = 960, 620, 1440, 1180
    c.rect((bx1, by1, bx2, by2), fill=(255, 250, 244), outline=ORANGE, width=4, radius=12)
    c.text(((bx1 + bx2) / 2, by1 + 20), "ESP32 DevKit V1", size=22, fill=ORANGE, anchor="ma", bold=True)
    c.text(((bx1 + bx2) / 2, by1 + 50), "30-pin · ESP32-WROOM-32", size=13, fill=MUTED, anchor="ma")
    c.text(((bx1 + bx2) / 2, by1 + 78), "USB serial ↔ Raspberry Pi", size=13, fill=BLUE, anchor="ma", bold=True)

    # modules
    def mod(x1, y1, x2, y2, title, sub, pin, col=BLUE, side="left"):
        c.rect((x1, y1, x2, y2), fill=WHITE, outline=col, width=2, radius=8)
        c.text((x1 + 12, y1 + 9), title, size=15, fill=INK, bold=True)
        c.text((x1 + 12, y1 + 31), sub, size=11, fill=MUTED)
        c.text((x1 + 12, y2 - 24), pin, size=11, fill=col, bold=True)

    # left top I2C
    mod(120, 160, 600, 330, "I2C sensor bus", "SHT31 · VL53L0X · 4 × VL53L1X · PCF8574", "SDA 21 · SCL 22 · 3.3 V · GND", BLUE)
    c.line([(600, 245), (960, 700)], fill=BLUE, width=3)
    # left mid HX711
    mod(120, 390, 600, 540, "HX711 + 4 × 5 kg cells", "weight · 10/80 Hz · shielded cable", "DOUT 32 · SCK 33 · 3.3 V · GND", ORANGE)
    c.line([(600, 465), (960, 780)], fill=ORANGE, width=3)
    # left bottom switches
    mod(120, 600, 600, 760, "PCF8574 switches", "lid · door · drawer · home · 4 × bin present", "I2C 0x20 · INT 23 (optional)", GREEN_2)
    c.line([(600, 680), (960, 900)], fill=GREEN_2, width=3)
    # left bottom e-stop / button / IR
    mod(120, 810, 600, 1000, "Safety inputs", "IR beam · e-stop status · front button", "35 · 34 · 39 (input only)", RED)
    c.line([(600, 905), (960, 1040)], fill=RED, width=3)
    # right top stepper
    mod(1800, 160, 2280, 340, "A4988 + NEMA 17", "STEP / DIR / EN · 1/8 microstep", "25 · 26 · 27 · 12 V · GND", ORANGE)
    c.line([(1800, 250), (1440, 700)], fill=ORANGE, width=3)
    # right mid servo
    mod(1800, 390, 2280, 540, "Hopper servo", "DS3225MG · 6 V · spring return", "13 · PWM 50 Hz", ORANGE)
    c.line([(1800, 465), (1440, 820)], fill=ORANGE, width=3)
    # right mid LED / buzzer
    mod(1800, 590, 2280, 740, "LED bar + buzzer", "WS2812B 8 LEDs · active buzzer", "2 (data) · 14 (buzzer)", GREEN_2)
    c.line([(1800, 665), (1440, 940)], fill=GREEN_2, width=3)
    # right bottom ToF XSHUT
    mod(1800, 790, 2280, 1000, "ToF XSHUT lines", "1 item + 4 bin sensors; assign 0x30-0x33", "4 · 16 · 17 · 18 · 19", BLUE)
    c.line([(1800, 895), (1440, 1060)], fill=BLUE, width=3)
    # right bottom power
    mod(1800, 1040, 2280, 1180, "Power", "5 V 3 A · 3.3 V · star ground", "5 V · 3V3 · GND", MUTED)
    c.line([(1800, 1110), (1440, 1120)], fill=MUTED, width=4)

    # pin labels on board
    left_pins = ["21 SDA", "22 SCL", "32 DOUT", "33 SCK", "35 IR", "34 ESTOP", "39 BUTTON", "23 INT"]
    right_pins = ["25 STEP", "26 DIR", "27 EN", "13 SERVO", "2 LED", "14 BUZZ", "4 TOF", "16-19 XSHUT"]
    for i, p in enumerate(left_pins):
        y = by1 + 110 + i * 55
        c.text((bx1 - 12, y), p, size=11, fill=BLUE, anchor="ra", bold=True)
    for i, p in enumerate(right_pins):
        y = by1 + 110 + i * 55
        c.text((bx2 + 12, y), p, size=11, fill=ORANGE, bold=True)

    # legend
    c.rect((80, 1290, 2320, 1510), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((100, 1305), "PIN NOTES", size=16, fill=GREEN, bold=True)
    notes = [
        "•  GPIO34-39 are input-only: use external 10 kΩ pull-ups; no internal pull-up.",
        "•  GPIO2 is a strapping pin; it drives the LED data line only after boot. Do not hold it low at reset.",
        "•  All five ToF sensors share I2C; hold XSHUT low, release one at a time, and assign 0x30-0x33.",
        "•  A4988 Vref = 0.64 V for 0.8 A with Rs = 0.1 Ω. Use 1/8 microstep: 1200 steps per 90°.",
        "•  Servo power is 6 V, not 5 V; add 1000 µF at the servo connector and common ground.",
        "•  The Pi connects by USB; the ESP32 appears as /dev/ttyUSB0. Do not also connect 5 V from the Pi to the ESP32 5 V pin.",
    ]
    yy = 1345
    for n in notes:
        c.text((100, yy), n, size=13, fill=INK)
        yy += 28

    footer(c, "Logical connection map. Use the pin table in Section 5.3 as the authoritative wiring schedule.")
    c.save(os.path.join(OUT, "fig08_connection_map.png"))


def state_machine():
    c = Canvas(2400, 1500, PAPER)
    header(c, "Control state machine", "控制狀態機", "Fig. 09")
    # swimlanes
    c.rect((60, 120, 2340, 520), fill=(247, 250, 253), outline=BLUE, width=1, radius=10)
    c.text((80, 132), "RASPBERRY PI  (Linux / Python)", size=16, fill=BLUE, bold=True)
    c.rect((60, 540, 2340, 1360), fill=(255, 251, 246), outline=ORANGE, width=1, radius=10)
    c.text((80, 552), "ESP32  (real-time firmware)", size=16, fill=ORANGE, bold=True)

    def state(x, y, w, h, title, sub="", fill=WHITE, outline=GREEN, tcol=INK):
        c.rect((x, y, x + w, y + h), fill=fill, outline=outline, width=3, radius=10)
        c.text((x + 12, y + 9), title, size=16, fill=tcol, bold=True)
        if sub:
            c.text((x + 12, y + 33), sub, size=11, fill=MUTED)

    # Pi states
    state(100, 190, 220, 80, "IDLE", "wait for ITEM event")
    state(390, 190, 220, 80, "CAPTURE", "3 frames · fixed exposure")
    state(680, 190, 240, 80, "CLASSIFY", "MobileNetV2 · confidence")
    state(1000, 190, 260, 80, "FUSE + DECIDE", "vision + weight + moisture + metal")
    state(1340, 190, 220, 80, "SEND SORT", "JSON command to ESP32")
    state(1640, 190, 220, 80, "WAIT", "DONE / ERROR / timeout")
    state(1940, 190, 260, 80, "LOG + APP", "SQLite · bin level · cloud")
    # Pi arrows
    for x1, x2 in ((320, 390), (610, 680), (920, 1000), (1260, 1340), (1560, 1640), (1860, 1940)):
        c.arrow((x1 + 8, 230), (x2 - 8, 230), fill=BLUE, width=3, head=10)
    c.arrow((1810, 270), (1810, 340), fill=RED, width=2, head=8, dash=(6, 5))
    c.text((1820, 300), "timeout", size=11, fill=RED)
    c.arrow((2070, 270), (600, 340), fill=BLUE, width=2, head=8, dash=(6, 5))
    c.text((1400, 325), "next item", size=11, fill=BLUE)

    # ESP32 states
    state(100, 620, 210, 80, "BOOT", "self-test · read switches", fill=(255, 247, 235), outline=ORANGE)
    state(380, 620, 210, 80, "HOME", "spout 45° · door closed", fill=(255, 247, 235), outline=ORANGE)
    state(660, 620, 210, 80, "IDLE", "wait · heartbeat", fill=(255, 247, 235), outline=ORANGE)
    state(940, 620, 230, 80, "ITEM", "ToF + weight > 20 g", fill=(255, 247, 235), outline=ORANGE)
    state(1240, 620, 230, 80, "WEIGH", "tare · 10 samples", fill=(255, 247, 235), outline=ORANGE)
    state(1540, 620, 260, 80, "WAIT_CLASS", "send ITEM · 5 s timeout", fill=(255, 247, 235), outline=ORANGE)
    state(100, 800, 240, 80, "ROTATE", "stepper → target bin", fill=(255, 247, 235), outline=ORANGE)
    state(410, 800, 240, 80, "VERIFY", "home / position / bin present", fill=(255, 247, 235), outline=ORANGE)
    state(720, 800, 240, 80, "DUMP", "servo opens 70° · 1.5 s", fill=(255, 247, 235), outline=ORANGE)
    state(1030, 800, 240, 80, "CLOSE", "spring + servo · limit", fill=(255, 247, 235), outline=ORANGE)
    state(1340, 800, 240, 80, "CONFIRM", "drop beam · bin level", fill=(255, 247, 235), outline=ORANGE)
    state(1650, 800, 240, 80, "REPORT", "DONE / ERROR event", fill=(255, 247, 235), outline=ORANGE)
    state(100, 1030, 300, 80, "FAULT", "jam · timeout · lid/drawer open · e-stop", fill=(255, 235, 235), outline=RED, tcol=RED)
    state(520, 1030, 300, 80, "SAFE STATE", "actuators off · LED red · app alert", fill=(255, 235, 235), outline=RED, tcol=RED)

    # ESP32 arrows
    seq = [
        ((310, 660), (380, 660)), ((590, 660), (660, 660)), ((870, 660), (940, 660)),
        ((1170, 660), (1240, 660)), ((1470, 660), (1540, 660)),
        ((1670, 700), (220, 800)), ((340, 840), (410, 840)), ((650, 840), (720, 840)),
        ((960, 840), (1030, 840)), ((1270, 840), (1340, 840)), ((1580, 840), (1650, 840)),
        ((1770, 880), (820, 1030)), ((1770, 880), (220, 1030)),
    ]
    for (x1, y1), (x2, y2) in seq:
        c.arrow((x1, y1), (x2, y2), fill=ORANGE, width=2, head=9)
    # labels
    c.text((1680, 720), "class + bin", size=11, fill=ORANGE)
    c.text((1760, 930), "any fault", size=11, fill=RED)
    c.text((330, 1080), "clear + re-home", size=11, fill=RED)
    c.arrow((520, 1070), (380, 700), fill=RED, width=2, head=8, dash=(5, 5))
    # cross-lane
    c.arrow((1050, 620), (1050, 270), fill=GREEN_2, width=3, head=10)
    c.text((1060, 430), "ITEM event", size=12, fill=GREEN_2, bold=True)
    c.arrow((1240, 270), (1240, 620), fill=BLUE, width=3, head=10)
    c.text((1250, 430), "SORT command", size=12, fill=BLUE, bold=True)
    c.arrow((1650, 620), (1650, 270), fill=GREEN_2, width=2, head=9, dash=(5, 5))
    c.text((1660, 470), "DONE / ERROR", size=11, fill=GREEN_2)

    # notes
    c.rect((80, 1170, 2320, 1335), fill=WHITE, outline=GREY, width=1, radius=8)
    c.text((100, 1185), "TRANSITION RULES", size=15, fill=GREEN, bold=True)
    notes = [
        "•  IDLE → ITEM only when lid closed, drawer closed, door closed, spout home, no e-stop.",
        "•  WAIT_CLASS times out after 5 s → FAULT; the item stays on the door; app asks user to retry.",
        "•  ROTATE always approaches the target clockwise; VERIFY checks the home flag and step count.",
        "•  DUMP opens the door only when the target bin is present and < 90% full.",
        "•  Any fault opens the door? No: keep it closed, disable actuators, show red, wait for user.",
    ]
    yy = 1220
    for n in notes:
        c.text((100, yy), n, size=12, fill=INK)
        yy += 21

    footer(c, "The Pi can fail without causing motion: the ESP32 only moves on an explicit, validated SORT command.")
    c.save(os.path.join(OUT, "fig09_state_machine.png"))


if __name__ == "__main__":
    hopper_detail()
    sequence()
    power_wiring()
    connection_map()
    state_machine()
