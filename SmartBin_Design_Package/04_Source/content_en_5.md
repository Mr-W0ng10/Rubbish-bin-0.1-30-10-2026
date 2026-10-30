# Appendix A. Full bill of materials

The table below is the recommended build. Prices are indicative Hong Kong/Taobao street prices in October 2026, in HKD. Add 15% for shipping, tax and spares. The editable workbook is `Smart_Waste_Sorting_Bin_BOM.xlsx`.

**BOM notes**

- “Core” items are needed for the four-stream sorter. “Optional” items improve evidence or reliability but can be omitted in the lean build.
- Buy **six** load cells and match the four closest; load cells from different batches can have different sensitivity.
- Buy **one spare** A4988, HX711 and ToF sensor. They are cheap and save a demo.
- The battery is the highest-risk purchase. Use a certified pack with a BMS and a matching charger; do not buy loose cells.
- The 3D-printed parts are: camera bracket, sensor mounts, spout collar, servo bracket, bin corner inserts, cable clips. Budget 1 kg PETG.

[BOM]

# Appendix B. Cut list

Nominal dimensions in mm. Add 1–2 mm clearance where parts meet; sand to fit. Seal all plywood edges.

[CUTLIST]

**Cutting order**

1. Cut the drawer bottom and sides first; check the bins fit.
2. Cut the bin-section sides/back/top/bottom around the drawer.
3. Cut the base and electronics bay.
4. Cut the mid-frame and hopper support plate; drill the load-cell holes.
5. Cut the lid and hopper panels.
6. Cut the PP liners and drip tray.
7. Dry-assemble; mark and drill pilot holes; then seal and paint.

# Appendix C. Pin and connector schedule

[PINMAP]

**Connector schedule**

| Connector | Pins | Signal | Cable | Mate |
|---|---|---|---|---|
| J1 | 1 | 12 V + | 18 AWG red | Battery/fuse |
| J1 | 2 | 12 V − | 18 AWG black | Battery/fuse |
| J2 | 1 | 5 V | 20 AWG red | Buck 1 |
| J2 | 2 | GND | 20 AWG black | Buck 1 |
| J3 | 1 | 6 V | 20 AWG orange | Buck 3 |
| J3 | 2 | GND | 20 AWG black | Buck 3 |
| J4 | 1 | SDA | 24 AWG blue | I2C bus |
| J4 | 2 | SCL | 24 AWG green | I2C bus |
| J4 | 3 | 3.3 V | 24 AWG red | I2C bus |
| J4 | 4 | GND | 24 AWG black | I2C bus |
| J5 | 1 | STEP | 24 AWG | A4988 |
| J5 | 2 | DIR | 24 AWG | A4988 |
| J5 | 3 | EN | 24 AWG | A4988 |
| J5 | 4 | GND | 24 AWG | A4988 |
| J6 | 1 | 6 V | 20 AWG | Servo |
| J6 | 2 | GND | 20 AWG | Servo |
| J6 | 3 | PWM | 24 AWG | Servo |
| J7 | 1 | E+ | shielded | Load cells |
| J7 | 2 | E− | shielded | Load cells |
| J7 | 3 | A− | shielded | Load cells |
| J7 | 4 | A+ | shielded | Load cells |
| J8 | 1 | 5 V | 20 AWG | LED ring |
| J8 | 2 | GND | 20 AWG | LED ring |
| J8 | 3 | MOSFET drain | 20 AWG | LED ring |
| J9 | 1 | 5 V | 20 AWG | LED bar |
| J9 | 2 | GND | 20 AWG | LED bar |
| J9 | 3 | DATA | 24 AWG | LED bar |

# Appendix D. Serial protocol and API reference

## D.1 Message rules

- One JSON object per line, UTF-8, LF terminator.
- Maximum line length 512 bytes.
- Unknown keys are ignored; unknown commands return `{"evt":"ERROR","code":"BAD_CMD"}`.
- Every command has a response within 500 ms, except `SORT` which may take 10 s.
- Heartbeat every 2 s; 3 missed heartbeats → `SAFE`.

## D.2 Commands

| Command | Fields | Response | Notes |
|---|---|---|---|
| `HELLO` | `v` | `READY` | Handshake; firmware version |
| `SORT` | `bin` 1–4, `id`, `timeout_ms` | `SORTING` then `DONE`/`ERROR` | Validates interlocks |
| `HOME` | — | `READY` | Homes spout, closes door |
| `STATUS` | — | `STATUS` | Full state snapshot |
| `STOP` | — | `SAFE` | Stops motion, keeps power |
| `TARE` | — | `TARE_OK` | Hopper must be empty/closed |
| `CAL` | `sensor`, `value` | `CAL_OK` | Stores calibration |

## D.3 REST API

| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/api/status` | — | `{state, bins, battery, last_event}` |
| GET | `/api/events` | — | `[{id, ts, class, confidence, weight_g, bin}]` |
| POST | `/api/sort` | `{bin, confirm:true}` | `{ok:true}` or error |
| POST | `/api/tare` | `{}` | `{ok:true}` |
| GET | `/api/export.csv` | — | CSV file |
| GET | `/api/health` | — | `{pi:true, esp32:true, uptime_s}` |

## D.4 Example session

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

# Appendix E. Test record templates

## E.1 Unit test record

| Test ID | Date | Operator | Setup | Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|
| UT1 | | | | | | |
| UT2 | | | | | | |
| UT3 | | | | | | |

## E.2 50-item system test

| # | Item description | True class | Predicted | Confidence | Weight (g) | Moisture | Metal | Bin | Time (s) | Jam? | Correct? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | |

**Summary:** overall accuracy = ___%; per-class recall = ___; mean cycle time = ___ s; jam rate = ___%; failures = ___.

## E.3 Safety test record

| Test | Trial 1 | Trial 2 | Trial 3 | Pass? | Notes |
|---|---|---|---|---|---|
| Lid open → no motion | | | | | |
| Drawer open → no motion | | | | | |
| Door open → no motion | | | | | |
| E-stop during move | | | | | |
| Power loss during move | | | | | |
| Pi disconnect during idle | | | | | |

# Appendix F. References

[1] Hong Kong Environmental Protection Department, “Waste reduction and recycling,” https://www.epd.gov.hk/epd/english/environmentinhk/waste/waste_main.html

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

*End of English design package.*
