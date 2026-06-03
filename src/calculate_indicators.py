"""Calculate macro-control indicators for oil well sample data."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["supply_production_ratio"] = (
        result["supply_capacity_index"] / result["production_demand_index"].replace(0, np.nan)
    ).round(3)
    result["oil_per_kwh"] = (
        result["daily_oil_t"] / result["power_kwh"].replace(0, np.nan)
    ).round(4)
    result["fluid_drawdown_m"] = (
        result["dynamic_fluid_level_m"] - result["static_fluid_level_m"]
    ).round(1)

    result["control_zone"] = np.select(
        [
            result["supply_production_ratio"] < 0.82,
            result["supply_production_ratio"] <= 1.18,
        ],
        ["short_supply", "balanced"],
        default="excess_supply",
    )

    energy_rank = result["energy_intensity_kwh_per_t"].rank(pct=True)
    potential_rank = result["measure_potential_score"].rank(pct=True)
    result["priority_score"] = (0.58 * potential_rank + 0.42 * energy_rank).mul(100).round(2)
    result["priority_level"] = pd.cut(
        result["priority_score"],
        bins=[-1, 50, 75, 100],
        labels=["watch", "optimize", "priority"],
    ).astype(str)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/sample_wells_500.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/sample_wells_500_with_indicators.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input)
    result = calculate_indicators(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Wrote indicators to {args.output}")


if __name__ == "__main__":
    main()
