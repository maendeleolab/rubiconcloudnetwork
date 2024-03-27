#!/usr/bin/env python3

import boto3
import sys
from resources.visibility import *
from time import sleep

# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# ec2 is used to return the "profile_name" (IAM role for the account),
# the service name (in this scenario ec2) and region id.
# This permits us to reuse the functions for any account and region.

# This is a function to describe resources tag names
# The main objective is to access the vlaue of the tag key "Name"


def get_virtual_private_gateway_state(name, ec2):
	try:
		resources = ec2.describe_vpn_gateways(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False
		)
		print(f'virtual_private_gateway_state: {resources["VpnGateways"][0]["State"]}')
		return resources["VpnGateways"][0]["State"]
	except Exception as err:
		logging.error(f'Error found in "get_virtual_private_gateway_state": {err}...')


def get_virtual_private_gateway_id(name, ec2):
	try:
		resources = ec2.describe_vpn_gateways(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				],
				#DryRun=True|False
		)
		print(f'virtual_private_gateway_id: {resources["VpnGateways"][0]["VpnGatewayId"]}')
		return resources["VpnGateways"][0]["VpnGatewayId"]
	except Exception as err:
		logging.error(f'Error found in "get_virtual_private_gateway_id": {err}...')


def virtual_private_gateway(name, aws_bgp_asn, ec2):
	try:
		resources = ec2.create_vpn_gateway(
				#AvailabilityZone='string',
				Type='ipsec.1',
				TagSpecifications=[
						{
								'ResourceType':'vpn-gateway',
								'Tags': [
										{
												'Key': 'Name',
												'Value': name
										},
								]
						},
				],
				AmazonSideAsn=aws_bgp_asn,
				#DryRun=True|False
		)
		print(f'Vpn Gateway Id: {resources["VpnGateway"]["VpnGatewayId"]}')
		while True:
			state = resources["VpnGateway"]["State"]
			if state == "available":
				break
			else:
				sleep(5)
				print(state)
			state
	except Exception as err:
		logging.error(f'Error found in "virtual_private_gateway": {err}...')


def attach_virtual_private_gateway(vpc_id, vpn_gateway_id, ec2):
	try:
		resources = ec2.attach_vpn_gateway(
				VpcId=vpc_id,
				VpnGatewayId=vpn_gateway_id,
				#DryRun=True|False
		)
		while True:
			state = resources["VpcAttachment"]["State"]
			if state == "attached":
				print(f'Virtual Private Gateway {state}...')
				break
			else:
				sleep(5)
				print(state)
			state
	except Exception as err:
		logging.error(f'Error found in attach_"virtual_private_gateway": {err}...')


def describe_vpc_resources(name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs'][0]['Tags']:
            return item['Value']

    except Exception as err:
        logger.error(f'Resource {name} does not exist. Error found: {err}...')


# This functions returns the vpc ipv6 block minus the last 6 characters
# e.g: 2600:1f18:4ac5:ed00::/56
# returns 2600:1f18:4ac5:ed0 to give us the ability to create /64 ipv6 subnets
def get_ipv6_cidr(resource_name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        resource_name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs']:
            ipv6_block = item['Ipv6CidrBlockAssociationSet'][0]['Ipv6CidrBlock']
            print(ipv6_block[:-6])
            return ipv6_block[:-6]
    except Exception as err:
        logger.error(f'Error found in "get_ipv6_cidr" {err}...')


# This is to use for creating route in route tables
def get_ipv6_block(resource_name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        resource_name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs']:
            ipv6_block = item['Ipv6CidrBlockAssociationSet'][0]['Ipv6CidrBlock']
            print(f'Ipv6 Cidr: {ipv6_block}...')
            return ipv6_block
    except Exception as err:
        logger.error(f'Error found in "get_ipv6_block": {err}...')


# This is a function to describe the resources ids
def get_vpc_id(resource_name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        resource_name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs']:
            return item['VpcId']
    except Exception as err:
        logger.error(f'Error found in "get_vpc_id" {err}...')


# This is a function to create resources
def create_vpc_resources(name, cidr, ipv6_cidr, ec2):
    try:
        results = describe_vpc_resources(name, ec2)
        if results == name:
            print(f'Vpc: {name} already exists...')
            pass
        elif results != name:
            print(f'Creating {name}...')
            resources = ec2.create_vpc(
                CidrBlock=cidr,
                AmazonProvidedIpv6CidrBlock=bool(ipv6_cidr), #True|False,
                # Ipv6Pool='string',
                # Ipv6CidrBlock='string',
                # Ipv4IpamPoolId='string',
                # Ipv4NetmaskLength=123,
                # Ipv6IpamPoolId='string',
                # Ipv6NetmaskLength=123,
                # DryRun=True|False,
                InstanceTenancy='default',
                # Ipv6CidrBlockNetworkBorderGroup='string',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': name
                            },
                        ]
                    },
                ]
            )
            print(f'Created vpc id: {resources["Vpc"]["VpcId"]}...')
            return resources
    except Exception as err:
        logger.error(f'Error found in "create_vpc_resources": {err}...')


# The function adds an additional cidr to the vpc
def add_vpc_cidr_block(resource_id, cidr, ipv6_cidr, ec2):
    try:
        if cidr == None:
            pass
        else:
            resources = ec2.associate_vpc_cidr_block(
                AmazonProvidedIpv6CidrBlock=bool(ipv6_cidr), #True|False,
                CidrBlock=cidr,
                VpcId=resource_id
            )
            print(f'Cidr: {cidr} is associated to VpcId: {resource_id}...')
    except Exception as err:
        logger.error(f'Error found in "add_vpc_cidr_block": {err}...')


# The functions modify resources attributes
def modify_dns_hostnames(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableDnsHostnames={
                'Value': value  # True|False
            }
        )
        print(f'Vpc Id: {resource_id} DNS Hostnames Attribute Modified...')
    except Exception as err:
        logger.error(f'Error found in "modify_dns_hostnames": {err}...')


# modify_dns_hostnames(describe_ids(name), value, ec2)
def modify_dns_support(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableDnsSupport={
                'Value': value  # True|False
            }
        )
        print(f'Vpc Id: {resource_id} DNS Support Attribute Modified...')
    except Exception as err:
        logger.error(f'Error found in "modify_dns_support": {err}...')


# modify_dns_support(describe_ids(name), value, ec2)
def modify_network_address_usage_metrics(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableNetworkAddressUsageMetrics={
                'Value': value  # True|False
            }
        )
        print(
            f'Vpc Id: {resource_id} Network Address Usage Metrics Attribute Modified...')
    except Exception as err:
        logger.error(f'Error found in "modify_network_address_usage_metrics": {err}...')


# This is a function to delete resources
def delete_vpc_resources(resource, ec2):
    try:
        if resource == None:
            pass
        else:
            print(f'Delete vpc...')
            resources = ec2.delete_vpc(
                VpcId=resource,
                # DryRun=True|False
            )
    except Exception as err:
        logger.error(f'Error found in "delete_vpc_resources": {err}...')

