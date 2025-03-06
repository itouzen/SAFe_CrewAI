from agents.scrum_master import ScrumMaster
from agents.rte import ReleaseTrainEngineer

def run_daily_standup(teams):
    rte = ReleaseTrainEngineer()
    blockers = []

    # Each Scrum Master gathers updates from their team
    for team in teams:
        scrum_master = ScrumMaster(team)
        team_blockers = scrum_master.run_standup()
        blockers.extend(team_blockers)

    # RTE resolves major blockers across teams
    if blockers:
        rte.resolve_risks(blockers)

    return blockers