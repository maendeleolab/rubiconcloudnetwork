#!/usr/bin/env python3
from time import sleep
#from resources.elbs_api_calls import *
from resources.visibility import *


def get_vpce_id(endpoint_name, ec2):
	try:
		resources = ec2.describe_vpc_endpoints(
				#DryRun=True|False,
				#VpcEndpointIds=[
				#    'string',
				#],
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										endpoint_name,
								]
						},
				],
				#MaxResults=123,
				#NextToken='string'
		)
		print(f'Vcpe Id: {resources["VpcEndpoints"][0]["VpcEndpointId"]}...')
		return resources["VpcEndpoints"][0]["VpcEndpointId"]
	except Exception as err:
		logger.error(f'Error found in "get_vpce_id": {err}...')


def get_vpce_name(endpoint_name, ec2):
	try:
		resources = ec2.describe_vpc_endpoints(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										endpoint_name,
								]
						},
				],
				#MaxResults=123,
				#NextToken='string'
		)
		for vpce in resources["VpcEndpoints"][0]["Tags"]:
			if vpce["Value"] == endpoint_name:
					print(f'Vcpe name: {vpce["Value"]}...')
					return True
	except Exception as err:
		logger.error(f'Error found in "get_vpce_name": {err}...')


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
		logger.error(f'Error found in "get_connect_endpoint_state": {err}...')


def get_endpoint_service_id(name, ec2):
	try:
		resources = ec2.describe_vpc_endpoint_services(
				#DryRun=True|False,
				#ServiceNames=[
				#    'string',
				#],
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#MaxResults=123,
				#NextToken='string'
		)
		print(f'Service Id: {resources["ServiceDetails"][0]["ServiceId"]}...')
		return resources['ServiceDetails'][0]['ServiceId']
	except Exception as err:
		logger.error(f'Error found in "get_endpoint_service_id": {err}...')


def get_endpoint_service_name(name, ec2):
	try:
		resources = ec2.describe_vpc_endpoint_services(
				#DryRun=True|False,
				#ServiceNames=[
				#    'string',
				#],
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#MaxResults=123,
				#NextToken='string'
		)
		print(f'Service Name: {resources["ServiceDetails"][0]["ServiceName"]}...')
		return resources['ServiceDetails'][0]['ServiceName']
	except Exception as err:
		logger.error(f'Error found in "get_endpoint_service_name": {err}...')


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
		logger.error(f'Error found in "get_connect_endpoint_id": {err}...')


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
		logger.error(f'Error found in "create_connect_endpoint": {err}...')


def vpc_endpoint_service(
	ec2,
  #elbv2,
	endpoint_name,
	acceptance,
	ipv4_address_type=None,
	ipv6_address_type=None,
	#privatedns=None,
	network_lb='network_lb',
	#gateway_lb='gateway_lb'
	): 
	try:
		resources = ec2.create_vpc_endpoint_service_configuration(
				#DryRun=True|False,
				AcceptanceRequired=acceptance, #True|False,
				#PrivateDnsName=privatedns,
				NetworkLoadBalancerArns=[
						#get_elb_arn(network_lb, elbv2),
						network_lb,
				],
				#GatewayLoadBalancerArns=[
				#		gateway_lb,
				#],
				SupportedIpAddressTypes=[
						ipv4_address_type,
						ipv6_address_type,
				],
				#ClientToken='string',
				TagSpecifications=[
						{
								'ResourceType':'vpc-endpoint-service',
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
	except Exception as err:
		logger.error(f'Error found in "vpc_endpoint_service": {err}...')


def create_vpce(
	endpoint_type, #'Interface'|'Gateway'|'GatewayLoadBalancer'
	vpc_id, # vpc id
	service_name,
	az1,
	az2,
	endpoint_sg,
	ip_address_type, #'ipv4'|'dualstack'|'ipv6'
	privatedns, # true or false
	endpoint_name,
	ec2
	):
	try:
		if get_vpce_name(endpoint_name, ec2) == True:
			print(f'{endpoint_name} already exists...')
			pass
		else:
			resources = ec2.create_vpc_endpoint(
					#DryRun=True|False,
					VpcEndpointType=endpoint_type, #'Interface'|'Gateway'|'GatewayLoadBalancer',
					VpcId=vpc_id,
					ServiceName=get_endpoint_service_name(service_name, ec2),
					#PolicyDocument='string',
					#RouteTableIds=[
					#    'string',
					#],
					SubnetIds=[
							az1,
							az2,
					],
					SecurityGroupIds=[
							endpoint_sg,
					],
					IpAddressType=ip_address_type, #'ipv4'|'dualstack'|'ipv6',
					#DnsOptions={
					#    'DnsRecordIpType': 'ipv4'|'dualstack'|'ipv6'|'service-defined',
					#    'PrivateDnsOnlyForInboundResolverEndpoint': True|False
					#},
					#ClientToken='string',
					PrivateDnsEnabled=privatedns, #True|False,
					TagSpecifications=[
							{
									'ResourceType':'vpc-endpoint',
									'Tags': [
											{
													'Key': 'Name',
													'Value': endpoint_name
											},
									]
							},
					],
					#SubnetConfigurations=[
					#    {
					#        'SubnetId': 'string',
					#        'Ipv4': 'string',
					#        'Ipv6': 'string'
					#    },
					#]
			)
			print(resources)
	except Exception as err:
		logger.error(f'Error found in "create_vpce": {err}...')


def modify_service_permissions(
	endpoint_name,
	principals,
	ec2
	):
	try:
		resources = ec2.modify_vpc_endpoint_service_permissions(
				#DryRun=True|False,
				ServiceId=get_endpoint_service_id(endpoint_name, ec2),
				AddAllowedPrincipals=[
						principals,
				],
				#RemoveAllowedPrincipals=[
				#    'string',
				#]
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "modify_service_permissions": {err}...')

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
		logger.error(f'Error found in "delete_connect_endpoint": {err}...')


def delete_vpc_endpoint_service(endpoint_name, ec2):
	try:
		resources = ec2.delete_vpc_endpoint_service_configurations(
				#DryRun=True|False,
				ServiceIds=[
						get_endpoint_service_id(endpoint_name, ec2),
				]
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "delete_vpc_endpoint_service": {err}...')


def delete_vpce(endpoint_name, ec2):
	try:
		resources = ec2.delete_vpc_endpoints(
				#DryRun=True|False,
				VpcEndpointIds=[
						get_vpce_id(endpoint_name, ec2),
				]
		)
	except Exception as err:
		logger.error(f'Error found in "delete_vpce": {err}...')

# Describe the vpce connections to the service, then reject them.
# This function is used when deleting an endpoint service.
def reject_vpce_connections(service_name, ec2):
	try:
		connections = ec2.describe_vpc_endpoint_connections(
				Filters=[
						{
								'Name': 'service-id',
								'Values': [
										get_endpoint_service_id(service_name, ec2)
								]
						},
				],
		)
		for id in connections["VpcEndpointConnections"]:
			vpce_id = id["VpcEndpointId"]
			print(f'Vpce connections:{vpce_id}...')
			resources = ec2.reject_vpc_endpoint_connections(
					#DryRun=True|False,
					ServiceId=service_name,
					VpcEndpointIds=[
							vpce_id,
					]
			)
			print(resources)
	except Exception as err:
		logger.error(f'Error found in "reject_vpce_connections": {err}...')
