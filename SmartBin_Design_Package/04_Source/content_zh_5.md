# 附錄 A. 完整物料清單

下表是建議方案。價格為 2026 年 10 月香港／淘寶參考價，港幣。加 15% 運費、稅和備件。可編輯工作簿：`Smart_Waste_Sorting_Bin_BOM.xlsx`。

**BOM 備註**

- 「Core」是四分類必需；「Optional」可增強證據或可靠性，精簡方案可省略。
- 負重感測器買 **6 個**，配對最接近的 4 個；不同批次靈敏度可能不同。
- 多買 **一個備用** A4988、HX711、ToF。它們便宜，能救一次示範。
- 電池是最高風險採購。用有 BMS 的認證電池組和匹配充電器；不要買裸電池。
- 3D 打印件：鏡頭支架、感測器座、滑槽環、伺服座、桶角插件、線夾。預算 1 kg PETG。

[BOM]

# 附錄 B. 切割表

名義尺寸 mm。相接處留 1–2 mm 間隙；打磨到合適。夾板邊要密封。

[CUTLIST]

**切割順序**

1. 先切抽屜底和側板；確認桶放得進。
2. 圍着抽屜切桶區側／後／頂／底。
3. 切底座和電子倉。
4. 切中框和料斗支撐板；鑽負重感測器孔。
5. 切蓋和料斗板。
6. 切 PP 內襯和滴水盤。
7. 乾組裝；劃線、鑽導孔；然後密封、油漆。

# 附錄 C. 接腳與連接器表

[PINMAP]

**連接器表**

| 連接器 | 腳 | 訊號 | 電纜 | 對接 |
|---|---|---|---|---|
| J1 | 1 | 12 V + | 18 AWG 紅 | 電池／保險絲 |
| J1 | 2 | 12 V − | 18 AWG 黑 | 電池／保險絲 |
| J2 | 1 | 5 V | 20 AWG 紅 | 降壓 1 |
| J2 | 2 | GND | 20 AWG 黑 | 降壓 1 |
| J3 | 1 | 6 V | 20 AWG 橙 | 降壓 3 |
| J3 | 2 | GND | 20 AWG 黑 | 降壓 3 |
| J4 | 1 | SDA | 24 AWG 藍 | I2C |
| J4 | 2 | SCL | 24 AWG 綠 | I2C |
| J4 | 3 | 3.3 V | 24 AWG 紅 | I2C |
| J4 | 4 | GND | 24 AWG 黑 | I2C |
| J5 | 1 | STEP | 24 AWG | A4988 |
| J5 | 2 | DIR | 24 AWG | A4988 |
| J5 | 3 | EN | 24 AWG | A4988 |
| J5 | 4 | GND | 24 AWG | A4988 |
| J6 | 1 | 6 V | 20 AWG | 伺服 |
| J6 | 2 | GND | 20 AWG | 伺服 |
| J6 | 3 | PWM | 24 AWG | 伺服 |
| J7 | 1 | E+ | 屏蔽 | 負重 |
| J7 | 2 | E− | 屏蔽 | 負重 |
| J7 | 3 | A− | 屏蔽 | 負重 |
| J7 | 4 | A+ | 屏蔽 | 負重 |
| J8 | 1 | 5 V | 20 AWG | LED 環 |
| J8 | 2 | GND | 20 AWG | LED 環 |
| J8 | 3 | MOSFET 汲極 | 20 AWG | LED 環 |
| J9 | 1 | 5 V | 20 AWG | LED 燈條 |
| J9 | 2 | GND | 20 AWG | LED 燈條 |
| J9 | 3 | DATA | 24 AWG | LED 燈條 |

# 附錄 D. 序列協定與 API 參考

## D.1 訊息規則

- 每行一個 JSON，UTF-8，LF 結尾。
- 最大行長 512 bytes。
- 忽略未知鍵；未知指令回 `{"evt":"ERROR","code":"BAD_CMD"}`。
- 每個指令 500 ms 內回覆，`SORT` 可長達 10 秒。
- 每 2 秒心跳；漏 3 次 → `SAFE`。

## D.2 指令

| 指令 | 欄位 | 回覆 | 備註 |
|---|---|---|---|
| `HELLO` | `v` | `READY` | 握手；韌體版本 |
| `SORT` | `bin` 1–4、`id`、`timeout_ms` | `SORTING` 後 `DONE`／`ERROR` | 驗證連鎖 |
| `HOME` | — | `READY` | 回原點、關活門 |
| `STATUS` | — | `STATUS` | 完整狀態 |
| `STOP` | — | `SAFE` | 停止動作，保持電源 |
| `TARE` | — | `TARE_OK` | 料斗空、活門關 |
| `CAL` | `sensor`、`value` | `CAL_OK` | 儲存校正 |

## D.3 REST API

| 方法 | 路徑 | Body | 回覆 |
|---|---|---|---|
| GET | `/api/status` | — | `{state, bins, battery, last_event}` |
| GET | `/api/events` | — | `[{id, ts, class, confidence, weight_g, bin}]` |
| POST | `/api/sort` | `{bin, confirm:true}` | `{ok:true}` 或錯誤 |
| POST | `/api/tare` | `{}` | `{ok:true}` |
| GET | `/api/export.csv` | — | CSV |
| GET | `/api/health` | — | `{pi:true, esp32:true, uptime_s}` |

## D.4 範例

```text
Pi → ESP32: {"cmd":"HELLO","v":1}
ESP32 → Pi: {"evt":"READY","fw":"1.0.0","home":true}
Pi → ESP32: {"cmd":"STATUS"}
ESP32 → Pi: {"evt":"STATUS","state":"IDLE","bin_levels":[12,45,80,3],"door":false,"lid":true}
ESP32 → Pi: {"evt":"ITEM","weight_g":128.4,"moisture":0.12,"metal":false,"tof_mm":180}
Pi → ESP32: {"cmd":"SORT","bin":2,"id":"20261029-001","timeout_ms":8000}
ESP32 → Pi: {"evt":"SORTING","bin":2,"steps":1200}
ESP32 → Pi: {"evt":"DONE","bin":2,"ms":4210,"drop":true}
```

# 附錄 E. 測試記錄範本

## E.1 單元測試記錄

| 測試編號 | 日期 | 操作者 | 設置 | 結果 | 通過／失敗 | 備註 |
|---|---|---|---|---|---|---|
| UT1 | | | | | | |
| UT2 | | | | | | |
| UT3 | | | | | | |

## E.2 50 件系統測試

| # | 物件描述 | 真實類別 | 預測 | 信心 | 重量（g） | 濕度 | 金屬 | 桶 | 時間（s） | 卡料？ | 正確？ | 備註 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | |

**總結：** 整體準確率 = ___%；各類 recall = ___；平均週期 = ___ 秒；卡料率 = ___%；失敗 = ___。

## E.3 安全測試記錄

| 測試 | 第 1 次 | 第 2 次 | 第 3 次 | 通過？ | 備註 |
|---|---|---|---|---|---|
| 開蓋 → 不動作 | | | | | |
| 抽屜打開 → 不動作 | | | | | |
| 活門打開 → 不動作 | | | | | |
| 動作中急停 | | | | | |
| 動作中停電 | | | | | |
| 待機中 Pi 斷線 | | | | | |

# 附錄 F. 參考資料

[1] 香港環境保護署，「減廢與回收」，https://www.epd.gov.hk/epd/english/environmentinhk/waste/waste_main.html

[2] Espressif Systems, “ESP32 series datasheet,” https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf

[3] Raspberry Pi Foundation, “Raspberry Pi Zero 2 W product page,” https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/

[4] Google, “TensorFlow Lite,” https://www.tensorflow.org/lite

[5] M. Sandler et al., “MobileNetV2: Inverted residuals and linear bottlenecks,” CVPR 2018, https://arxiv.org/abs/1801.04381

[6] Pololu, “A4988 stepper motor driver carrier,” https://www.pololu.com/product/1182

[7] Avia Semiconductor, “HX711 24-bit ADC datasheet,” https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf

[8] STMicroelectronics, “VL53L1X datasheet,” https://www.st.com/resource/en/datasheet/vl53l1x.pdf

[9] ElecSchematics, “HC-SR04 datasheet,” https://www.electroschematics.com/wp-content/uploads/2013/07/HCSR04-datasheet-version-1.pdf

[10] Vishay, “TSOP382xx IR receiver datasheet,” https://www.vishay.com/docs/82491/tsop382.pdf

[11] FastAPI documentation, https://fastapi.tiangolo.com/

[12] SQLite documentation, https://www.sqlite.org/

[13] OpenCV documentation, https://opencv.org/

[14] IEC 62133-2, “Secondary cells and batteries containing alkaline or other non-acid electrolytes — Safety requirements for portable sealed secondary cells, and for batteries made from them, for use in portable applications — Part 2: Lithium systems,” https://webstore.iec.ch/publication/32588

---

*英文版與中文版內容對應；如兩版有差異，以英文版技術數字為準，並請自行核對實物。*
