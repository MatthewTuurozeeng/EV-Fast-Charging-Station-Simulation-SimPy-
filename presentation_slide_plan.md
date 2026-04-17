# Presentation Slide Plan — EV Fast‑Charging Station Simulation (10 minutes)

**Audience:** Lecturer + students
**Goal:** Highlight deliverables, demonstrate a functional demo, and align with the grading rubric.
**Total time:** ~10 minutes (≈ 10 slides, with a 2-minute live demo)

---

## What I changed and why

- Aligned slide contents to the notebook (`part1_simulation_notebook.ipynb`) and the report (`FINAL_REPORT.md`).
- Added exact key metrics (from the report and notebook), explicit demo steps referencing notebook cell numbers (so you can run them live), and stronger rubric mapping so reviewers can see how each part is assessed.

---

## Slide 1 — Title & Context (0:30)

Content:

- Title: "EV Fast‑Charging Station Simulation with Dynamic Pricing (SimPy)"
- Author: Matthew Tuurozeeng — Course + date
- One‑line goal: Simulate a highway rest stop (6 DC fast chargers) and compare fixed vs dynamic pricing.

Speaker note: brief two‑line intro and what the demo will show.

---

## Slide 2 — Problem & Objectives (0:45)

Content:

- Short problem statement: customer wait, congestion, pricing as a control lever.
- Objectives (bulleted): build DES, compare fixed vs dynamic pricing, measure queue/wait/utilization/revenue.

Rubric mapping: Model correctness; Predictions & insights.

---

## Slide 3 — Deliverables & Repo (0:30)

Content:

- Files delivered: `part1_simulation_notebook.ipynb` (analysis + plots), `ev_charging_model.py` (core functions), `run_simulation.py` (runner), `FINAL_REPORT.md`, `ASSUMPTIONS.md`.
- How to reproduce: run the notebook top→bottom or use `run_simulation.py`.

Rubric mapping: Communication & reproducibility (10%).

---

## Slide 4 — Data & Input Modeling (1:00)

Content (concise):

- Arrival process: Poisson arrivals → exponential inter‑arrival times. (Mean λ = 12 EV/hour in default scenario.)
- SoC at arrival: Beta(2,4), clipped to [0.05, 0.95].
- Charging curve: tapering DC fast‑charging approximation (high power at low SoC, tapering above ~50%).
- Pricing rule: base price $0.40/kWh; surge = base × (1 + 0.5) when queue > 3; balk prob = 0.15 on surge.

Rubric mapping: Data use & input modeling (25%).

---

## Slide 5 — Model Design & Verification (1:00)

Content:

- SimPy structure: arrival process, EV process (compute charge, price, optional balk, request charger, charge, depart).
- Resource handling: `simpy.Resource` with capacity = number_of_chargers.
- Logging and metrics: queue & utilization time series, wait times, charging times, revenue (noted in notebook).
- Quick verification: observed wait times and utilization are in sensible ranges (face validity checks described in `FINAL_REPORT.md`).

Rubric mapping: Model correctness (25%).

---

## Slide 6 — Baseline Results (0:45)

Content:

- Use numbers reported in `FINAL_REPORT.md`:
  - Average queue length: ~0.009
  - Maximum queue length: 2
  - Avg waiting time: ~0.004 hours (~15 seconds)
  - Average utilization: ~0.53
  - Revenue (approx.): ~1843 (computed by the simplified revenue formula in notebook)
- Main point: under default parameters, station is lightly loaded; dynamic pricing rarely triggers.

Rubric mapping: Predictions & insights (25%).

---

## Slide 7 — Dynamic Pricing & Managerial Insight (0:45)

Content:

- Show comparison table (baseline vs dynamic) from the notebook.
- Emphasize interpretation: pricing has minimal effect when system under capacity; effective when system near/above capacity.

Rubric mapping: Predictions & insights; managerial implications.

---

## Slide 8 — Sensitivity / High‑Demand Scenario (1:00)

Content:

- Explain the high‑demand experiment used in the notebook: increased λ (24/hr), fewer chargers (4), lower surge threshold.
- Show the divergence metrics and visuals: queue spikes, more frequent surge activation, increased balking.

Rubric mapping: Validation & sensitivity (15%).

---

## Slide 9 — Key Visualizations (0:45)

Content (pick 2–3 visuals with short captions):

- Queue length vs time (fixed vs dynamic)
- Charger utilization vs time (fixed vs dynamic)
- Price over time & queue overlay (dynamic scenario)

Rubric mapping: Communication & reproducibility.

---

## Slide 10 — Live Demo (2:00)

Purpose: run the minimal cells to reproduce the key results and show the high‑demand divergence.

Exact demo steps (by notebook cell number):

1. Open `part1_simulation_notebook.ipynb`.
2. Run Cell 15 — this runs the baseline and dynamic scenarios (params + run_simulation_scenario). (Allow ~30–40s for cells to run if not precomputed.)
3. Run Cell 17 — shows the summary comparison table (comparison_df).
4. Run Cell 19 — displays the primary time‑series plots for dynamic pricing (queue/utilization/price).
5. (Optional) For the high‑demand demo, run Cell 21 (set high_demand_params and run scenarios) then Cell 23 (high comparison table) and Cell 26 (high‑demand plots) to show surge behavior.

Backup plan: If runtime is slow or plotting fails, show the pre‑rendered images already present in the executed notebook cells (cells with stored plot outputs). These are available in the notebook; mention them and narrate the expected change.

Demo tips:

- Pre‑run once locally before the presentation so execution is faster and verify packages (`simpy`, `numpy`, `pandas`, `matplotlib`) are available.
- Keep only the notebook visible; minimize terminal output.

---

## Slide 11 — Validation, Limitations & Next Steps (0:45)

Content:

- Validation: face validity, parameter sweeps, and high‑demand test show expected responses.
- Limitations: simplified charging curve (no direct NREL ingestion), static arrival process (no time‑of‑day), single 24‑hour horizon.
- Next steps: incorporate real datasets (NREL), model time‑varying arrivals, test alternative elasticities for balking.

Rubric mapping: Validation & sensitivity.

---

## Slide 12 — Conclusion & Q&A (0:30)

Content:

- One‑line takeaway: “Dynamic pricing controls congestion when the station is near capacity; otherwise it has little effect.”
- Invite questions and point to the repo for reproducibility.

---

## Appendices (speaker notes & rubric mapping)

- Quick mapping to rubric items so examiners can cross‑check slides:
  1. Data use & input modeling (25%): Slide 4 — explain Poisson + Beta SoC + charging curve + pricing.
  2. Model correctness (25%): Slide 5 — SimPy structure, resources, logging, checks.
  3. Predictions & insights (25%): Slides 6–8 — baseline, dynamic, sensitivity results & managerial insights.
  4. Validation & sensitivity (15%): Slide 8 and Slide 11 — high‑demand experiments + next steps.
  5. Communication & reproducibility (10%): Slides 3 & 9 — repo contents and reproducible plots.

## Quick rehearsal checklist

- Open notebook, run cells 15, 17, 19 (and 21, 23, 26 for high demand) ahead of time.
- Keep backup screenshots of plots in a single folder inside the repo (e.g., `slides_assets/`) in case live plotting fails.
- Ensure `presentation_slide_plan.md` and `FINAL_REPORT.md` are available in the repository to show reproducibility.

---

## File saved

- `presentation_slide_plan.md` (this file) — revised and aligned with notebook & report.

If you want, I can also: produce a slide deck (PowerPoint `.pptx`) with these slides prefilled, or generate a Google Slides-compatible outline. Tell me which you prefer and I will create it next.
