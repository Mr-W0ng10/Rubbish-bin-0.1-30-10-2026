# 5. Electrical design

## 5.1 Power architecture

[FIG:fig07_power_wiring.png|Figure 6. Power distribution and safety wiring. The e-stop cuts the 12 V actuator bus; the Pi and ESP32 stay alive on their own 5 V rails for logging.|170]

| Rail | Source | Loads | Notes |
|---|---|---|---|
| 12 V | 3S Li-ion pack (12.6 V max) or 12 V 5 A adapter | A4988 VMOT, LED ring, spare | 5 A fuse; main switch; e-stop |
| 5 V 5 A | Buck 1 | Raspberry Pi Zero 2 W, USB camera | 5.1 V; 5 A; heatsink |
| 5 V 3 A | Buck 2 | ESP32, sensors, LED bar | 5 V; 3 A; separate from Pi |
| 6 V 5 A | Buck 3 | DS3225MG servo | 1000 µF at servo; 6.0–6.8 V |
| 3.3 V | ESP32 regulator | I2C sensors, HX711, PCF8574 | Do not exceed 300 mA total |

**Power budget (peak):**

| Load | Voltage | Current | Power |
|---|---:|---:|---:|
| Raspberry Pi Zero 2 W | 5 V | 1.2 A | 6 W |
| USB camera | 5 V | 0.2 A | 1 W |
| ESP32 + sensors | 5 V | 0.25 A | 1.25 W |
| Servo (peak) | 6 V | 2.0 A | 12 W |
| Stepper | 12 V | 0.8 A | 9.6 W |
| LED ring | 12 V | 0.25 A | 3 W |
| LED bar + buzzer | 5 V | 0.1 A | 0.5 W |
| **Peak** | | | **≈33 W** |

A 12 V 6 Ah pack (≈72 Wh) gives about 2 h at 50% duty, or 4 h at 25% duty. The Pi alone draws ≈0.6–1.2 A at 5 V; use a 5 A buck with a heatsink, not a small LM2596.

**Do not** power the servo from the Pi’s 5 V rail. Servo inrush causes brownouts and SD-card corruption. Use a separate 6 V buck, a 1000 µF electrolytic, and a common ground.

## 5.2 Battery and adapter safety

- Use a **factory-assembled 3S2P 18650 pack with a BMS**, 12.6 V, 6 Ah, with a matching 12.6 V charger. Do not solder loose 18650 cells unless you are trained and supervised.
- Mount the pack in a rigid, vented enclosure away from the hopper and bins. Add a 5 A fuse on the positive lead within 150 mm of the pack.
- Add a main switch that disconnects the pack; a keyed switch is better for a public demo.
- Charge the pack **outside** the bin, on a non-flammable surface, with a fire-resistant bag nearby. Do not charge unattended.
- If the pack swells, gets hot, or smells sweet, stop using it and dispose of it at a recycling point.
- For bench testing, use a **12 V 5 A CE/BS-marked adapter** instead of the battery. It is safer and removes battery anxiety from long tests.

## 5.3 ESP32 pin allocation

[FIG:fig08_connection_map.png|Figure 7. Logical ESP32 connection map. Use the table below as the authoritative pin schedule.|170]

[PINMAP]

**Important pin notes:**

- GPIO34–39 are **input-only** and have no internal pull-ups. Fit external 10 kΩ pull-ups to 3.3 V for the IR receiver, e-stop status and front button.
- GPIO2 is a strapping pin. It drives the WS2812 data line after boot; do not hold it low during reset. If your board has an onboard LED on GPIO2, it may flicker at boot; that is normal.
- GPIO12 is a strapping pin; avoid using it for a switch that can be low at boot. It is used here only for the optional fan MOSFET.
- The ESP32 ADC is non-linear; for the moisture sensor, use a calibrated threshold, not an absolute voltage. Better: use a capacitive-to-digital sensor (FDC2214) if you need higher stability.
- All five ToF sensors share I2C. Hold XSHUT low, release one at a time, and assign addresses 0x30–0x33. The item ToF can stay at 0x29.
- The PCF8574 handles slow switches; polling at 20 Hz is enough. The INT line is optional.

## 5.4 Raspberry Pi connections

The Pi has only one USB data port on the Zero 2 W. Use a **micro-USB OTG hub** with two ports: one for the USB camera, one for the ESP32. The camera and ESP32 together draw <500 mA; a passive hub is usually fine. If the camera disconnects, use a powered hub.

- Pi power: 5 V 5 A buck into the USB-C power port (or the 5 V GPIO pins with a proper cable; the USB-C port is safer).
- Camera: USB UVC, 1280 × 720 or 1920 × 1080; test both.
- ESP32: USB serial; appears as `/dev/ttyUSB0` or `/dev/ttyACM0`.
- Fan: 5 V 40 mm fan on the electronics bay; connect to 5 V or a MOSFET on GPIO12.
- Do not connect the Pi’s 5 V to the ESP32’s 5 V pin if the ESP32 is also powered by its own buck. Choose one source. The simplest is: Pi USB powers the ESP32; the ESP32’s 5 V pin is not connected to the buck.

## 5.5 Sensor interfaces

### HX711 and load cells

- Four 5 kg half-bridge cells wired in a combinator; red E+, black E−, white A−, green A+.
- HX711 to ESP32: VCC 3.3 V, GND, DT→GPIO32, SCK→GPIO33.
- Shield: connect to GND at the HX711 end only; leave the load-cell end floating.
- Mount the HX711 away from the stepper driver; use a 100 nF decoupling capacitor.
- Calibration: known masses 0, 100, 500, 1000, 1500 g; linear regression; store the scale factor in NVS.

### ToF sensors (VL53L0X / VL53L1X)

- VIN 3.3 V, GND, SDA/SCL, XSHUT to a GPIO.
- 4.7 kΩ pull-ups to 3.3 V on SDA/SCL; many breakout boards already include them. Do not parallel too many 4.7 kΩ resistors; if you have five boards, remove duplicates or use 10 kΩ.
- Address assignment at boot: hold all XSHUT low; release item ToF (0x29); release bin 1 and set 0x30; bin 2 → 0x31; bin 3 → 0x32; bin 4 → 0x33.
- Mount bin ToF at the outer corner of each bin, angled 10–15° toward the centre; the beam should hit the waste surface, not the bin wall. Calibrate empty distance and set full at 80% of bin height.

### Ultrasonic alternative (budget)

If you use HC-SR04 instead of VL53L1X:

- 5 V supply; echo is 5 V, so use a 1 kΩ/2 kΩ divider to 3.3 V.
- Trigger sequentially, 20 ms apart, to avoid cross-talk.
- Mount at the bin corner with a foam cone; the wide beam may see the bin wall. Calibrate per bin.
- Cost saving ≈ HK$140, but reliability is lower in a narrow bin with soft waste.

### IR break-beam

- 940 nm IR LED + TSOP38238 receiver; modulate the LED at 38 kHz with ESP32 LEDC.
- Emitter: 3.3 V through 68–100 Ω; receiver: 3.3 V, GND, OUT→GPIO35 with 10 kΩ pull-up and 100 nF decoupling.
- Align across the hopper mouth; the beam should be broken by a hand but not by the closed lid.
- Test under sunlight and LED ring light; the 38 kHz modulation rejects ambient light.

### Moisture pad

- Capacitive soil-moisture sensor, 3.3 V, analog output to GPIO36 (ADC1_CH0).
- Power the sensor from 3.3 V only during measurement to reduce corrosion; use a MOSFET or a GPIO-controlled load switch if needed.
- Calibrate dry/wet; use hysteresis; map to a 0–1 moisture score, not a binary “wet” unless the score is stable.
- The sensor is under HDPE; do not expose the PCB directly to waste.

### Metal coil

- DIY kit output: digital (HIGH = metal). Power 3.3–5 V; check the kit’s output voltage before connecting to ESP32.
- If the output is 5 V, use a divider or a 3.3 V-compatible module.
- Mount the coil on nylon standoffs; keep it away from the load cells and stepper.
- Calibrate with the hopper empty and with a can at the centre/edge. Record detection rate; if <80%, treat it as optional evidence.

### Switches and PCF8574

- PCF8574 at 0x20; SDA/SCL; A0–A2 to GND.
- P0 lid reed, P1 door switch, P2 drawer switch, P3 spout home, P4–P7 bin present 1–4.
- Switches to GND; PCF8574 has weak pull-ups; add 10 kΩ external pull-ups if cables are long.
- Debounce 30 ms in firmware; a lid bounce must not trigger a false “closed”.

## 5.6 Actuator drivers

### Stepper (A4988)

- VMOT 12 V + 100 µF electrolytic; VDD 3.3 V; GND common.
- STEP→GPIO25, DIR→GPIO26, EN→GPIO27.
- 1/8 microstep; Vref = 0.64 V for 0.8 A with Rs = 0.1 Ω.
- Heat sink; do not touch the driver after a long move. Disable (EN high) when idle to reduce heat.
- Use acceleration limiting; a sudden 1200-step move can stall. Start at 400 steps/s, accelerate to 1200 steps/s.

### Servo (DS3225MG)

- 6 V from Buck 3; 1000 µF electrolytic + 100 nF ceramic at the connector.
- Signal→GPIO13; 50 Hz; 500–2500 µs.
- Do not power from the ESP32 5 V pin. Common ground with ESP32.
- Set the closed position first, then the open position; use a limit switch to confirm closed, not the servo’s internal position.
- Add a spring to close on power loss; the servo only pulls open.

### LED ring and LED bar

- LED ring: 12 V, 0.25 A, switched by an IRLZ44N MOSFET; gate→GPIO12 through 100 Ω, 10 kΩ pull-down. Always-on during capture; no PWM flicker.
- WS2812B bar: 5 V, data→GPIO2 through 330 Ω; 1000 µF bulk capacitor; common ground. Limit brightness to 30% to reduce current and heat.

## 5.7 Wiring and connector schedule

| From | To | Cable | Connector | Notes |
|---|---|---|---|---|
| Battery + | Fuse | 18 AWG red | Blade fuse holder | Within 150 mm of pack |
| Fuse | Main switch | 18 AWG red | Spade | 10 A switch |
| Main switch | E-stop | 18 AWG red | Spade | NC contact |
| E-stop | 12 V bus | 18 AWG red | Terminal block | Actuator bus |
| 12 V bus | A4988 VMOT | 18 AWG red/black | Screw terminal | 100 µF local |
| 12 V bus | Buck 1/2/3 | 18 AWG red/black | Screw terminal | Fused individually? Add 2 A fuses if possible |
| Buck 1 5 V | Pi USB-C | 20 AWG red/black | USB-C | 5.1 V |
| Buck 2 5 V | ESP32 5 V | 20 AWG red/black | JST-XH | Do not backfeed |
| Buck 3 6 V | Servo | 20 AWG orange/black | JST-Futaba | 1000 µF |
| Pi USB | Camera | USB cable | USB-A/micro-B | 1 m, service loop |
| Pi USB | ESP32 | USB cable | USB-A/micro-B | Data + 5 V; choose one source |
| ESP32 | HX711 | 4-core shielded | JST-XH | DT/SCK |
| ESP32 | I2C bus | 4-core shielded | JST-XH | SDA/SCL/3V3/GND |
| ESP32 | PCF8574 | 4-core | JST-XH | I2C |
| ESP32 | A4988 | 4-core | JST-XH | STEP/DIR/EN/GND |
| ESP32 | Servo | 3-core | JST-Futaba | 6 V/GND/SIG |
| ESP32 | E-stop status | 2-core | JST-XH | Opto output |
| Hopper | Mid-frame | 6-core | Aviation plug | Servo, moisture, door switch, coil |
| Lid | Base | USB + 4-core | Grommet | Camera, ToF, LED, reed |

**Label both ends** of every cable with the signal name and connector number. Use ferrules on stranded wire; do not tin wires into screw terminals (they cold-flow and loosen).

## 5.8 Noise, grounding and cable routing

- Use a **star ground** at the power distribution board. Connect the Pi, ESP32, bucks, drivers and sensors to this point; do not daisy-chain ground through signal cables.
- Keep the stepper and servo cables at least 50 mm from the HX711 and I2C cables. Cross at 90° if they must cross.
- Use shielded cable for the load cells; ground the shield at the HX711 end only.
- Twist SDA/SCL with GND; keep I2C leads <500 mm. If you need longer, lower the I2C clock to 50 kHz or use a bus extender.
- Add a 100 nF ceramic + 10 µF electrolytic at each sensor breakout; add a 1000 µF at the servo.
- Do not route the camera USB cable parallel to the stepper cable; separate by 50 mm or use a ferrite bead.
- The 12 V and 5 V wires should be separate twisted pairs; keep the battery leads short.

## 5.9 Electronics enclosure and ventilation

- Mount the Pi, ESP32, bucks, driver and terminals on a 3 mm acrylic plate in the base bay.
- Add a 40 mm 5 V fan with a dust filter; intake low, exhaust high. Do not blow air over the load cells.
- Separate the battery compartment from the electronics with a 3 mm FR4/plywood barrier; vent both.
- Use cable glands for every cable entering the bay; leave a drip loop so water cannot run into the box.
- Put a service USB port and a power switch on the front; label them.
- Keep the 12 V and 5 V fuses accessible without removing the electronics.

## 5.10 Bench test before assembly

Test each subsystem on the bench, with no waste:

1. **Power:** 12 V bus, 5 V rails, 6 V rail; check polarity and voltage before connecting loads.
2. **ESP32:** blink, serial monitor, I2C scan; confirm all addresses.
3. **HX711:** raw counts; place 100 g, 500 g, 1 kg; check linearity.
4. **ToF:** read distance with a wall and a bin; check all five addresses.
5. **IR beam:** break with a card; check debounce.
6. **Moisture:** dry/wet sponge; record raw values.
7. **Metal:** can at centre/edge; record detection.
8. **Stepper:** 10 moves to each position; check home repeatability.
9. **Servo:** 20 open/close cycles; check door limit and spring.
10. **E-stop:** press while moving; confirm actuators stop and ESP32 reports the fault.

Only after all ten pass should you install the electronics in the bin.

---

# 6. Firmware and software

## 6.1 Division of responsibility

| Layer | Raspberry Pi | ESP32 |
|---|---|---|
| Boot | Linux, Python service | Arduino/PlatformIO firmware |
| Camera | Capture, exposure, crop | — |
| AI | MobileNetV2 TFLite inference | — |
| Fusion | Rules + confidence | — |
| Sensors | — | HX711, ToF, IR, moisture, metal, switches |
| Motion | Sends target bin | Stepper, servo, homing, limits |
| Safety | Monitors heartbeat | Interlocks, watchdog, e-stop |
| Data | SQLite, API, cloud | Event log, settings in NVS |
| UI | FastAPI + PWA | LED bar + buzzer |

## 6.2 Serial protocol

Newline-delimited JSON at **115200 baud**, USB CDC. Every message is one line. The Pi sends commands; the ESP32 sends events and acknowledgements. A heartbeat every 2 s; if the Pi misses 3 heartbeats, the ESP32 goes to `SAFE`.

**Pi → ESP32**

```json
{"cmd":"HELLO","v":1}
{"cmd":"SORT","bin":2,"id":"20261029-001","timeout_ms":8000}
{"cmd":"HOME"}
{"cmd":"STATUS"}
{"cmd":"STOP"}
{"cmd":"TARE"}
{"cmd":"CAL","sensor":"moisture","value":0.42}
```

**ESP32 → Pi**

```json
{"evt":"READY","fw":"1.0.0","home":true}
{"evt":"ITEM","weight_g":128.4,"moisture":0.12,"metal":false,"tof_mm":180}
{"evt":"SORTING","bin":2,"steps":1200}
{"evt":"DONE","bin":2,"ms":4210,"drop":true}
{"evt":"ERROR","code":"JAM","msg":"drop beam not broken","bin":2}
{"evt":"BIN","levels":[12,45,80,3],"present":[true,true,true,true]}
{"evt":"HEARTBEAT","ms":123456}
```

**Error codes:** `LID_OPEN`, `DRAWER_OPEN`, `DOOR_OPEN`, `NO_BIN`, `BIN_FULL`, `JAM`, `TIMEOUT`, `ESTOP`, `HOME_FAIL`, `PI_LOST`.

## 6.3 ESP32 state machine

[FIG:fig09_state_machine.png|Figure 8. Control state machine. The Pi decides; the ESP32 executes only after validating interlocks and a target bin.|170]

The firmware is a non-blocking state machine. Do not use `delay()` for more than 1 ms in the main loop; use `millis()` timers.

**States:**

- `BOOT`: self-test, read switches, check e-stop.
- `HOME`: rotate clockwise to home, close door, verify drawer/lid.
- `IDLE`: heartbeat, read sensors, wait for a valid item.
- `ITEM`: ToF + weight confirm; send `ITEM` event.
- `WEIGH`: tare, wait for stable weight, send weight.
- `WAIT_CLASS`: wait for `SORT` or `STOP`; 5 s timeout.
- `ROTATE`: move stepper to target; verify home flag/step count.
- `DUMP`: open door, wait 1.5 s, check drop beam.
- `CLOSE`: close door, verify limit, home spout.
- `REPORT`: send `DONE`/`ERROR`, update bin levels.
- `FAULT`/`SAFE`: actuators off, LED red, wait for user.

**Transition guards:**

- `IDLE → ITEM` only if lid closed, drawer closed, door closed, spout home, no e-stop, no fault.
- `WAIT_CLASS → ROTATE` only if bin present, bin <90% full, target 1–4.
- `ROTATE → DUMP` only if home flag/step count within ±5 steps and door closed.
- `DUMP → CLOSE` after 1.5 s or drop beam; if no drop, retry once, then `FAULT`.
- Any state → `FAULT` on e-stop, lid open, drawer open, or Pi heartbeat lost.
- `FAULT → HOME` only after the user clears the fault and presses the front button.

## 6.4 Motion control

- Use `AccelStepper` or a simple step timer with acceleration.
- Steps per 90°: 1200 (1/8 microstep, 3:1 belt).
- Positions: bin 1 = 0, bin 2 = 1200, bin 3 = 2400, bin 4 = 3600 (relative to home at 45°).
- Always approach clockwise: compute `delta = (target - current + 4800) % 4800`; move `delta` steps clockwise.
- Speed: start 400 steps/s, accelerate to 1200 steps/s, decelerate before target.
- After move, hold torque for 300 ms, then disable the driver (EN high) to reduce heat. The 3:1 belt and bearing friction hold position; if the spout drifts, keep the driver enabled at 50% current.
- Home: move clockwise until the switch triggers; back off 20 steps; approach at 200 steps/s; set zero.
- Stall detection: A4988 has no StallGuard. Use the home switch and a timeout; if the move does not finish in 4 s, `FAULT`.

## 6.5 Sensor acquisition and filtering

| Sensor | Rate | Filter | Calibration |
|---|---|---|---|
| HX711 | 10 Hz | median of 10 + moving average 5 | scale factor, tare |
| ToF item | 20 Hz | median 5 | offset at door |
| ToF bins | 2 Hz each | median 5 | empty/full distance |
| Moisture | 5 Hz | moving average 10 | dry/wet thresholds |
| Metal | 10 Hz | 3-of-5 majority | centre/edge can |
| Switches | 50 Hz | 30 ms debounce | lid/door/drawer/home |
| SHT31 | 0.2 Hz | none | optional |

**Weight stability:** read 10 samples at 10 Hz; if the standard deviation is <2 g, accept the mean; otherwise wait up to 1 s. Tare with the door closed and the hopper empty at boot and before each cycle.

## 6.6 Safety and fault handling

- **E-stop:** hardware cuts 12 V to stepper/servo/LED; the ESP32 reads the status via an optocoupler and goes to `SAFE`. The Pi logs the event.
- **Lid/drawer/door:** read every 50 ms; if open during motion, stop the stepper immediately (disable), close the door if possible, set `FAULT`.
- **Watchdog:** ESP32 task watchdog 5 s; Pi heartbeat 2 s; if lost, `SAFE`.
- **Brownout:** ESP32 brownout detector on; if the 5 V rail drops, reset and home. The Pi should use a UPS or a 5 V 5 A buck with bulk capacitance.
- **Jam:** if the drop beam is not broken within 2 s, retry the door once; if still no drop, `FAULT` and app message “open lid, clear funnel”.
- **Bin full/missing:** refuse to sort; keep the item on the door; app asks the user to empty/replace the bin.
- **Power loss:** spring closes the door; the spout stays; on reboot, home and check for an item. If the weight is >20 g, ask the user to remove it.

## 6.7 Vision pipeline

1. **Capture:** 3 frames at 1280 × 720, fixed exposure/gain/white balance; wait 200 ms after the LED ring is on.
2. **Pre-process:** crop the hopper region (not the whole frame), resize to 224 × 224, normalize; optional brightness/contrast check.
3. **Inference:** MobileNetV2 TFLite; output 4 class probabilities + confidence.
4. **Temporal vote:** average the 3 frames; if the top class is consistent in ≥2 frames, accept; otherwise lower confidence.
5. **Fusion:** combine with weight, moisture, metal; see 6.9.
6. **Decision:** if confidence ≥0.70 and the sensor evidence agrees, sort; if 0.50–0.70, use sensor rules; if <0.50, ask the user.
7. **Log:** store the class, confidence, top-2 classes, weight, moisture, metal, bin, time, image path (optional).

**Performance target:** Pi Zero 2 W, MobileNetV2 1.0 at 224 × 224, TFLite float16: 150–400 ms per frame; 3 frames + pre-processing <1.5 s. If slower, use MobileNetV2 0.5 at 160 × 160 or a Pi 4.

## 6.8 Dataset and training

- **Classes:** `plastic_bottle`, `metal`, `wet`, `other`. Add an `unsure` outcome in software; do not train a fifth class unless you have enough data.
- **Quantity:** 300–500 images per class, captured with the actual camera, lid, LED ring and hopper. Include different positions, orientations, crushed/uncrushed, labels, transparent bottles, cans, food containers, wet waste in bags, dry paper/glass/fabric.
- **Split:** 80% train, 10% validation, 10% test; split by physical item, not by frame, to avoid leakage.
- **Augmentation:** flip, rotate ±20°, brightness/contrast ±15%, slight blur, random crop; do not use extreme colour shifts that break material cues.
- **Training:** transfer learning from ImageNet MobileNetV2; freeze base, train dense head 10 epochs, fine-tune last 30 layers 10 epochs; Adam 1e-4 then 1e-5; class weights; early stopping.
- **Conversion:** TFLite float16; optionally int8 with a representative dataset. Test on the Pi, not just on the laptop.
- **Evaluation:** confusion matrix, per-class precision/recall/F1, overall accuracy; test with 50 physical items, 3 trials each. Report the confusion matrix in the final report.
- **Dataset hygiene:** keep a CSV with filename, class, item ID, lighting, notes. Do not train on the test items. Take photos of failures; they are the most useful data.

## 6.9 Fusion rules

Start with vision; use sensors to confirm or override only when the evidence is strong.

| Condition | Decision |
|---|---|
| Vision confidence ≥0.75 and top class agrees with sensors | Top class |
| Vision says metal, coil detects metal, weight >15 g | Metal |
| Vision says plastic, coil no metal, weight <120 g, moisture <0.4 | Plastic |
| Moisture >0.65 and vision says wet/other | Wet |
| Vision says wet but moisture <0.35 and weight <80 g | Re-check; likely other |
| Vision confidence <0.50 | Ask user; default to other after 10 s |
| Coil metal but vision says plastic and weight >150 g | Metal (confidence boost) |
| Bin full/missing | Refuse; ask user |

**Do not** hard-code “metal = heavy” or “wet = heavy”; a full plastic bottle can be heavy, and a dry paper cup can be light. Use weight as a prior, not a rule.

## 6.10 Database schema

```sql
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  class TEXT NOT NULL,
  confidence REAL,
  weight_g REAL,
  moisture REAL,
  metal INTEGER,
  bin INTEGER,
  bin_level INTEGER,
  image_path TEXT,
  status TEXT,
  error_code TEXT
);
CREATE TABLE bins (
  id INTEGER PRIMARY KEY,
  name TEXT,
  level_pct INTEGER,
  present INTEGER,
  last_emptied TEXT
);
CREATE TABLE settings (
  key TEXT PRIMARY KEY,
  value TEXT
);
```

Use SQLite in WAL mode; write one row per event; keep images only if disk allows. Export CSV from the app.

## 6.11 API and app

**FastAPI endpoints:**

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/status` | Current state, bin levels, battery, last event |
| GET | `/api/events?limit=50` | Recent events |
| POST | `/api/sort` | Manual sort `{bin:1..4}` (confirmation required) |
| POST | `/api/calibrate` | Start tare/moisture/ToF calibration |
| GET | `/api/export.csv` | Download events |
| GET | `/api/health` | Pi/ESP32 heartbeat |

**PWA screens:**

1. **Dashboard:** big status, four bin bars, battery, last sort, “Open lid” instruction.
2. **History:** table with time, class, weight, confidence, bin; filter; CSV export.
3. **Manual sort:** choose bin; confirmation; only when an item is present.
4. **Settings:** bin names, thresholds, Wi-Fi, calibration, cloud opt-in.
5. **Alerts:** bin full, jam, lid/drawer open, e-stop, low battery.

The PWA can be served by the Pi at `http://smartbin.local:8000`. If there is no network, the Pi runs a Wi-Fi hotspot `SmartBin` and the user opens `http://192.168.4.1:8000`. This is the most reliable demo setup.

## 6.12 Cloud (optional)

- Local-first: SQLite is the source of truth; cloud is a copy.
- Use Firebase Firestore or Supabase free tier; sync events when online; queue offline.
- Do not stream camera images to the cloud by default; privacy and bandwidth.
- Secure the API with a token; do not expose the Pi to the public internet without a VPN.
- For the final demo, local Wi-Fi is enough; cloud is a bonus, not a dependency.

## 6.13 Repository structure

```text
smart-bin/
  firmware/
    esp32/
      src/main.cpp
      src/config.h
      src/sensors.cpp
      src/motion.cpp
      src/protocol.cpp
  pi/
    app/
      main.py
      vision.py
      fusion.py
      db.py
      serial_link.py
      static/
    models/
      mobilenetv2_waste.tflite
    data/
      events.db
  hardware/
    drawings/
    bom.xlsx
    pinmap.csv
  docs/
    README.md
    calibration.md
    test-records/
```

Use git from day one; commit weekly; tag the version you demo.

## 6.14 Key code sketches

**ESP32: non-blocking state machine (skeleton)**

```cpp
enum State { BOOT, HOME, IDLE, ITEM, WEIGH, WAIT_CLASS, ROTATE, DUMP, CLOSE, REPORT, FAULT };
State state = BOOT;
uint32_t tState = 0;

void loop() {
  readSwitches();
  if (estopPressed() || lidOpen() || drawerOpen()) enterFault("INTERLOCK");
  switch (state) {
    case IDLE:
      if (itemPresent() && weightG() > 20) { sendItem(); state = WAIT_CLASS; tState = millis(); }
      break;
    case WAIT_CLASS:
      if (millis() - tState > 5000) enterFault("TIMEOUT");
      break;
    case ROTATE:
      if (stepper.distanceToGo() == 0) { verifyPosition(); state = DUMP; tState = millis(); }
      stepper.run();
      break;
    case DUMP:
      if (millis() - tState > 1500) { closeDoor(); state = CLOSE; }
      break;
    // ...
  }
}
```

**Pi: sort request**

```python
def sort_item(frame):
    probs = model.predict(preprocess(frame))
    cls, conf = top_class(probs)
    weight = esp32.last_item["weight_g"]
    moisture = esp32.last_item["moisture"]
    metal = esp32.last_item["metal"]
    decision = fuse(cls, conf, weight, moisture, metal)
    if decision is None:
        return ask_user(probs)
    esp32.send({"cmd": "SORT", "bin": decision.bin, "id": event_id})
    return wait_for_done(timeout=10)
```

**Pi: serial link**

```python
import serial, json, threading
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
def reader():
    for line in ser:
        try:
            msg = json.loads(line.decode().strip())
            events.put(msg)
        except json.JSONDecodeError:
            log.warning("bad line: %r", line)
threading.Thread(target=reader, daemon=True).start()
```

## 6.15 Calibration procedures

### Load cells

1. Warm up 5 min; hopper empty; door closed.
2. Send `TARE`; record raw counts.
3. Place 100 g, 500 g, 1000 g, 1500 g at the centre; record raw counts.
4. Fit `weight = (raw - offset) / scale`; check error <±5 g.
5. Repeat with a 500 g mass at four corners; error <±10 g.
6. Store the scale factor in NVS; re-tare every cycle.

### Moisture

1. Dry the pad; record raw ADC (air).
2. Put a damp sponge (not dripping) on the pad; record raw ADC.
3. Put a dry plastic bottle on the pad; record raw ADC.
4. Set `wet` threshold halfway between dry and wet with 0.15 hysteresis.
5. Repeat 5 times; if the readings overlap, increase the cover thickness or use a better sensor.

### Metal

1. Empty hopper; tune the kit until the output is stable (no metal).
2. Place a steel can at the centre; adjust sensitivity until detection.
3. Test at four edges; record detection.
4. Test an aluminium can, a plastic bottle, and a wet sponge; record false positives.
5. If false positives >10%, reduce sensitivity or omit the coil.

### Bin ToF

1. Empty bin; record distance to bottom.
2. Put a flat board at 25%, 50%, 75%, 100% of bin height; record distance.
3. Fit a linear map `fill% = a * distance + b`; check ±10%.
4. Repeat for each bin; store per-bin calibration.

### Camera

1. Print a grid target at the door plane.
2. Set manual exposure, gain and white balance under the LED ring.
3. Check the full hopper is in frame; adjust height/focus.
4. Capture 20 images of the same item; check brightness variation <10%.
5. Re-check after changing the lid or LED.

---

# 7. Cost, procurement and resources

## 7.1 BOM summary

| Group | Cost (HKD) | Share |
|---|---:|---:|
| Structure | 1,395 | 34% |
| Motion | 490 | 12% |
| Sensing | 1,030 | 25% |
| Power | 700 | 17% |
| Assembly | 435 | 11% |
| **Total (recommended)** | **4,050** | **100%** |

The full BOM is in Appendix A and in the separate `Smart_Waste_Sorting_Bin_BOM.xlsx`. Prices are indicative Hong Kong/Taobao street prices in October 2026; verify before ordering. Add 15% contingency for shipping, broken parts and replacements.

## 7.2 Budget tiers

| Build | Changes | Estimated cost |
|---|---|---:|
| **Lean** | HC-SR04 instead of 4 × VL53L1X; 12 V adapter instead of battery; reuse donor bins; plywood offcuts; no gas struts; no SHT31; no metal kit | ≈ HK$3,200 |
| **Recommended** | As listed in Appendix A; battery + adapter; 4 × VL53L1X; metal kit; gas struts | ≈ HK$4,050 |
| **Enhanced** | Pi 4 2 GB; aluminium frame; spare servo/stepper; 5 MP camera with better lens; UPS | ≈ HK$4,800 |

The recommended build is the best balance for a final-year demo. The lean build is acceptable if budget is tight, but the ultrasonic bin sensors and vision-only metal detection will be less reliable; document that as a limitation.

## 7.3 Procurement and lead times

| Item | Where | Lead time | Notes |
|---|---|---|---|
| Raspberry Pi Zero 2 W | HK reseller / online | 1–2 weeks | Buy two if possible; one spare |
| USB camera | Computer shop / Taobao | 1 week | Check UVC and 90° FOV |
| NEMA 17, A4988, GT2 | Taobao / robot shop | 1–2 weeks | Order spare A4988 |
| Load cells, HX711 | Taobao | 1–2 weeks | Buy 6 cells, match them |
| ToF sensors | Taobao | 1–2 weeks | Buy 1 spare VL53L1X |
| 12 V Li-ion pack | Battery specialist | 1–2 weeks | Certified pack + charger |
| Plywood/PP | Local shop | 2–3 days | Cut to the cut list |
| 3D printing | School/lab/online | 2–5 days | PETG, 30% infill |
| Fasteners | Local hardware | Same day | Buy 20% spares |

**Order early:** the battery, Pi, camera and ToF sensors are the long-lead items. If they are delayed, build the frame and drawer first; they do not depend on electronics.

## 7.4 Cost-saving and reuse

- Use offcuts or donated plywood; paint/seal them.
- Reuse 12 L food containers or cat-litter buckets as bins; cut the notch.
- Use a phone as a camera? Not recommended: mounting, focus, exposure and USB tethering are unreliable. A HK$120 USB camera is worth it.
- Use a 12 V adapter for bench testing; buy the battery only for the final demo.
- 3D-print brackets at school; avoid expensive online printing.
- Buy a kit of M4/M5 screws instead of individual packs.
- Skip the SHT31 and metal kit if budget is tight; they are optional evidence.

## 7.5 Tools

[TOOLS]

If the lab already has these, budget only for consumables (solder, blades, drill bits, tape). Add a fire-resistant Li-ion bag and safety glasses; they are not optional.

## 7.6 Procurement risks

| Risk | Mitigation |
|---|---|
| Pi Zero 2 W out of stock | Pi 4 2 GB or Pi 3 A+; same code, more power |
| Camera FOV wrong | Test with a phone/printed grid before cutting the lid; buy a 90° lens |
| Load cells mismatched | Buy 6 from the same batch; calibrate each; use 4 closest |
| Battery shipping delay | Use 12 V adapter for development; borrow a pack for demo |
| 3D printer unavailable | Plywood brackets or laser-cut acrylic; redesign tabs |
| Prices over budget | Lean substitutions; reuse; 15% contingency |

---

# 8. Build, test and evaluation plan

## 8.1 Schedule

The project runs from November 2026 to late April 2027. This schedule assumes one student working ~10–12 hours/week, with lab access. Adjust to your actual timetable.

| Weeks | Dates | Tasks | Milestone |
|---|---|---|---|
| 1–2 | 2–15 Nov 2026 | Finalise design; BOM; order long-lead parts; proposal slides | Proposal ready |
| 3–4 | 16–29 Nov | Cut frame/drawer; build bins; bench electronics | Frame and drawer |
| 5–6 | 30 Nov–13 Dec | Hopper, door, load cells, spout, bearing | First mechanical assembly |
| 7–8 | 14–27 Dec | ESP32 firmware; sensors; stepper/servo; serial protocol | Subsystems work on bench |
| 9–10 | 28 Dec–10 Jan 2027 | Dataset collection; model training; interim report | Interim report 1st submission |
| 11–12 | 11–24 Jan | Integrate vision; first end-to-end sort | First automatic sort |
| 13–14 | 25 Jan–7 Feb | Calibration; 4-class test; fix jams | 50% target accuracy |
| 15–16 | 8–21 Feb | PWA; bin levels; cloud; progress review prep | App dashboard |
| 17–18 | 22 Feb–7 Mar | 50-item test; reliability; safety; video | Test report v1 |
| 19–20 | 8–21 Mar | Refinement; enclosure; labels; user test | Demo-ready |
| 21–22 | 22 Mar–4 Apr | Final testing; report draft; poster | Report draft |
| 23–24 | 5–18 Apr | Final report; video; presentation; buffer | Submission ready |
| — | 27 Apr 2027 | Final deadline | Submit |

**Buffers:** 1 week after the first assembly; 1 week after the first end-to-end sort; 1 week before the final deadline. Do not compress testing.

## 8.2 Work breakdown and milestones

| Work package | Output | Depends on |
|---|---|---|
| WP1 Requirements and concept | Requirement table, concept selection | — |
| WP2 Mechanical design | Drawings, cut list, BOM | WP1 |
| WP3 Mechanical build | Frame, drawer, bins, hopper, spout | WP2, parts |
| WP4 Electronics | Power, sensors, drivers, wiring | WP2, parts |
| WP5 Firmware | ESP32 state machine, serial protocol | WP4 |
| WP6 Vision | Dataset, model, TFLite on Pi | WP3, camera |
| WP7 Integration | End-to-end sort | WP3–WP6 |
| WP8 App/data | PWA, SQLite, CSV, optional cloud | WP5, WP7 |
| WP9 Test/evaluation | Accuracy, cycle time, jam rate, safety | WP7, WP8 |
| WP10 Documentation | Report, poster, video, demo | All |

## 8.3 Test plan

### Unit tests

| ID | Test | Procedure | Pass criterion |
|---|---|---|---|
| UT1 | Load cell linearity | 0/100/500/1000/1500 g | error ≤ ±5 g |
| UT2 | Load cell corner error | 500 g at four corners | error ≤ ±10 g |
| UT3 | ToF bin level | 25/50/75/100% boards | error ≤ ±10% |
| UT4 | Moisture | dry/wet sponge, 5 repeats | clear separation |
| UT5 | Metal | can centre/edge, plastic control | ≥80% detection, ≤10% false |
| UT6 | Stepper home | 20 homes | ±2 steps |
| UT7 | Stepper position | 20 moves to each bin | ±3° |
| UT8 | Servo door | 100 cycles | no jam; limit switch every time |
| UT9 | IR beam | hand/card, 20 trials | 100% detection |
| UT10 | E-stop | press during move, 5 trials | stop <100 ms; fault logged |

### Integration tests

| ID | Test | Procedure | Pass criterion |
|---|---|---|---|
| IT1 | Load → weigh → class | 10 items per class | event within 2 s; weight ±5 g |
| IT2 | Class → rotate → drop | 40 items | correct bin ≥85%; no jam |
| IT3 | Bin full | Fill bin to 95% | refuse; app alert |
| IT4 | Missing bin | Remove bin 2 | refuse; app alert |
| IT5 | Lid/drawer open | Open during cycle | stop; fault; no motion |
| IT6 | Pi disconnect | Unplug USB during idle | ESP32 safe; no motion |
| IT7 | Power loss | Switch off during cycle | door closes; reboot safe |

### System test

- 50 mixed items, 3 runs, random order; record class, confidence, weight, moisture, metal, bin, time, success, jam, notes.
- Compute overall accuracy, per-class recall, confusion matrix, mean cycle time, 95th percentile, jam rate.
- Measure noise at 1 m; measure power; measure battery life.
- User test: 3–5 users, first-time use, task completion, SUS score, comments.

### Test record template

| # | Item | True class | Predicted | Confidence | Weight (g) | Moisture | Metal | Bin | Time (s) | Result | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | |

## 8.4 Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Metal detection unreliable | High | Medium | Vision + weight fusion; coil optional; document |
| R2 | Transparent plastic vs glass | High | Medium | Local dataset; confidence threshold; manual override |
| R3 | Wet sensor fouling | Medium | High | Replaceable HDPE cover; clean; calibrate |
| R4 | Item jams in funnel | Medium | High | 110 mm outlet; 59° walls; drop beam; access panel |
| R5 | Stepper misses steps | Medium | Medium | 3:1 belt; current limit; home each cycle |
| R6 | Load cell drift | Medium | Medium | Tare each cycle; shielded cable; quality cells |
| R7 | Battery safety | Low | High | Certified pack; fuse; charge outside; fire bag |
| R8 | Camera glare | High | Medium | Diffuse ring; matte black; polarizer |
| R9 | Lid cable wear | Medium | Medium | USB cable; service loop; strain relief |
| R10 | Schedule slip | High | High | Order early; build frame first; cut scope to lean |
| R11 | Cost overrun | Medium | Medium | 15% contingency; reuse; lean BOM |
| R12 | User confusion | Medium | Medium | Labels; LED; app instructions; user test |

## 8.5 Mapping to the FYP assessment

| Assessment area | Evidence in this package |
|---|---|
| Problem, goals, objectives | Section 1; problem statement; SMART objectives |
| Feasibility and proposed solution | Sections 2–3; concept comparison; BOM; schedule |
| Requirements | Section 1.4; FR/NFR tables; acceptance criteria |
| Detailed design | Sections 4–6; drawings; calculations; pin map; state machine |
| Implementation | Build sequence; code sketches; calibration; photos/logs |
| Testing and evaluation | Section 8; unit/integration/system tests; metrics |
| Schedule and resources | Sections 7–8; BOM; 24-week plan; risk register |
| Final report/presentation | Use the figures and tables; add your own results |

**What to photograph for the report:** cut parts, frame assembly, drawer, hopper, load cells, spout, wiring, sensor mounts, first sort, failures, final demo, app screens, test setup. Keep a logbook with dates and decisions.

## 8.6 What to do if you run out of time

Prioritise in this order:

1. Safe mechanical build with manual bin selection (no AI) — demonstrates mechanism.
2. Load cells + bin levels + app logging — demonstrates sensors/data.
3. Vision classification with manual confirm — demonstrates AI.
4. Full automatic sort — the ideal.

A working, well-tested 3-stream sorter is better than an unfinished 4-stream sorter. Document what is not finished honestly.

---

# 9. Limitations, future work and conclusion

## 9.1 Limitations

- **One item at a time.** Multiple items or a bag will confuse the classifier and may jam.
- **Size/weight limit.** 110 mm spout, 1.5 kg door; 2 L bottles and heavy bags are out.
- **Metal detection is confirmatory.** The DIY coil is not a certified detector; aluminium foil and thin cans may be missed.
- **Wet/dry is evidence, not truth.** A wet label on a dry bottle or a sealed wet bag can mislead.
- **Dataset bias.** Accuracy depends on the items you collect; a new building’s waste may differ.
- **No glass/paper separation.** They go to “other”; this is a deliberate scope choice.
- **No compaction/odour control.** The bin fills; wet waste may smell; clean regularly.
- **Battery life.** 2–4 h continuous; not a full-day public bin.
- **Prototype safety.** Not certified; do not use unattended in public.

## 9.2 Future work

- Add a fifth bin for paper/glass; increase spout positions to 5.
- Use a Pi 4 or Jetson Nano for a larger model / real-time detection.
- Add a load-cell-based “fill mass” estimate and compaction.
- Add a UV-C or ozone module for odour (with safety interlocks).
- Add a solar panel and battery management for outdoor use.
- Add a QR/NFC user ID and gamification for recycling behaviour.
- Add a cloud dashboard for a building manager; predict fill and optimize collection.
- Improve the metal detector with a proper eddy-current front end.
- Add a self-test routine and remote diagnostics.

## 9.3 Conclusion

This package gives you a complete, buildable design: a 480 × 480 × 940 mm bin, four 10.7 L bins, a 320 × 320 mm weigh hopper, a 110 mm rotating spout, a Pi + ESP32 control stack, a camera-based classifier, and a phone app. It is deliberately low-cost, repairable, and safe enough for an indoor final-year demonstration.

The hard parts are not the CAD: they are **dataset quality, jam-free mechanics, and honest testing**. Build the frame and drawer first, get the sensors working on the bench, then integrate vision. Keep the scope tight, document every failure, and let the test data tell the story. A well-tested 85% system with clear limitations is a stronger FYP than an untested 99% claim.

---
