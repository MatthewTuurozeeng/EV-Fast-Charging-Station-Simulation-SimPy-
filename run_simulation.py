from __future__ import annotations

from pprint import pprint

from ev_charging_model import SimulationParams, run_scenario


def main() -> None:
    params = SimulationParams()
    baseline = run_scenario(params, dynamic_pricing=False)
    dynamic = run_scenario(params, dynamic_pricing=True)

    print("Baseline metrics")
    pprint(baseline["metrics"])
    print("\nDynamic pricing metrics")
    pprint(dynamic["metrics"])


if __name__ == "__main__":
    main()
