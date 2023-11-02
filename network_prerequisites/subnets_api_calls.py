#!/usr/bin/env python3

import boto3


# This function creates a subnet in an availability zone

def deploy_subnet(resource, az_id, cidr, vpc_id, ec2):
  try:
    resources = ec2.create_subnet(
	TagSpecifications=[
	    {
		'ResourceType': 'subnet',
		'Tags': [
		    {
			'Key': 'Name',
			'Value': resource
		    },
		]
	    },
	],
	AvailabilityZone=az_id,
	#AvailabilityZoneId='string',
	CidrBlock=cidr,
	#Ipv6CidrBlock='string',
	#OutpostArn='string',
	VpcId=vpc_id,
	#DryRun=True|False,
	#Ipv6Native=True|False
    )
    print(f'{resources["Subnet"]["SubnetId"]}:{resources["Subnet"]["CidrBlock"]} in {resources["Subnet"]["AvailabilityZone"]}...')
  except Exception as err:
    print(f'Error found: {err}...')
