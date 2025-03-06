import sqlite3
import pandas as pd

def get_metrics():
    conn = sqlite3.connect("data/metrics.db")
    query = "SELECT * FROM metrics"
    metrics = pd.read_sql_query(query, conn)
    conn.close()
    return metrics