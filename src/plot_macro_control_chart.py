"""Plot macro-control chart examples for oil well sample data."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from calculate_indicators import calculate_indicators


ZONE_COLORS = {
    "short_supply": "#d95f02",
    "balanced": "#1b9e77",
    "excess_supply": "#7570b3",
}


def _prepare(input_path: Path) -> pd.DataFrame:
    return calculate_indicators(pd.read_csv(input_path))


def plot_supply_production_matching(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))
    for zone, part in df.groupby("control_zone"):
        ax.scatter(
            part["production_demand_index"],
            part["supply_capacity_index"],
            s=42,
            alpha=0.72,
            color=ZONE_COLORS.get(zone, "#666666"),
            label=zone,
            edgecolor="white",
            linewidth=0.4,
        )
    low, high = 25, 175
    ax.plot([low, high], [low, high], color="#222222", linewidth=1.2, label="balance")
    ax.plot([low, high], [low * 0.82, high * 0.82], color="#888888", linewidth=1, linestyle="--")
    ax.plot([low, high], [low * 1.18, high * 1.18], color="#888888", linewidth=1, linestyle="--")
    ax.set_title("Supply-Production Matching")
    ax.set_xlabel("Production demand index")
    ax.set_ylabel("Supply capacity index")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_energy_value_chart(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))
    scatter = ax.scatter(
        df["energy_intensity_kwh_per_t"],
        df["daily_oil_t"],
        c=df["pump_efficiency_pct"],
        s=df["daily_liquid_m3"] * 1.8,
        alpha=0.7,
        cmap="viridis",
        edgecolor="white",
        linewidth=0.4,
    )
    ax.set_title("Energy Value Chart")
    ax.set_xlabel("Energy intensity (kWh/t oil)")
    ax.set_ylabel("Daily oil (t/d)")
    ax.grid(alpha=0.25)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Pump efficiency (%)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_measure_potential_chart(df: pd.DataFrame, output_path: Path) -> None:
    top = df.sort_values("measure_potential_score", ascending=False).head(20).sort_values(
        "measure_potential_score"
    )
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(top["well_id"], top["measure_potential_score"], color="#4477aa")
    ax.set_title("Top 20 Measure Potential Wells")
    ax.set_xlabel("Measure potential score")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_liquid_supply_status_chart(df: pd.DataFrame, output_path: Path) -> None:
    table = (
        df.pivot_table(index="block", columns="liquid_supply_status", values="well_id", aggfunc="count")
        .fillna(0)
        .astype(int)
    )
    for column in ["short_supply", "balanced", "excess_supply"]:
        if column not in table:
            table[column] = 0
    table = table[["short_supply", "balanced", "excess_supply"]]

    fig, ax = plt.subplots(figsize=(9, 6))
    bottom = None
    for status in table.columns:
        ax.bar(
            table.index,
            table[status],
            bottom=bottom,
            label=status,
            color=ZONE_COLORS.get(status, "#666666"),
        )
        bottom = table[status] if bottom is None else bottom + table[status]
    ax.set_title("Liquid Supply Status by Block")
    ax.set_xlabel("Block")
    ax.set_ylabel("Well count")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_framework_diagram(output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    boxes = [
        ("Well data", 0.08, 0.68),
        ("Indicator engine", 0.36, 0.68),
        ("Macro-control charts", 0.64, 0.68),
        ("Field decisions", 0.36, 0.28),
    ]
    for text, x, y in boxes:
        ax.text(
            x,
            y,
            text,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=14,
            bbox={"boxstyle": "round,pad=0.45", "facecolor": "#f2f2f2", "edgecolor": "#333333"},
        )
    arrows = [
        ((0.18, 0.68), (0.28, 0.68)),
        ((0.46, 0.68), (0.56, 0.68)),
        ((0.64, 0.60), (0.46, 0.36)),
        ((0.36, 0.36), (0.36, 0.58)),
    ]
    for start, end in arrows:
        ax.annotate(
            "",
            xy=end,
            xytext=start,
            xycoords="axes fraction",
            arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#333333"},
        )
    ax.text(
        0.5,
        0.08,
        "Supply-production matching | Energy value | Measure potential | Liquid supply status",
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        color="#444444",
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/sample_wells_500.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("examples"))
    parser.add_argument("--asset-dir", type=Path, default=Path("assets"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.asset_dir.mkdir(parents=True, exist_ok=True)
    df = _prepare(args.input)
    plot_supply_production_matching(df, args.output_dir / "supply_production_matching.png")
    plot_energy_value_chart(df, args.output_dir / "energy_value_chart.png")
    plot_measure_potential_chart(df, args.output_dir / "measure_potential_chart.png")
    plot_liquid_supply_status_chart(df, args.output_dir / "liquid_supply_status_chart.png")
    plot_framework_diagram(args.asset_dir / "framework_diagram.png")
    print(f"Wrote charts to {args.output_dir} and {args.asset_dir}")


if __name__ == "__main__":
    main()
