#!/usr/bin/env python3



def get_vpc_peering_connection_id(name, ec2):
	try:
		resources = ec2.describe_vpc_peering_connections(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#MaxResults=200
		)
		print(f'Peering connection id:
		{resources["VpcPeeringConnections"]["VpcPeeringConnectionId"]')
		return resources["VpcPeeringConnections"]["VpcPeeringConnectionId"]
	except Exception as err:
		print(f'Error found: {err}...')


def get_vpc_peering_connection_name(name, ec2):
	try:
		resources = ec2.describe_vpc_peering_connections(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#NextToken='string'
				#MaxResults=200
		)
		for item in resources['VpcPeeringConnections'][0]['Tags']:
			print(f'Vpc peering: {item["Value"]}')
			return item["Value"]
	except Exception as err:
		print(f'Error found: {err}...')


def get_vpc_peering_connection_status(name, ec2):
	try:
		resources = ec2.describe_vpc_peering_connections(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False,
				#NextToken='string'
				#MaxResults=200
		)
		for item in resources['VpcPeeringConnections'][0]['Status']:
			print(f'Vpc peering: {item["Code"]}')
			return item["Code"]
	except Exception as err:
		print(f'Error found: {err}...')



def accept_vpc_peering(name, ec2):
	try:
		resources = ec2.accept_vpc_peering_connection(
				#DryRun=True|False,
				VpcPeeringConnectionId=get_vpc_peering_connection_name(name, ec2)
		)
		print(f'Peering connection: {name} accepted...')
		return get_vpc_peering_connection_status(name, ec2)
	except Exception as err:
		print(f'Error found: {err}...')


def delete_vpc_peering(name, ec2):
	try:
		resources = ec2.delete_vpc_peering_connection(
				#DryRun=True|False,
				VpcPeeringConnectionId=get_vpc_peering_connection_name(name, ec2)
		)
	except Exception as err:
		print(f'Error found: {err}...')


def modify_vpc_peering(name, accepter_dns=None, requester_dns=None, ec2):
	try:
		response = client.modify_vpc_peering_connection_options(
				AccepterPeeringConnectionOptions={
						'AllowDnsResolutionFromRemoteVpc': accepter_dns, #True|False,
				},
				#DryRun=True|False,
				RequesterPeeringConnectionOptions={
						'AllowDnsResolutionFromRemoteVpc': requester_dns, #True|False,
				},
				VpcPeeringConnectionId=get_vpc_peering_connection_name(name, ec2)
		)
	except Exception as err:
		print(f'Error found: {err}...')


