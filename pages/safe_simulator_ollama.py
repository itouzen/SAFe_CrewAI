# safe_simulator_ollama.py
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
import ollama
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Validation functions
def validate_ollama_server():
    """Check if Ollama server is running"""
    try:
        response = requests.get("http://localhost:11434", timeout=10)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def validate_model_available(model_name: str):
    """Check if specified model is available locally"""
    try:
        models = ollama.list()['models']
        return any(m['model'].startswith(model_name) for m in models)
    except Exception as e:
        st.error(f"Model validation failed: {str(e)}")
        return False

# Assertion checks
def assert_safe_setup(agents, tasks):
    assert len(agents) >= 3, "At least 3 SAFe roles required"
    assert any(task.description.startswith("Facilitate PI Planning") for task in tasks), "Missing PI Planning task"
    assert all(agent.tools for agent in agents.values()), "All agents must have tools assigned"

# 1. Define Tools =============================================================
class JiraTool(BaseTool):
    name: str = "Jira Tool"
    description: str = "Manages user stories and sprint backlogs."
    def _run(self, task: str, assignee: str) -> str:
        assert isinstance(task, str), "Task must be a string"
        assert isinstance(assignee, str), "Assignee must be a string"
        return f"Task '{task}' created and assigned to {assignee}."

class DocumentationTool(BaseTool):
    name: str = "Documentation Tool"
    description: str = "Stores SAFe artifacts."
    def _run(self, content: str) -> str:
        assert len(content) > 10, "Content must be at least 10 characters"
        return f"Documentation updated: {content}"

# 2. Create SAFe Agents =======================================================
def create_safe_agents(model_name: str):
    llm = LLM(
        base_url="http://localhost:11434",
        model="ollama/llama3.2",
        temperature=0.3,
        top_k=20
    )

    return {
        "RTE": Agent(
            role="Release Train Engineer",
            goal="Facilitate PI Planning",
            backstory="Experienced SAFe RTE",
            tools=[JiraTool(), DocumentationTool()],
            verbose=True,
            llm=llm,
            max_iter=3
        ),
        "Product Manager": Agent(
            role="Product Manager",
            goal="Prioritize features",
            backstory="Strategic product leader",
            tools=[DocumentationTool()],
            verbose=True,
            llm=llm,
            max_iter=3
        ),
        "Dev Team": Agent(
            role="Agile Team",
            goal="Deliver working software",
            backstory="Cross-functional team",
            tools=[JiraTool()],
            verbose=True,
            llm=llm,
            max_iter=5
        )
    }

# 3. Define SAFe Tasks =======================================================
def create_safe_tasks(agents):
    return [
        Task(
            description="Facilitate PI Planning event with all teams",
            expected_output="PI Objectives and Program Board",
            agent=agents["RTE"],
            tools=[JiraTool(), DocumentationTool()],
            async_execution=False
        ),
        Task(
            description="Prioritize features based on strategic themes",
            expected_output="Prioritized feature backlog",
            agent=agents["Product Manager"],
            tools=[DocumentationTool()],
            async_execution=False
        ),
        Task(
            description="Execute sprint: plan, daily scrums, demo",
            expected_output="Working software increment",
            agent=agents["Dev Team"],
            tools=[JiraTool()],
            async_execution=False
        )
    ]

# 4. Streamlit UI =============================================================
def main():
    st.set_page_config(page_title="SAFe Ollama Simulator", layout="wide")
    
    # Header
    st.title("🚀 Local SAFe Simulator with Ollama")
    st.markdown("Simulate SAFe using local LLMs (Llama 3.2/Qwen 2.5)")
    
    # Model selection
    selected_model = st.sidebar.selectbox(
        "Select LLM",
        ("llama3.2", "qwen2.5"),
        index=0
    )
    
    # Validation checks
    if not validate_ollama_server():
        st.error("Ollama server not running! Start with `ollama serve`")
        return
        
    if not validate_model_available(selected_model):
        st.error(f"Model {selected_model} not found! Install with `ollama pull {selected_model}`")
        return
    
    # Simulation Controls
    if st.sidebar.button("Run SAFe Simulation"):
        with st.spinner(f"Running simulation with {selected_model}..."):
            try:
                start_time = time.time()
                
                agents = create_safe_agents(selected_model)
                tasks = create_safe_tasks(agents)
                
                # Pre-execution assertions
                assert_safe_setup(agents, tasks)
                
                safe_crew = Crew(
                    agents=list(agents.values()),
                    tasks=tasks,
                    process=Process.sequential,
                    verbose=True
                )
                
                results = safe_crew.kickoff()
                
                # Post-execution validation
                # assert isinstance(results, dict), "Results should be a dictionary"
                # assert "tasks" in results, "Missing tasks in results"
                # assert "artifacts" in results, "Missing artifacts in results"
                
                st.session_state.results = results
                st.session_state.execution_time = time.time() - start_time
                
            except AssertionError as ae:
                st.error(f"Validation failed: {str(ae)}")
            except Exception as e:
                st.error(f"Simulation failed: {str(e)}")

    # Display results
    if "results" in st.session_state:
        st.header("Simulation Results")
        st.caption(f"Executed in {st.session_state.execution_time:.2f} seconds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("PI Artifacts")
            if "artifacts" in st.session_state.results:
                for artifact in st.session_state.results["artifacts"]:
                    st.markdown(f"- {artifact}")
            
        with col2:
            st.subheader("Task Outcomes")
            if "tasks" in st.session_state.results:
                for task in st.session_state.results["tasks"]:
                    st.markdown(f"**{task['description']}**")
                    st.markdown(f"```\n{task['result']}\n```")
        
        # Raw output
        with st.expander("Debug Details"):
            st.json(st.session_state.results)

if __name__ == "__main__":
    main()