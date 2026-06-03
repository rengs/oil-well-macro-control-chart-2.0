"""Streamlit demo app for Oil Well Macro Control Chart 2.0."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from calculate_indicators import calculate_indicators


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample_wells_500.csv"


st.set_page_config(page_title="Oil Well Macro Control Chart 2.0", layout="wide")
st.title("Oil Well Macro Control Chart 2.0")

uploaded = st.sidebar.file_uploader("Upload well CSV", type=["csv"])
if uploaded is not None:
    raw = pd.read_csv(uploaded)
else:
    raw = pd.read_csv(DATA_PATH)

data = calculate_indicators(raw)
blocks = sorted(data["block"].unique())
selected_blocks = st.sidebar.multiselect("Block", blocks, default=blocks)
filtered = data[data["block"].isin(selected_blocks)]

metric_cols = st.columns(4)
metric_cols[0].metric("Wells", len(filtered))
metric_cols[1].metric("Avg daily oil", f"{filtered['daily_oil_t'].mean():.2f} t/d")
metric_cols[2].metric("Avg energy", f"{filtered['energy_intensity_kwh_per_t'].mean():.1f} kWh/t")
metric_cols[3].metric("Priority wells", int((filtered["priority_level"] == "priority").sum()))

left, right = st.columns(2)
with left:
    st.subheader("Supply-production matching")
    st.scatter_chart(
        filtered,
        x="production_demand_index",
        y="supply_capacity_index",
        color="control_zone",
    )

with right:
    st.subheader("Energy value")
    st.scatter_chart(
        filtered,
        x="energy_intensity_kwh_per_t",
        y="daily_oil_t",
        color="priority_level",
    )

st.subheader("Top measure potential wells")
top = filtered.sort_values("measure_potential_score", ascending=False).head(20)
st.bar_chart(top.set_index("well_id")["measure_potential_score"])

st.subheader("Well table")
st.dataframe(filtered.sort_values("priority_score", ascending=False), use_container_width=True)
