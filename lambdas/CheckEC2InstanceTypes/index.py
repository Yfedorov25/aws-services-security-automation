import boto3
import json
import logging
import os
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
sns_topic_arn = os.environ['SNS_TOPIC_ARN']
all_findings = ["Here is EC2 Instance Type Enforcement Report for all regions:"]
acceptable_types = ['t2.micro', 't3.micro', 't3.large']

# Get a list of all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

for region in regions:
    ec2 = boto3.client('ec2', region_name=region)
    cloudtrail = boto3.client('cloudtrail', region_name=region)

    paginator = ec2.get_paginator('describe_instances')
    for page in paginator.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                instance_state = instance['State']['Name']
                launch_time = instance['LaunchTime']

                if instance_type not in acceptable_types and instance_state == 'running':
                    # Lookup CloudTrail for events around the launch time
                    events = cloudtrail.lookup_events(
                        LookupAttributes=[
                            {'AttributeKey': 'ResourceName', 'AttributeValue': instance_id}
                        ],
                        StartTime=launch_time - timedelta(minutes=10),
                        EndTime=launch_time + timedelta(minutes=10),
                        MaxResults=50
                    )

                    user_identity = "Unknown"
                    for event in events['Events']:
                        event_detail = json.loads(event.get('CloudTrailEvent', '{}'))
                        if event_detail.get('eventName') == 'StartInstances':
                            user_identity = event_detail.get('userIdentity', {}).get('arn', 'Unknown')
                            break

                    ec2.stop_instances(InstanceIds=[instance_id])
                    launch_time_str = launch_time.strftime('%Y-%m-%d %H:%M:%S')
                    instance_info = f"Region: {region}, Instance {instance_id} of type {instance_type} launched on {launch_time_str} by {user_identity} was stopped."
                    all_findings.append(instance_info)

if len(all_findings) > 1:
    message = "\n".join(all_findings)
    sns_client = boto3.client('sns')
    sns_client.publish(TopicArn=sns_topic_arn, Message=message)
    logger.info("Sent SNS notification about non-compliant EC2 instances across all regions.")

return {
    'statusCode': 200,
    'body': 'EC2 instance type enforcement completed across all regions.'
}