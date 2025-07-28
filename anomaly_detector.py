import boto3
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

INSTANCE_ID = "i-0293dc76e816f7b99"
REGION_NAME = "us-east-1"


def fetch_metrics(instance_id: str, region_name: str) -> pd.DataFrame:
    """Fetches the last 3 hours of CPU Utilization metrics from AWS CloudWatch."""
    print(f"Fetching CPU metrics for instance: {instance_id} in region {region_name}...")
    
    client = boto3.client("cloudwatch", region_name=region_name)
    
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "cpu_utilization_query",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": "CPUUtilization",
                        "Dimensions": [{"Name": "InstanceId", "Value": instance_id}],
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
                "ReturnData": True,
            },
        ],
        StartTime=datetime.utcnow() - timedelta(hours=3), 
        EndTime=datetime.utcnow(),                        
    )

    if not response["MetricDataResults"][0]["Timestamps"]:
        print("Warning: No data returned from CloudWatch. The instance may be too new.")
        return pd.DataFrame()

    df = pd.DataFrame({
        "Timestamp": response["MetricDataResults"][0]["Timestamps"],
        "Value": response["MetricDataResults"][0]["Values"],
    })
    
    df = df.sort_values(by="Timestamp").set_index("Timestamp")
    print(f"Successfully fetched {len(df)} data points.")
    return df


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Uses a machine learning model (Isolation Forest) to find unusual data points."""
    if df.empty:
        return df

    print("Running anomaly detection model...")
    model = IsolationForest(contamination=0.05, random_state=42)
    
    df["anomaly"] = model.fit_predict(df[["Value"]])
    
    print("Anomaly detection complete.")
    return df


if __name__ == "__main__":
    print("--- Starting Cloud Service Anomaly Detector ---")
    
    metrics_df = fetch_metrics(INSTANCE_ID, REGION_NAME)


    if not metrics_df.empty:
        anomalies_df = detect_anomalies(metrics_df)
        
        print("\n--- Analysis Results (Most Recent 5 Data Points) ---")
        print(anomalies_df.tail(5))

        found_anomalies = anomalies_df[anomalies_df["anomaly"] == -1]
        if not found_anomalies.empty:
            print(f"\nDetected {len(found_anomalies)} potential anomalies:")
            print(found_anomalies)
        else:
            print("\nNo anomalies detected in the dataset.")