# Modeling Assumptions & Data Usage Note

## Dataset usage decision
This project does **not** ingest the NREL Workplace Charging dataset directly. The dataset is referenced as a credible source for realistic charging behavior, but integrating it end‑to‑end (cleaning, filtering, fitting, and validating a curve) was out of scope for this simulation deliverable.

## Simplified charging curve rationale
Instead, the model uses a **SoC‑dependent tapering power curve** that reflects typical DC fast‑charging behavior:
- High power at low SoC (near 0–50%).
- Gradual taper between mid‑range SoC (about 50–80%).
- Lower power above 80% SoC.

This curve is implemented in `ev_charging_model.py` as a piecewise function and yields charging times that are consistent with public NREL charging‑curve descriptions.

## Why this still approximates NREL behavior
NREL datasets and PyChargeModel show that DC fast‑charging does not remain constant power; it tapers as the battery approaches higher SoC. The simplified curve captures that dominant shape and therefore **approximates typical NREL behavior** without performing explicit curve fitting on the dataset.

If direct dataset integration is required later, the existing curve can be replaced with a data‑driven function (e.g., fitted spline or empirical average power‑vs‑SoC curve) while keeping the rest of the simulation unchanged.
