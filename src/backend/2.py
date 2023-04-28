import boto3
import sys
from datetime import datetime, timedelta
client = boto3.client('cloudwatch')
response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': 'i-0ac4a07fec31eee94'
                },
            ],
            StartTime=datetime(2023, 3, 23) - timedelta(seconds=600),
            EndTime=datetime(2023, 3, 23),
            Period=3600,
            Statistics=[
                'Average',
            ]
            # Unit='Percent'
        )

datapoints = response['Datapoints']
if datapoints:
    cpu_utilization = datapoints[-1]['Average']
else:

    cpu_utilization = 0


for k, v in response.items():
        if k == 'Datapoints':
            for y in v:
                print(y['Average'])