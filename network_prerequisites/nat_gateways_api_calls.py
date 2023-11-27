#!/usr/bin/env python3

from elastic_ips_api_calls import *
from subnets_api_calls import *



# This function returns the name
def get_nat_name(name, ec2):
  try:
    resources = ec2.describe_nat_gateways(
        #DryRun=True|False,
        Filters=[
            {
              'Name': 'tag:Name',
                'Values': [
                    name,
                ]
            },
        ],
    )
    for item in resources['NatGateways'][0]['Tags']:
      print(f'Nat: {item["Value"]}')
      return item["Value"]
  except Exception as err:
    print(f'Error found: {err}...')

# This function returns the state
def get_nat_state(name, ec2):
  try:
    resources = ec2.describe_nat_gateways(
        #DryRun=True|False,
        Filters=[
            {
              'Name': 'tag:Name',
                'Values': [
                    name,
                ]
            },
        ],
    )
    for item in resources['NatGateways']:
      print(f'Nat: {item["State"]}')
      return item["State"]
  except Exception as err:
    print(f'Error found: {err}...')

# This function returns the id
def get_nat_id(name, ec2):
  try:
    resources = ec2.describe_nat_gateways(
        #DryRun=True|False,
        Filters=[
            {
              'Name': 'tag:Name',
                'Values': [
                    name,
                ]
            },
        ],
    )
    for item in resources['NatGateways']:
      print(f'Nat id: {item["NatGatewayId"]}')
      return item["NatGatewayId"]
  except Exception as err:
    print(f'Error found: {err}...')

# This function creates a public nat gateway
def create_public_nat(name, subnet, ec2):
  try:
    resources = ec2.create_nat_gateway(
        AllocationId=get_allocation_id(name, ec2),
        #ClientToken='string',
        #DryRun=True|False,
        SubnetId=get_subnet_id(subnet, ec2),
        TagSpecifications=[
            {
                'ResourceType': 'natgateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ]
            },
        ],
        #ConnectivityType='private'|'public',
        #SecondaryAllocationIds=[
        #    'string',
        #],
    )
    print(f'Created nat gateway: {resources["NatGatewayId"}')
  except Exception as err:
    print(f' Error found: {err}...')


# This function creates a private nat gateway
def create_private_nat(name, subnet, number_of_secondary_ips, ec2):
  try:
    resources = client.create_nat_gateway(
        AllocationId='string',
        ClientToken='string',
        DryRun=True|False,
        SubnetId='string',
        TagSpecifications=[
            {
                'ResourceType':'natgateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ]
            },
        ],
        ConnectivityType='private',
        SecondaryPrivateIpAddressCount=int(number_of_secondary_private_addresses)
    )
    print(f'Creating private nat: {name}, number of secondary ips: {number_of_secondary_ips}')
  except Exception as err:
    print(f'Error found: {err}...')

