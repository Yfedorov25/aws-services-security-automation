# AWS Services Security Automation

## Overview

This repository contains a collection of AWS CloudFormation templates and Lambda functions designed to enhance security and compliance across various AWS services. Each solution focuses on a specific security aspect, ensuring best practices are followed within your AWS environment.

## Table of Contents

- [Solutions Overview](#solutions-overview)
- [Usage Instructions](#usage-instructions)
- [Deployment Instructions](#deployment-instructions)
- [Solutions Description](#solutions-description)
- [Contributing](#contributing)
- [License](#license)

## Solutions Overview

The repository includes the following solutions:

- S3 with CloudFront Check
- EC2 Instance Type Check
- SSH Access Restriction and CloudTrail Investigation
- Restrict Open Ports
- CloudWatch Logs Retention Check
- Route 53 Health Check and Alarm

Each solution is stored in separate folders within the `services-security` and `route53-public-http-hosts` directories. The corresponding Lambda function code for each solution is located in the `lambdas` folder.

## Usage Instructions

To deploy these solutions:

1. Navigate to the desired solution's folder.
2. Review and update the CloudFormation template and Lambda function as needed.
3. Deploy the template using the AWS Management Console, AWS CLI, or your preferred deployment tool.

## Deployment Instructions

This repository uses a GitHub Actions workflow for automated deployment of CloudFormation templates. To set up and use this workflow:

1. **Configure GitHub Secrets**:
    - Navigate to your GitHub repository's settings.
    - Go to the "Secrets" section.
    - Add the following secrets:
        - `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
        - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
    These credentials should be for an IAM user with permissions necessary to deploy the CloudFormation templates.

2. **Set Environment Variables**:
    - In the GitHub Actions workflow file, ensure the environment variables `STACK_NAME`, `STACK_NAME_ROUTE53`, `S3_BUCKET_NAME`, `S3_BUCKET_NAME_ROUTE_53`, and `AWS_DEFAULT_REGION` are correctly set.

3. **Deployment Process**:
    - The workflow is triggered on a push to the `main` branch.
    - It performs the following steps for each template:
        - Checks out the code.
        - Sets up Python 3.8.
        - Installs the AWS SAM CLI.
        - Configures AWS credentials using the provided secrets.
        - Builds the SAM application for each CloudFormation template in the respective directories.
        - Deploys each built template using AWS SAM, creating or updating the specified CloudFormation stacks.

4. **Monitor Deployment**:
    - Check the Actions tab in your GitHub repository to monitor the deployment process.

## Solutions Description

### S3 with CloudFront Check

**Purpose:** Regularly assesses S3 buckets for compliance with security and integration standards.

**Features:**
- Regular scanning of S3 buckets for security checks.
- Detection of buckets that lack CloudFront integration and are publicly accessible.
- Notification dispatch via SNS for non-compliant findings.

**Use Case:** Ideal for maintaining data security and optimizing content delivery efficiency.

### EC2 Instance Type Check

**Purpose:** Ensures EC2 instances conform to predefined, authorized types to maintain organizational standards.

**Features:**
- Continuous scanning of EC2 instances across all regions.
- Verification of instances against an approved list.
- Automated reporting of instances that do not meet the specified criteria.

**Use Case:** Enforces compliance with organizational standards and prevents unauthorized instance usage, enhancing both security and cost management.

### SSH Access Restriction and CloudTrail Investigation

**Purpose:** Secures network access by monitoring and controlling SSH access through security groups.

**Features:**
- Audits security groups for open SSH ports.
- Integrates with CloudTrail to track configuration changes and access attempts.
- Alerts on non-compliance with SSH access controls.

**Use Case:** Crucial for securing network access points and monitoring for unauthorized configuration changes.

### Restrict Open Ports

**Purpose:** Maintains a minimal security risk posture by ensuring only essential ports are accessible.

**Features:**
- Scans for and identifies open ports that are non-compliant with security policies.
- Automatically closes ports that should not be open.
- Sends detailed reports and alerts when ports are modified or closed.

**Use Case:** Vital for reducing potential entry points for cyber attacks and maintaining a robust security posture.

### CloudWatch Logs Retention Check

**Purpose:** Enforces a standardized retention policy across all CloudWatch Log Groups for compliance.

**Features:**
- Reviews and adjusts retention settings for CloudWatch Log Groups.
- Applies uniform retention policies across all regions.
- Documents and reports on retention policy enforcement actions.

**Use Case:** Essential for compliant and efficient log management, aligning with organizational or regulatory requirements.

### Route 53 Health Check and Alarm

**Purpose:** Offers proactive surveillance and alerting mechanisms for domain health and availability.

**Features:**
- Configures health checks for critical domains.
- Establishes CloudWatch Alarms for immediate issue notification.
- Empowers rapid response capabilities through Lambda function integrations.

**Use Case:** Key for maintaining domain availability and swift response to potential downtimes or disruptions.

## Contributing

I welcome contributions to this repository. If you have suggestions or improvements, please submit a pull request or open an issue.
