#!/usr/bin/env python3
from time import sleep


def get_connect_endpoint_state(endpoint_name, ec2):
	try:
		resources = ec2.describe_instance_connect_endpoints(
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string',
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										endpoint_name,
								]
						},
				],
		)
		return resources["InstanceConnectEndpoints"][0]["State"]
	except Exception as err:
		print(f'Error found in "get_connect_endpoint_state": {err}...')


def get_connect_endpoint_id(endpoint_name, ec2):
	try:
		resources = ec2.describe_instance_connect_endpoints(
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string',
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										endpoint_name,
								]
						},
				],
		)
		return resources["InstanceConnectEndpoints"][0]["InstanceConnectEndpointId"]
	except Exception as err:
		print(f'Error found in "get_connect_endpoint_id": {err}...')


def create_connect_endpoint(endpoint_name, 
                         subnet_id, 
                         sg_id,
                         preserve_client_ip, 
                         ec2
	):
	try: 
		resources = ec2.create_instance_connect_endpoint(
				#DryRun=True|False,
				SubnetId=subnet_id,
				SecurityGroupIds=[
						sg_id,
				],
				PreserveClientIp=preserve_client_ip, #True|False,
				#ClientToken='string',
				TagSpecifications=[
						{
								'ResourceType':'instance-connect-endpoint',
								'Tags': [
										{
												'Key': 'Name',
												'Value': endpoint_name
										},
								]
						},
				]
		)
		print(resources)
		while True:
			if get_connect_endpoint_state(endpoint_name, ec2) != 'create-complete':
				sleep(2)
			elif get_connect_endpoint_state(endpoint_name, ec2) == 'create-complete':
				break
			print(get_connect_endpoint_state(endpoint_name, ec2))
	except Exception as err:
		print(f'Error found in "create_connect_endpoint": {err}...')


def delete_connect_endpoint(endpoint_name, ec2):
	try:
		resources = ec2.delete_instance_connect_endpoint(
				#DryRun=True|False,
				InstanceConnectEndpointId=get_connect_endpoint_id(endpoint_name, ec2)
		)
		while True:
			if get_connect_endpoint_state(endpoint_name, ec2) == 'delete-complete':
				sleep(2)
			else:
				break
			get_connect_endpoint_state(endpoint_name, ec2)
	except Exception as err:
		print(f'Error found in "delete_connect_endpoint": {err}...')


