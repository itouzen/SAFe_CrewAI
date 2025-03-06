from crewai import Agent

class ProductOwner(Agent):
    def __init__(self):
        super().__init__(name="Product Owner")
    
    def prioritize_backlog(self, backlog):
        # Prioritize backlog items by business value and urgency
        return sorted(backlog, key=lambda x: (x['priority'], -x['estimated_effort']))