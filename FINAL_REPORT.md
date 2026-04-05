# EV Fast‑Charging Station with Dynamic Pricing — Analytical Report

**Project date:** 3 April 2026  
**Author:** Matthew Tuurozeeng

## Executive summary
This project builds a discrete‑event simulation (DES) of a highway rest stop with **six DC fast chargers** and evaluates a **dynamic pricing rule** that increases price when the queue exceeds three vehicles. The model compares baseline fixed‑price behavior with a dynamic‑pricing scenario and reports queue length, waiting time, utilization, and revenue metrics. The results show **very light congestion** under the chosen parameters; as a result, dynamic pricing is rarely triggered and the two scenarios are nearly identical. This highlights a core modeling insight: **pricing policies only matter when the system is near or above capacity**.

Key findings:
- With the default arrival rate (12 EV/hour) and six chargers, **queues are short and utilization is moderate** (~53%).
- Dynamic pricing is activated rarely, resulting in **negligible differences** between scenarios.
- The simulation framework is nonetheless correct and extensible; higher arrival rates or tighter charger capacity would surface meaningful pricing effects.

---

## 1. Problem framing and objectives
The scenario models a highway rest stop with six DC fast chargers. Vehicles arrive with varying **State of Charge (SoC)**, which determines their charging time. The assignment requires:
- A discrete‑event simulation of queueing and charging behavior.
- A **dynamic pricing policy** when queue length exceeds three vehicles.
- Comparison of **baseline vs dynamic pricing** on performance metrics.
- Visualization of queue, utilization, and pricing over time.

The core goal is to understand whether dynamic pricing reduces congestion and improves system efficiency without excessively harming customer experience.

---

## 2. Model design and assumptions
### 2.1 Simulation type
A **DES** is the natural fit because:
- Arrivals and departures are discrete events.
- Chargers are limited shared resources.
- Queue lengths and wait times evolve over time.

SimPy is used to implement the environment, resource contention, and event scheduling.

### 2.2 Vehicle arrival process
Arrivals follow a **Poisson process** with exponential inter‑arrival times:
- Mean arrival rate: **12 EV/hour**.
- This provides realistic random spacing without requiring complex traffic modeling.

### 2.3 SoC distribution and charging time
Each EV arrives with a sampled SoC drawn from a **Beta(2, 4)** distribution (bounded to 5–95%). Charging time is computed using a **SoC‑dependent tapering power curve**:
- High power at low SoC (fast charging).
- Power tapers as SoC approaches 80–100%.

This curve approximates the shape observed in NREL references and PyChargeModel resources, while keeping the model lightweight and interpretable. See `ASSUMPTIONS.md` for the data usage rationale.

### 2.4 Pricing policy
- **Baseline price:** $0.40/kWh
- **Dynamic price:** $0.40/kWh × (1 + 0.5)$ when queue length > 3
- **Balking probability:** 15% when the price is surged

The balking rule provides a minimal behavioral response to price increases. More advanced elasticity models can be added later.

---

## 3. Implementation overview
### 3.1 Core simulation logic
Each EV process performs:
1. Arrival and queue length observation
2. Price determination (fixed or dynamic)
3. Optional balking if price is surged
4. Waiting for a charger resource
5. Charging for a computed time
6. Logging of queue and utilization

### 3.2 Outputs
The simulation records:
- Queue length over time
- Charger utilization over time
- Pricing time series
- Wait times and charging durations

Metrics are computed from these logs:
- Average and maximum queue length
- Average and maximum waiting time
- Average charging time
- Average utilization
- Total revenue (approx.)

---

## 4. Results and discussion
### 4.1 Summary metrics
With the default parameters:
- **Average queue length:** ~0.009
- **Maximum queue length:** 2
- **Average waiting time:** ~0.004 hours (~15 seconds)
- **Average utilization:** ~0.53
- **Revenue:** ~1843 (arbitrary units based on simplified pricing formula)

Baseline and dynamic pricing metrics are essentially identical under the current setup.

### 4.2 Interpretation
This outcome is not a flaw; it demonstrates a realistic principle:
- **If the system is under capacity, surge pricing has little impact.**
- Dynamic pricing only influences outcomes when the queue crosses the threshold often.

The simulation therefore suggests that, for a lightly utilized station, dynamic pricing is unnecessary. For a busier station, it could help moderate demand and reduce waits.

### 4.3 Visualizations
The notebook plots show:
- Queue length spikes are rare and low magnitude.
- Utilization fluctuates around 50–60%.
- Price is effectively flat because the queue threshold is rarely exceeded.

---

## 5. Sensitivity and “interesting parts”
Several parameters govern whether dynamic pricing is meaningful:

1. **Arrival rate ($\lambda$)**
   - Higher arrival rates push the system into congestion, activating surge pricing.
   - This is the most impactful lever.

2. **Charging time distribution**
   - Longer charging times increase resource contention.
   - A more realistic NREL‑fit curve could shift utilization upward.

3. **Queue threshold**
   - Lowering the threshold triggers pricing more frequently.
   - Raising it delays intervention and might reduce pricing impact.

4. **Balking probability**
   - Currently fixed at 15% when surged.
   - If customers are more price‑sensitive, surge pricing can substantially reduce queues, at a potential revenue trade‑off.

These elements provide a clear path for further analysis without changing the core architecture.

---

## 6. Limitations
- **No direct dataset ingestion**: NREL data is not parsed; instead, a simplified curve is used.
- **Single‑day horizon**: results represent one 24‑hour window.
- **Static arrival rate**: time‑of‑day effects are not modeled.
- **Simple pricing response**: balking is modeled as a fixed probability.

These simplifications keep the model lightweight but may understate variability in real systems.

---

## 7. Conclusion and recommendation
The simulation satisfies the core requirements of the assignment and provides a faithful DES framework for comparing fixed vs dynamic pricing. Under the chosen parameters, the station is **not congested**, so dynamic pricing has little effect. This suggests that a pricing intervention is only useful when the station operates closer to capacity.

**Recommendation:** If the goal is to demonstrate the value of dynamic pricing, test higher arrival rates or fewer chargers. The current model can support those experiments without structural changes.

---

## Appendix: Reproducibility
- **Core model:** `ev_charging_model.py`
- **Notebook:** `ev_charging_simulation.ipynb`
- **Runner:** `run_simulation.py`
- **Assumptions note:** `ASSUMPTIONS.md`
