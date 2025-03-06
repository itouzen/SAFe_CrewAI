from crewai import Agent

class DevelopmentTeam(Agent):
    def __init__(self, name, members, velocity):
        super().__init__(name=f"DevTeam-{name}")
        self.members = members
        self.velocity = velocity

    def complete_tasks(self, tasks):
        completed_tasks = []
        remaining_velocity = self.velocity

        for task in tasks:
            if task['estimated_effort'] <= remaining_velocity:
                completed_tasks.append(task)
                remaining_velocity -= task['estimated_effort']
            else:
                task['estimated_effort'] -= remaining_velocity
                break

        return completed_tasks