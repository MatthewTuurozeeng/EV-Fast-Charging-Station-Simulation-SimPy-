from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import simpy


@dataclass
class SimulationParams:
    num_chargers: int = 6
    sim_hours: float = 24.0
    arrival_rate_per_hour: float = 12.0
    battery_kwh: float = 75.0
    target_soc: float = 0.8
    base_price: float = 0.40
    surge_multiplier: float = 0.5
    queue_threshold: int = 3
    price_balk_prob: float = 0.15
    random_seed: int = 42


def _power_kw_at_soc(soc: float) -> float:
    if soc < 0.5:
        return 150.0
    if soc < 0.8:
        return 150.0 - (soc - 0.5) * (80.0 / 0.3)
    return 70.0 - (soc - 0.8) * (50.0 / 0.2)


def charging_time_hours(
    soc_start: float,
    soc_target: float,
    battery_kwh: float,
    step: float = 0.01,
) -> float:
    if soc_start >= soc_target:
        return 0.0

    soc = soc_start
    time_hours = 0.0
    while soc < soc_target:
        next_soc = min(soc + step, soc_target)
        energy_kwh = (next_soc - soc) * battery_kwh
        power_kw = max(_power_kw_at_soc(soc), 10.0)
        time_hours += energy_kwh / power_kw
        soc = next_soc
    return time_hours


def _time_weighted_average(series: List[Tuple[float, float]], total_time: float) -> float:
    if not series:
        return 0.0
    series = sorted(series, key=lambda x: x[0])
    if series[0][0] > 0:
        series = [(0.0, series[0][1])] + series
    if series[-1][0] < total_time:
        series.append((total_time, series[-1][1]))

    weighted_sum = 0.0
    for (t0, v0), (t1, _) in zip(series[:-1], series[1:]):
        weighted_sum += (t1 - t0) * v0
    return weighted_sum / total_time


def run_scenario(params: SimulationParams, dynamic_pricing: bool) -> Dict[str, object]:
    rng = np.random.default_rng(params.random_seed)
    env = simpy.Environment()
    station = simpy.Resource(env, capacity=params.num_chargers)

    queue_log: List[Tuple[float, int]] = [(0.0, 0)]
    utilization_log: List[Tuple[float, float]] = [(0.0, 0.0)]
    price_log: List[Tuple[float, float]] = []
    wait_times: List[float] = []
    charge_times: List[float] = []

    served = 0
    balked = 0
    total_charging_time = 0.0

    def log_queue():
        queue_log.append((env.now, len(station.queue)))

    def log_utilization():
        utilization_log.append((env.now, station.count / params.num_chargers))

    def ev_process(ev_id: int):
        nonlocal served, balked, total_charging_time
        arrival_time = env.now
        log_queue()

        soc_arrival = float(rng.beta(2.0, 4.0))
        soc_arrival = min(max(soc_arrival, 0.05), 0.95)
        charge_time = charging_time_hours(
            soc_arrival, params.target_soc, params.battery_kwh
        )

        price = params.base_price
        if dynamic_pricing and len(station.queue) > params.queue_threshold:
            price = params.base_price * (1.0 + params.surge_multiplier)

        price_log.append((env.now, price))

        if price > params.base_price and rng.random() < params.price_balk_prob:
            balked += 1
            return

        with station.request() as req:
            yield req
            wait_time = env.now - arrival_time
            wait_times.append(wait_time)
            log_queue()
            log_utilization()

            yield env.timeout(charge_time)
            charge_times.append(charge_time)
            total_charging_time += charge_time
            served += 1

            log_utilization()

    def arrival_process():
        ev_id = 0
        while True:
            interarrival = rng.exponential(1.0 / params.arrival_rate_per_hour)
            yield env.timeout(interarrival)
            ev_id += 1
            env.process(ev_process(ev_id))

    env.process(arrival_process())
    env.run(until=params.sim_hours)

    avg_queue = _time_weighted_average(queue_log, params.sim_hours)
    avg_utilization = total_charging_time / (params.sim_hours * params.num_chargers)

    metrics = {
        "served": served,
        "balked": balked,
        "avg_queue": avg_queue,
        "max_queue": max([q for _, q in queue_log], default=0),
        "avg_wait": float(np.mean(wait_times)) if wait_times else 0.0,
        "max_wait": float(np.max(wait_times)) if wait_times else 0.0,
        "avg_charge": float(np.mean(charge_times)) if charge_times else 0.0,
        "avg_utilization": avg_utilization,
        "revenue": sum(charge_times) * params.base_price * 60.0,
    }

    logs = {
        "queue": queue_log,
        "utilization": utilization_log,
        "price": price_log,
        "wait_times": wait_times,
        "charge_times": charge_times,
    }

    return {"metrics": metrics, "logs": logs}


def to_step_frame(series: List[Tuple[float, float]], sim_hours: float) -> pd.DataFrame:
    if not series:
        return pd.DataFrame({"time": [0.0, sim_hours], "value": [0.0, 0.0]})

    data = sorted(series, key=lambda x: x[0])
    if data[0][0] > 0:
        data = [(0.0, data[0][1])] + data
    if data[-1][0] < sim_hours:
        data.append((sim_hours, data[-1][1]))

    return pd.DataFrame(data, columns=["time", "value"])
