# -*- coding: utf-8 -*-
"""Clean cover illustration for the design package."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from draw_lib import *

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02_Drawings"))


def cover():
    c = Canvas(1800, 1120, WHITE)
    # left: front view
    S = 0.95
    ox, oy = 110, 1040
    W, H = 480, 940

    def X(x): return ox + x * S
    def Y(z): return oy - z * S

    # shadow
    c.ellipse((X(-20), Y(0) - 8, X(500), Y(0) + 14), fill=(238, 241, 239), outline=None)
    # body
    c.rect((X(0), Y(H), X(W), Y(0)), fill=(252, 253, 252), outline=INK, width=3)
    # layers
    c.line([(X(0), Y(900)), (X(W), Y(900))], fill=INK, width=1)
    c.line([(X(0), Y(600)), (X(W), Y(600))], fill=INK, width=1)
    c.line([(X(0), Y(520)), (X(W), Y(520))], fill=INK, width=1)
    c.line([(X(0), Y(120)), (X(W), Y(120))], fill=INK, width=1)
    # bins 2x2
    bins = [(-117, -117, BLUE_2), (117, -117, (250, 235, 190)), (-117, 117, (210, 235, 214)), (117, 117, (230, 232, 234))]
    for cx, cy, col in bins:
        # front view: only x; use 2 columns and two depth rows indicated by tone
        x1 = 240 + cx - 105
        x2 = 240 + cx + 105
        c.rect((X(x1), Y(500), X(x2), Y(140)), fill=col, outline=INK, width=1)
    # drawer front
    c.rect((X(0), Y(520), X(12), Y(130)), fill=(223, 228, 226), outline=INK, width=1)
    # hopper
    c.rect((X(60), Y(900), X(420), Y(600)), fill=(246, 248, 245), outline=INK, width=2)
    c.rect((X(80), Y(888), X(400), Y(642)), fill=(251, 251, 249), outline=LINE, width=1)
    # door
    c.rect((X(95), Y(642), X(385), Y(628)), fill=(222, 231, 226), outline=INK, width=1)
    # spout
    c.polygon([(X(185), Y(600)), (X(295), Y(600)), (X(370), Y(540)), (X(310), Y(520))],
              fill=(225, 235, 230), outline=ORANGE, width=2)
    # camera + LED
    c.rect((X(220), Y(895), X(260), Y(860)), fill=(38, 43, 48), outline=INK, width=1)
    c.ellipse((X(228), Y(874), X(252), Y(850)), fill=(15, 20, 25), outline=WHITE, width=1)
    c.ellipse((X(202), Y(892), X(278), Y(816)), fill=None, outline=YELLOW, width=4)
    # labels
    c.text((X(500), Y(860)), "CAMERA + LED", size=20, fill=BLUE, bold=True)
    c.text((X(500), Y(835)), "物件辨識", size=18, fill=MUTED)
    c.text((X(500), Y(730)), "WEIGH HOPPER", size=20, fill=GREEN, bold=True)
    c.text((X(500), Y(705)), "稱重料斗", size=18, fill=MUTED)
    c.text((X(500), Y(610)), "ROTATING SPOUT", size=20, fill=ORANGE, bold=True)
    c.text((X(500), Y(585)), "旋轉滑槽", size=18, fill=MUTED)
    c.text((X(500), Y(420)), "4 FIXED BINS", size=20, fill=GREEN, bold=True)
    c.text((X(500), Y(395)), "四個固定桶", size=18, fill=MUTED)
    # leader lines
    for y, tx, ty in ((850, X(280), Y(865)), (720, X(390), Y(720)), (600, X(350), Y(555)), (400, X(430), Y(430))):
        c.line([(X(460), y), (tx, ty)], fill=MUTED, width=1, dash=(4, 4))

    # right: stat cards
    x0 = 1180
    c.text((x0, 90), "DESIGN AT A GLANCE", size=22, fill=GREEN, bold=True)
    cards = [
        ("4", "streams", "plastic · metal · wet · other", GREEN),
        ("42.8 L", "capacity", "4 × 10.7 L usable bins", BLUE),
        ("6-9 s", "per item", "sort cycle, excluding loading", ORANGE),
        ("HK$4,050", "recommended", "lean build ≈ HK$3,200", GREEN),
    ]
    for i, (big, small, sub, col) in enumerate(cards):
        y = 140 + i * 185
        c.rect((x0, y, 1720, y + 150), fill=(248, 250, 249), outline=GREY, width=1, radius=10)
        c.text((x0 + 22, y + 16), big, size=40, fill=col, bold=True)
        c.text((x0 + 22, y + 66), small, size=18, fill=INK, bold=True)
        c.text((x0 + 22, y + 92), sub, size=13, fill=MUTED)
    # bottom pill
    c.rect((x0, 920, 1720, 980), fill=GREEN, outline=None, radius=10)
    c.text((x0 + 20, 940), "VISION + SENSORS + 4-BIN MECHANISM", size=14, fill=WHITE, bold=True)

    c.save(os.path.join(OUT, "cover_hero.png"))


if __name__ == "__main__":
    cover()
