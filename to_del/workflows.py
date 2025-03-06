from dataclasses import dataclass
from typing import List, Dict
import random
from datetime import datetime, timedelta
from agents import Risk, Dependency
from dataclasses import dataclass, field

@dataclass
class ProgramIncrement:
    id: str
    start_date: datetime
    end_date: datetime
    objectives: List[str]
    features: List[Dict]
    teams: List[Dict]
    risks: List[Risk] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    
    def calculate_progress(self) -> Dict:
        return {
            'total_points': sum(f['story_points'] for f in self.features),
            'completed_points': sum(f['story_points'] for f in self.features 
                                 if f.get('status') == 'Completed'),
            'risks_by_severity': self._group_risks_by_severity(),
            'dependency_status': self._analyze_dependency_status()
        }

class SAFeWorkflow:
    def __init__(self):
        self.features = []
        self.teams = []
        self.program_increments = []
        self.historical_data = {}
        
    def generate_synthetic_data(self, num_features: int, num_teams: int):
        # Generate more realistic features
        skills = ['Frontend', 'Backend', 'DevOps', 'QA', 'Architecture', 'Security']
        feature_types = ['Enhancement', 'Bug Fix', 'New Feature', 'Technical Debt']
        
        for i in range(num_features):
            dependencies = []
            if i > 0:  # Create realistic dependency chains
                num_deps = random.randint(0, min(3, i))
                dependencies = [f"F{random.randint(1, i)}" for _ in range(num_deps)]
            
            self.features.append({
                'id': f"F{i+1}",
                'name': f"Feature {i+1}",
                'description': f"Description for Feature {i+1}",
                'type': random.choice(feature_types),
                'story_points': random.randint(5, 21),
                'priority': random.randint(1, 4),
                'dependencies': dependencies,
                'skills_required': random.sample(skills, k=random.randint(1, 3)),
                'business_value': random.randint(1, 10),
                'risk_level': random.choice(['Low', 'Medium', 'High']),
                'status': 'Not Started'
            })
        
        # Generate teams with specializations
        for i in range(num_teams):
            team_size = random.randint(5, 9)
            primary_skills = random.sample(skills, k=random.randint(2, 4))
            self.teams.append({
                'name': f"Team {i+1}",
                'size': team_size,
                'capacity': team_size * 10,
                'capabilities': primary_skills,
                'velocity': random.randint(15, 25),
                'specialization': random.choice(primary_skills),
                'historical_velocity': [
                    random.randint(15, 25) for _ in range(5)
                ]
            })