# EV Fast-Charging Station Simulation (SimPy)

This project models a highway rest stop with **6 DC fast chargers** and implements **dynamic pricing** when the queue exceeds 3 vehicles. It compares a baseline fixed-price scenario to a dynamic-pricing scenario.

## What’s inside
- `ev_charging_model.py`: core simulation model and helpers.
- `ev_charging_simulation.ipynb`: notebook walkthrough with plots.
- `part1_simulation_notebook.ipynb`: Part 1 model with explanations (all-in-notebook).
- `run_simulation.py`: quick runner that prints summary metrics.
- `solution_plan.md`: solution design and modeling plan.
- `ASSUMPTIONS.md`: data usage note and modeling assumptions.
- `FINAL_REPORT.md`: draft analytical report (2–3 pages).

## Quick start
1. Create and activate a Python environment (3.10+ recommended).
2. Install dependencies.
3. Open the notebook and run all cells.

## Notes
- The charging-time model uses a simplified SoC-dependent power curve. You can replace it with NREL/PyChargeModel data if desired.

## Sources
- NREL Workplace Charging Data: https://catalog.data.gov/dataset/workplace-charging-data-c0796
- PyChargeModel (NREL): https://github.com/NREL/PyChargeModel
- SimPy docs: https://simpy.readthedocs.io/en/latest/
