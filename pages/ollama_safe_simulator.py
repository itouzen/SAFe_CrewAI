import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

# Initialize Ollama model
llm = LLM(
    base_url="http://localhost:11434",
    model="ollama/qwen2.5",
)

# 1. Define Tools =============================================================
class JiraTool(BaseTool):
    name: str = "Jira Tool"
    description: str = "Manages user stories, tasks, and sprint backlogs."
    def _run(self, task: str, assignee: str) -> str:
        return f"Task '{task}' created and assigned to {assignee}."

class DocumentationTool(BaseTool):
    name: str = "Documentation Tool"
    description: str = "Stores SAFe artifacts and team decisions."
    def _run(self, content: str) -> str:
        return f"Documentation updated: {content}"

# 2. Create SAFe Agents =======================================================
def create_safe_agents():
    return {
        "RTE": Agent(
            role="Release Train Engineer",
            goal="Facilitate PI Planning and ensure ART alignment",
            backstory="Experienced SAFe RTE with strong coordination skills",
            tools=[JiraTool(), DocumentationTool()],
            verbose=True,
            llm=llm  # Use Ollama
        ),
        "Product Manager": Agent(
            role="Product Manager",
            goal="Define program vision and prioritize features",
            backstory="Strategic leader focused on customer value",
            tools=[DocumentationTool()],
            verbose=True,
            llm=llm  # Use Ollama
        ),
        "Scrum Master": Agent(
            role="Scrum Master",
            goal="Remove team impediments and facilitate ceremonies",
            backstory="Agile coach passionate about team empowerment",
            tools=[JiraTool()],
            verbose=True,
            llm=llm  # Use Ollama
        ),
        "Dev Team": Agent(
            role="Agile Team",
            goal="Deliver working software increments",
            backstory="Cross-functional team of developers and testers",
            tools=[JiraTool()],
            verbose=True,
            llm=llm  # Use Ollama
        )
    }

# 3. Define SAFe Tasks =======================================================
def create_safe_tasks(agents):
    return [
        Task(
            description="Facilitate PI Planning event with all teams",
            expected_output="PI Objectives and Program Board",
            agent=agents["RTE"],
            tools=[JiraTool(), DocumentationTool()]
        ),
        Task(
            description="Prioritize features based on strategic themes",
            expected_output="Prioritized feature backlog with business value",
            agent=agents["Product Manager"],
            tools=[DocumentationTool()]
        ),
        Task(
            description="Execute sprint: plan, daily scrums, demo, retrospective",
            expected_output="Sprint backlog and working software increment",
            agent=agents["Dev Team"],
            tools=[JiraTool()]
        ),
        Task(
            description="Identify and resolve cross-team dependencies",
            expected_output="Dependency map and mitigation plan",
            agent=agents["Scrum Master"],
            tools=[JiraTool()]
        )
    ]

# 4. Streamlit UI =============================================================
def main():
    st.set_page_config(page_title="SAFe Simulator", layout="wide")
    
    # Header
    st.title("🚀 SAFe Implementation Simulator")
    st.markdown("Simulate a SAFe Agile Release Train using AI Agents")
    
    # Simulation Controls
    with st.sidebar:
        st.header("Simulation Controls")
        if st.button("Run SAFe Simulation"):
            with st.spinner("Running PI Planning and Sprint Execution..."):
                # Create agents and tasks
                agents = create_safe_agents()
                tasks = create_safe_tasks(agents)
                
                # Create and run crew
                safe_crew = Crew(
                    agents=list(agents.values()),
                    tasks=tasks,
                    process=Process.sequential,
                    verbose=True
                )
                
                # Store results in session state
                st.session_state.results = safe_crew.kickoff()
    
    # Results Visualization
    if "results" in st.session_state:
        st.header("Simulation Results")
        
        # ART Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ART PI Board")
            st.image("https://i.imgur.com/7Xk7Qq8.png", caption="Program Board")
            
            st.subheader("PI Objectives")
            st.markdown("""
            - Objective 1: Implement core payment processing
            - Objective 2: Enhance user authentication flow
            - Objective 3: Improve API response times
            """)
        
        with col2:
            st.subheader("Feature Backlog")
            st.dataframe({
                "Feature": ["Payment Gateway", "Auth v2", "API Optimization"],
                "Priority": ["High", "Critical", "Medium"],
                "Status": ["Planned", "In Progress", "Backlog"]
            })
            
            st.subheader("Team Velocity")
            st.bar_chart({
                "Team 1": 35,
                "Team 2": 42,
                "Team 3": 38
            })
        
        # Raw Output
        with st.expander("Detailed Simulation Logs"):
            st.write(st.session_state.results)

# Run the app
if __name__ == "__main__":
    main()
