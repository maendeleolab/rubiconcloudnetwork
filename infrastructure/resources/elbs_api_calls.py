#!/usr/bin/env python3

from resources.visibility import *


def create_targets(
						elbv2,
						vpc_id,
						target_type,
						ip_address_type,
						targets_name='rubiconcloud_elb',
						protocol='TCP',
						port='5555',
						health_protocol='TCP',
						health_interval='30',
						health_timeout='10',
						healthy_count='5',
						unhealthy_count='10',
	):
	try:
		resources = elbv2.create_target_group(
				Name=targets_name,
				#Protocol='HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
				Protocol=protocol,
				#ProtocolVersion='string',
				Port=int(port),
				VpcId=vpc_id,
				#HealthCheckProtocol='HTTP'|'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
				HealthCheckProtocol=health_protocol,
				#HealthCheckPort='string',
				#HealthCheckEnabled=True|False,
				#HealthCheckPath='string',
				HealthCheckIntervalSeconds=int(health_interval), #5-300
				HealthCheckTimeoutSeconds=int(health_timeout), #2-120
				HealthyThresholdCount=int(healthy_count), #2-10
				UnhealthyThresholdCount=int(unhealthy_count), #2-10
				#Matcher={
				#    'HttpCode': 'string',
				#    'GrpcCode': 'string'
				#},
				#TargetType='instance'|'ip'|'lambda'|'alb',
				TargetType=target_type,
				Tags=[
						{
								'Key': 'Name',
								'Value': targets_name
						},
				],
				IpAddressType=ip_address_type, #'ipv4'|'ipv6'
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "create_targets": {err}...')


def create_elb(
					elb_name,
					subnet1,
					subnet2,
					elb_sg,
					elbv2,
					elb_type,
					ip_address_type='ipv4',
					scheme=None,
	):
	try:
		resources = elbv2.create_load_balancer(
				Name=elb_name,
				Subnets=[
						subnet1,
						subnet2,
				],
				SecurityGroups=[
						elb_sg,
				],
				#Scheme='internet-facing'|'internal',
				Scheme=scheme,
				Tags=[
						{
								'Key': 'Name',
								'Value': elb_name
						},
				],
				#Type='application'|'network'|'gateway',
				Type=elb_type,
				#IpAddressType='ipv4'|'dualstack',
				IpAddressType=ip_address_type,
				#CustomerOwnedIpv4Pool='string'
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "create_elb": {err}...')


def get_elb_arn(elb_name, elbv2):
	try:
		resources = elbv2.describe_load_balancers(
				Names=[
						elb_name,
				]
		)
		print(f'Elb arn: {resources["LoadBalancers"][0]["LoadBalancerArn"]}...')
		return resources["LoadBalancers"][0]["LoadBalancerArn"]
	except Exception as err: 
		logger.error(f'Error found in "get_elb_arn": {err}...')


def get_targets_arn(target_name, elbv2):
	try:
		resources = elbv2.describe_target_groups(
				Names=[
						target_name,
				]
		)
		print(f'Target arn: {resources["TargetGroups"][0]["TargetGroupArn"]}...')
		return resources["TargetGroups"][0]["TargetGroupArn"]
	except Exception as err:
		logger.error(f'Error found in "get_targets_arn": {err}...')


def listeners(
	target_name,
	elb_name,
	port,
	protocol,
	elbv2
	):
	try:
		resources = elbv2.create_listener(
				DefaultActions=[
						{
								'TargetGroupArn': get_targets_arn(target_name, elbv2),
								'Type': 'forward',
						},
				],
				LoadBalancerArn=get_elb_arn(elb_name, elbv2),
				Port=int(port),
				Protocol=protocol,
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "listeners": {err}...')


def register_target(
							target_name,
							instance_id,
							port,
							elbv2
	):
	try:
		resources = elbv2.register_targets(
				TargetGroupArn=get_targets_arn(target_name, elbv2),
				Targets=[
						{
								'Id': instance_id,
								'Port': int(port),
						},
				]
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "register_target": {err}...')


def deregister_target(
							target_name,
							instance_id,
							port,
							elbv2
	):
	try:
		resources = elbv2.deregister_targets(
				TargetGroupArn=get_targets_arn(target_name, elbv2),
				Targets=[
						{
								'Id': instance_id,
								'Port': int(port),
						},
				]
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "deregister_target": {err}...')


def get_elb_state(elb_name, elbv2):
	try:
		resources = elbv2.describe_load_balancers(
				Names=[
						elb_name,
				]
		)
		print(f'Elb state: {resources["LoadBalancers"][0]["State"]["Code"]}...')
		return resources["LoadBalancers"][0]["State"]["Code"]
	except Exception as err: 
		logger.error(f'Error found in "get_elb_state": {err}...')


def delete_targets(target_name, elbv2):
	try:
		resources = elbv2.delete_target_group(
				TargetGroupArn=get_targets_arn(target_name, elbv2)
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "delete_targets": {err}...')


def delete_elb(elb_name, elbv2):
	try:
		resources = elbv2.delete_load_balancer(
				LoadBalancerArn=get_elb_arn(elb_name, elbv2)
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "delete_elb": {err}...')
