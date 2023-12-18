import json
import os
import http.client
from urllib.parse import urlparse
from datetime import datetime, timedelta

def send_slack_message(webhook_url, message):
    parsed_url = urlparse(webhook_url)
    payload = json.dumps({"text": message})
    headers = {'Content-Type': 'application/json'}

    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("POST", parsed_url.path, payload, headers)
    response = conn.getresponse()
    return response.read().decode()

def adjust_time(time_str):
    aws_time_format = "%Y-%m-%dT%H:%M:%S.%f+0000"
    time_obj = datetime.strptime(time_str, aws_time_format)
    adjusted_time = time_obj + timedelta(hours=2)
    friendly_time_format = "%Y-%m-%d %H:%M:%S"
    return adjusted_time.strftime(friendly_time_format)

def lambda_handler(event, context):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    state_change_time = sns_message.get('StateChangeTime', None)
    adjusted_time_str = adjust_time(state_change_time) if state_change_time else "N/A"

    alarm_name = sns_message.get('AlarmName', 'N/A')
    new_state = sns_message.get('NewStateValue', 'N/A')
    reason = sns_message.get('NewStateReason', 'N/A')

    domain_names = json.loads(os.environ['DOMAIN_NAMES'])
    domain_name = domain_names.get(alarm_name, 'Unknown Domain')

    slack_message = (f"⚠️ Alert: '{domain_name}' has changed state to {new_state}.\n"
                    f"🔍 Reason: {reason}\n"
                    f"🕒 Time: {adjusted_time_str} (local time)\n"
                    f"Please check the Route 53 health checks for more details.")

    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    slack_response = send_slack_message(slack_webhook_url, slack_message)
    print(slack_response)

    return {'statusCode': 200, 'body': json.dumps('Message sent to Slack')}
