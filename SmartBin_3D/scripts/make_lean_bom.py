# -*- coding: utf-8 -*-
"""Create a simple lean <=HK$1000 BOM workbook."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
OUT = os.path.join(BASE, "Lean_1000_BOM.xlsx")
GREEN = "1F4E45"
SOFT = "F7F9F8"
BORDER = "D9DEE3"
thin = Side(style="thin", color=BORDER)
box = Border(left=thin, right=thin, top=thin, bottom=thin)

items = [
    ("ESP32 DevKit V1", "30-pin, WiFi, USB", 1, 45, "Controller; no Raspberry Pi"),
    ("ESP32-S3-CAM", "8 MB PSRAM, 16 MB flash, OV2640, WiFi", 1, 120, "On-device MobileNetV2; no laptop"),
    ("5 kg load cell + HX711", "Single-point cell, 24-bit ADC", 1, 35, "Fixed weigh platform"),
    ("NEMA 17 stepper", "42BYGH, 0.45 Nm, 1.7 A", 1, 75, "Rotate spout; 3:1 GT2 belt"),
    ("A4988 driver", "With heatsink; 1/8 microstep", 1, 18, "Set Vref ~0.64 V"),
    ("MG996R servo", "Metal gear, 10 kg-cm", 1, 35, "Trapdoor; spring-assisted"),
    ("IR break-beam", "940 nm LED + receiver", 1, 15, "Item/hand detection at mouth"),
    ("Capacitive moisture sensor", "3.3 V analog, corrosion-resistant", 1, 15, "Wet/dry evidence on door"),
    ("OLED 0.96\" SSD1306", "I2C, 128x64", 1, 20, "Class / weight / state; no laptop"),
    ("IR obstacle sensors x4", "FC-51 or equivalent", 4, 5, "Bin-full at fixed height"),
    ("microSD 16 GB", "Class 10, SPI", 1, 15, "Logs + local dataset"),
    ("Microswitches", "Lid, home, door", 3, 3, "Interlocks / homing"),
    ("12 V 3 A adapter", "CE/BS marked, 5.5x2.1 mm", 1, 45, "NEMA17 + buck; no Li-ion"),
    ("5 V 3 A buck", "12 V -> 5 V, terminals", 1, 18, "ESP32 / servo / sensors"),
    ("Plywood / acrylic", "5-12 mm offcuts, 420x900-ish", 1, 160, "Frame and panels"),
    ("3D-printed brackets", "PETG, ~0.5 kg", 1, 45, "Spout collar, sensor mounts, hinges"),
    ("Bins x4", "Reused 5-8 L containers", 4, 9, "No notches needed; standard bins"),
    ("Hinges, handle, fasteners", "Piano hinge, M3/M4 screws, feet", 1, 60, "Assembly"),
    ("Wire, connectors, heatshrink", "Dupont/JST, 22-24 AWG", 1, 45, "Wiring"),
    ("Labels / tape", "Colour + icon + text", 1, 20, "Bin labels"),
    ("Misc / spare", "Spare servo, fuse, cable ties", 1, 15, "Contingency"),
]
wb = Workbook()
ws = wb.active
ws.title = "Lean BOM"
ws.sheet_view.showGridLines = False
ws.merge_cells("A1:F1")
c = ws["A1"]; c.value = "Lean Smart Bin — target BOM <= HK$1,000"
c.font = Font(name="Calibri", size=18, bold=True, color=GREEN)
ws.merge_cells("A2:F2")
c = ws["A2"]; c.value = "Assumes you already own a laptop for vision/AI and a phone for the web app. Laptop is NOT in this BOM."
c.font = Font(name="Calibri", size=10, italic=True, color="5A6778")

headers = ["Item", "Specification", "Qty", "Unit (HKD)", "Total (HKD)", "Note"]
for i, h in enumerate(headers, 1):
    cell = ws.cell(row=4, column=i, value=h)
    cell.fill = PatternFill("solid", fgColor=GREEN)
    cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    cell.border = box
    cell.alignment = Alignment(vertical="center", wrap_text=True)

r = 5
for name, spec, qty, unit, note in items:
    ws.cell(row=r, column=1, value=name)
    ws.cell(row=r, column=2, value=spec)
    ws.cell(row=r, column=3, value=qty)
    ws.cell(row=r, column=4, value=unit)
    ws.cell(row=r, column=5, value=f"=C{r}*D{r}")
    ws.cell(row=r, column=6, value=note)
    for c in range(1, 7):
        cell = ws.cell(row=r, column=c)
        cell.border = box
        cell.font = Font(name="Calibri", size=9.5, color="1F2937")
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        if r % 2 == 0:
            cell.fill = PatternFill("solid", fgColor=SOFT)
    ws.cell(row=r, column=3).alignment = Alignment(horizontal="center", vertical="top")
    ws.cell(row=r, column=4).number_format = '#,##0'
    ws.cell(row=r, column=5).number_format = '#,##0'
    r += 1

last = r - 1
tr = r
ws.merge_cells(start_row=tr, start_column=1, end_row=tr, end_column=4)
c = ws.cell(row=tr, column=1, value="Subtotal / 小計")
c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
c.fill = PatternFill("solid", fgColor=GREEN)
c.alignment = Alignment(horizontal="right", vertical="center")
ws.cell(row=tr, column=5, value=f"=SUM(E5:E{last})")
ws.cell(row=tr, column=5).font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
ws.cell(row=tr, column=5).fill = PatternFill("solid", fgColor=GREEN)
ws.cell(row=tr, column=5).number_format = '#,##0'
for c in range(1, 7):
    ws.cell(row=tr, column=c).border = box
ws.row_dimensions[tr].height = 22

# contingency and total
ws.cell(row=tr+2, column=1, value="Subtotal").font = Font(name="Calibri", size=10, bold=True)
ws.cell(row=tr+2, column=5, value=f"=E{tr}").number_format = '#,##0'
ws.cell(row=tr+3, column=1, value="15% contingency").font = Font(name="Calibri", size=10)
ws.cell(row=tr+3, column=5, value=f"=E{tr}*0.15").number_format = '#,##0'
ws.cell(row=tr+4, column=1, value="TOTAL (target <= 1,000)").font = Font(name="Calibri", size=11, bold=True)
ws.cell(row=tr+4, column=5, value=f"=E{tr+2}+E{tr+3}").font = Font(name="Calibri", size=11, bold=True)
ws.cell(row=tr+4, column=5).number_format = '#,##0'

ws.merge_cells(start_row=tr+6, start_column=1, end_row=tr+6, end_column=6)
c = ws.cell(row=tr+6, column=1, value="If you must buy a laptop/tablet for AI, the budget cannot stay under HK$1,000. This design explicitly assumes an owned laptop.")
c.font = Font(name="Calibri", size=9, italic=True, color="B03A3A")
c.alignment = Alignment(wrap_text=True)

for col, w in {"A": 28, "B": 42, "C": 6, "D": 12, "E": 13, "F": 48}.items():
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A5"
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
print("expected subtotal", sum(q*u for _,_,q,u,_ in items))
