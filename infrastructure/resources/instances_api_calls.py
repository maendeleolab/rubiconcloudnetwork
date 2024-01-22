#!/usr/bin/env python3
from time import sleep
from resources.visibility import *


def get_instance_id(name, ec2):
	try:
		resources = ec2.describe_instances(
			Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string'
		)
		for tag in resources['Reservations'][0]['Instances'][0]['Tags']:
				print(f'Id: {resources["Reservations"][0]["Instances"][0]["InstanceId"]}')
				return resources["Reservations"][0]["Instances"][0]["InstanceId"]
	except Exception as err:
		logger.error(f'Error found in "get_instance_id": {err}...')


def get_instance_state(name, ec2):
	try:
		resources = ec2.describe_instances(
			Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string'
		)
		print(f'State:{resources["Reservations"][0]["Instances"][0]["State"]["Name"]}')
		return resources["Reservations"][0]["Instances"][0]["State"]["Name"]
	except Exception as err:
		logger.error(f'Error found in "get_instance_state": {err}...')


def get_instance_name(name, ec2):
	try:
		resources = ec2.describe_instances(
			Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string'
		)
		for tag in resources['Reservations'][0]['Instances'][0]['Tags']:
				print('='*80)
				print(f'Name: {tag["Value"]}')
				print(f'Id: {resources["Reservations"][0]["Instances"][0]["InstanceId"]}')
				print(f'Type: {resources["Reservations"][0]["Instances"][0]["InstanceType"]}')
				print(f'Image: {resources["Reservations"][0]["Instances"][0]["ImageId"]}')
				#print(f'Public dns:{resources["Reservations"][0]["Instances"][0]["PublicDnsName"]}')
				#print(f'Public ip:{resources["Reservations"][0]["Instances"][0]["PublicIpAddress"]}')
				print(f'Private dns:{resources["Reservations"][0]["Instances"][0]["PrivateDnsName"]}')
				print(f'Private ip:{resources["Reservations"][0]["Instances"][0]["PrivateIpAddress"]}')
				print('='*80)
				return tag['Value']
	except Exception as err:
		logger.error(f'Error found in "get_instance_name": {err}...')


def deploy_instances(
	instance_name,
	image,
	instance_type,
	key_name,
	max_count,
	min_count,
	monitoring,
	security_group_ids,
	subnet_id,
	associate_public_ip,
	#profile_arn,
	profile_name,
	user_data,
	ec2
	):
	try:
		if get_instance_name(instance_name, ec2) == instance_name:
			print(f'{instance_name} already exists...')
			pass
		else:
			resources = ec2.run_instances(
					ImageId=image,
					InstanceType=instance_type,
					KeyName=key_name,
					MaxCount=int(max_count),
					MinCount=int(min_count),
					Monitoring={
							'Enabled': monitoring #True|False
					},
					#SecurityGroupIds=[
					#		security_group_ids,
					#],
					#SubnetId=subnet_id,
					NetworkInterfaces=[
													{
															'AssociatePublicIpAddress': associate_public_ip, # True|False,
					'DeviceIndex': 0,
					'Groups': [
													security_group_ids,
											],
					'SubnetId': subnet_id,
					#'ConnectionTrackingSpecification': {
					#								'TcpEstablishedTimeout': 300, # in: 60 seconds. Max: 432000
					#								'UdpStreamTimeout': 60, # Min: 60 seconds. Max: 180 seconds
					#								'UdpTimeout': 60 # Min: 30 seconds. Max: 60 seconds
					#						}
													}
					],
					UserData=user_data,
					#AdditionalInfo='string',
					#DryRun=True|False,
					IamInstanceProfile={
					    #'Arn': profile_arn,
					    'Name': profile_name
					},
					TagSpecifications=[
							{
									'ResourceType':'instance',
									'Tags': [
											{
													'Key': 'Name',
													'Value': instance_name
											},
									]
							},
					],
					MaintenanceOptions={
							'AutoRecovery': 'default'
					},
			)
			print(resources)
			while True:
				if get_instance_state(instance_name, ec2) != 'running':
					sleep(2)
				elif get_instance_state(instance_name, ec2) == 'running':
					break
				get_instance_state(instance_name, ec2)
	except Exception as err:
		logger.error(f'Error found in "deploy_instances": {err}...')


def delete_instance(instance_name, ec2):
	try:
		resources = ec2.terminate_instances(
				InstanceIds=[
						get_instance_id(instance_name, ec2),
				],
				#DryRun=True|False
		)
		print(resources)
		while True:
			if get_instance_state(instance_name, ec2) != 'terminated':
				sleep(2)
			elif get_instance_state(instance_name, ec2) == 'terminated':
				break
			get_instance_state(instance_name, ec2)
	except Exception as err:
		logger.error(f'Error found in "delete_instance": {err}...')

