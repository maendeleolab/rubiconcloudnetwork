#!/usr/bin/env python3

from organizations_api_calls import *

# Creating a boto3 object for the client to interact with
# the ec2 service in aws
org = boto3.client('organizations', region_name='us-east-1')


describe_org()

