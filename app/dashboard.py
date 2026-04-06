import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from src.components.simulator import RaceSimulator

# Page config
st.set_page_config(page_title="F1 Strategy Simulator", layout="wide")

st.title("🏎️ F1 Strategy Simulator — Interactive Dashboard")

# Sidebar controls
st.sidebar.header("Race Settings")

total_laps = st.sidebar.slider("Total Laps", 5, 60, 30)
start_tire = st.sidebar.selectbox("Starting Tire", ["soft", "medium", "hard"])
pit_lap = st.sidebar.slider("Pit Lap", 1, total_laps, 10)
pit_tire = st.sidebar.selectbox("Pit Tire", ["soft", "medium", "hard"])

# Tire colors
tire_colors = {
    "soft": "#ff4d4d",
    "medium": "#ffd633",
    "hard": "#cccccc"
}


# 🔥 Plotly Strategy Graph
def plot_strategy(laps, lap_times, tire_history, pit_lap):
    fig = go.Figure()

    # Colored segments
    for i in range(len(laps) - 1):
        fig.add_trace(go.Scatter(
            x=laps[i:i+2],
            y=lap_times[i:i+2],
            mode='lines',
            line=dict(color=tire_colors[tire_history[i]], width=4),
            showlegend=False
        ))

    # Smooth base line
    fig.add_trace(go.Scatter(
        x=laps,
        y=lap_times,
        mode='lines',
        line=dict(color='cyan', width=2),
        name="Lap Time",
        opacity=0.4
    ))

    # Points with hover
    fig.add_trace(go.Scatter(
        x=laps,
        y=lap_times,
        mode='markers',
        marker=dict(size=8, color=[tire_colors[t] for t in tire_history]),
        text=[f"Tire: {t}" for t in tire_history],
        hovertemplate="Lap %{x}<br>Time %{y:.2f}s<br>%{text}",
        name="Laps"
    ))

    # Pit stop marker
    fig.add_vline(
        x=pit_lap,
        line_dash="dash",
        line_color="cyan",
        annotation_text="Pit Stop",
        annotation_position="top"
    )

    fig.update_layout(
        title="🏎️ Strategy Visualization",
        xaxis_title="Lap",
        yaxis_title="Lap Time",
        template="plotly_dark",
        hovermode="x unified",
        height=500
    )

    return fig


# ⏱️ Cumulative Time Graph
def plot_cumulative(laps, lap_times):
    cum_time = np.cumsum(lap_times)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=laps,
        y=cum_time,
        mode='lines+markers',
        line=dict(color='cyan', width=3),
        marker=dict(size=6),
        name="Total Time"
    ))

    fig.update_layout(
        title="⏱️ Total Race Time Progress",
        xaxis_title="Lap",
        yaxis_title="Total Time",
        template="plotly_dark",
        height=400
    )

    return fig


# ▶️ Run Simulation
if st.button("Run Simulation 🚀"):

    sim = RaceSimulator(total_laps, start_tire)

    laps = []
    lap_times = []
    tire_history = []

    while True:
        if sim.current_lap == pit_lap:
            action = {"soft": 1, "medium": 2, "hard": 3}[pit_tire]
        else:
            action = 0

        state, reward, done = sim.step(action)

        laps.append(state[0] - 1)
        lap_times.append(-reward)
        tire_history.append(state[1])

        if done:
            break

    # Layout split
    col1, col2 = st.columns([2, 1])

    with col1:
        fig1 = plot_strategy(laps, lap_times, tire_history, pit_lap)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = plot_cumulative(laps, lap_times)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("📊 Race Telemetry")

        st.metric("Total Time", f"{sim.total_time:.2f}s")
        st.metric("Final Tire", tire_history[-1])
        st.metric("Final Tire Age", state[2])

        st.markdown("---")

        st.subheader("🛞 Strategy")
        st.write(f"Start: {start_tire}")
        st.write(f"Pit Lap: {pit_lap}")
        st.write(f"Pit Tire: {pit_tire}")