# -*- coding: utf-8 -*-
"""Small PIL drawing library for the design package diagrams."""
from PIL import Image, ImageDraw, ImageFont
import math, os, re

FONT_DIR = r"C:\Windows\Fonts"
F_EN = os.path.join(FONT_DIR, "segoeui.ttf")
F_EN_B = os.path.join(FONT_DIR, "segoeuib.ttf")
F_EN_SB = os.path.join(FONT_DIR, "seguisb.ttf")
F_ZH = os.path.join(FONT_DIR, "msjh.ttc")
F_ZH_B = os.path.join(FONT_DIR, "msjhbd.ttc")
F_MONO = os.path.join(FONT_DIR, "consola.ttf")
F_MONO_B = os.path.join(FONT_DIR, "consolab.ttf")

# Palette
INK = (31, 41, 55)
MUTED = (90, 103, 120)
LINE = (120, 132, 148)
PAPER = (255, 255, 255)
SOFT = (244, 247, 246)
GREEN = (31, 78, 69)
GREEN_2 = (64, 121, 105)
LIME = (163, 201, 74)
LIME_2 = (216, 232, 177)
ORANGE = (217, 130, 43)
BLUE = (46, 111, 158)
BLUE_2 = (214, 232, 244)
RED = (176, 58, 58)
YELLOW = (245, 196, 74)
GREY = (225, 229, 232)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def font(size, zh=False, bold=False, mono=False):
    if mono:
        return ImageFont.truetype(F_MONO_B if bold else F_MONO, size)
    if zh:
        return ImageFont.truetype(F_ZH_B if bold else F_ZH, size)
    return ImageFont.truetype(F_EN_B if bold else (F_EN_SB if False else F_EN), size)


class Canvas:
    def __init__(self, w, h, bg=PAPER, s=2):
        self.w, self.h, self.s = w, h, s
        self.img = Image.new("RGB", (w * s, h * s), bg)
        self.d = ImageDraw.Draw(self.img)
        self.bg = bg

    def _xy(self, xy):
        if isinstance(xy[0], (list, tuple)):
            return [tuple(int(v * self.s) for v in p) for p in xy]
        return tuple(int(v * self.s) for v in xy)

    def text(self, xy, txt, size=28, fill=INK, zh=False, bold=False, anchor="la", align="left", mono=False, stroke=0, stroke_fill=None):
        if not zh and re.search(r"[\u3400-\u9fff]", str(txt)):
            zh = True
        f = font(int(size * self.s), zh=zh, bold=bold, mono=mono)
        self.d.multiline_text(self._xy(xy), txt, font=f, fill=fill, anchor=anchor, align=align,
                              spacing=int(size * 0.25 * self.s), stroke_width=int(stroke * self.s),
                              stroke_fill=stroke_fill)

    def textbox(self, xy, txt, size=26, fill=INK, zh=False, bold=False, anchor="la", align="left", maxw=None, line_gap=1.25):
        """Draw wrapped text, return bottom y."""
        f = font(int(size * self.s), zh=zh, bold=bold)
        maxw_px = int(maxw * self.s) if maxw else None
        words = txt.split(" ")
        lines, cur = [], ""
        for word in words:
            test = (cur + " " + word).strip()
            if maxw_px and self.d.textlength(test, font=f) > maxw_px and cur:
                lines.append(cur)
                cur = word
            else:
                cur = test
        if cur:
            lines.append(cur)
        # For Chinese text without spaces, split by character if needed.
        if maxw_px and len(lines) == 1 and self.d.textlength(lines[0], font=f) > maxw_px:
            chars, lines, cur = list(lines[0]), [], ""
            for ch in chars:
                if self.d.textlength(cur + ch, font=f) > maxw_px and cur:
                    lines.append(cur)
                    cur = ch
                else:
                    cur += ch
            if cur:
                lines.append(cur)
        y = xy[1]
        for line in lines:
            self.text((xy[0], y), line, size=size, fill=fill, zh=zh, bold=bold, anchor=anchor, align=align)
            y += size * line_gap
        return y

    def rect(self, xy, fill=None, outline=LINE, width=2, radius=0):
        xy = self._xy(xy)
        if radius:
            self.d.rounded_rectangle(xy, radius=int(radius * self.s), fill=fill, outline=outline, width=int(width * self.s))
        else:
            self.d.rectangle(xy, fill=fill, outline=outline, width=int(width * self.s))

    def ellipse(self, xy, fill=None, outline=LINE, width=2):
        self.d.ellipse(self._xy(xy), fill=fill, outline=outline, width=int(width * self.s))

    def polygon(self, xy, fill=None, outline=LINE, width=2):
        self.d.polygon(self._xy(xy), fill=fill, outline=outline, width=int(width * self.s))

    def arc(self, xy, start, end, fill=LINE, width=2):
        self.d.arc(self._xy(xy), start=start, end=end, fill=fill, width=int(width * self.s))

    def line(self, xy, fill=LINE, width=2, dash=None):
        pts = self._xy(xy)
        if dash:
            # simple dashed line
            total = 0
            segs = []
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]; x2, y2 = pts[i + 1]
                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)
                n = max(1, int(dist / (dash[0] + dash[1])))
                for j in range(n):
                    t0 = j * (dash[0] + dash[1]) / dist
                    t1 = min(1, (j * (dash[0] + dash[1]) + dash[0]) / dist)
                    segs.append(((x1 + dx * t0, y1 + dy * t0), (x1 + dx * t1, y1 + dy * t1)))
            for a, b in segs:
                self.d.line([a, b], fill=fill, width=int(width * self.s))
        else:
            self.d.line(pts, fill=fill, width=int(width * self.s), joint="curve")

    def arrow(self, xy1, xy2, fill=INK, width=3, head=12, dash=None):
        x1, y1 = xy1; x2, y2 = xy2
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(ang) * 0.9, y2 - head * math.sin(ang) * 0.9
        self.line([(x1, y1), (bx, by)], fill=fill, width=width, dash=dash)
        p1 = (x2, y2)
        p2 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
        p3 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
        self.d.polygon(self._xy([p1, p2, p3]), fill=fill)

    def hatch(self, xy, fill=GREY, outline=LINE, step=12, angle=45):
        x1, y1, x2, y2 = xy
        self.rect(xy, fill=fill, outline=outline, width=1)
        # diagonal hatch lines clipped by rectangle
        diag = (x2 - x1) + (y2 - y1)
        for k in range(-int((y2 - y1) / step), int((x2 - x1) / step) + 1):
            # line y = x + c in local coords
            c = k * step
            # find intersections
            pts = []
            for x in (x1, x2):
                y = y1 + (x - x1) + c
                if y1 <= y <= y2:
                    pts.append((x, y))
            for y in (y1, y2):
                x = x1 + (y - y1) - c
                if x1 <= x <= x2:
                    pts.append((x, y))
            if len(pts) >= 2:
                self.line(pts[:2], fill=outline, width=1)

    def save(self, path, dpi=(300, 300)):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        out.save(path, "PNG", dpi=dpi, optimize=True)
        print("saved", path, out.size)


def dim_h(c, x1, x2, y, label, offset=0, color=BLUE, size=22):
    c.line([(x1, y + offset), (x1, y + offset + 8)], fill=color, width=1)
    c.line([(x2, y + offset), (x2, y + offset + 8)], fill=color, width=1)
    c.arrow((x1, y + offset + 4), (x2, y + offset + 4), fill=color, width=1, head=7)
    c.arrow((x2, y + offset + 4), (x1, y + offset + 4), fill=color, width=1, head=7)
    c.text(((x1 + x2) / 2, y + offset - 6), label, size=size, fill=color, anchor="mb", bold=True)


def dim_v(c, y1, y2, x, label, offset=0, color=BLUE, size=22):
    c.line([(x + offset, y1), (x + offset + 8, y1)], fill=color, width=1)
    c.line([(x + offset, y2), (x + offset + 8, y2)], fill=color, width=1)
    c.arrow((x + offset + 4, y1), (x + offset + 4, y2), fill=color, width=1, head=7)
    c.arrow((x + offset + 4, y2), (x + offset + 4, y1), fill=color, width=1, head=7)
    c.text((x + offset - 6, (y1 + y2) / 2), label, size=size, fill=color, anchor="rm", bold=True)


def callout(c, num, x, y, tx, ty, color=ORANGE, r=16, size=22, side="left"):
    c.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=WHITE, width=2)
    c.text((x, y), str(num), size=size, fill=WHITE, anchor="mm", bold=True)
    c.line([(x, y), (tx, ty)], fill=color, width=2)
    c.ellipse((tx - 4, ty - 4, tx + 4, ty + 4), fill=color, outline=None)


def iso_box(c, x, y, w, d, h, fill, outline=LINE, top=None, side=None, alpha=255):
    """Simple isometric box: x,y is front-bottom-left; w along +x, d along +y (screen right/up), h up."""
    dx, dy = 0.55 * d, -0.32 * d
    # front face
    p_front = [(x, y), (x + w, y), (x + w, y - h), (x, y - h)]
    # top face
    p_top = [(x, y - h), (x + w, y - h), (x + w + dx, y - h + dy), (x + dx, y - h + dy)]
    # right face
    p_right = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y - h + dy), (x + w, y - h)]
    c.d.polygon(c._xy(p_front), fill=fill, outline=outline)
    c.d.polygon(c._xy(p_right), fill=side or tuple(max(0, int(v * 0.82)) for v in fill), outline=outline)
    c.d.polygon(c._xy(p_top), fill=top or tuple(min(255, int(v * 1.08)) for v in fill), outline=outline)


def badge(c, x, y, txt, fill=GREEN, fg=WHITE, size=18, pad=10):
    f = font(int(size * c.s), bold=True)
    tw = c.d.textlength(txt, font=f) / c.s
    c.rect((x, y, x + tw + 2 * pad, y + size + 2 * pad * 0.7), fill=fill, outline=None, radius=6)
    c.text((x + pad, y + pad * 0.55), txt, size=size, fill=fg, bold=True)
