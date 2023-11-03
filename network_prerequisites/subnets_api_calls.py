#!/usr/bin/env python3

import boto3


# This function creates subnets in availability zones
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

# This function returns the subnet name
def describe_subnet_resources(subnet_name, ec2):
  try:
    resources = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    subnet_name,
                ]
            }
        ]
        #DryRun=True|False,
    )
    for item in resources['Subnets'][0]['Tags']:
        return item['Value']
  except Exception as err:
      print(f'Error found: {err}...')

# This function returns the subnet id
def get_subnet_ids(subnet_name, ec2):
  try:
    resources = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    subnet_name,
                ]
            }
        ]
        #DryRun=True|False,
    )
    for item in resources['Subnets']:
      print(f'{subnet_name}:{item["SubnetId"]}...')
      return item['SubnetId']
  except Exception as err:
      print(f'Error found: {err}...')

# This function deletes subnets ids
def delete_subnet_resources(subnet_id, ec2):
  try:
    if subnet_id == None:
      pass
    else:
      print('Delete subnet...')
      resources = ec2.delete_subnet(
          SubnetId=subnet_id,
          #DryRun=True|False
      )
  except Exception as err:
    print(f'Error found: {err}...')
