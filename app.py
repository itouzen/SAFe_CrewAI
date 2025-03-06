import streamlit as st
from workflows.pi_planning import run_pi_planning
from workflows.daily_standup import run_daily_standup
from workflows.sprint_execution import execute_sprint
from workflows.inspect_adapt import run_inspect_and_adapt
from utils.generate_data import generate_backlog

# Generate synthetic data
teams = [
    {"name": "Team A", "capacity": 30, "velocity": 10, "members": [{"name": "Alice"}, {"name": "Bob"}]},
    {"name": "Team B", "capacity": 25, "velocity": 12, "members": [{"name": "Charlie"}, {"name": "Eve"}]}
]
backlog = generate_backlog().to_dict('records')

st.title("SAFe Simulation Dashboard")

# PI Planning
st.header("PI Planning")
backlog, teams, dependencies = run_pi_planning(backlog, teams)
st.write("Dependencies Identified:")
st.write(dependencies)

# Daily Standup
st.header("Daily Standup")
blockers = run_daily_standup(teams)
st.write("Blockers Identified:")
st.write(blockers)

# Sprint Execution
st.header("Sprint Execution")
backlog, sprint_progress = execute_sprint(teams, backlog)
st.write("Sprint Progress:")
st.write(sprint_progress)

# Inspect & Adapt
st.header("Inspect & Adapt")
metrics, recommendations = run_inspect_and_adapt(teams, sprint_progress)
st.write("Performance Metrics:")
st.write(metrics)
st.write("Recommendations:")
st.write(recommendations)