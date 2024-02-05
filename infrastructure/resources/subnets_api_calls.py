#!/usr/bin/env python3


import boto3
from resources.visibility import *

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
            # DryRun=True|False,
        )
        for item in resources['Subnets'][0]['Tags']:
            return item['Value']
    except Exception as err:
        logger.error(f'Error found in "describe_subnet_resources": {err}...')


# This function returns the subnet id
def get_subnet_id(subnet_name, ec2):
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
            # DryRun=True|False,
        )
        for item in resources['Subnets']:
            return item['SubnetId']
    except Exception as err:
        logger.error(f'Error found in "get_subnet_id": {err}...')


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
            # AvailabilityZoneId='string',
            CidrBlock=cidr,
            # Ipv6CidrBlock='string',
            # OutpostArn='string',
            VpcId=vpc_id,
            # DryRun=True|False,
            #Ipv6Native=bool(ipv6_only), #True|False
        )
        print(
            f'Created {resources["Subnet"]["SubnetId"]} in {resources["Subnet"]["AvailabilityZone"]}...')
    except Exception as err:
        logger.error(f'Error found in "deploy subnet": {err}...')


# This function creates ipv6 only subnets in availability zones
def deploy_ipv6_subnet(
	ec2, 
	resource, 
	az_id, 
	ipv6_cidr, 
	ipv6_only,
	vpc_id,
	cidr=None 
	):
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
					# AvailabilityZoneId='string',
					CidrBlock=cidr,
					Ipv6CidrBlock=ipv6_cidr,
					# OutpostArn='string',
					VpcId=vpc_id,
					# DryRun=True|False,
					Ipv6Native=bool(ipv6_only), #True|False
			)
			print(
					f'{resources["Subnet"]["SubnetId"]}:{resources["Subnet"]["SubnetId"]} in {resources["Subnet"]["AvailabilityZone"]}...')
	except Exception as err:
			logger.error(f'Error found in "deploy_ipv6_subnet": {err}...')


# This function creates ipv6 only subnets in availability zones
def deploy_ipv6_onlysubnet(
	ec2, 
	resource, 
	az_id, 
	ipv6_cidr, 
	ipv6_only,
	vpc_id
	):
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
					# AvailabilityZoneId='string',
					#CidrBlock=cidr,
					Ipv6CidrBlock=ipv6_cidr,
					# OutpostArn='string',
					VpcId=vpc_id,
					# DryRun=True|False,
					Ipv6Native=bool(ipv6_only), #True|False
			)
			print(
					f'{resources["Subnet"]["SubnetId"]}:{resources["Subnet"]["SubnetId"]} in {resources["Subnet"]["AvailabilityZone"]}...')
	except Exception as err:
			logger.error(f'Error found in "deploy_ipv6_subnet": {err}...')


# This function modifies subnets attributes
def modify_subnet(
	subnet_name,
	assign_ipv6, #True|False
	assign_public_ipv4, #True|False
	enable_dns64, #True|False
	enable_ipv4_dns_hostname, #True|False
	enable_ipv6_dns_hostname, #True|False
	ec2
	):
	try:
		resources = ec2.modify_subnet_attribute(
				AssignIpv6AddressOnCreation={
						'Value': assign_ipv6
				},
				MapPublicIpOnLaunch={
						'Value': assign_public_ipv4
				},
				SubnetId=get_subnet_id(subnet_name, ec2),
				#MapCustomerOwnedIpOnLaunch={
				#    'Value': True|False
				#},
				#CustomerOwnedIpv4Pool='string',
				EnableDns64={
						'Value': enable_dns64
				},
				PrivateDnsHostnameTypeOnLaunch='resource-name',
				EnableResourceNameDnsARecordOnLaunch={
						'Value': enable_ipv4_dns_hostname 
				},
				EnableResourceNameDnsAAAARecordOnLaunch={
						'Value': enable_ipv6_dns_hostname
				},
				#EnableLniAtDeviceIndex=123,
				#DisableLniAtDeviceIndex={
				#    'Value': True|False
				#}
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "modify_subnet": {err}...')

# This function deletes subnets ids
def delete_subnet_resources(subnet_id, ec2):
    try:
        if subnet_id == None:
            pass
        else:
            print('Delete subnet...')
            resources = ec2.delete_subnet(
                SubnetId=subnet_id,
                # DryRun=True|False
            )
    except Exception as err:
        logger.error(f'Error found: {err}...')
