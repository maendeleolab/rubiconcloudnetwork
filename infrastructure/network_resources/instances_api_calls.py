#!/usr/bin/env python3

def deploy_instances(
try:
	instance_name,
	image,
	instance_type,
	key_name,
	max_count,
	min_count,
	monitoring,
	security_group_ids,
	subnet_id,
	user_data,
ec2
	):

	resources = ec2.run_instances(
			ImageId=image,
			InstanceType=instance_type,
			KeyName=key_name,
			MaxCount=int(max_count),
			MinCount=int(min_count),
			Monitoring={
					'Enabled': monitoring #True|False
			},
			SecurityGroupIds=[
					security_group_ids,
			],
			SubnetId=subnet_id,
			UserData=user_data,
			#AdditionalInfo='string',
			#DryRun=True|False,
			#IamInstanceProfile={
			#    'Arn': 'string',
			#    'Name': 'string'
			#},
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
print(=*15)
print(f'Instance id: {resources["Instances"]["InstanceId"]}')
print(f'Instance type: {resources["Instances"]["InstanceType"]}')
print(f'Instance image: {resources["Instances"]["ImageId"]}')
print(f'Instance public dns: {resources["Instances"]["PublicDnsName"]}')
print(f'Instance public ip: {resources["Instances"]["PublicIpAddress"]}')
print(f'Instance private dns: {resources["Instances"]["PrivateDnsName"]}')
print(f'Instance private ip: {resources["Instances"]["PrivateIpAddress"]}')
print(=*15)
except Exception as err:
print(f'Error found: {err}...')
