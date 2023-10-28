#!/usr/bin/env python3

import boto3, sys

# Creating a boto3 object for the client to interact with
# the ec2 service in aws
org = boto3.client('organizations', region_name='us-east-1')


def describe_org():
  resources = org.describe_organization()
  print(resources)

def create_account():
  resources = org.create_account(
      Email='string',
      AccountName='string',
      #RoleName='string',
      #IamUserAccessToBilling='ALLOW'|'DENY',
      Tags=[
	  {
	      'Key': 'Description',
	      'Value': 'test'
	  },
      ]
  )
  print(resources)
