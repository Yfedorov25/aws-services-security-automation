Overview
This repository contains a collection of AWS CloudFormation templates and Lambda functions designed to enhance security and compliance across various AWS services. Each solution focuses on a specific security aspect, ensuring best practices are followed within your AWS environment.

Table of Contents
Solutions Overview
Usage Instructions
Solutions Description
S3 with CloudFront Check
EC2 Instance Type Check
SSH Access Restriction and CloudTrail Investigation
Restrict Open Ports
CloudWatch Logs Retention Check
Route 53 Health Check and Alarm
Contributing
License
Solutions Overview
The repository includes the following solutions:

S3 with CloudFront Check
EC2 Instance Type Check
SSH Access Restriction and CloudTrail Investigation
Restrict Open Ports
CloudWatch Logs Retention Check
Route 53 Health Check and Alarm
Each solution is stored in separate folders within the services-security and route53-public-http-hosts directories. The corresponding Lambda function code for each solution is located in the lambdas folder.

Usage Instructions
To deploy these solutions:

Navigate to the desired solution's folder.
Review and update the CloudFormation template and Lambda function as needed.
Deploy the template using the AWS Management Console, AWS CLI, or your preferred deployment tool.

Solutions Description

S3 with CloudFront Check
Purpose: Regularly assesses S3 buckets for compliance with security and integration standards.
Features:
Regular scanning of S3 buckets.
Detection of buckets lacking CloudFront integration and having public access.
Notifications via SNS for non-compliance.
Use Case: Ideal for maintaining data security and optimizing content delivery efficiency.

EC2 Instance Type Check
Purpose: Ensures that EC2 instances conform to pre-defined, authorized types.
Features:
Continuous scanning of EC2 instances in all regions.
Verification of instances against an approved list.
Reports instances that don't meet the specified criteria.
Use Case: Enforces compliance with organizational standards and prevents unauthorized instance usage, enhancing both security and cost management.

SSH Access Restriction and CloudTrail Investigation
Purpose: Secures network access by ensuring SSH access is strictly controlled.
Features:
Audits security groups for open SSH ports.
Leverages CloudTrail for audit trails of changes and access attempts.
Issues alerts for any detected SSH access non-compliance.
Use Case: Crucial for securing network access points and monitoring for unauthorized configuration changes.

Restrict Open Ports
Purpose: Focuses on keeping only essential ports open to minimize security risks.
Features:
Scans and identifies non-standard open ports.
Automatically closes non-compliant ports.
Sends detailed reports and alerts of changes.
Use Case: Vital for reducing potential entry points for cyber attacks and maintaining a robust security posture.

CloudWatch Logs Retention Check
Purpose: Standardizes log retention across all CloudWatch Log Groups.
Features:
Consistent review of log group retention settings.
Application of uniform retention policies.
Reporting of adjustments across all regions.
Use Case: Essential for compliant and efficient log management, aligning with organizational or regulatory requirements.

Route 53 Health Check and Alarm
Purpose: Provides proactive monitoring and alerts for domain health issues.
Features:
Implements health checks for specific domains.
Sets up alarms for instant alerts on issues.
Facilitates quick responses through Lambda integrations.
Use Case: Key for maintaining domain availability and swift response to potential downtimes or disruptions.

Contributing
Contributions to this repository are welcome. Please ensure that your pull requests are well-documented and follow the existing structure for consistency.
