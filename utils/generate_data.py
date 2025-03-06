import pandas as pd
import random

def generate_backlog():
    backlog = []
    for i in range(50):
        backlog.append({
            "id": i,
            "type": random.choice(["Feature", "Epic", "User Story"]),
            "priority": random.randint(1, 5),
            "estimated_effort": random.randint(1, 13)
        })
    return pd.DataFrame(backlog)

if __name__ == "__main__":
    backlog = generate_backlog()
    backlog.to_csv("data/backlog.csv", index=False)