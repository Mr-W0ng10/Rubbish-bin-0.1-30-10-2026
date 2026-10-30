# Smart Waste Sorting Bin
## Engineering Design Package — English Version

**A low-cost, vision-assisted, four-stream sorting bin for a final-year engineering project**

Version 1.0 · 29 October 2026

Prepared for a CCIT4080-style final-year project. This is a design and build package, not a submission-ready report. You must build, test, photograph and write up your own results.

---

# How to use this document

This package is deliberately more detailed than a typical project proposal. It gives you a complete, buildable design, the reasoning behind each choice, a costed bill of materials, dimensioned drawings, wiring tables, firmware/software architecture, calibration steps, a test plan and a schedule.

**Read it in three passes.**

1. **Pass 1 — understand the machine (Sections 1–3).** Read the problem, requirements, concept comparison and system overview. This is the material you need for your proposal presentation.
2. **Pass 2 — build it (Sections 4–6).** Use the drawings, cut list, pin table and build sequence. Do not order every part before you have checked the dimensions against your own bin and camera.
3. **Pass 3 — prove it (Sections 7–9).** Use the test plan, risk register and schedule. Your marks come from evidence of design decisions, build progress, testing and evaluation — not from a perfect-looking CAD model.

**What is fixed and what you should verify**

| Fixed design intent | Verify before cutting or ordering |
|---|---|
| Four streams: plastic bottle, metal, wet, dry/other | Your local bin sizes and available plastics |
| Top-loading weigh hopper with bottom door | Camera field of view with your actual lens |
| Four fixed bins + rotating spout | Bin supplier dimensions (the 190 × 190 mm internal size is nominal) |
| Raspberry Pi + ESP32 two-processor architecture | Local price and availability; a Pi 4 is a drop-in upgrade |
| 12 V SELV power, fused, e-stop | Battery certification and charger compatibility |
| Target cost ≤ HK$4,500 | Current street prices; use the lean substitutions if needed |

**A note on academic integrity.** Use this as an engineering reference. Measure your own parts, keep a logbook, record failures, and write your report in your own words. If your course requires disclosure of AI-assisted drafting, disclose it. Do not present a design you did not build and test as completed.

[CALLOUT:About the drawings|Figures in this document are A4 overviews. Full-resolution PNGs are in 02_Drawings; print Figures 3–5 at A3 when you need to read every dimension. The text tables are the authoritative build data.]

**Safety first.** The prototype uses 12 V, but a Li-ion pack can deliver very high fault current. Use a certified pack with a BMS, a fuse, a main switch and an e-stop. Do not charge the pack unattended inside the bin. Do not put sharp, hot, medical, or liquid waste into the prototype. This is an indoor demonstration machine, not a certified appliance.

---

# Contents

1. Project definition
2. Design exploration and decisions
3. System overview
4. Mechanical design
5. Electrical design
6. Firmware and software
7. Cost, procurement and resources
8. Build, test and evaluation plan
9. Limitations, future work and conclusion
Appendix A. Full bill of materials

Appendix B. Cut list

Appendix C. Pin and connector schedule

Appendix D. Serial protocol and API

Appendix E. Test record templates

Appendix F. References

**Quick navigation**

| If you need to… | Read |
|---|---|
| Explain the project in a proposal | Sections 1–3, Figures 1–2, BOM summary |
| Buy parts this week | Section 7, Appendix A, Appendix B |
| Cut and assemble the frame | Section 4, Figures 2–5, Appendix B |
| Wire the electronics | Section 5, Figures 6–7, Appendix C |
| Write the firmware/software | Section 6, Figure 8, Appendix D |
| Plan the tests and report | Section 8, Appendix E |

---

# 1. Project definition

## 1.1 The problem

Hong Kong’s waste problem is not only about landfill space. It is also about **contamination**: recyclables placed in the wrong bin, or food-soiled materials placed in recycling, reduce the value of the whole collection and can send an entire load to landfill. A well-designed bin cannot fix the whole system, but it can remove one common barrier — the user has to make a quick, confident decision at the point of disposal.

Most existing public bins are passive. They rely on labels, colours and the user’s knowledge. Research on recycling behaviour consistently shows that confusion about materials, unclear labels and inconvenience are major causes of contamination. A bin that **sees the item, weighs it, checks moisture/metal, decides a stream, and records the event** can make sorting more reliable and produce useful data for the building or campus. For Hong Kong waste and recycling context, see [1].

The project is a good final-year engineering vehicle because it combines:

- mechanical design (drawer, hopper, door, rotating spout, load path);
- embedded systems (ESP32, sensors, stepper/servo, safety interlocks);
- computer vision (dataset, transfer learning, TFLite);
- app/cloud/data (local web app, database, optional cloud sync);
- engineering evaluation (accuracy, cycle time, jam rate, cost, usability).

The design in this package is intentionally **low-cost and repairable**. It uses plywood, standard plastic bins, 3D-printed brackets, a Raspberry Pi Zero 2 W, an ESP32 and off-the-shelf sensors. It does not use a industrial PLC, a 6-axis robot, or a custom injection-moulded enclosure.

## 1.2 Project goal and objectives

**Goal:** design, build and evaluate a low-cost smart bin that sorts one item at a time into four streams — plastic bottle, metal, wet waste, and dry/other — using a camera and a small sensor suite, with a phone app that records each event.

| ID | Objective | How it will be measured |
|---|---|---|
| O1 | Classify four streams with at least 85% overall accuracy | 50-item mixed test, three runs, confusion matrix |
| O2 | Complete a sort cycle in 10 s or less (excluding user loading) | Stopwatch/log timestamps over 50 cycles |
| O3 | Achieve at least 90% successful sorts without a jam or manual reset | 50-cycle reliability test |
| O4 | Estimate bin fill level within ±10% of the measured fill height | Compare ToF estimate with ruler at 25%, 50%, 75%, 100% |
| O5 | Keep the build cost at or below HK$4,500 | Final BOM with receipts |
| O6 | Prevent actuator motion when the lid, drawer or hopper door is open; stop within 100 ms on e-stop | Interlock test, 10 trials each |
| O7 | Record time, class, confidence, weight, moisture, metal flag, bin ID and fill level; export CSV | App/database inspection |
| O8 | Produce a repeatable build and test record suitable for the final report | Logbook, photos, test sheets, code repository |

**Non-goals for version 1.0:** paper/glass as separate streams, compaction, odour control, outdoor weatherproofing, multiple items at once, sharp/medical waste, and a certified safety rating. These are future work, not failures.

## 1.3 Scope and operating envelope

| Item | Design value | Reason |
|---|---|---|
| Waste streams | Plastic bottle, metal, wet, dry/other | Four bins; simple, visible, useful |
| Item size | ≤ 250 mm long, ≤ 110 mm diameter | Fits the 110 mm spout and 290 × 240 mm door |
| Item weight | ≤ 1.5 kg | Keeps door servo torque and load cells comfortable |
| Loading | One item at a time, indoor, manual lid | Simple, safe, demonstrable |
| Bin capacity | ≈ 10.7 L usable per bin; ≈ 42.8 L total | 190 × 190 × 360 mm internal minus 80 × 80 mm notch |
| Cycle time | 6–9 s typical; ≤ 10 s target | Camera + inference + 90° spout move |
| Power | 12 V 6 Ah Li-ion (BMS) or 12 V 5 A adapter | Portable demo; bench testing |
| Environment | 10–35 °C, dry indoor | Prototype, not outdoor |
| Users | One user at a time; standing height | Loading lip ≈ 900 mm |

## 1.4 Requirements

### Functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR1 | Detect that an item has been placed in the hopper | ToF + weight; event within 1 s |
| FR2 | Capture a well-lit image of the item | Camera sees the full hopper floor; no clipping |
| FR3 | Classify into four streams plus an “unsure” outcome | Confidence and class returned by the model |
| FR4 | Fuse vision with weight, moisture and metal evidence | Decision table produces one bin or “ask user” |
| FR5 | Rotate the spout to the selected bin | ±3° repeatability; home verified |
| FR6 | Open the hopper door, dump the item, close it | 100 cycles without a jam; door limit confirmed |
| FR7 | Confirm the item left the hopper | Drop beam or door/weight change |
| FR8 | Measure and display bin fill level | Four ToF sensors; % and alert at 90% |
| FR9 | Record each event with timestamp, class, confidence, weight, moisture, metal, bin and fill | SQLite row; CSV export |
| FR10 | Provide a manual sort override in the app | User selects bin after confirmation |
| FR11 | Show status without a screen | RGB LED bar + buzzer + app |
| FR12 | Support safe stop and recovery | E-stop, lid/drawer interlocks, re-home |

### Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR1 | Cost | ≤ HK$4,500 recommended build; lean build ≤ HK$3,300 |
| NFR2 | Buildability | Hand tools + local cutting/3D printing; no welding |
| NFR3 | Maintainability | Bins and hopper liner removable without tools; sensors replaceable |
| NFR4 | Safety | 12 V SELV; fused; e-stop; no motion with guards open; rounded edges |
| NFR5 | Reliability | ≥ 90% successful cycles over 50 items; no missed steps after homing |
| NFR6 | Usability | Loading height 850–950 mm; one-hand lid; clear labels; app instructions |
| NFR7 | Noise | < 65 dB(A) at 1 m during a cycle |
| NFR8 | Hygiene | Smooth wipe-clean liner; drip tray; no sharp internal corners |
| NFR9 | Privacy | Camera images processed locally; no faces stored; optional cloud opt-in |
| NFR10 | Documentation | Drawings, BOM, pin map, calibration and test records |

### Constraints and assumptions

- The bin is built in a school workshop or at home with hand tools; tolerance is ±2 mm, not machine-shop precision.
- The camera looks down through a fixed lid; ambient light is controlled by a ring light.
- The user closes the lid before sorting; the machine refuses to move if the lid is open.
- The prototype is demonstrated indoors on a level floor.
- The app runs on a phone/laptop on the same Wi-Fi network; cloud is optional.
- The design uses metric fasteners and mm dimensions.

## 1.5 Success criteria

A successful prototype is not “the model trains to 99% on my dataset”. It is a machine that:

1. sorts a mixed set of 50 real items with ≥85% overall accuracy and no unsafe behaviour;
2. completes ≥90% of cycles without a jam;
3. records every event correctly;
4. can be built and repaired by one student with the specified tools;
5. stays within the budget;
6. produces evidence — photos, logs, confusion matrix, timings, failure notes — that you can defend in the report and viva.

## 1.6 Standards, safety and academic context

This is a prototype, not a certified product. Still, design to good practice:

- **Electrical:** 12 V SELV; fuse on the battery positive; separate buck converters; strain relief; no exposed conductors; e-stop in the actuator supply.
- **Battery:** certified 3S pack with BMS; charge outside the enclosure; fire-resistant bag; no unattended charging.
- **Machinery:** guard the lid hinge, drawer, door and spout; limit switches; no operation with guards open; round or cover sharp edges.
- **Hygiene:** removable PP liners; silicone seals; drip tray; clean after wet-waste tests; gloves.
- **Data:** local-first; no personal data; camera images can be deleted; app access on a private network.
- **Academic:** cite sources; keep a logbook; record failures; do not claim features you did not test.

---
