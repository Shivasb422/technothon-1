# import boto3

 

# # initialize the CloudWatch client
# cloudwatch = boto3.client('cloudwatch')

 

# # set the instance ID for which to get the CPU utilization
# instance_id = 'i-0ac4a07fec31eee94'

 

# # retrieve the average CPU utilization metric for the instance over the last 5 minutes
# response = cloudwatch.get_metric_statistics(
#     Namespace='AWS/EC2',
#     MetricName='CPUUtilization',
#     Dimensions=[
#         {
#             'Name': 'InstanceId',
#             'Value': instance_id
#         },
#     ],
#     StartTime='2023-03-23T19:00:00Z',
#     EndTime='2023-03-24T20:00:00Z',
#     Period=30000,
#     Statistics=['Average']
# )

 

# # extract the average CPU utilization from the response
# datapoints = response['Datapoints']
# if datapoints:
#     cpu_utilization = datapoints[-1]['Average']
# else:
#     cpu_utilization = 0

 

# # print the CPU utilization
# print(f"Average CPU utilization for {instance_id}: {cpu_utilization}%")

import boto3
from datetime import datetime, timedelta
import pytz

 

# initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch')

 

# set the instance ID for which to get the CPU utilization
instance_id = 'i-0ac4a07fec31eee94'
period = 300
x = 10

# get the current time in IST
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_now = datetime.now(ist_timezone)

 

# set the start time and end time to cover the last 5 minutes in IST
ist_end_time = ist_now.replace(second=0, microsecond=0)
ist_start_time = ist_end_time - timedelta(minutes=x)

 

# convert the start time and end time to UTC
utc_start_time = ist_start_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
utc_end_time = ist_end_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

 

# retrieve the average CPU utilization metric for the instance over the last 5 minutes in IST
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance_id
        },
    ],
    StartTime=utc_start_time,
    EndTime=utc_end_time,
    Period=period,
    Statistics=['Average']
)

 

# extract the average CPU utilization from the response
datapoints = response['Datapoints']
if datapoints:
    cpu_utilization = datapoints[-1]['Average']
else:
    cpu_utilization = 0

 

# print the CPU utilization
print(f"Average CPU utilization for {instance_id} over the last {x} minutes (IST): {cpu_utilization}%")