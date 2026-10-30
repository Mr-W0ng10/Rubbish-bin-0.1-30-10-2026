# 4. Mechanical design

## 4.1 Overall dimensions and frame

[FIG:fig04_exploded.png|Figure 5. Exploded assembly. Build from the base up; test the drawer, hopper and spout before final assembly.|155]

The bin is a 480 × 480 × 940 mm plywood box with four functional layers. The dimensions are chosen around standard 12 L plastic bins and a 110 mm PVC spout, not around a fancy enclosure.

| Layer | Height (mm) | What is inside | Access |
|---|---:|---|---|
| Feet | 20 | Rubber feet, floor clearance | Bottom |
| Electronics bay | 100 | Pi, ESP32, bucks, fuse, driver, terminals | Rear/front vented panel |
| Bin drawer | 400 | 4 bins, drawer slides, drip tray | Pull-out front |
| Mid-frame | 80 | Load cells, funnel, bearing, spout | Top/inside |
| Weigh hopper | 300 | Hopper, door, moisture pad, metal coil | Lift lid |
| Lid | 40 | Camera, LED ring, item ToF, reed switch | Hinged at back |
| **Total** | **940** | | |

**Frame construction:** 18 mm plywood panels joined with M4 screws and 20 × 20 mm aluminium angle or wooden cleats. Seal all internal surfaces with a water-resistant varnish or self-adhesive PP sheet. Do not rely on glue alone for the load-bearing joints; use screws and cleats.

**Why plywood rather than 2020 extrusion:** plywood is cheaper, easier to cut, and dampens vibration. It is also easier to repair. The trade-off is that wood moves with humidity; seal it and use slotted holes for the mid-frame and load-cell mounts so you can re-align.

**Access:** the front drawer holds all four bins. The electronics bay has a separate vented cover; do not put the electronics in the bin drawer. The hopper liner lifts out; the lid is held open by two 60 N gas struts or a friction stay.

## 4.2 Bin drawer and bins

The top view in Figure 4 shows the 2 × 2 layout and the corner notches. The key dimensions are:

### Geometry

- Bin **outer** size: 210 × 210 × 380 mm.
- Bin **internal** size: 190 × 190 × 360 mm.
- Each bin has an **80 × 80 mm notch** cut into its inner top corner. The four notches create a 160 × 160 mm clear central area for the 150 mm bearing and the funnel.
- Bin centres: **(±117, ±117) mm** from the drawer centre. The outer footprint is 444 × 444 mm.
- Drawer: **456 × 456 × 380 mm** outer, on a pair of 450 mm three-fold slides rated ≥45 kg. Clearance: 6 mm per side.
- Drawer front: 480 × 400 mm, with a handle and a magnetic catch.

**Capacity calculation:**

\[
V = (190 \times 190 - 80 \times 80) \times 360 = 10.69 \times 10^6\ \text{mm}^3 \approx 10.7\ \text{L}
\]

Four bins give **≈ 42.8 L**. That is enough for a demonstration and a few days of light household use. If you need more capacity, increase the bin height to 450 mm; the frame height becomes 1030 mm, which is still usable.

### Bin fabrication

The cheapest route is to buy four 12 L PP storage boxes of approximately 190 × 190 mm internal and cut the notch. Cutting a notch in a moulded bin leaves an open edge; seal it with a PP patch and neutral silicone, or 3D-print a corner insert that closes the notch. A neater route is to fabricate the bins from 3 mm PP sheet: bottom, four walls, and a notch wall. This is more work but gives a clean, sealed bin.

**Do not** use cardboard or bare wood for the bins; wet waste will destroy them.

### Drawer details

- Slides: one pair, 450 mm, 45 kg rated, mounted at the drawer sides. The drawer must not tip when pulled fully out; add a stop or a support foot.
- Bin locating: 20 mm plywood cleats or 3D-printed corner blocks; leave 2 mm clearance so the bins drop in.
- Bin-present detection: a **reed switch** on the fixed frame and a small magnet on each bin. This avoids wiring to the moving drawer. The reed closes when the bin is inserted; the ESP32 reads it through a PCF8574.
- Drawer-closed switch: a lever microswitch on the frame; the machine refuses to sort if the drawer is open.
- Drip tray: a 456 × 456 mm PP tray with a 20 mm lip, removable. Drill a few 6 mm drain holes in the drawer bottom and put a absorbent pad under the tray.
- Label each bin on the front and top: colour + icon + English/Chinese text. Do not rely on colour alone.

### Cleaning

Lift the bins out; wipe the drawer and drip tray with a disinfectant wipe. Remove the hopper liner and wash it in warm soapy water. Do not hose the electronics bay. Let everything dry before reassembly.

## 4.3 Weigh hopper and door

### Load path

The hopper is a 360 × 360 × 300 mm plywood box with a 320 × 320 × 260 mm PP liner. It sits on a 360 × 360 mm support plate, which rests on **four 5 kg load cells** at a 300 × 300 mm bolt pattern. The load cells are bolted to the mid-frame. The hopper must be free to move vertically but restrained horizontally:

- use M5 shoulder screws or dowel pins through oversized holes for horizontal location;
- leave 0.5–1 mm vertical clearance;
- do not connect the hopper to the frame with a rigid pipe, cable gland, or earth strap that bypasses the cells;
- route the servo and sensor cables with a service loop so they do not carry load.

**Capacity check:** hopper + door + servo + liner ≈ 3.5 kg tare; item ≤ 1.5 kg; four 5 kg cells give 20 kg capacity. Even with an off-centre item, each cell sees less than 5 kg. The safety factor is >4.

**Resolution:** HX711 at 10 Hz or 80 Hz; with 5 kg cells, 1 g resolution is achievable after calibration. Use a 10-sample median and a 5-sample moving average. Tare at the start of every cycle.

### Door

- Door: 290 × 240 mm, 6 mm PP or plywood, hinged at the back.
- Opening: 70°; the item slides out because the hopper floor slopes 5° toward the door.
- Seal: closed-cell silicone gasket around the door; the door must not leak rice or crumbs into the mid-frame.
- Actuation: 25 kg·cm metal-gear servo (DS3225MG or equivalent), mounted **outside** the hopper on a bracket. A 50 mm arm pulls a 1 mm stainless cable; a spring returns the door closed.
- Spring: a tension spring or a torsion spring at the hinge. On power loss, the spring closes the door. The servo only pulls it open.
- Limit switch: a lever microswitch confirms “door closed”. The machine will not weigh or rotate unless the door is closed.
- Hinge: stainless piano hinge or two nylon bushes; no metal particles near the metal coil.

**Torque check:** door mass ≈ 0.5 kg at 0.145 m → 0.71 N·m; item 1.5 kg at 0.145 m → 2.13 N·m; total ≈ 2.84 N·m. A 25 kg·cm servo is 2.45 N·m at the shaft. With a 50 mm arm and a cable attached 145 mm from the hinge, the mechanical advantage is 145/50 = 2.9, so the available door torque is ≈ 7.1 N·m; safety factor ≈ 2.5. The spring assists closing and carries the door when power is off. If you regularly sort 1.5 kg items, upgrade to a 35 kg·cm servo or a 12 V worm-gear motor.

**Do not** rely on the servo to hold the door closed when idle; use the spring and a mechanical stop so the servo can be disabled.

### Moisture pad

A capacitive soil-moisture sensor is mounted under a 1.5 mm HDPE cover on the door, at the centre. The item rests on the cover; water from wet waste changes the capacitance. The sensor is not in direct contact with waste, so it is easy to clean.

- Cut a 60 × 30 mm window in the door, mount the sensor PCB flush, and seal the edges with neutral silicone.
- Cover with a replaceable 1.5 mm HDPE sheet; tape the edges with PP tape.
- Route the 3-wire cable along the hinge with a silicone service loop.
- Calibrate dry (air) and wet (damp sponge) and set a threshold with hysteresis (e.g., wet > 0.65, dry < 0.45).
- Replace the cover if it is scratched or stained.

**Limitation:** a dry plastic bottle with a wet label may read “wet”; a wet item inside a sealed bag may read “dry”. The moisture sensor is evidence, not a verdict. The vision model and weight are the primary classifiers.

### Metal coil

A DIY inductive metal-detector kit is mounted on the **fixed mid-frame**, centred under the hopper door, facing up. The coil is 150 mm diameter, wound with 30 turns of 0.5 mm enamelled copper wire, and tuned to the kit. The door is 6 mm PP; the field passes through it. The item can be anywhere on the door within the coil area.

- Keep the coil at least 40 mm from steel screws, the load cells, and the servo; use nylon standoffs.
- Shield the coil with aluminium foil only on the back, not the front; ground the foil to the module ground.
- Calibrate with the hopper empty, then with a known can at the centre and at the edge.
- The module output is digital (metal/no metal); the ESP32 reads it through a GPIO or the PCF8574.
- If the coil is unreliable, leave it out and rely on vision + weight; document the limitation honestly.

**Why not a small inductive proximity sensor?** A typical LJ12A3-4-Z/BX only detects metal within 4 mm of its face. A can lying 50 mm away on the door will not be detected. A large coil is the only low-cost way to cover the door area.

## 4.4 Funnel, bearing and rotating spout

### Funnel

- Inlet: 280 × 260 mm, matching the door opening.
- Outlet: 110 mm diameter.
- Height: 140 mm; wall angle ≈ 59° from horizontal.
- Material: 3 mm PP, welded or bolted with silicone seals; or PETG printed in four sections and solvent-welded.
- The funnel must be smooth inside; sand all joints and avoid ledges where a bottle cap can catch.
- The funnel is fixed to the mid-frame, not the hopper. The hopper door drops the item into the funnel; the funnel does not touch the hopper.

**Why 110 mm?** A typical 500 mL PET bottle is 60–65 mm diameter; a 1.5 L bottle is 85–90 mm; a 330 mL can is 66 mm. A 110 mm outlet passes these with clearance. A 2 L bottle (≈110 mm) is tight; label the bin as “≤1.5 L” and test.

### Bearing and spout

- Bearing: 150 mm OD lazy Susan bearing, 5 mm thick, mounted on the mid-frame around the funnel outlet.
- Spout: 110 mm PVC 45° elbow, cut and sanded; the upper opening is centred under the funnel outlet; the lower outlet is at **radius 130 mm**.
- Collar: 3D-printed PETG ring clamped to the bearing inner ring; the elbow is fixed to the collar with stainless screws and silicone.
- Drive: NEMA 17 stepper, 3:1 GT2 belt (20T motor, 60T spout), 200 mm belt. The stepper is mounted on the mid-frame with a slotted bracket for belt tension.
- Home: a slotted optical switch or lever microswitch at 45° (bin 1). A flag on the collar interrupts the switch.
- Positions: bin 1 = 45°, bin 2 = 135°, bin 3 = 225°, bin 4 = 315°. Always approach the target clockwise to remove backlash.
- Guard: a clear 3 mm PP ring around the spout, with a 20 mm gap for inspection; it prevents fingers from reaching the pinch point.

**Geometry check:** bin centres are at (±117, ±117) mm, radius 165 mm. The spout outlet is at 130 mm, so the drop point is 35 mm inside the bin centre. The bin opening is 190 mm, so the drop is well inside. The 80 × 80 mm notches give clearance for the 150 mm bearing and the 110 mm outlet.

**Stepper calculation:**

- Spout + collar mass ≈ 0.35 kg; centre of mass at 0.13 m → 0.45 N·m.
- Bearing friction + belt preload ≈ 0.08 N·m; acceleration ≈ 0.05 N·m.
- Required ≈ 0.58 N·m. NEMA 17 (0.45 N·m) × 3:1 = 1.35 N·m; safety factor ≈ 2.3.
- Steps: 200 full steps/rev × 8 microsteps × 3 = 4800 steps/rev; 90° = 1200 steps.
- Speed: 1200 steps/s with acceleration limiting; 90° move ≈ 1.0 s + 0.3 s acceleration.
- Current: 0.8 A; A4988 Vref = 0.64 V with Rs = 0.1 Ω. Use 1/8 microstep.

**Homing:** on boot and after any fault, rotate clockwise until the home switch triggers, then back off 20 steps and approach slowly. This gives repeatable home without a encoder.

## 4.5 Lid, camera and lighting

### Lid

- 480 × 480 mm, 18 mm plywood with a 3 mm acrylic window or a camera hole.
- Hinged at the back with a stainless piano hinge; two 60 N gas struts or a friction stay hold it open.
- A closed-cell foam gasket seals against the top frame to block ambient light.
- A magnetic reed switch detects “lid closed”. The machine will not sort if the lid is open.
- A front handle and a clear “OPEN / CLOSE” label.

### Camera

- 5 MP USB UVC camera, 90° diagonal field of view, manual focus, 1 m cable.
- Mounted on the underside of the lid, centred over the hopper, lens **228 mm above the door**.
- 3D-printed bracket with a 30 mm hole; the lens sits behind a 2 mm clear acrylic window (anti-glare, replaceable).
- USB cable routed through a 25 mm grommet at the hinge, with a 300 mm service loop and a strain relief. USB is used instead of a Pi camera ribbon because it survives repeated lid motion and is easy to replace.

**Field of view check:** a 90° diagonal lens on a 4:3 sensor gives about 77° horizontal and 62° vertical. At 228 mm:

\[
W = 2 \times 228 \times \tan(38.5^\circ) \approx 368\ \text{mm},\quad
H = 2 \times 228 \times \tan(31^\circ) \approx 276\ \text{mm}
\]

The hopper is 320 × 260 mm, so the camera sees the whole door with a small margin. If your lens is 75°, raise the camera to 260 mm or use a wider lens; check with a printed grid before cutting the lid.

### Lighting

- 12 V 3 W LED ring, 80 mm inner diameter, 6000 K, CRI > 90, with a white acrylic diffuser.
- Mounted around the camera, 20 mm above the lens; the ring is always on during capture (not PWM-dimmed) to avoid flicker.
- Matte black inside the hopper; no shiny screws or labels in the field of view.
- If plastic bottles glare, add a circular polarizer film or move the ring further from the lens. Fix the camera exposure and white balance in software; do not rely on auto-exposure.

## 4.6 Sensor placement

| Sensor | Location | Orientation | Range / interface | Why there |
|---|---|---|---|---|
| USB camera | Lid centre, 228 mm above door | Down | 0.2–2 m / USB | Full view of item; fixed geometry |
| Item ToF (VL53L0X) | Lid, 60 mm from camera | Down | 30–1000 mm / I2C | Confirms item presence and height; robust to shadows |
| IR break-beam | Hopper mouth, 20 mm below top lip | Across opening | 0–300 mm / GPIO | Detects a hand or protruding item; safety |
| Load cells ×4 | Under hopper support plate | Vertical | 0–5 kg each / HX711 | Weight; confirms real item; class prior |
| Moisture pad | Door centre, under HDPE | Up | Capacitive / ADC | Wet vs dry evidence |
| Metal coil | Mid-frame under door | Up | 150 mm coil / digital | Metal confirmation anywhere on door |
| Bin ToF ×4 | Mid-frame, outer corner of each bin | Down | 40–2000 mm / I2C | Fill level; no cross-talk |
| Lid reed | Front lip | — | Digital / PCF8574 | Lid closed interlock |
| Door switch | Hopper front | — | Digital / PCF8574 | Door closed before weigh/move |
| Drawer switch | Bin frame | — | Digital / PCF8574 | Drawer closed interlock |
| Spout home | Mid-frame at 45° | — | Digital / PCF8574 | Home reference |
| Bin present ×4 | Fixed frame, one per bin | — | Reed / PCF8574 | Refuses to sort into a missing bin |
| SHT31 | Bin section back wall | — | I2C | Temperature/humidity log (optional) |
| E-stop | Front panel | — | NC + opto / GPIO | Cuts actuator 12 V; status to ESP32 |

**Placement rules:**

- Keep the camera and item ToF away from the LED ring’s direct reflection; use a diffuser and a matte black surround.
- Keep the load-cell cables away from the stepper and servo cables; cross at 90° if unavoidable.
- Mount the bin ToF sensors at the **outer corners** of each bin, outside the spout’s swept area, so falling waste cannot hit them. Use a 1 mm clear window and a small hood.
- Do not mount the metal coil on the hopper; it must not affect the load cells.
- Put the SHT31 away from the wet bin and the electronics heat.

## 4.7 Actuator and structure sizing

| Item | Calculation | Result |
|---|---|---|
| Load cells | 4 × 5 kg = 20 kg; tare 3.5 kg; item 1.5 kg; off-centre factor 1.5 | Safety factor >4 |
| Door servo | 2.84 N·m load; 2.45 N·m servo × 2.9 mechanical advantage ≈ 7.1 N·m | Safety factor ≈ 2.5 |
| Stepper | 0.58 N·m required; 0.45 N·m × 3 = 1.35 N·m | Safety factor ≈ 2.3 |
| Spout bearing | 0.35 kg spout + 1.5 kg item; 150 mm lazy Susan rated >10 kg | Adequate |
| Lid struts | 2 × 60 N; lid ≈ 2 kg | Holds lid open; check closing force |
| Drawer slides | 45 kg pair; drawer + bins + waste ≈ 12–18 kg | Safety factor >2.5 |

**Deflection check:** the 18 mm plywood mid-frame spans 480 mm and carries the hopper (≈5 kg) plus a 1.5 kg item. The deflection is small (<1 mm) for a 480 mm span with 18 mm plywood; if you use 12 mm plywood, add a centre rib. The bin drawer bottom must be stiff enough not to sag under 15 kg; use 18 mm plywood or add a 20 × 40 mm rib.

## 4.8 Tolerance, alignment and adjustment

- **Bin locating:** use cleats with 2 mm clearance; the bins must drop in without force but not move when the drawer closes.
- **Spout alignment:** slot the stepper bracket by 5 mm for belt tension; slot the bearing mount by 3 mm for centring. Check the drop point with a laser pointer or a plumb line.
- **Hopper:** slot the load-cell mounting holes by 2 mm; shim the support plate so the door is level within 1 mm.
- **Lid:** use a hinge with 2 mm adjustment; the gasket should compress evenly.
- **Camera:** print a grid target at the door height and check that the whole hopper is inside the frame; adjust the bracket height by ±10 mm.
- **Homing:** after assembly, home 20 times and record the switch position; repeatability should be within ±2 steps.

## 4.9 Build sequence

1. **Cut and seal the plywood.** Label every panel with its part number. Drill pilot holes before assembly.
2. **Build the base and electronics bay.** Fit the vent, cable glands, power switch, e-stop and service USB port. Do not install electronics yet.
3. **Fit the drawer slides and drawer.** Check that the drawer pulls out 400 mm without tipping. Fit the drip tray and bin cleats.
4. **Make the bins.** Cut the 80 × 80 mm notches; seal the cut edges; fit handles and labels. Check that all four drop into the drawer.
5. **Build the mid-frame.** Mount the load cells, funnel, bearing and spout. Check that the spout rotates 360° without hitting anything.
6. **Build the hopper.** Fit the door, hinge, gasket, servo, spring, moisture pad and metal coil. Check that the door closes squarely and the spring closes it with power off.
7. **Fit the hopper to the mid-frame.** Check that it floats freely on the load cells; no cable or pipe should bypass the cells.
8. **Fit the lid.** Mount the camera, LED ring, item ToF and reed switch. Set the camera height and focus. Check the field of view with a grid.
9. **Wire the electronics on the bench.** Test each sensor and actuator separately before installing them in the bin.
10. **Install the electronics.** Use the acrylic mounting plate; label every cable; strain-relieve; keep power and signal separate.
11. **Calibrate.** Load cells, moisture, metal, bin ToF, camera exposure, spout home.
12. **Dry-run.** Run 20 cycles with empty/dry items; then 20 with rice; then 20 with real dry recyclables; only then test wet waste.

## 4.10 Cut list

The full cut list is in Appendix B. Key panels:

| Part | Size (mm) | Qty | Material |
|---|---|---:|---|
| Base | 480 × 480 | 1 | 18 mm plywood |
| Base front/back | 480 × 100 | 2 | 18 mm plywood |
| Base sides | 444 × 100 | 2 | 18 mm plywood |
| Bin section sides | 480 × 400 | 2 | 18 mm plywood |
| Bin section back | 444 × 400 | 1 | 18 mm plywood |
| Bin section top/bottom | 480 × 480 | 2 | 18 mm plywood |
| Drawer bottom | 456 × 456 | 1 | 18 mm plywood |
| Drawer sides | 456 × 360 | 2 | 18 mm plywood |
| Drawer front | 480 × 400 | 1 | 18 mm plywood |
| Hopper support plate | 360 × 360 | 1 | 18 mm plywood |
| Mid-frame | 480 × 480 | 1 | 18 mm plywood |
| Lid | 480 × 480 | 1 | 18 mm plywood + 3 mm acrylic |
| Hopper door | 290 × 240 | 1 | 6 mm PP/plywood |
| Spout guard | 300 × 200 | 1 | 3 mm PP |
| Drip tray | 456 × 456 | 1 | 3 mm PP |

**Cutting tips:** cut the drawer and bins first, then fit the frame around them. Leave 1–2 mm clearance; you can shim but you cannot shrink. Drill pilot holes for all screws; plywood splits easily.

## 4.11 Safety guards and pinch points

- **Lid hinge:** cover the hinge line with a 3 mm PP strip; add a gas strut or friction stay so the lid cannot fall on a hand.
- **Drawer:** add a stop so it cannot be pulled completely out; a 45 kg slide pair is strong enough, but the bin can tip if the drawer is overloaded.
- **Hopper door:** the door closes with a spring; keep fingers out of the 70° arc. The lid must be closed to run, so the user cannot reach the door during motion.
- **Spout:** a clear PP guard ring around the rotating spout; a 20 mm inspection gap. The spout is inside the bin section and the drawer must be closed to run.
- **E-stop:** mushroom head, red, latching, on the front panel; label “STOP MOTION / 停止動作”. It cuts 12 V to the stepper, servo and LED; the Pi/ESP32 stay on 5 V for logging.
- **Fuse:** 5 A blade fuse within 150 mm of the battery positive.
- **Edges:** round or cover all plywood edges; seal them so they do not swell.
- **Lifting:** the empty bin is 22–26 kg; lift with two people or use the base handles. Do not lift by the lid.

## 4.12 Cleaning and maintenance

| Task | Frequency | Method |
|---|---|---|
| Empty bins | When 90% full | Lift out; rinse; dry |
| Wipe hopper liner | After wet waste | Warm soapy water; dry fully |
| Clean camera window | Weekly | Microfibre + lens cleaner; no solvent |
| Check spout/funnel | Weekly | Remove guard; inspect for jam; wipe |
| Check load cells | Monthly | Verify tare; check cables; no debris |
| Check door gasket | Monthly | Replace if torn; silicone-safe cleaner |
| Check battery | Each use | Voltage; swelling; BMS; charge outside |
| Check fasteners | Monthly | M4/M5 screws; drawer slides; hinge |
| Recalibrate | After moving or major repair | Load cell, moisture, bin ToF |

**Spare parts to keep:** one servo, one A4988, one HX711, one ToF sensor, fuses, silicone gasket, PP sheet offcuts. These are cheap and save a demo.

---
