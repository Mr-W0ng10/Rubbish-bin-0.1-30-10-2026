# 智能分類垃圾桶 — 完整設計包

> **2026-10-30 更新：** 你之後要求 **standalone、BOM ≤ HK$1,000、ESP32-S3-CAM＋MobileNetV2**。本資料夾的 `01_Documents` 主 PDF（EN／ZH）與 `02_Drawings/SmartBin_Drawings_A3.pdf` 已換成 **v2（9 頁＋4 頁 A3）**；舊 50／56 頁 HK$4,050 版已移到 `_archive_v1_HK4050`。最新說明看 [`../SmartBin_3D/README_3D.md`](../SmartBin_3D/README_3D.md)。

**Smart Waste Sorting Bin — Engineering Design Package v1.0**  
2026 年 10 月 29 日 · 繁體中文＋English

---

## 先看哪一個？

| 你想做什麼 | 打開這個 |
|---|---|
| 看完整中文設計（建議先看） | [智能分類垃圾桶_設計方案_ZH-Hant.pdf](01_Documents/智能分類垃圾桶_設計方案_ZH-Hant.pdf) |
| 看完整英文設計（給老師／報告用） | [Smart_Waste_Sorting_Bin_Design_EN.pdf](01_Documents/Smart_Waste_Sorting_Bin_Design_EN.pdf) |
| 買零件、看價格 | [Smart_Waste_Sorting_Bin_BOM.xlsx](03_Spreadsheets/Smart_Waste_Sorting_Bin_BOM.xlsx) |
| 印 A3 圖紙 | [SmartBin_Drawings_A3.pdf](02_Drawings/SmartBin_Drawings_A3.pdf) |
| 改 Word 文件 | [中文 DOCX](01_Documents/智能分類垃圾桶_設計方案_ZH-Hant.docx) · [English DOCX](01_Documents/Smart_Waste_Sorting_Bin_Design_EN.docx) |
| 看個別圖 | [02_Drawings](02_Drawings) 內的 PNG |

> 圖是 A4 概覽；需要讀尺寸時，打開 `02_Drawings` 的 PNG 或印 A3。文字表格才是施工的權威資料。

---

## 設計一句話

> 上方投放、有蓋；一件垃圾落在彈簧關閉的稱重料斗活門上，量重量並拍照；Pi 上的 MobileNetV2 配合濕度、金屬、重量證據，選擇四類之一；110 mm 滑槽轉到對應的固定桶；物件經漏斗落下；手機 App 記錄。

**四類：** 膠樽（藍）、金屬（黃）、濕垃圾（綠）、乾／其他（灰）。

---

## 關鍵數字

| 項目 | 數值 |
|---|---|
| 整體尺寸 | 480 闊 × 480 深 × 940 高 mm |
| 投放高度 | 約 900 mm |
| 空機重量 | 約 22–26 kg |
| 桶 | 4 × 190 × 190 × 360 mm 內部；每桶約 10.7 L |
| 總容量 | 約 42.8 L |
| 最大物件 | 長 250 mm × 直徑 110 mm × 1.5 kg |
| 分類時間 | 一般 6–9 秒；目標 ≤10 秒 |
| 目標準確率 | 50 件混合測試整體 ≥85% |
| 電源 | 12 V 6 Ah 鋰電（BMS）或 12 V 5 A 適配器 |
| 建議成本 | 約 HK$4,050；精簡約 HK$3,200；增強約 HK$4,800 |

---

## 為何選「固定四桶＋旋轉滑槽」，不是轉下面的桶？

- 轉 2 × 2 四桶連垃圾要 10–15 kg，需要大軸承、高扭矩馬達、至少 650–700 mm 圓形外殼；480 mm 方形托盤的對角線已 679 mm，放不進 480 mm 外殼。
- 固定桶只轉一個 0.35 kg 滑槽，扭矩小、外殼緊湊、抽屜簡單、垃圾不會在旋轉時灑出。
- 代價：桶的內角要切 80 × 80 mm 缺口，讓 150 mm 軸承和漏斗通過。這是簡單的 PP 板／塑膠桶加工。

---

## 你現在先買什麼（首 10 項）

1. Raspberry Pi Zero 2 W ×1（最好 2 塊）
2. 5 MP USB UVC 鏡頭（90° 對角視角、手動對焦）
3. ESP32 DevKit V1 ×1
4. NEMA 17 步進馬達（0.45 N·m）＋ A4988
5. 25 kg·cm 金屬齒輪伺服（DS3225MG 或同級）
6. 4 × 5 kg 負重感測器＋ HX711 集線板（買 6 個配對）
7. VL53L1X ToF ×4（滿度）＋ VL53L0X ×1（物件）
8. 12 V 6 Ah 鋰電（BMS）＋ 12.6 V 充電器；或先買 12 V 5 A 適配器
9. 18 mm 夾板、3 mm PP 板、抽屜滑軌 450 mm 45 kg、鋼琴鉸
10. 110 mm PVC 45° 彎頭、150 mm 懶人轉盤軸承、GT2 20T/60T 皮帶組

**不要先買：** 螢幕、壓縮機、UV-C、訂製齒輪、廉價裸 18650 電池。

---

## 製作順序（先做機構，後做 AI）

1. 切夾板、做底座和電子倉。
2. 裝抽屜滑軌、抽屜、四個桶（切 80 × 80 mm 缺口）。
3. 做中框：負重感測器、漏斗、軸承、滑槽。
4. 做料斗：活門、鉸鏈、矽膠密封、伺服、彈簧、濕度墊、金屬線圈。
5. 裝蓋：鏡頭、LED 環、物件 ToF、磁簧。
6. 在實驗室逐個測試感測器和執行器。
7. 接 ESP32、Pi、電源；燒錄韌體；測試序列協定。
8. 校正負重、濕度、金屬、桶滿度、鏡頭曝光、滑槽原點。
9. 收集資料集、訓練 MobileNetV2、部署 TFLite。
10. 整合全自動分類；50 件測試；拍片；寫報告。

**不要**一開始就做 AI；先讓機構和感測器可靠。

---

## 你需要自己核對的地方

- 你買到的桶內尺寸（190 × 190 mm 是名義值）。
- 鏡頭實際視角；用格紙在 228 mm 高度測試。
- 負重感測器靈敏度；四點校正。
- 金屬線圈在實際框架附近的漂移；必要時省略，只用視覺＋重量。
- 電池認證與充電器相容性。
- 所有價格（2026 年 10 月參考價）。

---

## 安全（必讀）

- 12 V SELV；電池正極 150 mm 內加 5 A 保險絲；總開關；急停。
- 用有 BMS 的認證鋰電池組；在外殼外充電；防火袋；不無人看管。
- 蓋、抽屜、活門未關，執行器不動作。
- 不要放入尖銳、高溫、醫療、液體垃圾。
- 這是室內示範原型，不是認證家電。

---

## 對 FYP 的下一步

1. 用第 1–3 章做開題簡報（問題、目標、方案比較、可行性）。
2. 用第 7 章和 BOM 做資源分配與預算。
3. 用第 8 章的時間表做 24 週計劃。
4. 先做框架和抽屜，兩週內有實物照片，對 progress review 很重要。
5. 測試數據比模型分數重要：50 件、混淆矩陣、時間、卡料率、成本。

---

## 檔案結構

```text
SmartBin_Design_Package/
  01_Documents/      EN/ZH DOCX + PDF
  02_Drawings/       PNG figures + A3 drawings PDF
  03_Spreadsheets/   BOM / budget / tools / pins / cut list / schedule
  04_Source/         Markdown content and Python build scripts
  README.md          this file
```

---

## 誠實說明

本設計包由 AI 協助整理，提供一個可製作的工程基準。你仍需自己量度、購買、製作、測試、記錄失敗，並用自己的文字寫報告。如果課程要求披露 AI 輔助，請如實披露。不要把未製作、未測試的功能說成已完成。
