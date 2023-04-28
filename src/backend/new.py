import sys
import boto3
import os
from datetime import datetime, timedelta

os.environ['TZ'] = 'Asia/Kolkata'

aws_access_key_id = os.environ['AKIATCH7KFDEZY2WCB7J']
aws_secret_access_key = os.environ['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']
region = os.environ['ap-south-1']

instance_name = 'Cloud_Cost_Optimization_Server'
instance_id = os.environ['i-0ac4a07fec31eee94']


def initialize_client():

    client = boto3.client(
        'cloudwatch',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region
    )

    return client    

def request_metric(client,InstanceId):

    startTime= datetime.today() + timedelta(days=-1)
    startTimeFormat = startTime.strftime('%Y-%m-%d') + ' 00:00:00'

    endTime = datetime.today() + timedelta(days=-1)
    endTimeFormat = endTime.strftime('%Y-%m-%d') + ' 23:59:59'

    response = client.get_metric_statistics(
        Namespace = 'AWS/EC2',
        Period = 3600,
        StartTime = startTimeFormat,
        EndTime = endTimeFormat,
        MetricName = 'CPUUtilization',
        Statistics=['Maximum','Minimum','Average'],
        Dimensions = [
            {
                'Name': 'InstanceId',
                'Value': InstanceId
            }   
        ],        
    )

    return response["Datapoints"]    

def send_notification(subject,message):
    topic_arn = os.environ['topic_arn']
    sns = boto3.client(
        'sns',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region
        )
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

    return sns

def send_formatted_message(metric_response):
    
    startTime= datetime.today() + timedelta(days=-1)
    startTimeFormat = startTime.strftime('%Y-%m-%d') + ' 00:00:00'

    endTime = datetime.today() + timedelta(days=-1)
    endTimeFormat = endTime.strftime('%Y-%m-%d') + ' 23:59:59'


    Max = str(metric_response[0]["Maximum"]) + "%"
    Min = str(metric_response[0]["Minimum"]) + "%"
    Average = str(metric_response[0]["Average"]) + "%"


    sub = "CPU Utilization Summary from " +  startTimeFormat + " to " + endTimeFormat
    msg = """

        Period: 
        From {startTime} To {endTime}
        ------------------------------------------------------------------------------------
        Metrics Summary:
        ------------------------------------------------------------------------------------

        Instance Name Metrics
        Maximum      :   {Max}
        Minimum      :   {Min}
        Average      :   {Average}
        



        ------------------------------------------------------------------------------------
        """.format(Max=Max, Min=Min, 
        Average=Average,instance_name=instance_name,
        startTime=startTimeFormat,endTime=endTimeFormat)
    send_notification(sub, msg)

def lambda_handler(event,context):

    #getting average,min, max for CPU utilization
    cloudwatch_client = initialize_client()
    metric_response = request_metric(cloudwatch_client,instance_id)

    #send email
    res = send_formatted_message(metric_response)
    print(res)


