import boto3
from datetime import datetime, timedelta
from operator import itemgetter
import smtplib
# from email.mime.text import MIMEText


AccessKey = "AKIATCH7KFDEZY2WCB7J"
SecretKey = "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"

# Mail sender function
# def SendMail(alert):
#     # Define to/from
#     sender = 'sender email'
#     recipient = 'recipient email'

#     # Create message
#     msg = MIMEText(alert)
#     msg['Subject'] = "CPU Utilization Alert on server with InstanceID %s " % InstanceID
#     msg['From'] = sender
#     msg['To'] = recipient

#     # Create server object with SSL option
#     server = smtplib.SMTP_SSL('smtp.zoho.com', 465)         # May be another mail server

#     # Perform operations via server
#     server.login('mail login', 'mail password')
#     server.sendmail(sender, [recipient], msg.as_string())
#     server.quit()


now = datetime.utcnow()  # Now time in UTC format
past = now - timedelta(minutes=120)  # Minus 60 minutes

# Amazon Cloud Watch connection
client_cw = boto3.client(
    'cloudwatch',
    aws_access_key_id = AccessKey,
    aws_secret_access_key = SecretKey,

)

# Amazon EC2 connection
client_ec2 = boto3.client(
    'ec2',
    aws_access_key_id = AccessKey,
    aws_secret_access_key = SecretKey,

)

response = client_ec2.describe_instances()  # Get all instances from Amazon EC2

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        # This will print output the value of the Dictionary key 'InstanceId'
        print(instance["InstanceId"])

        # Get CPU Utilization for each InstanceID
        CPUUtilization = client_cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance["InstanceId"]}],
            StartTime=past,
            EndTime=now,
            Period=600,
            Statistics=['Average'])

        datapoints = CPUUtilization['Datapoints']                               # CPU Utilization results
        last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]    # Last result
        utilization = last_datapoint['Average']                                 # Last utilization
        load = round((utilization / 100.0), 3)                                  # Last utilization in %
        timestamp = str(last_datapoint['Timestamp'])                            # Last utilization timestamp
        print("{0} load at {1}".format(load, timestamp))

        # Send mail if CPU load more than 50%
        if load > 50:
            InstanceID = instance["InstanceId"]
            print("Upscale")