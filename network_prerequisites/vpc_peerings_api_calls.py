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


response = client.accept_vpc_peering_connection(
    DryRun=True|False,
    VpcPeeringConnectionId='string'
)



response = client.delete_vpc_peering_connection(
    DryRun=True|False,
    VpcPeeringConnectionId='string'
)



response = client.modify_vpc_peering_connection_options(
    AccepterPeeringConnectionOptions={
        'AllowDnsResolutionFromRemoteVpc': True|False,
        'AllowEgressFromLocalClassicLinkToRemoteVpc': True|False,
        'AllowEgressFromLocalVpcToRemoteClassicLink': True|False
    },
    DryRun=True|False,
    RequesterPeeringConnectionOptions={
        'AllowDnsResolutionFromRemoteVpc': True|False,
        'AllowEgressFromLocalClassicLinkToRemoteVpc': True|False,
        'AllowEgressFromLocalVpcToRemoteClassicLink': True|False
    },
    VpcPeeringConnectionId='string'
)



