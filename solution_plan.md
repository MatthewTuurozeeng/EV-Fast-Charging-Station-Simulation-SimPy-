# EV Fast-Charging Station with Dynamic Pricing — Solution Plan

**Project date:** 2 April 2026

## Problem Understanding (from the brief)
We must build a **discrete-event simulation** of a highway rest stop with **6 DC fast chargers**. EVs arrive with varying **State of Charge (SoC)** that drives **charging duration**. A **dynamic pricing rule** increases price when queue length > 3. We must compare baseline fixed-price vs dynamic pricing, and report queue length, waiting time, charger utilization, and optional revenue/abandonment metrics.

##  Recommended Model Type (and justification)
**Model:** *Discrete-Event Simulation (DES) with queueing system and resource constraints* using **SimPy**.

**Justification:**
- Charging stations are discrete resources (6 chargers) and arrivals are event-driven.
- Vehicles wait in a queue, acquire a charger, charge for a duration, then depart.
- Pricing policy changes based on queue length at arrival (event-based) which DES models naturally.
- SimPy is designed for this and has official examples for similar problems.

## System Contract (inputs → outputs)
**Inputs:** arrival rate & distribution, SoC distribution, charging curve or charging-time function, pricing policy, number of chargers.

**Outputs:** time series of queue length, utilization, price; summary stats (avg/max wait, avg/max queue length, utilization, revenue, abandonment).

**Success criteria:** simulation runs for a defined horizon; both scenarios compared with visualizations and metrics.

---

## Core Model Design
### **Entities**
- **EV (vehicle process)**
- **Charging Station (resource)**

### **State Variables (system-level)**
- $Q(t)$ = queue length at time $t$
- $U(t)$ = number of chargers busy (0–6)
- $P(t)$ = price level at time $t$ (baseline price or surge price)
- $N_{served}$ = number of vehicles that completed charging
- $N_{left}$ = number of vehicles that leave without charging (if modeled)
- $R$ = cumulative revenue (if included)

### **EV-Level Variables**
- $SoC_{arr}$ = state of charge at arrival
- $E_{need}$ = energy required to reach target SoC
- $T_{charge}$ = charging duration (function of SoC and curve)
- $T_{wait}$ = waiting time in queue

### **Parameters (explicit)**
- **Number of chargers:** $C = 6$
- **Arrival process:** choose Poisson process with rate $\lambda$ vehicles/hour
- **SoC distribution:** e.g., Beta or truncated normal (to be fitted or assumed)
- **Charging curve parameters:** from NREL dataset or PyChargeModel
- **Target SoC:** e.g., 80% or 100%
- **Baseline price:** $p_0$ (e.g., $0.40/kWh$)
- **Surge price factor:** $p_1 = p_0 \times (1 + \alpha)$ when $Q(t) > 3$
- **Price sensitivity (optional):** probability of balking or lower arrival rate under surge pricing
- **Simulation horizon:** e.g., 24 hours or multiple days (steady-state)

---

##  Model Logic (step‑by‑step flow)
1. **Initialize environment** with SimPy and a `Resource(capacity=6)`.
2. **Generate EV arrivals** with inter-arrival times drawn from exponential distribution.
3. For each arrival:
   - Sample $SoC_{arr}$.
   - Compute energy required and charging time using curve/data.
   - Observe current queue length and set price level.
   - (Optional) apply price sensitivity to decide if EV balks/abandons.
4. EV requests charger:
   - Wait in queue; collect $T_{wait}$.
   - Once assigned, charge for $T_{charge}$.
5. Update metrics: utilization, waiting time, charging time, revenue.
6. Repeat until simulation ends.
7. Run **two scenarios**:
   - Fixed price (no surge)
   - Dynamic price (surge when $Q>3$)
8. Compare summary statistics and plot time-series outputs.

---

## Data Integration Plan (SoC and Charging Time)
**Preferred approach:**
- Use NREL charging dataset to derive a **realistic charging-time curve** or estimate average power vs SoC.
- Alternatively, use PyChargeModel to approximate **charging duration as a function of SoC**.

**Simplified fallback if data is not processed:**
- Charging time $T_{charge}$ proportional to energy needed and effective power:
  $$T_{charge} = \frac{E_{need}}{P_{eff}}$$
- $P_{eff}$ can be made SoC-dependent (tapering near high SoC).

---

##  Performance Metrics (report)
- Average and maximum queue length
- Average and maximum waiting time
- Charger utilization (time-based)
- Average charging duration
- % EVs that leave without charging (if modeled)
- Revenue (if included)

---

## Visualization Outputs
- Queue length vs time
- Charger utilization vs time
- Price vs time (dynamic pricing)
- (Optional) distribution of waiting times

---

##  Implementation Steps (practical and clear)
1. **Set up project** with SimPy + pandas + matplotlib.
2. **Implement charging-time function** from dataset or curve approximation.
3. **Code EV arrival process** (Poisson).
4. **Create EV process** with queueing, waiting, charging, and logging.
5. **Log time series** (queue, utilization, price).
6. **Run baseline scenario** and store results.
7. **Run dynamic pricing scenario** and store results.
8. **Compute metrics** and compare.
9. **Generate plots and tables.**
10. **Write analytical report** with explanation of system behavior and pricing impact.

---

## Edge Cases to Cover
- Extremely high arrival rates → long queues.
- Very low SoC → long charge time and blocking.
- Surge price active for long periods.
- Zero arrival rate (sanity check).

---

## Deliverables Mapping
- **Simulation code** (Python + SimPy)
- **Short model assumptions doc** (arrival process, SoC logic, pricing)
- **Performance comparison plots and tables**
- **2–3 page analytical report** with discussion and recommendation

---

## Citations / Sources
1. NREL EV Charging Data (dataset): https://catalog.data.gov/dataset/workplace-charging-data-c0796
2. PyChargeModel (NREL GitHub): https://github.com/NREL/PyChargeModel
3. SimPy documentation and examples: https://simpy.readthedocs.io/en/latest/
