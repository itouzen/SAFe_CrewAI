from crewai import Agent
from pydantic import BaseModel

class ReleaseTrainEngineer(Agent, BaseModel):
    role: str
    goal: str
    backstory: str

    def __init__(self, role: str, goal: str, backstory: str):
        super().__init__(name="RTE")  # This calls the parent class constructor
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def assign_feature(self, feature, teams):
        # Assign features based on team capacity
        for team in teams:
            if team['capacity'] >= feature['estimated_effort']:
                team['capacity'] -= feature['estimated_effort']
                feature['assigned_team'] = team['name']
                return team
        raise Exception("No team has enough capacity for this feature!")

    def identify_dependencies(self, backlog):
        # Identify dependencies between features
        dependencies = []
        for item in backlog:
            if "depends_on" in item:
                dependencies.append((item['id'], item['depends_on']))
        return dependencies

    def resolve_risks(self, risks):
        for risk in risks:
            print(f"Resolved risk for team: {risk['team']}")

    def evaluate_performance(self, teams, progress):
        # Calculate team velocity and delivery rates
        metrics = []
        for team in teams:
            completed = sum(item['progress'] for item in progress if item['team'] == team['name'])
            metrics.append({
                "team": team['name'],
                "velocity": completed / team['capacity']
            })
        return metrics

    def provide_recommendations(self, metrics):
        recommendations = []
        for metric in metrics:
            if metric['velocity'] < 0.75:
                recommendations.append(f"Increase capacity for team {metric['team']}")
        return recommendations