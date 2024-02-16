#!/usr/bin/env python3
from resources.visibility import *


# This function returns the internet gateway tag "Name" key
def get_igw_name(igw_name, ec2):
    try:
        if igw_name == None:
            pass
        else:
            resources = ec2.describe_internet_gateways(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            igw_name,
                        ]
                    },
                ],
                # DryRun=True|False,
            )
            for item in resources['InternetGateways'][0]['Tags']:
                print(f'Resource name: {item["Value"]}...')
                return item['Value']
    except Exception as err:
        logger.error(f'Error found in "get_igw_name": {err}...')


# This function returns the internet gateway id
def get_igw_id(igw_name, ec2):
    try:
        if igw_name == None:
            pass
        else:
            resources = ec2.describe_internet_gateways(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            igw_name,
                        ]
                    },
                ],
                # DryRun=True|False,
            )
            for item in resources['InternetGateways']:
                print(f'{igw_name}: {item["InternetGatewayId"]}...')
                return item['InternetGatewayId']
    except Exception as err:
        logger.error(f'Error found in "get_igw_id": {err}...')


# This function returns the state of the internet gateway attachment
def get_igw_attachment_state(igw_name, ec2):
    try:
        if igw_name == None:
            pass
        else:
            resources = ec2.describe_internet_gateways(
                # DryRun=True|False,
                InternetGatewayIds=[
                    igw_name,
                ],
            )
            for item in resources['InternetGateways'][0]['Attachments']:
                print(
                    f'Internet gateway: {igw_name}, state: {item["State"]}...')
                return item['State']
    except Exception as err:
        logger.error(f'Error found in "get_igw_attachment_state": {err}...')


# This function creates the internet gateway
def create_igw(igw, ec2):
    try:
        if get_igw_name(igw, ec2) == igw:
            print(f'Internet Gateway: {igw} already exists...')
            pass
        else:
            resources = ec2.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': igw
                            },
                        ]
                    },
                ],
                # DryRun=True|False
            )
            print(
                f'{igw}: {resources["InternetGateway"]["InternetGatewayId"]}...')
    except Exception as err:
        logger.error(f'Error found in "create_igw": {err}...')


# This function attaches the internet gateway to a vpc
def create_igw_attachment(igw_name, vpc_id, ec2):
    try:
        resources = ec2.attach_internet_gateway(
            # DryRun=True|False,
            InternetGatewayId=get_igw_id(igw_name, ec2),
            VpcId=vpc_id
        )
        print(f'Attaching igw: {igw_name} to vpc id: {vpc_id}...')
    except Exception as err:
        logger.error(f'Error found in "create_igw_attachment": {err}...')


# This function detaches the internet gateway to a vpc
def detach_igw(igw_name, vpc_id, ec2):
    try:
        resources = ec2.detach_internet_gateway(
            # DryRun=True|False,
            InternetGatewayId=get_igw_id(igw_name, ec2),
            VpcId=vpc_id
        )
        print(f'Detaching igw: {igw_name} from vpc id: {vpc_id}...')
    except Exception as err:
        logger.error(f'Error found in "detach_igw": {err}...')


def get_ipv6_eigw_id(name, ec2):
	try:
		resources = ec2.describe_egress_only_internet_gateways(
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string',
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				]
		)
		print(f'{resources["EgressOnlyInternetGateways"][0]["EgressOnlyInternetGatewayId"]}...')
		return resources["EgressOnlyInternetGateways"][0]["EgressOnlyInternetGatewayId"]
	except Exception as err:
		logger.error(f'Error found in "get_ipv6_eigw_id": {err}...')


def get_ipv6_eigw_state(name, ec2):
	try:
		resources = ec2.describe_egress_only_internet_gateways(
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string',
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				]
		)
		print(f'{resources["EgressOnlyInternetGateways"][0]["Attachments"][0]["State"]}...')
		return resources["EgressOnlyInternetGateways"][0]["Attachments"][0]["State"]
	except Exception as err:
		logger.error(f'Error found in "get_ipv6_eigw_id": {err}...')


def get_ipv6_eigw_name(name, ec2):
	try:
		resources = ec2.describe_egress_only_internet_gateways(
				#DryRun=True|False,
				#MaxResults=123,
				#NextToken='string',
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										name,
								]
						},
				]
		)
		for item in resources["EgressOnlyInternetGateways"][0]["Tags"]:
			if item['key'] == 'Name':
				print(f'Name: {item["value"]}...')
				return item['value']
	except Exception as err:
		logger.error(f'Error found in "get_ipv6_eigw_id": {err}...')


def create_ipv6_eigw(name, vpc_id, ec2):
	try:
		if get_ipv6_eigw_name(name, ec2) == name:
			print(f'{name} already exists...')
			pass
		else:
			resources = ec2.create_egress_only_internet_gateway(
					#ClientToken='string',
					#DryRun=True|False,
					VpcId=vpc_id,
					TagSpecifications=[
							{
									'ResourceType':'egress-only-internet-gateway',
									'Tags': [
											{
													'Key': 'Name',
													'Value': name
											},
									]
							},
					]
			)
			print(resources)
			while True:
				if get_ipv6_eigw_state(name, ec2) == 'attached':
					get_ipv6_eigw_state(name, ec2)
					break
				else:
					sleep(2)
				get_ipv6_eigw_state(name, ec2)
	except Exception as err:
		logger.error(f'Error found in "create_ipv6_eigw": {err}...')


# This function deletes the internet gateway
def delete_igw(igw_id, ec2):
    try:
        if igw_id == None:
            pass
        else:
            print(f'Delete {igw_id}...')
            resources = ec2.delete_internet_gateway(
                # DryRun=True|False,
                InternetGatewayId=igw_id
            )
    except Exception as err:
        logger.error(f'Error found in "delete_igw": {err}...')


def delete_ipv6_eigw(resource_id, ec2):
	try:
		resources = ec2.delete_egress_only_internet_gateway(
				#DryRun=True|False,
				EgressOnlyInternetGatewayId=get_ipv6_eigw_id(resource_id, ec2)
		)
	except Exception as err:
		logger.error(f'Error found in "delete_ipv6_eigw": {err}...')


