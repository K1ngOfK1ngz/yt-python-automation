#!/usr/bin/python3

import json
import boto3
import requests
import sys


def lambda_handler(event, context):
    region = event['region']
    
    # Get instance id from event, will need this value to pull more details of the ec2 instance [*BONUS: Set up Cloudwatch Event to trigger]
    instance_id = event['detail']['instance-id']
    
    # Get instance details [*BONUS: Use boto3 to get more details]
    instance_ip = event['detail']['instance-ip']
    instance_name = event['detail']['instance-name']
    
    HOST_NAME = "ip-172-31-93-xxx" # Replace with your hostname
    SITE_NAME = "monitoring" # Replace with your sitename
    API_URL   = "http://{}/{}/check_mk/api/1.0".format(HOST_NAME, SITE_NAME)
    
    # Retrieve creds - event test json will pass this in [*BONUS use SSM Parameter Store!]
    USERNAME = event['checkmk_creds']['admin']
    PASSWD  = event['checkmk_creds']['passwd']

    # Build the header content
    headers_details = {"Content-Type": "application/json", "Accept" : "application/json", "Authorization" : "Bearer {} {}".format(USERNAME, PASSWD)}
    host_data = json.dumps({
        "attributes" : {
            "ipaddress" : instance_ip
        },
        "folder" : "/",
        "host_name" : instance_name
    })
    
    HOST_API = API_URL + "/domain-types/host_config/collections/all"
    r = requests.post(HOST_API, host_data, headers = headers_details, verify=False)
    print(r.text)
    
    # The code above only puts the host to add in pending status. Another API call needs to be requested to activate new changes
    activate_body = json.dumps({
        "force_foreign_changes" : "false",
        "redirect" : "false",
        "sites" : [SITE_NAME]
    })
    

    activate_api = API_URL + "/domain-types/activation_run/actions/activate-changes/invoke"
    r = requests.post(activate_api, activate_body, headers = headers_details, verify=False)
    print(r.text)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
