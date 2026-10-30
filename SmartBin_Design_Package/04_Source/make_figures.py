# -*- coding: utf-8 -*-
"""Dimensioned figures, sequence, wiring and state machine."""
import os, math, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from draw_lib import *
from make_diagrams import header, footer

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_Drawings"))
os.makedirs(OUT, exist_ok=True)


def cross_section():
    c = Canvas(2600, 3000, PAPER)
    header(c, "Front section & sensor locations", "正視剖面圖與感測器位置（mm）", "Fig. 02")
    S = 2.6
    ox, oy = 220, 2860
    W, H = 480, 940

    def X(x): return ox + x * S
    def Y(z): return oy - z * S

    # floor shadow
    c.ellipse((X(-25), Y(0) - 16, X(505), Y(0) + 24), fill=(236, 239, 237), outline=None)

    # outer shell and layers
    c.rect((X(0), Y(H), X(W), Y(0)), fill=(251, 252, 251), outline=INK, width=3)
    c.line([(X(0), Y(900)), (X(W), Y(900))], fill=INK, width=2)
    c.line([(X(0), Y(600)), (X(W), Y(600))], fill=INK, width=2)
    c.line([(X(0), Y(520)), (X(W), Y(520))], fill=INK, width=2)
    c.line([(X(0), Y(120)), (X(W), Y(120))], fill=INK, width=2)
    # feet
    for x in (25, 430):
        c.rect((X(x), Y(0), X(x + 25), Y(-20)), fill=GREY, outline=INK, width=1)

    # base / electronics
    c.rect((X(0), Y(120), X(W), Y(20)), fill=(238, 242, 245), outline=INK, width=2)
    c.text((X(12), Y(108)), "ELECTRONICS BAY  電子倉", size=17, fill=BLUE, bold=True)
    c.text((X(12), Y(86)), "Raspberry Pi · ESP32 · buck converters", size=12, fill=MUTED)
    c.text((X(12), Y(68)), "fuse · stepper driver · terminal blocks", size=12, fill=MUTED)
    for i in range(6):
        c.line([(X(385), Y(102 - i * 8)), (X(458), Y(102 - i * 8))], fill=LINE, width=1)
    c.text((X(420), Y(48)), "VENT", size=9, fill=MUTED, anchor="mm")

    # bin section
    c.rect((X(0), Y(520), X(W), Y(120)), fill=WHITE, outline=INK, width=2)
    c.text((X(10), Y(508)), "BIN DRAWER  垃圾桶抽屜", size=13, fill=GREEN, bold=True)
    # drawer outline
    c.rect((X(12), Y(520), X(468), Y(130)), fill=(250, 251, 250), outline=MUTED, width=1)
    # front bins (190 internal)
    for x1, x2, name, cls, col in ((28, 218, "BIN 1", "plastic", BLUE_2), (262, 452, "BIN 2", "metal", (250, 235, 190))):
        c.rect((X(x1), Y(500), X(x2), Y(140)), fill=col, outline=INK, width=2)
        c.text((X(x1 + 8), Y(480)), name, size=14, fill=INK, bold=True)
        c.text((X(x1 + 8), Y(462)), cls, size=12, fill=MUTED)
    # rim
    c.rect((X(28), Y(520), X(218), Y(500)), fill=(230, 235, 232), outline=INK, width=1)
    c.rect((X(262), Y(520), X(452), Y(500)), fill=(230, 235, 232), outline=INK, width=1)
    # inner-corner notches 80 x 80
    c.rect((X(138), Y(500), X(218), Y(420)), fill=WHITE, outline=INK, width=1)
    c.rect((X(262), Y(500), X(342), Y(420)), fill=WHITE, outline=INK, width=1)
    c.text((X(178), Y(460)), "80×80\nnotch", size=9, fill=RED, anchor="mm", align="center")
    c.text((X(302), Y(460)), "80×80\nnotch", size=9, fill=RED, anchor="mm", align="center")
    # drawer front
    c.rect((X(0), Y(520), X(12), Y(130)), fill=(223, 228, 226), outline=INK, width=2)
    c.rect((X(2), Y(360), X(8), Y(300)), fill=GREY, outline=INK, width=1)
    c.text((X(6), Y(280)), "HANDLE", size=8, fill=MUTED, anchor="mm")
    # rear bins note
    c.text((X(240), Y(155)), "Rear bins 3 / 4 are directly behind bins 1 / 2 — see Fig. 03 top view.", size=11, fill=MUTED, anchor="ma")
    # bin ToF sensors
    for x in (40, 406):
        c.rect((X(x), Y(520), X(x + 18), Y(502)), fill=BLUE, outline=INK, width=1)
        c.text((X(x + 9), Y(493)), "ToF", size=8, fill=BLUE, anchor="mm", bold=True)
    c.text((X(240), Y(480)), "4 × ToF bin-level sensors 滿度感測", size=9, fill=BLUE, anchor="mm")

    # mid frame
    c.rect((X(0), Y(600), X(W), Y(520)), fill=(232, 237, 234), outline=INK, width=2)
    c.text((X(8), Y(590)), "MID FRAME  中框", size=13, fill=GREEN, bold=True)
    c.text((X(8), Y(572)), "load cells · funnel · spout bearing", size=10, fill=MUTED)

    # hopper support plate and load cells
    c.rect((X(60), Y(630), X(420), Y(620)), fill=(213, 221, 217), outline=INK, width=2)
    for x in (80, 360):
        c.rect((X(x), Y(620), X(x + 40), Y(600)), fill=YELLOW, outline=INK, width=1)
        c.text((X(x + 20), Y(610)), "LC", size=9, fill=INK, anchor="mm", bold=True)
    c.text((X(240), Y(636)), "4 × 5 kg load cells", size=9, fill=ORANGE, anchor="ma", bold=True)

    # hopper body
    c.rect((X(60), Y(900), X(420), Y(630)), fill=(252, 252, 252), outline=INK, width=3)
    c.rect((X(80), Y(888), X(400), Y(642)), fill=(246, 246, 243), outline=LINE, width=1)
    c.text((X(70), Y(880)), "HOPPER  料斗", size=14, fill=INK, bold=True)
    c.text((X(70), Y(862)), "320 × 320 × 260 mm internal", size=10, fill=MUTED)
    # door
    c.rect((X(95), Y(642), X(385), Y(628)), fill=(223, 231, 226), outline=INK, width=2)
    c.text((X(120), Y(646)), "HOPPER DOOR  料斗門", size=10, fill=INK, bold=True)
    c.ellipse((X(86), Y(642), X(98), Y(630)), fill=INK, outline=None)
    # spring
    c.line([(X(360), Y(640)), (X(330), Y(620))], fill=RED, width=2)
    # servo on outside bracket
    c.rect((X(420), Y(705), X(462), Y(655)), fill=(230, 230, 230), outline=INK, width=1)
    c.text((X(441), Y(680)), "SERVO", size=8, fill=INK, anchor="mm", bold=True)
    c.line([(X(420), Y(665)), (X(385), Y(635))], fill=INK, width=2)
    c.text((X(441), Y(715)), "25 kg·cm", size=8, fill=MUTED, anchor="ma")

    # funnel
    c.polygon([(X(100), Y(630)), (X(380), Y(630)), (X(295), Y(490)), (X(185), Y(490))],
              fill=(232, 239, 234), outline=INK, width=2)
    c.text((X(240), Y(565)), "FUNNEL  漏斗", size=10, fill=INK, anchor="mm", bold=True)
    c.text((X(240), Y(548)), "280 → 110 mm, 59° walls", size=8, fill=MUTED, anchor="mm")
    # metal coil under door, fixed to mid-frame
    c.arc((X(165), Y(622), X(315), Y(586)), 0, 180, fill=ORANGE, width=5)
    c.text((X(240), Y(582)), "METAL COIL  金屬線圈", size=8, fill=ORANGE, anchor="mm", bold=True)
    # moisture pad on door
    c.rect((X(145), Y(642), X(335), Y(636)), fill=(176, 208, 230), outline=BLUE, width=2)
    c.text((X(240), Y(650)), "MOISTURE PAD  濕度墊", size=8, fill=BLUE, anchor="mm", bold=True)

    # spout bearing and spout
    c.rect((X(185), Y(490), X(295), Y(480)), fill=(208, 217, 212), outline=INK, width=1)
    c.text((X(240), Y(485)), "BEARING", size=7, fill=INK, anchor="mm", bold=True)
    # 45 deg elbow, outlet to the right (shown at bin 2)
    c.polygon([(X(190), Y(480)), (X(290), Y(480)), (X(370), Y(505)), (X(310), Y(515))],
              fill=(225, 235, 230), outline=ORANGE, width=2)
    c.text((X(330), Y(528)), "SPOUT  滑槽", size=9, fill=ORANGE, bold=True)
    c.arrow((X(240), Y(485)), (X(335), Y(505)), fill=ORANGE, width=2, head=8)
    c.text((X(240), Y(470)), "outlet r = 130 mm", size=8, fill=ORANGE, anchor="ma")

    # lid and camera
    c.rect((X(0), Y(940), X(W), Y(900)), fill=(238, 241, 238), outline=INK, width=2)
    c.text((X(12), Y(928)), "LID  蓋", size=13, fill=INK, bold=True)
    # camera bracket
    c.rect((X(220), Y(902), X(260), Y(858)), fill=(38, 43, 48), outline=INK, width=1)
    c.ellipse((X(228), Y(872), X(252), Y(848)), fill=(18, 23, 28), outline=WHITE, width=1)
    c.text((X(240), Y(840)), "USB CAMERA", size=9, fill=WHITE, anchor="mm", bold=True)
    # LED ring
    c.ellipse((X(202), Y(892), X(278), Y(816)), fill=None, outline=YELLOW, width=5)
    c.text((X(240), Y(802)), "LED RING", size=8, fill=ORANGE, anchor="mm", bold=True)
    # item ToF
    c.rect((X(300), Y(895), X(320), Y(875)), fill=BLUE, outline=INK, width=1)
    c.text((X(310), Y(866)), "ToF", size=8, fill=BLUE, anchor="mm", bold=True)
    # lid hinge and strut
    c.ellipse((X(0), Y(940), X(18), Y(922)), fill=INK, outline=None)
    c.line([(X(30), Y(935)), (X(45), Y(905))], fill=MUTED, width=3)
    # reed switch
    c.rect((X(410), Y(925), X(430), Y(905)), fill=RED, outline=INK, width=1)
    c.text((X(420), Y(896)), "REED", size=7, fill=RED, anchor="mm", bold=True)
    # IR beam
    c.line([(X(85), Y(880)), (X(395), Y(880))], fill=RED, width=2, dash=(6, 5))
    c.rect((X(78), Y(888), X(92), Y(872)), fill=RED, outline=INK, width=1)
    c.rect((X(388), Y(888), X(402), Y(872)), fill=RED, outline=INK, width=1)
    c.text((X(240), Y(890)), "IR SAFETY BEAM  紅外安全光束", size=8, fill=RED, anchor="mm", bold=True)

    # dimensions left
    dim_v(c, Y(940), Y(0), X(0) - 58, "940", color=BLUE, size=20)
    dim_v(c, Y(940), Y(900), X(0) - 58, "40", color=MUTED, size=14)
    dim_v(c, Y(900), Y(600), X(0) - 58, "300", color=MUTED, size=14)
    dim_v(c, Y(600), Y(520), X(0) - 58, "80", color=MUTED, size=14)
    dim_v(c, Y(520), Y(120), X(0) - 58, "400", color=MUTED, size=14)
    dim_v(c, Y(120), Y(20), X(0) - 58, "100", color=MUTED, size=14)
    dim_v(c, Y(20), Y(0), X(0) - 58, "20", color=MUTED, size=12)
    # dimensions right
    dim_h(c, X(0), X(480), Y(0) + 58, "480", color=BLUE, size=20)
    dim_h(c, X(60), X(420), Y(900) - 26, "320 hopper", color=MUTED, size=13)
    dim_h(c, X(95), X(385), Y(628) - 26, "290 door", color=MUTED, size=13)
    dim_v(c, Y(870), Y(642), X(480) + 50, "228 camera height", color=ORANGE, size=14)
    # camera FOV cone
    c.line([(X(240), Y(860)), (X(55), Y(642))], fill=ORANGE, width=1, dash=(4, 5))
    c.line([(X(240), Y(860)), (X(425), Y(642))], fill=ORANGE, width=1, dash=(4, 5))

    # Legend right
    lx = 1570
    c.text((lx, 135), "KEY COMPONENTS", size=21, fill=GREEN, bold=True)
    legend = [
        ("1", "Lid with USB camera + diffuse LED ring", "蓋：USB 鏡頭＋擴散 LED 環"),
        ("2", "IR safety beam across the hopper mouth", "料斗口紅外安全光束"),
        ("3", "Item ToF: presence & height", "物件 ToF：存在與高度"),
        ("4", "Weigh hopper on 4 × 5 kg load cells", "4 × 5 kg 負重感測器稱重料斗"),
        ("5", "Capacitive moisture pad on door", "門上電容式濕度墊"),
        ("6", "Fixed metal-detector coil under door", "門下固定金屬探測線圈"),
        ("7", "Servo + spring-assisted hopper door", "伺服＋彈簧輔助料斗門"),
        ("8", "Funnel: 280 mm inlet, 110 mm outlet", "漏斗：280 mm 入口，110 mm 出口"),
        ("9", "Rotating spout on 150 mm bearing", "150 mm 軸承旋轉滑槽"),
        ("10", "4 fixed bins in a pull-out drawer", "4 個固定桶於拉出抽屜"),
        ("11", "4 × ToF bin-level sensors", "4 × ToF 滿度感測器"),
        ("12", "Electronics bay: Pi, ESP32, power", "電子倉：Pi、ESP32、電源"),
    ]
    y = 180
    for num, a, b in legend:
        c.ellipse((lx, y, lx + 28, y + 28), fill=ORANGE, outline=None)
        c.text((lx + 14, y + 14), num, size=13, fill=WHITE, anchor="mm", bold=True)
        c.text((lx + 42, y), a, size=16, fill=INK, bold=True)
        c.text((lx + 42, y + 21), b, size=14, fill=MUTED)
        y += 55

    # Design notes
    c.rect((lx, 900, 2520, 1245), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((lx + 18, 915), "DESIGN NOTES", size=15, fill=GREEN, bold=True)
    notes = [
        "•  Overall 480 W × 480 D × 940 H mm; loading lip 900 mm.",
        "•  Hopper 320 × 320 × 260 mm internal; door 290 × 240 mm.",
        "•  Bins 190 × 190 × 360 mm internal, 80 × 80 mm corner notch.",
        "•  Usable bin volume ≈ 10.7 L each; total ≈ 42.8 L.",
        "•  Camera 90° diagonal FOV at 228 mm above door: 368 × 276 mm.",
        "•  Spout outlet radius 130 mm; bin centres at (±117, ±117).",
        "•  Nominal dimensions: leave 1-2 mm clearance and slotted mounts.",
    ]
    yy = 948
    for n in notes:
        c.text((lx + 18, yy), n, size=13, fill=INK)
        yy += 36

    # Materials / finish note
    c.rect((lx, 1280, 2520, 1420), fill=(240, 248, 241), outline=GREEN_2, width=1, radius=8)
    c.text((lx + 18, 1295), "MATERIALS & FINISH", size=14, fill=GREEN, bold=True)
    c.text((lx + 18, 1325), "18 mm plywood frame; 3 mm PP liner in hopper and bins;", size=12, fill=INK)
    c.text((lx + 18, 1348), "matte black inside hopper; silicone gasket on door;", size=12, fill=INK)
    c.text((lx + 18, 1371), "stainless hinges; all wet surfaces removable for cleaning.", size=12, fill=INK)

    # scale bar
    c.line([(lx, 1500), (lx + 100 * S, 1500)], fill=INK, width=4)
    c.line([(lx, 1494), (lx, 1506)], fill=INK, width=2)
    c.line([(lx + 100 * S, 1494), (lx + 100 * S, 1506)], fill=INK, width=2)
    c.text((lx + 50 * S, 1512), "100 mm", size=12, fill=INK, anchor="ma")

    footer(c, "Section A-A, viewed from the front. Schematic: verify on the built frame before drilling.")
    c.save(os.path.join(OUT, "fig02_cross_section.png"))


def top_view():
    c = Canvas(2400, 2100, PAPER)
    header(c, "Top view: bins, spout & sensor positions", "俯視圖：垃圾桶、滑槽與感測器位置（mm）", "Fig. 03")
    S = 2.3
    ox, oy = 650, 1000
    W = 480

    def X(x): return ox + x * S
    def Y(y): return oy + y * S

    # outer
    c.rect((X(-W/2), Y(-W/2), X(W/2), Y(W/2)), fill=(251, 252, 251), outline=INK, width=3)
    # drawer
    c.rect((X(-228), Y(-228), X(228), Y(228)), fill=WHITE, outline=MUTED, width=1)
    # bins 210 outer, centers +/-117
    bins = [(-117, -117, "BIN 1", "plastic", BLUE_2), (117, -117, "BIN 2", "metal", (250, 235, 190)),
            (-117, 117, "BIN 3", "wet", (210, 235, 214)), (117, 117, "BIN 4", "other", (230, 232, 234))]
    for cx, cy, name, cls, col in bins:
        c.rect((X(cx - 105), Y(cy - 105), X(cx + 105), Y(cy + 105)), fill=col, outline=INK, width=2)
        c.text((X(cx - 95), Y(cy - 95)), name, size=14, fill=INK, bold=True)
        c.text((X(cx - 95), Y(cy - 78)), cls, size=11, fill=MUTED)
    # inner corner notches
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x1 = 0 if sx == -1 else 0
        # notch 80x80 at inner corner of each bin
        if sx == -1 and sy == -1:
            c.rect((X(-80), Y(-80), X(0), Y(0)), fill=WHITE, outline=INK, width=1)
        if sx == 1 and sy == -1:
            c.rect((X(0), Y(-80), X(80), Y(0)), fill=WHITE, outline=INK, width=1)
        if sx == -1 and sy == 1:
            c.rect((X(-80), Y(0), X(0), Y(80)), fill=WHITE, outline=INK, width=1)
        if sx == 1 and sy == 1:
            c.rect((X(0), Y(0), X(80), Y(80)), fill=WHITE, outline=INK, width=1)
    # central funnel
    c.ellipse((X(-75), Y(-75), X(75), Y(75)), fill=(232, 239, 234), outline=INK, width=2)
    c.ellipse((X(-55), Y(-55), X(55), Y(55)), fill=WHITE, outline=ORANGE, width=2)
    c.text((0 + X(0), Y(0)), "FUNNEL\n110 outlet", size=9, fill=ORANGE, anchor="mm", align="center")
    # spout sweep
    c.ellipse((X(-130), Y(-130), X(130), Y(130)), fill=None, outline=ORANGE, width=2, )
    c.text((X(0), Y(145)), "spout outlet sweep r = 130", size=10, fill=ORANGE, anchor="ma")
    # spout at 45 deg
    ang = math.radians(45)
    ex, ey = 130 * math.cos(ang), 130 * math.sin(ang)
    c.line([(X(0), Y(0)), (X(ex), Y(ey))], fill=ORANGE, width=8)
    c.ellipse((X(ex - 18), Y(ey - 18), X(ex + 18), Y(ey + 18)), fill=ORANGE, outline=WHITE, width=2)
    c.text((X(ex + 8), Y(ey + 8)), "spout", size=9, fill=ORANGE, bold=True)
    # bin centres
    for cx, cy in ((-117, -117), (117, -117), (-117, 117), (117, 117)):
        c.ellipse((X(cx - 3), Y(cy - 3), X(cx + 3), Y(cy + 3)), fill=RED, outline=None)
    # sensors
    # bin ToF at outer corners
    for x, y in ((-205, -205), (205, -205), (-205, 205), (205, 205)):
        c.rect((X(x - 9), Y(y - 9), X(x + 9), Y(y + 9)), fill=BLUE, outline=WHITE, width=1)
    c.text((X(0), Y(-232)), "4 × ToF bin-level sensors (blue)", size=10, fill=BLUE, anchor="ma", bold=True)
    # camera at center
    c.ellipse((X(-20), Y(-20), X(20), Y(20)), fill=INK, outline=WHITE, width=2)
    c.ellipse((X(-9), Y(-9), X(9), Y(9)), fill=(20, 25, 30), outline=None)
    c.text((X(0), Y(-32)), "camera", size=9, fill=WHITE, anchor="mb", bold=True)
    # IR beam
    c.line([(X(-150), Y(-20)), (X(150), Y(-20))], fill=RED, width=2, dash=(6, 5))
    c.text((X(0), Y(-28)), "IR beam", size=8, fill=RED, anchor="ma")
    # dimensions
    dim_h(c, X(-240), X(240), Y(260), "480", color=BLUE, size=18)
    dim_h(c, X(-117), X(117), Y(240), "234 bin centres", color=MUTED, size=12)
    dim_v(c, Y(-240), Y(240), X(-260), "480", color=BLUE, size=18)
    dim_h(c, X(-105), X(105), Y(155), "210 bin", color=MUTED, size=12)
    dim_h(c, X(-80), X(0), Y(95), "80 notch", color=RED, size=11)
    dim_v(c, Y(-75), Y(75), X(95), "150 bearing", color=ORANGE, size=12)

    # legend
    lx = 1320
    c.text((lx, 140), "LAYOUT RULES", size=20, fill=GREEN, bold=True)
    rules = [
        ("Four fixed bins", "2 × 2 grid; each 210 × 210 mm outer, 190 × 190 mm internal."),
        ("Corner notches", "80 × 80 mm at each inner corner clears the 150 mm bearing and funnel."),
        ("Spout", "Rotates 45°/135°/225°/315°; outlet radius 130 mm; always approaches clockwise."),
        ("Bin centres", "±117 mm, ±117 mm; drop point is 35 mm inside each bin centre."),
        ("Drawer", "Slides out 400 mm; drawer-closed switch prevents sorting when open."),
        ("Service", "Lift bins out; wipe liner; check ToF windows and spout for jams."),
    ]
    y = 190
    for i, (a, b) in enumerate(rules):
        c.ellipse((lx, y + 2, lx + 28, y + 30), fill=GREEN, outline=None)
        c.text((lx + 14, y + 16), str(i + 1), size=12, fill=WHITE, anchor="mm", bold=True)
        c.text((lx + 42, y), a, size=15, fill=INK, bold=True)
        c.textbox((lx + 42, y + 23), b, size=12, fill=MUTED, maxw=490)
        y += 95
    # bin colour key
    c.text((lx, 800), "BIN COLOUR KEY", size=15, fill=GREEN, bold=True)
    keys = [("Plastic 塑料", BLUE_2), ("Metal 金屬", (250, 235, 190)), ("Wet 濕垃圾", (210, 235, 214)), ("Other 其他", (230, 232, 234))]
    for i, (a, col) in enumerate(keys):
        yy = 835 + i * 42
        c.rect((lx, yy, lx + 30, yy + 30), fill=col, outline=INK, width=1)
        c.text((lx + 42, yy + 5), a, size=13, fill=INK)

    footer(c, "Top view with lid removed. The camera and item ToF sit on the lid, centred over the hopper.")
    c.save(os.path.join(OUT, "fig03_top_view.png"))


def exploded():
    c = Canvas(2200, 2600, PAPER)
    header(c, "Exploded assembly", "爆炸圖：由上至下組裝", "Fig. 04")
    # Isometric-ish stack
    cx, base_y = 900, 2200
    w, d, h = 620, 430, 90
    # base
    iso_box(c, cx, base_y, w, d, 100, (224, 231, 227))
    c.text((cx + 10, base_y - 100), "1  BASE / ELECTRONICS BAY", size=18, fill=INK, bold=True)
    # bins/drawer
    iso_box(c, cx, base_y - 200, w, d, 300, (210, 230, 240))
    c.text((cx + 10, base_y - 500), "2  BIN DRAWER + 4 BINS", size=18, fill=INK, bold=True)
    # mid frame
    iso_box(c, cx, base_y - 560, w, d, 70, (212, 222, 217))
    c.text((cx + 10, base_y - 630), "3  MID FRAME + LOAD CELLS + SPOUT", size=18, fill=INK, bold=True)
    # hopper
    iso_box(c, cx + 60, base_y - 700, w - 120, d - 80, 260, (245, 247, 244))
    c.text((cx + 70, base_y - 960), "4  WEIGH HOPPER + DOOR", size=18, fill=INK, bold=True)
    # lid
    iso_box(c, cx - 20, base_y - 1060, w + 40, d + 30, 40, (232, 238, 234))
    c.text((cx - 10, base_y - 1100), "5  LID + CAMERA + LED RING", size=18, fill=INK, bold=True)

    # dashed assembly lines
    for x in (cx + 30, cx + w - 30):
        c.line([(x, base_y + 20), (x, base_y - 1140)], fill=MUTED, width=1, dash=(6, 6))
    # callouts
    notes = [
        ("A", "Lid hinge + gas strut; camera cable service loop", 1600, 400),
        ("B", "Hopper sits on 4 load cells; door hinges at back", 1600, 560),
        ("C", "Funnel + 150 mm bearing + rotating spout", 1600, 720),
        ("D", "Drawer on 45 kg slides; bins lift out", 1600, 880),
        ("E", "Electronics bay: fused 12 V, Pi, ESP32, drivers", 1600, 1040),
    ]
    for tag, txt, x, y in notes:
        c.ellipse((x, y, x + 32, y + 32), fill=ORANGE, outline=None)
        c.text((x + 16, y + 16), tag, size=14, fill=WHITE, anchor="mm", bold=True)
        c.textbox((x + 45, y - 2), txt, size=15, fill=INK, maxw=480)
    c.text((1600, 1180), "ASSEMBLY ORDER", size=18, fill=GREEN, bold=True)
    steps = [
        "1. Base + electronics plate; run power and USB service cables.",
        "2. Drawer slides; set 1 mm clearance; fit bins and reed magnets.",
        "3. Mid-frame; load cells; check hopper floats freely.",
        "4. Funnel, bearing, spout; set home flag; check 360° clearance.",
        "5. Hopper + door; set spring and servo; leak-test with dry rice.",
        "6. Lid + camera + LED; set focus at 230 mm; check FOV.",
        "7. Sensors; calibrate; run 20 dry cycles before waste.",
        "8. Labels, guards, final safety check.",
    ]
    y = 1220
    for s in steps:
        c.text((1600, y), s, size=14, fill=INK)
        y += 36

    # dimension note
    c.rect((80, 120, 840, 240), fill=(250, 250, 248), outline=GREY, width=1, radius=8)
    c.text((100, 135), "OVERALL 480 × 480 × 940 mm", size=16, fill=GREEN, bold=True)
    c.text((100, 165), "Empty mass ≈ 22-26 kg; four bins ≈ 10.7 L each.", size=13, fill=MUTED)
    c.text((100, 190), "Built from 18 mm plywood + 3 mm PP liners; no welded frame.", size=13, fill=MUTED)

    footer(c, "Exploded view is schematic. Build the drawer and mid-frame first; test every subsystem before final assembly.")
    c.save(os.path.join(OUT, "fig04_exploded.png"))


if __name__ == "__main__":
    cross_section()
    top_view()
    exploded()
