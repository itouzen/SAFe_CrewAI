import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tools.agents import ReleaseTrainEngineer, ScrumMaster, ProductOwner
from tools.workflows import SAFeWorkflow
import networkx as nx

def main():
    st.set_page_config(layout="wide")
    st.title("SAFe Simulation Dashboard")
    
    # Initialize simulation
    if 'workflow' not in st.session_state:
        st.session_state.workflow = SAFeWorkflow()
        st.session_state.workflow.generate_synthetic_data(num_features=20, num_teams=5)
    
    # Sidebar controls
    with st.sidebar:
        st.header("Simulation Controls")
        selected_team = st.selectbox("Select Team", 
                                   [team['name'] for team in st.session_state.workflow.teams])
        
        st.subheader("Team Parameters")
        selected_team_data = next(t for t in st.session_state.workflow.teams 
                                if t['name'] == selected_team)
        new_velocity = st.slider("Adjust Velocity", 
                               min_value=10, 
                               max_value=30, 
                               value=selected_team_data['velocity'])
        
        if st.button("Update Team Parameters"):
            update_team_parameters(selected_team, new_velocity)
    
    # Main dashboard
    tab1, tab2, tab3 = st.tabs(["Program Overview", "Dependencies & Risks", "Team Analytics"])
    
    with tab1:
        create_program_overview()
    
    with tab2:
        create_dependency_risk_view()
        
    with tab3:
        create_team_analytics(selected_team)

def create_program_overview():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Team Velocity Trend")
        velocity_data = []
        for team in st.session_state.workflow.teams:
            for i, v in enumerate(team['historical_velocity']):
                velocity_data.append({
                    'Team': team['name'],
                    'Sprint': f"Sprint {i+1}",
                    'Velocity': v
                })
        velocity_df = pd.DataFrame(velocity_data)
        st.plotly_chart(px.line(velocity_df, 
                               x='Sprint', 
                               y='Velocity', 
                               color='Team',
                               title="Team Velocity Over Time"))
    
    with col2:
        st.subheader("Feature Distribution")
        feature_data = pd.DataFrame([{
            'Priority': f['priority'],
            'Story Points': f['story_points'],
            'Business Value': f.get('business_value', 0),
            'Risk Level': f.get('risk_level', 'Medium'),
            'Type': f.get('type', 'New Feature')
        } for f in st.session_state.workflow.features])
        
        st.plotly_chart(px.scatter(feature_data, 
                                 x='Priority', 
                                 y='Story Points',
                                 size='Business Value',
                                 color='Risk Level',
                                 symbol='Type',
                                 title="Feature Analysis"))

def create_dependency_risk_view():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dependency Network")
        G = nx.DiGraph()
        
        # Create network graph
        for feature in st.session_state.workflow.features:
            G.add_node(feature['id'])
            for dep in feature.get('dependencies', []):
                G.add_edge(dep, feature['id'])
        
        # Use Plotly to create an interactive network visualization
        pos = nx.spring_layout(G)
        edge_trace = go.Scatter(
            x=[], y=[], mode='lines',
            line=dict(width=1, color='#888'),
            hoverinfo='none'
        )
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
            
        node_trace = go.Scatter(
            x=[], y=[], mode='markers+text',
            hoverinfo='text',
            text=[],
            marker=dict(size=20)
        )
        
        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (node,)
            
        fig = go.Figure([edge_trace, node_trace],
                       layout=go.Layout(
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=0,l=0,r=0,t=0),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Risk Analysis")
        risk_data = []
        for feature in st.session_state.workflow.features:
            if feature.get('risk_level'):
                risk_data.append({
                    'Feature': feature['id'],
                    'Risk Level': feature['risk_level'],
                    'Business Value': feature.get('business_value', 0),
                    'Dependencies': len(feature.get('dependencies', []))
                })
        
        risk_df = pd.DataFrame(risk_data)
        st.plotly_chart(px.scatter(risk_df,
                                 x='Dependencies',
                                 y='Business Value',
                                 color='Risk Level',
                                 size='