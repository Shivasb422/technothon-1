import boto3
import datetime

 

# create a Boto3 session with your AWS credentials
session = boto3.Session(
    aws_access_key_id='AKIATCH7KFDEZY2WCB7J',
    aws_secret_access_key='IhPrHDZHaJDR8VSEUUAwqQT/G/xpqkZq9km5DLQm',
    region_name='ap-south-1'
)

 

# create a CloudWatch client
cloudwatch = session.client('cloudwatch')

 

# specify the time range for which to fetch the metric data
end_time = datetime.datetime.utcnow()  # current time in UTC
start_time = end_time - datetime.timedelta(minutes=1440)  # 5 minutes ago

 
ec2Instances = boto3.resource('ec2')
for instance in ec2Instances.instances.all():
# print(listOfInstances)
# use the CloudWatch client to fetch the CPUUtilization metric for the specified instance
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',  # the namespace for EC2 metrics
        MetricName='CPUUtilization',  # the name of the metric to fetch
        Dimensions=[  # the dimensions of the metric
            {
                'Name': 'InstanceId',
                'Value': instance.id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # the granularity of the metric data (in seconds)
        Statistics=['Average']  # the type of statistic to fetch (e.g. average, maximum, minimum)
    )
    datapoints = response['Datapoints']
    if datapoints:
        average_cpu_utilization = sum(point['Average'] for point in datapoints) / len(datapoints)
        print(f"Average CPU utilization for {instance.id}: {average_cpu_utilization:.2f}%")
    else:
        print("No CPU utilization data available for the specified time range.")

   

