import streamlit as st
from crewai import Crew, Agent, Task
import random

# Define AI Agents
class ReleaseTrainEngineer(Agent):
    def execute(self, context):
        return f"RTE: Facilitating PI Planning. Addressing {random.choice(['dependencies', 'risks', 'team coordination'])}."

class ScrumMaster(Agent):
    def execute(self, context):
        return f"Scrum Master: Conducting daily standup. Removing {random.choice(['blockers', 'impediments'])}."

class ProductOwner(Agent):
    def execute(self, context):
        return f"Product Owner: Prioritizing backlog. Selecting features for the sprint."

class DevelopmentTeam(Agent):
    def execute(self, context):
        return f"Development Team: Working on stories. Completing {random.randint(3, 10)} points in this sprint."

# CrewAI Setup
crew = Crew(agents=[ReleaseTrainEngineer(), ScrumMaster(), ProductOwner(), DevelopmentTeam()])

def simulate_safe():
    results = [agent.execute({}) for agent in crew.agents]
    return results

# Streamlit UI
st.title("SAFe Simulation with CrewAI")

if st.button("Run Simulation"):
    results = simulate_safe()
    for result in results:
        st.write(result)

st.sidebar.header("Simulation Controls")
st.sidebar.slider("Team Velocity", 10, 50, 25)
st.sidebar.slider("Number of Dependencies", 0, 10, 3)

st.sidebar.markdown("Adjust parameters and rerun the simulation to observe different outcomes.")
