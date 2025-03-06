from agents.rte import ReleaseTrainEngineer
from agents.scrum_master import ScrumMaster

def run_pi_planning(backlog, teams):
    # Provide the required fields for RTE
    rte = ReleaseTrainEngineer(
        role="RTE",
        goal="Deliver value",
        backstory="Experienced RTE with a history of successful PI planning"
    )
    scrum_masters = [ScrumMaster(team) for team in teams]

    # Assign features to teams while considering dependencies and capacity
    for feature in backlog[backlog['type'] == "Feature"].to_dict('records'):
        assigned_team = rte.assign_feature(feature, teams)
        print(f"Assigned Feature {feature['id']} to Team {assigned_team['name']}")

    # Identify and log dependencies
    dependencies = rte.identify_dependencies(backlog)
    print(f"Dependencies Identified: {dependencies}")

    # Return updated backlog, team status, and dependency information
    return backlog, teams, dependencies