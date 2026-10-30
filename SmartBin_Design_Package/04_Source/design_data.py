# -*- coding: utf-8 -*-
"""Shared data for the Smart Waste Sorting Bin design package."""

SPECS = {
    "name_en": "Smart Waste Sorting Bin",
    "name_zh": "智能分類垃圾桶",
    "version": "1.0",
    "date": "29 October 2026",
    "outer_w": 480,
    "outer_d": 480,
    "outer_h": 940,
    "bin_count": 4,
    "bin_capacity_l": 10.7,
    "total_capacity_l": 42.8,
    "max_item_kg": 1.5,
    "sort_time_s": "6-9",
    "target_accuracy": ">= 85% overall (50-item mixed test)",
    "power": "12 V 6 Ah Li-ion (BMS) or 12 V 5 A bench adapter",
    "cost_recommended_hkd": 4050,
    "cost_min_hkd": 3200,
    "cost_enhanced_hkd": 4800,
}

# BOM: id, group, item_en, item_zh, spec, qty, unit_hkd, source, note_en, note_zh, priority
BOM = [
    ("S-01", "Structure", "Plywood sheet, 18 mm", "18 mm 夾板", "1220 x 2440 mm, B/BB or marine ply", 1, 380, "Local wood shop", "Frame, drawer, lid; cut list in Appendix B", "框架、抽屜、蓋；切割表見附錄 B", "Core"),
    ("S-02", "Structure", "PP / acrylic sheet, 3 mm", "3 mm PP／亞克力板", "600 x 400 mm, food-contact PP preferred", 4, 45, "Local plastics shop / Taobao", "Hopper liner, spout guard, drip shields", "料斗內襯、滑槽護板、滴水擋板", "Core"),
    ("S-03", "Structure", "Piano hinge, 500 mm", "鋼琴鉸鏈 500 mm", "Stainless steel, 32 mm open width", 2, 25, "Hardware shop", "Lid and hopper door", "蓋與料斗門", "Core"),
    ("S-04", "Structure", "Drawer slides, 450 mm", "抽屜滑軌 450 mm", "3-fold, 45 kg rated, pair", 2, 60, "Hardware shop", "One pair for the bin drawer", "垃圾桶抽屜一對", "Core"),
    ("S-05", "Structure", "Gas strut, 60 N", "氣壓撐桿 60 N", "250 mm extended, 10 mm ball ends", 2, 40, "Hardware shop", "Lid assist and stay", "協助開蓋及定位", "Core"),
    ("S-06", "Structure", "Rubber feet", "橡膠腳墊", "30 mm diameter, M6 thread", 4, 5, "Hardware shop", "Vibration and floor protection", "減震及保護地板", "Core"),
    ("S-07", "Structure", "Fixings assortment", "緊固件組合", "M4/M5 bolts, nuts, washers, inserts, angle brackets", 1, 150, "Hardware shop", "Allow 20% spare", "預留 20% 備用", "Core"),
    ("S-08", "Structure", "Silicone seal strip", "矽膠密封條", "10 x 3 mm, self-adhesive, 3 m", 1, 30, "Hardware shop", "Hopper door and lid gasket", "料斗門及蓋密封", "Core"),
    ("S-09", "Structure", "Storage bins, 12 L", "12 L 收納箱", "Approx. 190 x 190 x 360 mm, PP, 4 pcs", 4, 40, "Japan Home / Taobao", "Cut an 80 x 80 mm inner-corner notch", "內角切 80 x 80 mm 缺口", "Core"),
    ("S-10", "Structure", "PETG filament", "PETG 線材", "1.75 mm, 1 kg, black", 1, 120, "3D printing shop", "Camera bracket, sensor mounts, spout collar", "鏡頭支架、感測器座、滑槽環", "Core"),
    ("S-11", "Structure", "Adhesive and sealant", "膠水及密封膠", "Epoxy, acrylic cement, neutral silicone", 1, 60, "Hardware shop", "Do not use silicone on load cells", "負重感測器附近勿用矽膠", "Core"),
    ("S-12", "Structure", "Matte black paint", "啞黑噴漆", "400 ml, low sheen", 1, 45, "Hardware shop", "Inside hopper to reduce glare", "料斗內部減少反光", "Core"),

    ("M-01", "Motion", "NEMA 17 stepper motor", "NEMA 17 步進馬達", "42BYGH40, 1.7 A, 0.45 N·m, 1.8 deg", 1, 85, "Taobao / Robot shop", "Drives rotating spout through 3:1 GT2 belt", "經 3:1 GT2 皮帶驅動旋轉滑槽", "Core"),
    ("M-02", "Motion", "Stepper driver A4988", "A4988 步進驅動", "With heatsink; 1/8 microstep", 1, 20, "Taobao", "Set Vref to 0.64 V for 0.8 A", "Vref 調至 0.64 V（0.8 A）", "Core"),
    ("M-03", "Motion", "GT2 pulley set", "GT2 皮帶輪組", "20T motor, 60T shaft, 200 mm belt", 1, 55, "Taobao", "3:1 reduction; printed hub acceptable", "3:1 減速；可用打印輪轂", "Core"),
    ("M-04", "Motion", "Lazy Susan bearing", "轉盤軸承", "150 mm OD, 5 mm thick", 1, 30, "Hardware shop", "Spout collar bearing", "滑槽環軸承", "Core"),
    ("M-05", "Motion", "Ball bearings 608ZZ", "608ZZ 軸承", "8 x 22 x 7 mm", 4, 5, "Hardware shop", "Spout guide rollers", "滑槽導輪", "Core"),
    ("M-06", "Motion", "Metal-gear servo, 25 kg·cm", "金屬齒輪伺服 25 kg·cm", "DS3225MG or equivalent, 6.8 V", 1, 95, "Taobao / RC shop", "Hopper door; spring-assisted; max 1.5 kg item", "料斗門；彈簧輔助；物件上限 1.5 kg", "Core"),
    ("M-07", "Motion", "Servo horn, spring and cable set", "伺服舵角、彈簧及拉線", "Aluminium horn, 0.8 x 20 x 80 mm spring, 1 mm cable", 1, 35, "Hardware shop", "Spring closes door on power loss", "斷電時彈簧關門", "Core"),
    ("M-08", "Motion", "PVC elbow 110 mm, 45 deg", "110 mm PVC 45 度彎頭", "DWV or pressure pipe, outlet 110 mm", 1, 40, "Plumbing shop", "Rotating spout; cut and sand smooth", "旋轉滑槽；切磨光滑", "Core"),
    ("M-09", "Motion", "Funnel sheet / printed funnel", "漏斗板材／打印漏斗", "PP sheet or PETG print; inlet 280 x 260, outlet 110 mm", 1, 60, "Local plastics / 3D print", "60 deg walls; smooth joints", "60 度壁；接縫平滑", "Core"),
    ("M-10", "Motion", "Micro switches", "微動開關", "SPDT, 5 A, lever", 3, 10, "Taobao", "Home, door closed, drawer closed", "原點、門關、抽屜關", "Core"),
    ("M-11", "Motion", "Vibration motor, 12 V", "12 V 震動馬達", "10 mm coin, 3-5 V or 12 V via driver", 1, 20, "Taobao", "Optional anti-jam on funnel", "可選：漏斗防卡", "Optional"),

    ("E-01", "Sensing", "USB camera, 5 MP", "USB 鏡頭 5 MP", "UVC, 90 deg diagonal FOV, manual focus, 1 m cable", 1, 120, "Taobao / computer shop", "1280 x 720 capture; fixed exposure", "1280 x 720 擷取；固定曝光", "Core"),
    ("E-02", "Sensing", "Raspberry Pi Zero 2 W", "Raspberry Pi Zero 2 W", "Quad-core Cortex-A53, 512 MB RAM", 1, 180, "HK Raspberry Pi reseller", "Vision, web app, database, cloud sync", "視覺、網頁應用、資料庫、雲端同步", "Core"),
    ("E-03", "Sensing", "microSD card, 32 GB", "microSD 卡 32 GB", "Class 10 / A1", 1, 60, "Computer shop", "Use a branded card; back up image", "使用品牌卡；備份映像", "Core"),
    ("E-04", "Sensing", "ESP32 DevKit V1", "ESP32 DevKit V1", "30-pin, ESP32-WROOM-32, USB", 1, 45, "Taobao", "Real-time sensor and motion controller", "實時感測與運動控制", "Core"),
    ("E-05", "Sensing", "Load cell set, 5 kg", "5 kg 負重感測器組", "4 x half-bridge 5 kg + combinator + HX711", 1, 100, "Taobao", "Weigh hopper; 20 kg total capacity", "稱重料斗；總容量 20 kg", "Core"),
    ("E-06", "Sensing", "VL53L0X ToF sensor", "VL53L0X 飛時測距", "I2C, up to 2 m, item presence", 1, 30, "Taobao", "Lid-mounted, looks down at hopper", "裝於蓋，向下看料斗", "Core"),
    ("E-07", "Sensing", "VL53L1X ToF sensor", "VL53L1X 飛時測距", "I2C, up to 4 m, 4 pcs for bin levels", 4, 50, "Taobao", "Better than ultrasonic in narrow bins", "窄桶內比超聲波可靠", "Core"),
    ("E-08", "Sensing", "IR break-beam set", "紅外對射組", "940 nm LED + TSOP38238 receiver, 38 kHz", 1, 25, "Taobao", "Hand/object safety beam across hopper mouth", "料斗口安全光束", "Core"),
    ("E-09", "Sensing", "SHT31 temperature/humidity", "SHT31 溫濕度", "I2C, +/-2% RH", 1, 50, "Taobao", "Bin environment log (optional for sorting)", "桶內環境記錄（分類非必需）", "Optional"),
    ("E-10", "Sensing", "Capacitive moisture sensor", "電容式濕度感測", "Corrosion-resistant PCB, analog", 1, 30, "Taobao", "Under 1.5 mm HDPE cover on hopper door", "料斗門 1.5 mm HDPE 蓋下", "Core"),
    ("E-11", "Sensing", "DIY metal detector kit", "DIY 金屬探測套件", "3-5 V kit, 60 mm coil; add 150 mm custom coil", 1, 40, "Taobao", "Confirmation only; tune away from frame", "僅作確認；遠離金屬框調校", "Optional"),
    ("E-12", "Sensing", "PCF8574 I2C expander", "PCF8574 I2C 擴展", "8-bit, address 0x20", 1, 15, "Taobao", "Lid, door, drawer, home and bin-present switches", "蓋、門、抽屜、原點及桶在位開關", "Core"),
    ("E-13", "Sensing", "Reed switch and magnet set", "磁簧開關及磁鐵組", "NC/NO, 4 sets", 1, 30, "Taobao", "Bin-present detection without drawer wiring", "免抽屜布线偵測桶在位", "Core"),
    ("E-14", "Sensing", "Push button, e-stop, power switch", "按鈕、急停、電源開關", "22 mm, 1 NO/1 NC, 10 A", 1, 70, "Hardware shop", "Front panel; e-stop cuts actuator 12 V", "前面板；急停切斷執行器 12 V", "Core"),
    ("E-15", "Sensing", "WS2812B LED bar, 8 LEDs", "WS2812B 燈條 8 粒", "5 V, IP30, diffused", 1, 25, "Taobao", "Status indication; no screen needed", "狀態指示；無需螢幕", "Core"),
    ("E-16", "Sensing", "Piezo buzzer", "蜂鳴器", "3.3-5 V active", 1, 10, "Taobao", "Audible fault/sort confirmation", "錯誤／完成提示音", "Core"),

    ("P-01", "Power", "12 V 6 Ah Li-ion pack with BMS", "12 V 6 Ah 鋰電池組（含 BMS）", "3S2P 18650, certified assembly, 12.6 V charger", 1, 350, "Battery specialist", "Preferred: factory-assembled pack; never build unsupervised", "首選：工廠組裝；切勿無人監督自行組裝", "Core"),
    ("P-02", "Power", "12 V 5 A bench adapter", "12 V 5 A 桌面電源", "5.5 x 2.1 mm plug, CE/BS marked", 1, 80, "Computer shop", "Use for development and long tests", "開發及長時間測試用", "Core"),
    ("P-03", "Power", "Buck converter 12 V -> 5 V 5 A", "降壓模組 12 V -> 5 V 5 A", "XL4015 or similar, heatsink", 1, 45, "Taobao", "Raspberry Pi and USB hub", "Raspberry Pi 及 USB hub", "Core"),
    ("P-04", "Power", "Buck converter 12 V -> 6 V 5 A", "降壓模組 12 V -> 6 V 5 A", "XL4015 or similar, heatsink", 1, 40, "Taobao", "Servo only; 1000 uF near servo", "只供伺服；伺服旁 1000 uF", "Core"),
    ("P-05", "Power", "Buck converter 12 V -> 5 V 3 A", "降壓模組 12 V -> 5 V 3 A", "LM2596 or similar", 1, 25, "Taobao", "ESP32, sensors, LED bar", "ESP32、感測器、燈條", "Core"),
    ("P-06", "Power", "Fuse holder and 5 A fuses", "保險絲座及 5 A 保險絲", "Blade type, inline", 1, 25, "Hardware shop", "Within 150 mm of battery positive", "電池正極 150 mm 內", "Core"),
    ("P-07", "Power", "Power distribution board", "電源分配板", "Screw terminals, busbars", 1, 50, "Taobao", "Star ground point", "星形接地點", "Core"),
    ("P-08", "Power", "12 V relay module", "12 V 繼電器模組", "30 A automotive relay, 5 V coil", 1, 25, "Taobao", "Actuator bus controlled by e-stop/ESP32", "急停／ESP32 控制執行器電源", "Core"),
    ("P-09", "Power", "DC jacks, switch, wiring", "DC 插座、開關、線材", "18 AWG silicone wire, 2 m red/black", 1, 60, "Hardware shop", "Current-rated; ferrules on stranded wire", "額定電流；絞線用端子", "Core"),

    ("A-01", "Assembly", "Perfboard / interface PCB", "洞洞板／介面板", "100 x 150 mm, 2.54 mm pitch", 2, 20, "Electronics shop", "HX711, headers, terminal blocks", "HX711、排針、接線端子", "Core"),
    ("A-02", "Assembly", "Connectors and ferrules", "連接器及端子", "JST-XH, Dupont, WAGO, ferrules", 1, 90, "Taobao", "Label every cable at both ends", "每條線兩端貼標籤", "Core"),
    ("A-03", "Assembly", "Shielded load-cell cable", "屏蔽負重線", "4-core shielded, 1 m", 1, 30, "Taobao", "Shield grounded at HX711 end only", "屏蔽僅在 HX711 端接地", "Core"),
    ("A-04", "Assembly", "Cable glands and spiral wrap", "電纜防水頭及捲線管", "PG7/PG9, 2 m wrap", 1, 50, "Hardware shop", "Separate mains/battery from signal", "電源與訊號分開", "Core"),
    ("A-05", "Assembly", "Heat-shrink and sleeving", "熱縮管及套管", "Assorted", 1, 30, "Electronics shop", "Strain relief and insulation", "應力消除及絕緣", "Core"),
    ("A-06", "Assembly", "Fan, 40 mm 5 V", "5 V 40 mm 風扇", "With filter", 1, 30, "Computer shop", "Electronics bay ventilation", "電子倉通風", "Core"),
    ("A-07", "Assembly", "Acrylic mounting plate", "亞克力安裝板", "3 mm, 300 x 200 mm", 1, 30, "Plastics shop", "Electronics layout", "電子零件排列", "Core"),
    ("A-08", "Assembly", "Labels and signage", "標籤及標示", "Bilingual bin labels, safety labels, QR code", 1, 45, "Print shop", "Colour + icon + text (accessibility)", "顏色＋圖示＋文字（易讀）", "Core"),
    ("A-09", "Assembly", "Velcro, tape, cable clips", "魔術貼、膠帶、線夾", "Assorted", 1, 50, "Hardware shop", "Serviceable mounting", "可維修安裝", "Core"),
    ("A-10", "Assembly", "Bin liners / cleaning kit", "垃圾桶袋／清潔組", "Compostable liners, wipes, gloves", 1, 40, "Supermarket", "Hygiene and demo readiness", "衛生及演示準備", "Core"),
]

TOOLS = [
    ("T-01", "Soldering iron + stand + solder", "烙鐵＋架＋焊錫", 1, 180),
    ("T-02", "Digital multimeter", "數位萬用表", 1, 150),
    ("T-03", "Wire strippers / crimping tool", "剝線鉗／壓線鉗", 1, 120),
    ("T-04", "Electric drill + bits + hole saw", "電鑽＋鑽頭＋孔鋸", 1, 350),
    ("T-05", "Jigsaw or circular saw", "曲線鋸或圓鋸", 1, 300),
    ("T-06", "Screwdriver and hex key set", "螺絲批及內六角套裝", 1, 120),
    ("T-07", "Digital calipers", "數位卡尺", 1, 80),
    ("T-08", "Hot glue gun", "熱熔膠槍", 1, 80),
    ("T-09", "Safety glasses and gloves", "護目鏡及手套", 1, 60),
    ("T-10", "Li-ion fire bag", "鋰電池防火袋", 1, 80),
]

PIN_MAP = [
    ("I2C SDA", "GPIO21", "Bidirectional", "SHT31, VL53L0X, 4 x VL53L1X, PCF8574", "4.7 k pull-up to 3.3 V; assign ToF addresses with XSHUT"),
    ("I2C SCL", "GPIO22", "Bidirectional", "Same I2C bus", "Keep leads < 500 mm; twisted pair"),
    ("HX711 DOUT", "GPIO32", "Input", "HX711", "10 Hz or 80 Hz; shielded cable"),
    ("HX711 SCK", "GPIO33", "Output", "HX711", "Keep away from stepper wires"),
    ("Stepper STEP", "GPIO25", "Output", "A4988 STEP", "1/8 microstep; 1200 steps per 90 deg"),
    ("Stepper DIR", "GPIO26", "Output", "A4988 DIR", "Direction; always approach target clockwise"),
    ("Stepper EN", "GPIO27", "Output", "A4988 EN", "Active low; disable when idle to reduce heat"),
    ("Hopper servo", "GPIO13", "PWM 50 Hz", "DS3225MG signal", "6 V supply; common ground; 1000 uF"),
    ("IR receiver", "GPIO35", "Input only", "TSOP38238 OUT", "External 10 k pull-up; 100 nF decoupling"),
    ("E-stop status", "GPIO34", "Input only", "Optocoupler / divider", "External 10 k pull-up; low = pressed"),
    ("Front button", "GPIO39", "Input only", "Push button to GND", "External 10 k pull-up; debounce 30 ms"),
    ("WS2812 data", "GPIO2", "Output", "LED bar DIN", "330 ohm series; 5 V supply; level 3.3 V works"),
    ("Buzzer", "GPIO14", "Output", "Active buzzer", "NPN transistor if > 20 mA"),
    ("Item ToF XSHUT", "GPIO4", "Output", "VL53L0X XSHUT", "Pull low to reset; release after boot"),
    ("Bin 1 ToF XSHUT", "GPIO16", "Output", "VL53L1X #1", "Assign address 0x30"),
    ("Bin 2 ToF XSHUT", "GPIO17", "Output", "VL53L1X #2", "Assign address 0x31"),
    ("Bin 3 ToF XSHUT", "GPIO18", "Output", "VL53L1X #3", "Assign address 0x32"),
    ("Bin 4 ToF XSHUT", "GPIO19", "Output", "VL53L1X #4", "Assign address 0x33"),
    ("PCF8574 INT", "GPIO23", "Input", "PCF8574 INT", "Optional; polling is acceptable"),
    ("Spare / fan", "GPIO12", "Output", "Fan MOSFET", "Avoid strapping conflict; fan on during sorting"),
]

CUT_LIST = [
    ("C-01", "Base panel", "18 mm plywood", "480 x 480", 1, "Electronics bay floor; 20 mm feet"),
    ("C-02", "Base front/back", "18 mm plywood", "480 x 100", 2, "Electronics bay; vent holes"),
    ("C-03", "Base sides", "18 mm plywood", "444 x 100", 2, "Between front and back"),
    ("C-04", "Bin section sides", "18 mm plywood", "480 x 400", 2, "Left/right; drawer opening"),
    ("C-05", "Bin section back", "18 mm plywood", "444 x 400", 1, "Fixed back"),
    ("C-06", "Bin section top/bottom", "18 mm plywood", "480 x 480", 2, "Mid-frame and bin top"),
    ("C-07", "Drawer bottom", "18 mm plywood", "456 x 456", 1, "4 bin pockets; 6 mm clearance"),
    ("C-08", "Drawer sides", "18 mm plywood", "456 x 360", 2, "Bin retaining walls"),
    ("C-09", "Drawer front", "18 mm plywood", "480 x 400", 1, "Handle and latch"),
    ("C-10", "Hopper sides", "18 mm plywood", "360 x 300", 2, "Support frame; PP liner inside"),
    ("C-11", "Hopper front/back", "18 mm plywood", "324 x 300", 2, "Front has door opening"),
    ("C-12", "Hopper support plate", "18 mm plywood", "360 x 360", 1, "Rests on 4 load cells; 180 mm center hole"),
    ("C-13", "Hopper door", "6 mm PP/plywood", "280 x 240", 1, "Silicone gasket; hinge at back"),
    ("C-14", "Lid", "18 mm plywood + 3 mm acrylic", "480 x 480", 1, "Camera hole 30 mm; LED ring recess"),
    ("C-15", "Mid-frame", "18 mm plywood", "480 x 480", 1, "Load cells and spout bearing; 200 mm center hole"),
    ("C-16", "Funnel walls", "3 mm PP", "4 pieces, 280 x 150", 4, "60 deg; outlet 110 mm"),
    ("C-17", "Spout guard", "3 mm PP", "300 x 200", 1, "Clear guard around rotating spout"),
    ("C-18", "Drip tray", "3 mm PP", "456 x 456", 1, "Removable; 20 mm lip"),
]

if __name__ == "__main__":
    total = sum(q * u for _, _, _, _, _, q, u, _, _, _, _ in BOM)
    core = sum(q * u for *_, q, u, _, _, _, p in BOM if p == "Core")
    optional = total - core
    print("BOM lines:", len(BOM))
    print("Total HKD:", total)
    print("Core HKD:", core, "Optional HKD:", optional)
    print("Tools HKD:", sum(q * u for _, _, _, q, u in TOOLS))
