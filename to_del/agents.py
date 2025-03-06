from crewai import Agent, Task, Crew
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class Risk:
    id: str
    description: str
    impact: str
    probability: float
    mitigation: str
    status: str = "Open"
    owner: Optional[str] = None

@dataclass
class Dependency:
    id: str
    source_feature: str
    target_feature: str
    type: str  # "Technical", "Business", "Architecture"
    status: str = "Open"
    resolution_date: Optional[datetime] = None

class SAFeAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.agent = Agent(
            name=name,
            role=role,
            goal=f"Execute {role} responsibilities effectively",
            backstory=f"An experienced {role} in SAFe implementation",
            verbose=True
        )

class ReleaseTrainEngineer(SAFeAgent):
    def __init__(self, name: str):
        super().__init__(name, "Release Train Engineer")
        self.risks = []
        self.dependencies = []
        
    async def plan_pi(self, teams: List[Dict], features: List[Dict]):
        planning_outcome = {
            'team_assignments': {},
            'dependencies': [],
            'risks': [],
            'capacity_allocation': {},
            'program_board': self._create_program_board(features)
        }
        
        # Advanced feature assignment with load balancing
        for team in teams:
            assigned_features = self._assign_features_with_load_balancing(team, features)
            planning_outcome['team_assignments'][team['name']] = assigned_features
            planning_outcome['capacity_allocation'][team['name']] = self._calculate_capacity_allocation(assigned_features)
            
        # Identify and analyze dependencies
        planning_outcome['dependencies'] = self._analyze_dependencies(planning_outcome['team_assignments'])
        
        # Risk assessment
        planning_outcome['risks'] = self._assess_risks(planning_outcome)
        
        return planning_outcome
    
    def _create_program_board(self, features: List[Dict]):
        sprints = ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4', 'Sprint 5']
        board = {sprint: [] for sprint in sprints}
        
        for feature in features:
            target_sprint = self._determine_optimal_sprint(feature, board)
            board[target_sprint].append(feature)
            
        return board
    
    def _determine_optimal_sprint(self, feature: Dict, board: Dict):
        # Consider dependencies, team capacity, and feature priority
        dependencies = feature.get('dependencies', [])
        if not dependencies:
            # If no dependencies, assign based on priority
            return f"Sprint {min(5, feature['priority'])}"
            
        # Find the latest sprint containing a dependency
        latest_dependency_sprint = 1
        for sprint, features in board.items():
            for f in features:
                if f['id'] in dependencies:
                    latest_dependency_sprint = max(latest_dependency_sprint, 
                                                int(sprint.split()[-1]))
                    
        return f"Sprint {min(5, latest_dependency_sprint + 1)}"
    
    def _assess_risks(self, planning_outcome: Dict) -> List[Risk]:
        risks = []
        
        # Analyze team capacity risks
        for team, allocation in planning_outcome['capacity_allocation'].items():
            if allocation > 85:
                risks.append(Risk(
                    id=f"R{len(risks)+1}",
                    description=f"High capacity utilization for {team}",
                    impact="Potential delivery delays",
                    probability=0.7,
                    mitigation="Consider feature reallocation or capacity increase"
                ))
                
        # Analyze dependency risks
        dependency_clusters = self._identify_dependency_clusters(planning_outcome['dependencies'])
        for cluster in dependency_clusters:
            if len(cluster) > 3:
                risks.append(Risk(
                    id=f"R{len(risks)+1}",
                    description="Complex dependency cluster detected",
                    impact="Increased coordination overhead",
                    probability=0.6,
                    mitigation="Break down features or reorganize teams"
                ))
                
        return risks

class ProductOwner(SAFeAgent):
    def __init__(self, name: str, team_name: str):
        super().__init__(name, "Product Owner")
        self.team_name = team_name
        
    async def refine_backlog(self, features: List[Dict]):
        refined_features = []
        for feature in features:
            refined_feature = self._analyze_feature_value(feature)
            refined_feature = self._break_down_feature(refined_feature)
            refined_features.append(refined_feature)
        return refined_features
    
    def _analyze_feature_value(self, feature: Dict):
        # Simulate value analysis
        feature['business_value'] = random.randint(1, 10)
        feature['time_criticality'] = random.randint(1, 10)
        feature['risk_reduction'] = random.randint(1, 10)
        feature['wsjf'] = (feature['business_value'] + feature['time_criticality'] + 
                          feature['risk_reduction']) / feature['story_points']
        return feature

class DevelopmentTeam(SAFeAgent):
    def __init__(self, name: str, team_name: str):
        super().__init__(name, f"Development Team Member - {team_name}")
        self.team_name = team_name
        self.velocity_history = []
        
    async def estimate_feature(self, feature: Dict):
        base_points = feature['story_points']
        complexity_factor = self._assess_complexity(feature)
        uncertainty_factor = self._assess_uncertainty(feature)
        
        adjusted_points = base_points * complexity_factor * uncertainty_factor
        return round(adjusted_points)
    
    def _assess_complexity(self, feature: Dict):
        factors = {
            'dependencies': len(feature.get('dependencies', [])) * 0.1,
            'skills_required': len(feature.get('skills_required', [])) * 0.15,
            'integration_points': random.randint(1, 3) * 0.1
        }
        return 1 + sum(factors.values())