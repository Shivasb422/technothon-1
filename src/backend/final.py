import streamlit as st
import boto3
import datetime
import pandas as pd

# Define the Streamlit app
st.title('AWS EC2 CPU Utilization')
st.write('Enter the region and time range to fetch the CPUUtilization metric data for all EC2 instances in the region.')

# Get user input for region and minutes
region = st.selectbox('Select the AWS region:', ['us-east-1', 'us-west-1', 'us-west-2', 'ap-south-1', 'ap-northeast-1'])
minutes = st.number_input('Enter the number of minutes to go back in time:', value=1440, step=1)

# Create a Boto3 session with your AWS credentials
session = boto3.Session(
    aws_access_key_id='AKIATCH7KFDEZY2WCB7J',
    aws_secret_access_key='IhPrHDZHaJDR8VSEUUAwqQT/G/xpqkZq9km5DLQm',
    region_name=region
)

# Create a CloudWatch client
cloudwatch = session.client('cloudwatch')

# Specify the time range for which to fetch the metric data
end_time = datetime.datetime.utcnow()  # current time in UTC
start_time = end_time - datetime.timedelta(minutes=minutes)

# Get all EC2 instances in the specified region
ec2Instances = boto3.resource('ec2', region_name=region)

# Create a button to initiate the calculation
if st.button('Get CPU Utilization'):
    # Use the CloudWatch client to fetch the CPUUtilization metric for each instance
    cpu_data = []
    for instance in ec2Instances.instances.all():
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance.id
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,
            Statistics=['Average']
        )
        datapoints = response['Datapoints']
        if datapoints:
            average_cpu_utilization = sum(point['Average'] for point in datapoints) / len(datapoints)
            cpu_data.append({'Instance ID': instance.id, 'Average CPU Utilization': f'{average_cpu_utilization:.2f} %'})
        else:
            cpu_data.append({'Instance ID': instance.id, 'Average CPU Utilization': 'No CPU utilization data available'})

    # Display the CPU utilization data in a table
    df = pd.DataFrame(cpu_data)
    total_average = df['Average CPU Utilization'].str.rstrip(' %').astype('float').mean()
    st.write(df)
    st.write(f'Total Average CPU Utilization: {total_average:.2f} %')
    
    # Determine scaling recommendation based on total average CPU utilization
    if total_average < 25:
        st.warning('Scaling recommendation: CPU utilization is below 25%, so you may be able to save costs by scaling down the instance')
    elif total_average >= 25 and total_average <= 75:
        st.warning('Scaling recommendation: CPU utilization is between 25% and 80%, so the instance is being used normally.')
    else:
        st.warning('Scaling recommendation: CPU utilization is above 80%, so you may need to consider scaling up the instance.')
