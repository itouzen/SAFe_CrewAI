import random

def execute_sprint(teams, backlog):
    sprint_progress = []

    for team in teams:
        velocity = team['velocity']
        completed_work = random.randint(velocity - 2, velocity + 2)

        # Update backlog items assigned to the team
        assigned_items = [item for item in backlog if item['assigned_team'] == team['name']]
        for item in assigned_items:
            if item['estimated_effort'] <= completed_work:
                item['status'] = "Completed"
                completed_work -= item['estimated_effort']
            else:
                item['estimated_effort'] -= completed_work
                completed_work = 0

        sprint_progress.append({
            "team": team['name'],
            "progress": sum(1 for i in assigned_items if i['status'] == "Completed"),
            "remaining": sum(1 for i in assigned_items if i['status'] != "Completed")
        })

    return backlog, sprint_progress