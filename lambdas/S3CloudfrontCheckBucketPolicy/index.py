import boto3
import json
import os

def lambda_handler(event, context):
s3 = boto3.client('s3')
sns = boto3.client('sns')
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

response = s3.list_buckets()
buckets = response['Buckets']

non_compliant_buckets = []
for bucket in buckets:
    bucket_name = bucket['Name']
    is_public = False
    is_static_website = False
    has_cloudfront_policy = False

    # Check for public access
    try:
        public_access = s3.get_public_access_block(Bucket=bucket_name)
        if not any(public_access['PublicAccessBlockConfiguration'].values()):
            is_public = True
    except Exception as e:
        is_public = True

    # Check for static website hosting
    try:
        if s3.get_bucket_website(Bucket=bucket_name):
            is_static_website = True
    except Exception as e:
        is_static_website = False

    # Check for CloudFront-only bucket policy
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        has_cloudfront_policy = 'CloudFront' in json.loads(policy['Policy'])
    except Exception as e:
        has_cloudfront_policy = False

    # Determine non-compliance
    if is_public and is_static_website and not has_cloudfront_policy:
        non_compliant_buckets.append(bucket_name)

if non_compliant_buckets:
    alert_message = ("Alert! The following buckets are public and are not restricted to only "
                    "CloudFront can get bucket content. Change bucket policy to avoid security issues:\n" +
                    "\n".join(non_compliant_buckets))
    sns.publish(TopicArn=sns_topic_arn, Message=alert_message)
    print(alert_message)
    return alert_message
    return "Non-compliant buckets found"




    