from agents.rte import ReleaseTrainEngineer

def run_inspect_and_adapt(teams, progress):
    rte = ReleaseTrainEngineer()

    # Collect metrics and performance data
    metrics = rte.evaluate_performance(teams, progress)

    # Identify areas for improvement
    recommendations = rte.provide_recommendations(metrics)

    return metrics, recommendations