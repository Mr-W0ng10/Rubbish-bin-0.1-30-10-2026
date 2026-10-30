# -*- coding: utf-8 -*-
"""Generate the diagrams for the Smart Waste Sorting Bin design package."""
import os, math, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from draw_lib import *

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_Drawings"))
os.makedirs(OUT, exist_ok=True)


def header(c, title, subtitle, num):
    c.rect((0, 0, c.w, 92), fill=GREEN, outline=None)
    c.text((60, 22), title, size=32, fill=WHITE, bold=True)
    c.text((60, 60), subtitle, size=18, fill=LIME_2)
    c.text((c.w - 60, 32), num, size=18, fill=WHITE, anchor="ra", bold=True)


def footer(c, txt):
    c.line([(60, c.h - 52), (c.w - 60, c.h - 52)], fill=GREY, width=1)
    c.text((60, c.h - 40), txt, size=14, fill=MUTED)
    c.text((c.w - 60, c.h - 40), "Smart Waste Sorting Bin | Design Package v1.0", size=14, fill=MUTED, anchor="ra")


def architecture():
    c = Canvas(2400, 1600, SOFT)
    header(c, "System architecture", "系統架構：two processors, one controlled waste path", "Fig. 01")

    # Column headers
    c.text((120, 120), "USER & CLOUD", size=18, fill=GREEN, bold=True)
    c.text((850, 120), "REAL-TIME CONTROL", size=18, fill=GREEN, bold=True)
    c.text((1640, 120), "PHYSICAL PROCESS", size=18, fill=GREEN, bold=True)

    # User/app/cloud
    c.rect((100, 155, 650, 350), fill=WHITE, outline=GREEN_2, width=2, radius=12)
    c.text((125, 172), "Phone / PWA", size=25, fill=INK, bold=True)
    c.text((125, 205), "Dashboard · history · manual sort", size=16, fill=MUTED)
    c.text((125, 235), "Wi-Fi hotspot or home network", size=16, fill=MUTED)
    c.text((125, 275), "Cloud sync (optional)", size=18, fill=BLUE, bold=True)
    c.text((125, 303), "Firebase / Supabase · offline queue", size=15, fill=MUTED)

    # Pi box
    c.rect((100, 395, 650, 1010), fill=WHITE, outline=BLUE, width=3, radius=14)
    c.rect((100, 395, 650, 455), fill=BLUE, outline=None, radius=14)
    c.rect((100, 435, 650, 455), fill=BLUE, outline=None)
    c.text((125, 410), "Raspberry Pi Zero 2 W", size=26, fill=WHITE, bold=True)
    c.text((125, 475), "VISION + APP + DATA", size=15, fill=BLUE, bold=True)
    items = [
        ("USB camera", "5 MP UVC · 1280×720 · fixed exposure"),
        ("Capture & pre-process", "3 frames · crop · white balance"),
        ("MobileNetV2 classifier", "TFLite · 4 classes + confidence"),
        ("Sensor fusion", "vision + weight + moisture + metal"),
        ("Sort orchestration", "state machine · retries · logging"),
        ("FastAPI + SQLite", "REST API · event history · bin levels"),
        ("Cloud sync", "optional · retry queue"),
    ]
    y = 515
    for i, (a, b) in enumerate(items):
        c.rect((125, y, 625, y + 58), fill=(248, 251, 252) if i % 2 == 0 else WHITE, outline=GREY, width=1, radius=7)
        c.text((140, y + 9), a, size=18, fill=INK, bold=True)
        c.text((140, y + 32), b, size=14, fill=MUTED)
        y += 65

    # ESP32 box
    c.rect((830, 395, 1510, 1010), fill=WHITE, outline=ORANGE, width=3, radius=14)
    c.rect((830, 395, 1510, 455), fill=ORANGE, outline=None, radius=14)
    c.rect((830, 435, 1510, 455), fill=ORANGE, outline=None)
    c.text((855, 410), "ESP32 DevKit (real-time MCU)", size=25, fill=WHITE, bold=True)
    c.text((855, 475), "SENSORS + MOTION + SAFETY", size=15, fill=ORANGE, bold=True)
    items2 = [
        ("Sensor acquisition", "HX711 · ToF ×5 · IR · moisture · metal"),
        ("Debounce & filtering", "median / moving average / thresholds"),
        ("Motion control", "stepper 3:1 belt · servo door · homing"),
        ("Interlocks", "lid · drawer · door · e-stop · watchdog"),
        ("Serial protocol", "newline JSON over USB · 115200 baud"),
        ("Fault handling", "jam · timeout · bin missing · bin full"),
        ("Status outputs", "RGB bar · buzzer · event log"),
    ]
    y = 515
    for i, (a, b) in enumerate(items2):
        c.rect((855, y, 1485, y + 58), fill=(255, 250, 244) if i % 2 == 0 else WHITE, outline=GREY, width=1, radius=7)
        c.text((870, y + 9), a, size=18, fill=INK, bold=True)
        c.text((870, y + 32), b, size=14, fill=MUTED)
        y += 65

    # Sensors strip top right
    c.rect((1600, 155, 2300, 350), fill=WHITE, outline=GREEN_2, width=2, radius=12)
    c.text((1620, 170), "SENSOR SET", size=18, fill=GREEN, bold=True)
    sensors = [
        ("Camera", "material / shape"),
        ("ToF item", "presence / height"),
        ("Load cells", "weight"),
        ("Moisture pad", "wet / dry"),
        ("Metal coil", "metal confirm"),
        ("IR beam", "hand safety"),
        ("ToF ×4", "bin fill level"),
        ("Switches", "lid / door / drawer"),
    ]
    for i, (a, b) in enumerate(sensors):
        col, row = i % 4, i // 4
        x = 1620 + col * 168
        y = 205 + row * 66
        c.rect((x, y, x + 155, y + 55), fill=(240, 248, 241), outline=GREY, width=1, radius=6)
        c.text((x + 8, y + 6), a, size=14, fill=GREEN, bold=True)
        c.text((x + 8, y + 27), b, size=11, fill=MUTED)

    # Actuators bottom right
    c.rect((1600, 760, 2300, 1010), fill=WHITE, outline=ORANGE, width=2, radius=12)
    c.text((1620, 775), "ACTUATORS", size=18, fill=ORANGE, bold=True)
    acts = [
        ("NEMA 17", "rotates spout", "3:1 GT2"),
        ("Servo 25 kg", "hopper door", "spring return"),
        ("LED ring", "diffuse light", "12 V"),
        ("RGB bar", "status", "5 V"),
    ]
    for i, (a, b, d) in enumerate(acts):
        col, row = i % 2, i // 2
        x = 1620 + col * 330
        y = 815 + row * 88
        c.rect((x, y, x + 310, y + 72), fill=(255, 249, 240), outline=GREY, width=1, radius=6)
        c.text((x + 10, y + 7), a, size=17, fill=INK, bold=True)
        c.text((x + 10, y + 29), b, size=13, fill=MUTED)
        c.text((x + 10, y + 49), d, size=12, fill=ORANGE)

    # Physical process column
    c.rect((1600, 395, 2300, 700), fill=WHITE, outline=BLUE, width=2, radius=12)
    c.text((1620, 410), "WASTE PATH", size=18, fill=BLUE, bold=True)
    steps = [
        ("1  Load", "lid open · item placed"),
        ("2  Weigh & see", "door closed · camera + sensors"),
        ("3  Decide", "4-class label + confidence"),
        ("4  Rotate spout", "stepper to selected bin"),
        ("5  Drop", "door opens · item falls"),
        ("6  Confirm & home", "drop beam · close · home"),
    ]
    for i, (a, b) in enumerate(steps):
        y = 450 + i * 39
        c.text((1620, y), a, size=16, fill=INK, bold=True)
        c.text((1810, y + 1), b, size=14, fill=MUTED)
    c.line([(1608, 445), (1608, 680)], fill=BLUE, width=2)
    for i in range(6):
        c.ellipse((1600, 450 + i * 39, 1616, 466 + i * 39), fill=BLUE, outline=WHITE, width=1)

    # Arrows and labels
    # camera -> Pi via a clean route above the two controller boxes
    c.line([(1600, 250), (700, 250), (700, 475)], fill=BLUE, width=3)
    c.arrow((700, 475), (655, 475), fill=BLUE, width=3, head=12)
    c.text((920, 232), "USB camera  (UVC)", size=15, fill=BLUE, bold=True)
    # sensors -> ESP32, routed outside the waste-path box
    c.line([(1620, 350), (1620, 375), (1545, 375), (1545, 470)], fill=GREEN_2, width=3)
    c.arrow((1545, 470), (1515, 470), fill=GREEN_2, width=3, head=12)
    c.text((1552, 392), "I2C / GPIO", size=14, fill=GREEN_2, bold=True)
    # Pi <-> ESP32
    c.arrow((660, 700), (820, 700), fill=BLUE, width=4, head=14)
    c.arrow((820, 735), (660, 735), fill=BLUE, width=3, head=12)
    c.text((740, 660), "USB serial", size=15, fill=BLUE, anchor="ma", bold=True)
    c.text((740, 745), "JSON", size=14, fill=BLUE, anchor="ma")
    # Pi -> app/cloud
    c.arrow((375, 390), (375, 355), fill=BLUE, width=3, head=12)
    c.text((390, 360), "Wi-Fi / REST", size=13, fill=BLUE)
    # ESP32 -> actuators
    c.arrow((1490, 975), (1600, 900), fill=ORANGE, width=3, head=12)
    c.text((1500, 930), "PWM / STEP", size=13, fill=ORANGE, bold=True)
    # ESP32 -> physical process
    c.arrow((1515, 550), (1595, 550), fill=ORANGE, width=3, head=12)
    c.text((1515, 525), "motion", size=13, fill=ORANGE)
    # feedback from physical process
    c.arrow((1600, 610), (1515, 610), fill=GREEN_2, width=2, head=10, dash=(8, 6))
    c.text((1520, 620), "events", size=12, fill=GREEN_2)

    # Power rail bottom
    c.rect((100, 1070, 1510, 1200), fill=WHITE, outline=MUTED, width=2, radius=10)
    c.text((120, 1085), "POWER", size=16, fill=INK, bold=True)
    c.text((120, 1115), "12 V 6 Ah Li-ion (BMS) → 5 A fuse → main switch → e-stop → actuator bus", size=15, fill=MUTED)
    c.text((120, 1143), "Buck 1: 5 V 5 A → Pi · Buck 2: 6 V 5 A → servo · Buck 3: 5 V 3 A → ESP32 / sensors", size=14, fill=MUTED)
    c.text((120, 1170), "Common star ground · actuators cut by e-stop · Pi/ESP32 stay alive for logging", size=13, fill=GREEN, bold=True)
    # dashed power arrows
    for x in (375, 1160):
        c.arrow((x, 1070), (x, 1010), fill=MUTED, width=2, head=8, dash=(7, 5))

    # Legend
    c.text((60, 1240), "Signal types:", size=14, fill=MUTED, bold=True)
    c.line([(180, 1248), (230, 1248)], fill=BLUE, width=3); c.text((240, 1240), "USB / network", size=13, fill=MUTED)
    c.line([(390, 1248), (440, 1248)], fill=GREEN_2, width=3); c.text((450, 1240), "sensor bus", size=13, fill=MUTED)
    c.line([(570, 1248), (620, 1248)], fill=ORANGE, width=3); c.text((630, 1240), "actuator power / PWM", size=13, fill=MUTED)
    c.line([(850, 1248), (900, 1248)], fill=MUTED, width=2); c.text((910, 1240), "power", size=13, fill=MUTED)

    # Design rules strip
    c.rect((100, 1290, 2300, 1450), fill=WHITE, outline=GREY, width=2, radius=10)
    c.text((120, 1305), "FOUR RULES THAT MAKE THE PROTOTYPE SAFE AND TESTABLE", size=16, fill=GREEN, bold=True)
    rules = [
        ("1", "No motion unless the lid, drawer and hopper door are closed."),
        ("2", "The e-stop cuts actuator 12 V, but keeps the Pi and ESP32 alive for logging."),
        ("3", "Every cycle starts and ends at a known home position."),
        ("4", "If the classifier is unsure, ask the user; never guess silently."),
    ]
    for i, (n, t) in enumerate(rules):
        x = 120 + i * 545
        c.ellipse((x, 1345, x + 30, 1375), fill=ORANGE, outline=None)
        c.text((x + 15, 1360), n, size=14, fill=WHITE, anchor="mm", bold=True)
        c.textbox((x + 42, 1342), t, size=13, fill=INK, maxw=470)

    footer(c, "Two processors are used deliberately: Linux for vision/app, ESP32 for deterministic timing and safety.")
    c.save(os.path.join(OUT, "fig01_system_architecture.png"))


def cross_section():
    # Scale: 2.4 px/mm, drawing area left 1500 px; legend right.
    c = Canvas(2600, 3000, PAPER)
    header(c, "Front section & sensor locations", "正視剖面圖與感測器位置（mm）", "Fig. 02")
    S = 2.35
    ox, oy = 260, 2740  # origin at floor left
    W, H = 480, 940

    def X(x): return ox + x * S
    def Y(z): return oy - z * S

    # floor shadow
    c.ellipse((X(-20), Y(0) - 18, X(500), Y(0) + 26), fill=(235, 238, 236), outline=None)

    # outer shell
    c.rect((X(0), Y(H), X(W), Y(0)), fill=(250, 251, 250), outline=INK, width=3)
    c.rect((X(0), Y(H), X(W), Y(0)), fill=None, outline=INK, width=3)
    # feet
    for x in (25, 430):
        c.rect((X(x), Y(0), X(x + 25), Y(-20)), fill=GREY, outline=INK, width=1)
    # base / electronics
    c.rect((X(0), Y(100), X(W), Y(20)), fill=(238, 242, 245), outline=INK, width=2)
    c.text((X(12), Y(88)), "ELECTRONICS BAY  電子倉", size=16, fill=BLUE, bold=True)
    c.text((X(12), Y(65)), "Pi · ESP32 · buck converters · fuse · driver", size=12, fill=MUTED)
    # vent
    for i in range(6):
        c.line([(X(380), Y(80 - i * 8)), (X(455), Y(80 - i * 8))], fill=LINE, width=1)

    # bin section
    c.rect((X(0), Y(520), X(W), Y(120)), fill=WHITE, outline=INK, width=2)
    # drawer
    c.rect((X(10), Y(515), X(470), Y(130)), fill=(249, 250, 249), outline=MUTED, width=1)
    # four bins, front two visible; show 2x2 with back dashed
    bins = [
        (18, 138, 210, 500, "BIN 1", "plastic", BLUE_2),
        (228, 138, 420, 500, "BIN 2", "metal", (250, 235, 190)),
        (18, 18, 210, 130, "BIN 3", "wet", (210, 235, 214)),
        (228, 18, 420, 130, "BIN 4", "other", (230, 232, 234)),
    ]
    for (x1, z1, x2, z2, name, cls, col) in bins:
        c.rect((X(x1), Y(z2), X(x2), Y(z1)), fill=col, outline=INK, width=1)
        c.text((X(x1 + 8), Y(z2 - 22)), name, size=14, fill=INK, bold=True)
        c.text((X(x1 + 8), Y(z2 - 40)), cls, size=12, fill=MUTED)
    # bin notch at center (front bins): 80x80
    c.rect((X(210), Y(500), X(228), Y(420)), fill=WHITE, outline=INK, width=1)
    c.rect((X(228), Y(500), X(246), Y(420)), fill=WHITE, outline=INK, width=1)
    # drawer front
    c.rect((X(0), Y(400), X(10), Y(130)), fill=(225, 230, 228), outline=INK, width=2)
    c.rect((X(2), Y(300), X(8), Y(260)), fill=GREY, outline=INK, width=1)  # handle

    # mid frame
    c.rect((X(0), Y(600), X(W), Y(520)), fill=(232, 237, 234), outline=INK, width=2)
    c.text((X(8), Y(588)), "MID FRAME + LOAD CELLS + SPOUT BEARING", size=12, fill=GREEN, bold=True)

    # hopper support plate and load cells
    c.rect((X(60), Y(620), X(420), Y(600)), fill=(215, 222, 219), outline=INK, width=2)
    for x in (90, 350):
        c.rect((X(x), Y(620), X(x + 40), Y(600)), fill=YELLOW, outline=INK, width=1)
        c.text((X(x + 20), Y(610)), "LC", size=10, fill=INK, anchor="mm", bold=True)

    # hopper body
    c.rect((X(80), Y(900), X(400), Y(620)), fill=(252, 252, 252), outline=INK, width=3)
    c.rect((X(80), Y(900), X(400), Y(620)), fill=None, outline=INK, width=3)
    # hopper inner liner
    c.rect((X(92), Y(888), X(388), Y(640)), fill=(245, 245, 242), outline=LINE, width=1)
    # door at bottom (closed) with slight slope
    c.rect((X(95), Y(645), X(385), Y(625)), fill=(225, 232, 228), outline=INK, width=2)
    c.text((X(120), Y(632)), "HOPPER DOOR  料斗門", size=12, fill=INK, bold=True)
    # hinge
    c.ellipse((X(86), Y(645), X(98), Y(633)), fill=INK, outline=None)
    # servo
    c.rect((X(335), Y(700), X(380), Y(655)), fill=(230, 230, 230), outline=INK, width=1)
    c.text((X(357), Y(678)), "SERVO", size=9, fill=INK, anchor="mm", bold=True)
    # spring
    c.line([(X(325), Y(650)), (X(300), Y(630))], fill=RED, width=2)

    # funnel
    c.polygon(c._xy([(X(180), Y(625)), (X(300), Y(625)), (X(280), Y(560)), (X(200), Y(560))]),
              fill=(235, 240, 236), outline=INK)
    c.text((X(240), Y(588)), "FUNNEL", size=11, fill=INK, anchor="mm", bold=True)
    # spout bearing
    c.rect((X(190), Y(560), X(290), Y(548)), fill=(210, 218, 214), outline=INK, width=1)
    c.text((X(240), Y(553)), "BEARING", size=8, fill=INK, anchor="mm", bold=True)
    # rotating spout
    c.polygon(c._xy([(X(200), Y(548)), (X(280), Y(548)), (X(330), Y(520)), (X(290), Y(505))]),
              fill=(225, 235, 230), outline=ORANGE)
    c.text((X(300), Y(526)), "SPOUT", size=10, fill=ORANGE, bold=True)
    c.arrow((X(240), Y(548)), (X(320), Y(515)), fill=ORANGE, width=2, head=8)
    # spout guard
    c.rect((X(150), Y(545), X(350), Y(500)), fill=None, outline=LINE, width=1)

    # camera and LED ring on lid
    c.rect((X(0), Y(940), X(W), Y(900)), fill=(238, 241, 238), outline=INK, width=2)
    c.rect((X(0), Y(940), X(W), Y(900)), fill=None, outline=INK, width=2)
    c.text((X(12), Y(928)), "LID  蓋", size=14, fill=INK, bold=True)
    # camera bracket
    c.rect((X(220), Y(905), X(260), Y(860)), fill=(40, 45, 50), outline=INK, width=1)
    c.ellipse((X(228), Y(875), X(252), Y(851)), fill=(20, 25, 30), outline=WHITE, width=1)
    c.text((X(240), Y(845)), "CAMERA", size=10, fill=WHITE, anchor="mm", bold=True)
    # LED ring
    c.ellipse((X(205), Y(890), X(275), Y(820)), fill=None, outline=YELLOW, width=5)
    c.text((X(240), Y(807)), "LED RING", size=9, fill=ORANGE, anchor="mm", bold=True)
    # ToF on lid
    c.rect((X(295), Y(895), X(315), Y(875)), fill=BLUE, outline=INK, width=1)
    c.text((X(305), Y(868)), "ToF", size=9, fill=BLUE, anchor="mm", bold=True)
    # lid hinge
    c.ellipse((X(0), Y(940), X(18), Y(922)), fill=INK, outline=None)
    # gas strut
    c.line([(X(30), Y(935)), (X(45), Y(900))], fill=MUTED, width=3)
    # magnet/reed
    c.rect((X(410), Y(925), X(430), Y(905)), fill=RED, outline=INK, width=1)
    c.text((X(420), Y(898)), "REED", size=8, fill=RED, anchor="mm", bold=True)

    # IR beam
    c.line([(X(95), Y(885)), (X(385), Y(885))], fill=RED, width=2, dash=(6, 5))
    c.rect((X(88), Y(892), X(102), Y(878)), fill=RED, outline=INK, width=1)
    c.rect((X(378), Y(892), X(392), Y(878)), fill=RED, outline=INK, width=1)
    c.text((X(240), Y(895)), "IR SAFETY BEAM", size=9, fill=RED, anchor="mm", bold=True)

    # metal coil under hopper door (fixed)
    c.arc((X(170), Y(605), X(310), Y(570)), 0, 180, fill=ORANGE, width=4)
    c.text((X(240), Y(565)), "METAL COIL", size=9, fill=ORANGE, anchor="mm", bold=True)
    # moisture pad on door
    c.rect((X(150), Y(643), X(330), Y(637)), fill=(180, 210, 230), outline=BLUE, width=2)
    c.text((X(240), Y(650)), "MOISTURE PAD", size=9, fill=BLUE, anchor="mm", bold=True)

    # bin ToF sensors on mid-frame, at outer corners
    for x, label in ((45, "B1"), (405, "B2")):
        c.rect((X(x), Y(528), X(x + 18), Y(510)), fill=BLUE, outline=INK, width=1)
        c.text((X(x + 9), Y(503)), label, size=8, fill=BLUE, anchor="mm", bold=True)
    c.text((X(240), Y(505)), "ToF ×4 (bin fill)", size=9, fill=BLUE, anchor="mm", bold=True)

    # dimensions left
    dim_v(c, Y(940), Y(0), X(0) - 55, "940", color=BLUE)
    dim_v(c, Y(900), Y(620), X(0) - 55, "280", color=MUTED, size=18)
    dim_v(c, Y(620), Y(520), X(0) - 55, "100", color=MUTED, size=18)
    dim_v(c, Y(520), Y(120), X(0) - 55, "400", color=MUTED, size=18)
    dim_v(c, Y(120), Y(0), X(0) - 55, "120", color=MUTED, size=18)
    # dimensions right
    dim_h(c, X(0), X(480), Y(0) + 55, "480", color=BLUE)
    dim_h(c, X(80), X(400), Y(900) - 28, "320 (hopper opening)", color=MUTED, size=16)
    dim_h(c, X(95), X(385), Y(625) + 28, "290 (door)", color=MUTED, size=16)
    # camera height
    dim_v(c, Y(875), Y(645), X(480) + 45, "230 camera height", color=ORANGE, size=16)

    # callouts / legend right
    lx = 1600
    c.text((lx, 140), "KEY COMPONENTS", size=22, fill=GREEN, bold=True)
    legend = [
        ("1", "Lid with USB camera + diffuse LED ring", "蓋：USB 鏡頭＋擴散 LED 環"),
        ("2", "IR safety beam across the hopper mouth", "料斗口紅外安全光束"),
        ("3", "Item ToF: presence & height", "物件 ToF：存在與高度"),
        ("4", "Weigh hopper on 4 × 5 kg load cells", "4 × 5 kg 負重感測器稱重料斗"),
        ("5", "Capacitive moisture pad on door", "門上電容式濕度墊"),
        ("6", "Fixed metal-detector coil under door", "門下固定金屬探測線圈"),
        ("7", "Servo + spring-assisted hopper door", "伺服＋彈簧輔助料斗門"),
        ("8", "Funnel with 110 mm outlet", "110 mm 出口漏斗"),
        ("9", "Rotating spout on 150 mm bearing", "150 mm 軸承旋轉滑槽"),
        ("10", "4 fixed bins in a pull-out drawer", "4 個固定桶於拉出抽屜"),
        ("11", "4 × ToF bin-level sensors", "4 × ToF 滿度感測器"),
        ("12", "Electronics bay: Pi, ESP32, power", "電子倉：Pi、ESP32、電源"),
    ]
    y = 185
    for num, a, b in legend:
        c.ellipse((lx, y, lx + 30, y + 30), fill=ORANGE, outline=None)
        c.text((lx + 15, y + 15), num, size=14, fill=WHITE, anchor="mm", bold=True)
        c.text((lx + 45, y), a, size=17, fill=INK, bold=True)
        c.text((lx + 45, y + 22), b, size=15, fill=MUTED, zh=True)
        y += 58

    # notes
    c.rect((lx, 930, 2520, 1250), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((lx + 18, 945), "DESIGN NOTES", size=16, fill=GREEN, bold=True)
    notes = [
        "•  Overall 480 W × 480 D × 940 H mm; loading lip 900 mm.",
        "•  Hopper: 320 × 320 × 260 mm internal; door 290 × 240 mm.",
        "•  Bins: 190 × 190 × 360 mm internal, 80 × 80 mm corner notch; ~10.7 L each.",
        "•  Camera: 90° diagonal FOV at 230 mm above door; covers 368 × 276 mm.",
        "•  Spout outlet radius 130 mm; bin centres at 117, 117 mm (radius 165 mm).",
        "•  All dimensions are nominal; build with 1-2 mm clearance and slotted mounts.",
    ]
    yy = 978
    for n in notes:
        c.text((lx + 18, yy), n, size=14, fill=INK)
        yy += 34

    # scale bar
    c.line([(1600, 1370), (1600 + 100 * S, 1370)], fill=INK, width=4)
    c.line([(1600, 1364), (1600, 1376)], fill=INK, width=2)
    c.line([(1600 + 100 * S, 1364), (1600 + 100 * S, 1376)], fill=INK, width=2)
    c.text((1600 + 50 * S, 1382), "100 mm", size=13, fill=INK, anchor="ma")

    footer(c, "Section A-A, viewed from the front. Drawings are schematic; verify on the built frame before drilling.")
    c.save(os.path.join(OUT, "fig02_cross_section.png"))


if __name__ == "__main__":
    architecture()
    # The dimensioned section, top view, exploded view and wiring diagrams are in make_figures.py.
