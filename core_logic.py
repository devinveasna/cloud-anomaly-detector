import boto3
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import json

INSTANCE_ID = "i-0293dc76e816f7b99"
REGION_NAME = "us-east-1"

def fetch_metrics(instance_id: str, region_name: str) -> pd.DataFrame:
    """Fetches the last 3 hours of CPU Utilization metrics from AWS CloudWatch."""
    print(f"Fetching CPU metrics for instance: {instance_id}...")
    client = boto3.client("cloudwatch", region_name=region_name)
    response = client.get_metric_data(
        MetricDataQueries=[{"Id":"cpu","MetricStat":{"Metric":{"Namespace":"AWS/EC2","MetricName":"CPUUtilization","Dimensions":[{"Name":"InstanceId","Value":instance_id}]},"Period":300,"Stat":"Average"},"ReturnData":True}],
        StartTime=datetime.utcnow()-timedelta(hours=3), EndTime=datetime.utcnow()
    )
    if not response["MetricDataResults"][0]["Timestamps"]:
        print("Warning: No data returned from CloudWatch.")
        return pd.DataFrame()
    df = pd.DataFrame({"Timestamp": response["MetricDataResults"][0]["Timestamps"], "Value": response["MetricDataResults"][0]["Values"]})
    return df.sort_values(by="Timestamp").set_index("Timestamp")

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detects anomalies using an Isolation Forest model."""
    if df.empty: return df
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(df[["Value"]])
    return df

def run_full_analysis():
    """
    Runs the full analysis process and returns results in a dictionary.
    """
    print("--- Running Full Analysis ---")
    metrics_df = fetch_metrics(INSTANCE_ID, REGION_NAME)

    if metrics_df.empty:
        return {"status": "NO_DATA", "message": "Could not retrieve metrics from CloudWatch."}

    anomalies_df = detect_anomalies(metrics_df)

    results_list = json.loads(anomalies_df.reset_index().to_json(orient='records', date_format='iso'))

    return {
        "status": "SUCCESS",
        "instance_id": INSTANCE_ID,
        "analysis_timestamp_utc": datetime.utcnow().isoformat(),
        "results": results_list
    }