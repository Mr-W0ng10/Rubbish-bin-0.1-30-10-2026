# 2. Design exploration and decisions

## 2.1 Design drivers

The design was driven by six constraints, in this order:

1. **Buildable by a beginner.** Hand tools, local cutting, 3D-printed brackets, standard plastic bins. No welding, no custom gears, no high-voltage wiring.
2. **Low cost.** Target under HK$4,500 including battery and camera. Reuse where sensible; spend money on the parts that affect reliability (bearing, load cells, stepper, power).
3. **Safe to demonstrate.** The user must not be able to reach the sorting mechanism while it moves. The machine must fail safe on power loss or e-stop.
4. **Reliable sorting.** A simple, slow, repeatable mechanism is better than a fast, jam-prone one.
5. **Maintainable and cleanable.** Bins and hopper liner must come out without tools; wet waste must not reach electronics.
6. **Good enough to evaluate.** The design must produce measurable data: accuracy, cycle time, jam rate, fill-level error, cost.

## 2.2 Concept options

Four mechanisms were considered. The scores are 1 (poor) to 5 (good) for this project, not absolute engineering quality.

| Criterion | A. Rotating bin carousel, fixed chute | B. Fixed bins, rotating spout | C. X–Y gantry over bins | D. Manual bins with app guidance |
|---|---|---|---|---|
| Mechanical complexity | Medium | Medium | High | Low |
| Motor torque needed | High (moves all bins + waste) | Low (moves only the spout) | Medium | None |
| Footprint | Large (round carousel ≥ 600 mm) | Compact (480 × 480 mm) | Large (rails) | Compact |
| Jam/spill risk | Medium–high (waste shifts) | Low–medium | Medium | None |
| Bin standardisation | Standard bins on a tray | Standard bins with a corner notch | Standard bins | Standard bins |
| Build cost | Medium | Low–medium | High | Lowest |
| Demonstrability | Good | Excellent (visible spout move) | Good | Weak (no automation) |
| Score | 3.4 | **4.6** | 2.6 | 2.0 |

**Selected: B — four fixed bins and a rotating spout.**

### Why not rotate the bins?

A 2 × 2 tray of four 10 L bins plus waste can weigh 10–15 kg. Rotating that mass needs a large bearing, a geared motor with high torque, and a round enclosure large enough for the tray diagonal. A 480 mm square tray has a 679 mm diagonal, so it cannot rotate inside a 480 mm square bin. The enclosure would grow to at least 650–700 mm, which is heavy, expensive, and awkward to demonstrate. Waste can also shift and spill during rotation. The rotating-spout concept moves only a 0.3–0.5 kg elbow; the bins stay still, the drawer stays simple, and the enclosure stays compact.

### Why not a gantry?

An X–Y gantry is flexible but needs two axes, rails, belts, limit switches and a rigid frame. It is harder to align, more expensive, and adds two more failure modes. For four fixed positions, a single rotary axis is the right kinematic choice.

### Why not just manual bins with an app?

That is cheaper, but it does not meet the project’s engineering objective: the system must **act** on the classification. A display-only bin would also be hard to justify as a final-year engineering prototype. The selected design keeps the app as a record/override, not as the sorter.

## 2.3 Why two processors?

The original sketch suggested an ESP32-CAM as the only controller. That is possible, but it is a poor fit for a beginner building a four-class vision system with motors and many sensors.

| Criterion | ESP32-CAM only | Raspberry Pi only | **Pi Zero 2 W + ESP32** |
|---|---|---|---|
| Camera | Good, but fixed-focus and limited memory | USB camera, easy | USB camera + UVC |
| AI | TFLite Micro; hard to train/deploy | Python/TFLite; easy | Easy on Pi |
| Real-time motion | Good | Linux jitter; possible but risky | Deterministic on ESP32 |
| Pin count | Few; camera uses many pins | Enough, but 3.3 V and power limits | ESP32 handles I/O |
| App/cloud | Limited | Easy | Easy on Pi |
| Debugging | One binary | One Python app | Clear split; serial log |
| Cost | Lowest | Medium | Medium |
| **Verdict** | Cheap but risky | Simple but less robust | **Selected** |

The Pi handles the camera, inference, database, web app and optional cloud. The ESP32 handles sensors, debouncing, stepper/servo timing, interlocks and fault handling. They talk over USB serial using newline-delimited JSON. This split is also a good story for the report: Linux for high-level work, a microcontroller for real-time work.

A Pi 4 (2 GB) is a drop-in upgrade if the Zero 2 W is too slow for your model. The serial protocol and wiring do not change.

## 2.4 Why no screen?

A screen adds cost, power, a cut-out, glare, and a cleaning problem in a wet-waste bin. The user already carries a phone. The bin needs only:

- a **three-colour LED bar** (idle, scanning, sorted, error, bin full);
- a **buzzer** for confirmation/fault;
- a **phone PWA** for detail, history and manual override.

This keeps the front panel simple and hygienic. If your supervisor wants a display, a 0.96-inch OLED can be added on I2C for status text, but it is not required.

## 2.5 Key design decisions

| Decision | Options considered | Selected | Why |
|---|---|---|---|
| Item handling | Tilting tray / sliding plate / bottom door | **Bottom door** | Item sits still for weighing and imaging; door drops it cleanly; spring can close on power loss |
| Bin arrangement | 2 × 2 fixed / circular carousel / linear | **2 × 2 fixed** | Compact, standard bins, simple drawer, low torque |
| Spout | Rotating elbow / swinging arm / fixed chute | **Rotating elbow** | One axis, 90° positions, visible, low torque |
| Bin level | Ultrasonic ×4 / ToF ×4 / one sensor on a arm | **ToF ×4** | Narrow beam, no acoustic cross-talk, small window, I2C |
| Item presence | Camera only / ToF / weight only | **ToF + weight** | Camera can be fooled by a shadow; weight confirms a real item |
| Metal | Vision only / inductive proximity / coil | **Vision + coil confirmation** | A small inductive sensor only sees metal at its face; a coil sees a can anywhere on the door |
| Wet/dry | Vision only / capacitive pad / conductivity | **Vision + capacitive pad** | The pad is cheap and gives a physical moisture cue; vision handles the rest |
| Lid | Manual / servo / linear actuator | **Manual with gas strut** | Fewer actuators, safer, cheaper; the user must close it before sorting |
| Power | 12 V adapter / 12 V Li-ion / 5 V USB | **12 V Li-ion + adapter** | Portable demo; adapter for bench testing |

## 2.6 The one-sentence design

> A top-loading, lidded bin weighs and photographs one item on a spring-closed hopper door, uses a Pi-hosted MobileNetV2 classifier plus moisture/metal/weight evidence to choose one of four streams, rotates a 110 mm spout to the matching fixed bin, drops the item through a funnel, and records the event in a phone app.

## 2.7 What could go wrong — and the design response

| Failure | Design response |
|---|---|
| Item jams in funnel | 110 mm outlet, 59° walls, smooth joints, drop-confirmation beam, access panel, optional vibration motor |
| Transparent bottle confused with glass/metal | Local dataset, diffuse lighting, confidence threshold, metal coil, manual override |
| Wet waste contaminates sensor | Moisture pad under replaceable HDPE; coil and ToF fixed to frame, not door; drip tray; wipe-clean liner |
| Spout misses bin | Home switch each cycle, 3:1 belt, always approach clockwise, ±3° repeatability, 190 mm bin opening |
| Load cell drift | Tare each cycle; 4-cell platform; shielded cable; no pipe/cable bypassing the hopper |
| Lid opened during motion | Reed switch + software interlock; actuators stop; re-home required |
| Battery fault | Certified pack, BMS, fuse, main switch, e-stop, charge outside, fire bag |
| Pi crashes | ESP32 stops and shows fault; no motion without a valid SORT command; watchdog |
| User puts in a 2 L bottle | Label and app warning; 110 mm spout limits size; test with typical 500 mL–1.5 L items |

---

# 3. System overview

## 3.1 Architecture

[FIG:fig01_system_architecture.png|Figure 1. System architecture: sensors and actuators around the ESP32, vision/app/data on the Raspberry Pi, and a single controlled waste path.|170]

The system has five layers:

1. **Physical:** lid, hopper, door, funnel, spout, four bins, drawer.
2. **Sensing:** camera, item ToF, four load cells, moisture pad, metal coil, IR beam, four bin ToF sensors, switches.
3. **Real-time control:** ESP32 — sampling, debouncing, motion, interlocks, fault handling.
4. **Vision and application:** Raspberry Pi — camera capture, MobileNetV2 inference, sensor fusion, SQLite, FastAPI, PWA.
5. **User/cloud:** phone browser on the local network; optional Firebase/Supabase sync.

The important architectural rule: **the ESP32 never moves an actuator without an explicit, validated command**. If the Pi crashes or the USB cable falls out, the ESP32 goes to a safe state, not into a random sort.

## 3.2 Operating sequence

[FIG:fig06_sort_sequence.png|Figure 2. One sort cycle. The user loads and closes the lid; the machine weighs, images, decides, rotates, drops, confirms and homes.|170]

| Step | User action | Machine action | Typical time |
|---|---|---|---|
| 1 | Lift lid, place one item on the hopper door, close lid | Lid switch confirms; IR beam clear; LED blue | 0–2 s (user) |
| 2 | Wait | ToF detects item; load cells tare and weigh; camera captures 3 frames | 1–2 s |
| 3 | Wait | Pi classifies; fuses sensors; chooses bin or asks for help | 1–2 s |
| 4 | Wait | ESP32 rotates spout to target; verifies home/position | 1–2 s |
| 5 | Wait | Door opens 70°; item falls; drop beam confirms | 1–2 s |
| 6 | Wait | Door closes; spout homes; app updates | 1–2 s |
| 7 | Open lid, remove bin when full | Bin-level alert; drawer slides out | As needed |

**Total machine time:** 6–9 s typical. The target is ≤10 s excluding user loading.

## 3.3 Subsystems

| Subsystem | Main parts | Responsibility |
|---|---|---|
| Structure | Plywood frame, drawer, slides, lid, hinges | Hold everything rigid; allow bin access; guard moving parts |
| Weigh hopper | 4 × 5 kg cells, HX711, door, servo, spring | Hold item still; measure weight; drop item |
| Sorting | Funnel, bearing, spout, NEMA 17, A4988, belt | Direct item to the selected bin |
| Bins | 4 × 10.7 L PP bins, notched corners, drawer | Collect four streams; lift out for emptying |
| Vision | USB camera, LED ring, item ToF | Capture a consistent image; detect presence/height |
| Moisture/metal | Capacitive pad, inductive coil | Add physical evidence to the classifier |
| Bin level | 4 × VL53L1X ToF | Estimate fill; alert at 90% |
| Safety | Reed/micro switches, IR beam, e-stop, fuse | Prevent motion when open; cut actuators |
| Control | Pi Zero 2 W, ESP32, buck converters | Vision, app, real-time I/O |
| App/data | FastAPI, SQLite, PWA | Status, history, manual sort, CSV export |

## 3.4 Specifications at a glance

| Parameter | Value |
|---|---|
| Overall size | 480 W × 480 D × 940 H mm |
| Loading height | ≈ 900 mm |
| Empty mass | ≈ 22–26 kg |
| Bins | 4 × 190 × 190 × 360 mm internal; ≈ 10.7 L usable each |
| Total capacity | ≈ 42.8 L |
| Max item | 250 mm long × 110 mm diameter × 1.5 kg |
| Sorting time | 6–9 s typical; ≤ 10 s target |
| Classification | 4 classes + “unsure”; MobileNetV2 on Pi |
| Power | 12 V 6 Ah Li-ion (BMS) or 12 V 5 A adapter |
| Peak power | ≈ 35 W |
| Battery life | ≈ 2–4 h continuous demo; days in standby |
| Display | RGB LED bar + buzzer + phone PWA |
| Cost | ≈ HK$4,050 recommended; ≈ HK$3,200 lean; ≈ HK$4,800 enhanced |

## 3.5 Physical layout

[FIG:fig02_cross_section.png|Figure 3. Front section with dimensions and sensor locations. The hopper floats on four load cells; the spout rotates under the funnel; four bins sit in a pull-out drawer.|170]

[FIG:fig03_top_view_doc.png|Figure 4. Top view: 2 × 2 bins, 80 × 80 mm corner notches, 150 mm bearing, 130 mm spout radius, and the four ToF bin-level sensors.|170]

The layout is deliberately layered:

- **Top:** lid, camera, LED ring, item ToF, IR beam.
- **Upper middle:** weigh hopper, door, moisture pad, metal coil, load cells.
- **Lower middle:** funnel, bearing, rotating spout, four bin ToF sensors.
- **Bottom:** four bins in a drawer, then the electronics bay.

This keeps wet waste above the electronics, but the electronics bay is still sealed and ventilated separately. The hopper liner and bins are removable for cleaning.

## 3.6 Materials and finish

| Part | Material | Reason |
|---|---|---|
| Frame, drawer, lid | 18 mm plywood, sealed | Cheap, stiff, easy to cut; paint/seal for humidity |
| Hopper liner, bins | 3 mm PP or food-grade plastic | Wipe-clean, tough, low friction |
| Spout | 110 mm PVC 45° elbow | Smooth, cheap, available; sand internal joints |
| Funnel | 3 mm PP welded/bolted or PETG print | Smooth 59° walls; replaceable |
| Brackets | PETG 3D print | Camera, sensors, bearing collar, servo mount |
| Hinges | Stainless steel | Wet environment |
| Seals | Closed-cell silicone | Door and lid; not on load cells |
| Labels | Printed vinyl + icons | Colour + text + icon for accessibility |

## 3.7 User journey

1. User approaches; LED bar is green (idle).
2. User lifts the lid; LED turns white/blue.
3. User places one item on the hopper door and closes the lid.
4. LED pulses blue; app shows “scanning”.
5. Machine weighs and photographs; LED pulses amber.
6. Spout rotates; a short whirr; LED stays amber.
7. Door opens/closes; item drops; LED turns green; short beep.
8. App shows class, confidence, weight and bin.
9. If the bin is 90% full, LED turns orange and app shows “empty bin 2”.
10. If the machine is unsure, LED turns white and app asks the user to choose; the item stays in the hopper until the user confirms.

---
