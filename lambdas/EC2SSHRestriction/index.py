import boto3
import os
import logging
import json
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
sns_topic_arn = os.environ['SNS_TOPIC_ARN']
all_findings = ["Here is Unrestricted SSH Access Removal Report for all regions:"]

ec2_client_global = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client_global.describe_regions()['Regions']]

for region in regions:
    logger.info(f"Checking region {region} for unrestricted SSH access in security groups")
    try:
        ec2 = boto3.client('ec2', region_name=region)
        cloudtrail = boto3.client('cloudtrail', region_name=region)
        security_groups = ec2.describe_security_groups()['SecurityGroups']

        for sg in security_groups:
            for permission in sg['IpPermissions']:
                if permission['IpProtocol'] == 'tcp' and permission['FromPort'] <= 22 <= permission['ToPort']:
                    for ip_range in permission.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            
                            try:
                                ec2.revoke_security_group_ingress(
                                    GroupId=sg['GroupId'],
                                    IpPermissions=[{
                                        'IpProtocol': 'tcp',
                                        'FromPort': 22,
                                        'ToPort': 22,
                                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                                    }]
                                )
                                logger.info(f"Removed unrestricted SSH access from {sg['GroupId']} in region {region}")

                                
                                events = cloudtrail.lookup_events(
                                    LookupAttributes=[{
                                        'AttributeKey': 'EventName',
                                        'AttributeValue': 'AuthorizeSecurityGroupIngress'
                                    }],
                                    MaxResults=50 
                                )

                                for event in events['Events']:
                                    event_detail = json.loads(event['CloudTrailEvent'])
                                    request_params = event_detail.get('requestParameters', {})
                                    if request_params.get('groupId') == sg['GroupId']:
                                        user_identity = event_detail.get('userIdentity', {}).get('arn', 'Unknown user')
                                        event_time = event_detail.get('eventTime')
                                        message = f"Region: {region}, Security group {sg['GroupId']} was modified to remove unrestricted SSH by {user_identity} on {event_time}."
                                        all_findings.append(message)
                                        break

                            except Exception as e:
                                logger.error(f"Error revoking SSH access for {sg['GroupId']} in region {region}: {str(e)}")

    except ClientError as e:
        logger.error(f"Error processing security groups in region {region}: {str(e)}")

if len(all_findings) > 1:
    consolidated_message = "\n".join(all_findings)
    try:
        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic_arn, Message=consolidated_message)
        logger.info("Sent SNS notification about unrestricted SSH access removal across all regions.")
    except ClientError as e:
        logger.error(f"An error occurred while sending SNS notification: {e}")

return {"statusCode": 200, "body": "Unrestricted SSH access check completed across all regions."}
