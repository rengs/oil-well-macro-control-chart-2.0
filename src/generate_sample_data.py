"""Generate deterministic sample well data for macro control chart demos."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def build_sample_wells(rows: int = 500, seed: int = 20260604) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    blocks = np.array(["A-East", "A-West", "B-North", "B-South", "C-Center"])
    block = rng.choice(blocks, size=rows, p=[0.22, 0.2, 0.18, 0.24, 0.16])

    production_days = rng.integers(18, 31, size=rows)
    daily_liquid = rng.gamma(shape=4.2, scale=9.5, size=rows).clip(8, 130)
    water_cut = rng.beta(5.5, 2.2, size=rows).clip(0.18, 0.98)
    daily_oil = (daily_liquid * (1 - water_cut) * rng.normal(0.86, 0.08, size=rows)).clip(0.2, None)
    daily_water = (daily_liquid - daily_oil).clip(0.0, None)

    pump_depth = rng.normal(1450, 260, size=rows).clip(650, 2350)
    dynamic_level = (pump_depth - rng.normal(420, 130, size=rows)).clip(200, 2200)
    static_level = (dynamic_level - rng.normal(110, 55, size=rows)).clip(120, 2100)
    pump_efficiency = rng.normal(58, 15, size=rows).clip(18, 92)
    power_kwh = (daily_liquid * rng.normal(4.1, 0.9, size=rows) + pump_depth / 35).clip(35, 780)

    injection_support = rng.normal(1.0, 0.22, size=rows).clip(0.35, 1.65)
    supply_capacity = (
        injection_support * 62
        + pump_efficiency * 0.42
        + (pump_depth - dynamic_level) / 20
        + rng.normal(0, 7, size=rows)
    ).clip(25, 150)
    production_demand = (
        daily_liquid * 1.15
        + daily_oil * 3.6
        + production_days * 0.8
        + water_cut * 18
        + rng.normal(0, 6, size=rows)
    ).clip(30, 170)

    energy_intensity = power_kwh / daily_oil.clip(0.2, None)
    supply_ratio = supply_capacity / production_demand
    measure_potential = (
        np.abs(supply_ratio - 1.0) * 42
        + np.maximum(energy_intensity - np.median(energy_intensity), 0) * 0.18
        + np.maximum(55 - pump_efficiency, 0) * 0.7
        + water_cut * 18
        + rng.integers(0, 5, size=rows) * 2.5
    ).clip(0, 100)

    status = np.select(
        [supply_ratio < 0.82, supply_ratio <= 1.18],
        ["short_supply", "balanced"],
        default="excess_supply",
    )

    return pd.DataFrame(
        {
            "well_id": [f"W{idx:04d}" for idx in range(1, rows + 1)],
            "block": block,
            "production_days": production_days,
            "pump_depth_m": pump_depth.round(1),
            "daily_liquid_m3": daily_liquid.round(2),
            "daily_oil_t": daily_oil.round(2),
            "daily_water_m3": daily_water.round(2),
            "water_cut_pct": (water_cut * 100).round(2),
            "casing_pressure_mpa": rng.normal(1.8, 0.55, size=rows).clip(0.2, 4.2).round(2),
            "tubing_pressure_mpa": rng.normal(2.7, 0.75, size=rows).clip(0.4, 5.8).round(2),
            "dynamic_fluid_level_m": dynamic_level.round(1),
            "static_fluid_level_m": static_level.round(1),
            "pump_efficiency_pct": pump_efficiency.round(2),
            "power_kwh": power_kwh.round(2),
            "measure_count_30d": rng.integers(1, 8, size=rows),
            "maintenance_count_90d": rng.integers(0, 5, size=rows),
            "injection_support_index": injection_support.round(3),
            "supply_capacity_index": supply_capacity.round(2),
            "production_demand_index": production_demand.round(2),
            "energy_intensity_kwh_per_t": energy_intensity.round(2),
            "liquid_supply_status": status,
            "measure_potential_score": measure_potential.round(2),
        }
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--output", type=Path, default=Path("data/sample_wells_500.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build_sample_wells(rows=args.rows, seed=args.seed).to_csv(args.output, index=False)
    print(f"Wrote {args.rows} rows to {args.output}")


if __name__ == "__main__":
    main()
