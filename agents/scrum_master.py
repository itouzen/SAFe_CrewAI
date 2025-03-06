from crewai import Agent

class ScrumMaster(Agent):
    def __init__(self, team):
        super().__init__(name=f"ScrumMaster-{team['name']}")
        self.team = team

    def run_standup(self):
        # Gather team updates and identify blockers
        blockers = []
        for member in self.team['members']:
            if "blocker" in member:
                blockers.append({"team": self.team['name'], "blocker": member['blocker']})
        return blockers