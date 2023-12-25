import boto3
import os
import logging
import json
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
sns_topic_arn = os.environ['SNS_TOPIC_ARN']
sns_client = boto3.client('sns')
all_findings = ["Here is Non-compliant Security Group Rule Report for all regions:"]

# Get a list of all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

for region in regions:
    try:
        ec2 = boto3.client('ec2', region_name=region)
        cloudtrail = boto3.client('cloudtrail', region_name=region)
        paginator = ec2.get_paginator('describe_security_groups')

        for page in paginator.paginate():
            for sg in page['SecurityGroups']:
                for permission in sg['IpPermissions']:
                    if permission['IpProtocol'] == 'tcp':
                        for ip_range in permission['IpRanges']:
                            if ip_range['CidrIp'] == '0.0.0.0/0' and permission['FromPort'] not in [80, 443]:
                                ec2.revoke_security_group_ingress(GroupId=sg['GroupId'], IpPermissions=[permission])
                                logger.info(f"Revoked non-compliant rule from {sg['GroupId']} in region {region}")

                                # Adding port and protocol information
                                port = permission.get('FromPort')
                                protocol = permission['IpProtocol']

                                # Find the creator of the rule
                                try:
                                    events = cloudtrail.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': sg['GroupId']}])
                                    for event in events['Events']:
                                        event_detail = json.loads(event['CloudTrailEvent'])
                                        if event_detail.get('eventName') == 'AuthorizeSecurityGroupIngress':
                                            user_arn = event_detail.get('userIdentity', {}).get('arn', 'Unknown')
                                            finding = f"Region: {region}, Non-compliant rule (Port: {port}, Protocol: {protocol}) revoked from {sg['GroupId']} by {user_arn}"
                                            all_findings.append(finding)
                                            break
                                except Exception as e:
                                    logger.error(f"Error finding rule creator for {sg['GroupId']} in region {region}: {str(e)}")

    except ClientError as e:
        logger.error(f"Error processing security groups in region {region}: {str(e)}")

if len(all_findings) > 1:
    consolidated_message = "\n".join(all_findings)
    try:
        sns_client.publish(TopicArn=sns_topic_arn, Message=consolidated_message)
        logger.info("Sent SNS notification about non-compliant security group rules across all regions.")
    except ClientError as e:
        logger.error(f"An error occurred while sending SNS notification: {e}")

return {"statusCode": 200, "body": "Security group compliance check completed across all regions."}
