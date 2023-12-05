#!/usr/bin/env python3

from network_resources.elastic_ips_api_calls import *
from network_resources.subnets_api_calls import *
from time import sleep

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
def create_public_nat(name, subnet, eip, ec2):
	try:
		if get_nat_name(name, ec2) == name:
			print(f'Public nat: {name} already exists...')
			pass
		else:
			resources = ec2.create_nat_gateway(
					AllocationId=eip,
					#ClientToken='string',
					#DryRun=True|False,
					SubnetId=subnet,
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
			state = resources["NatGateway"]["State"]
			while True:
				if state == 'available':
					print(f'{name} state is {state} for next step...')
					break
				elif state == 'failed':
					print(f'{name} state is {state}...')
					print('*** Make sure the elastic ip allocation id is correct ***')
					break
				else:
					sleep(2)
					print(f'{name} state is {state}...')
				state = get_nat_state(name, ec2)

			print(f'Created nat gateway: {resources["NatGateway"]["NatGatewayId"]}')
	except Exception as err:
		print(f' Error found: {err}...')


# This function creates a private nat gateway
def create_private_nat(name, subnet, number_of_secondary_ips, ec2):
	try:
		if get_nat_name(name, ec2) == name:
			print(f'Public nat: {name} already exists...')
			pass
		else:
			resources = ec2.create_nat_gateway(
					#AllocationId=get_allocation_id(eip, ec2),
					#ClientToken='string',
					#DryRun=True|False,
					SubnetId=subnet,
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
					SecondaryPrivateIpAddressCount=int(number_of_secondary_ips)
			)
			state = resources["NatGateway"]["State"]
			while True:
				if state == 'available':
					print(f'{name} state is {state} for next step...')
					break
				elif state == 'failed':
					print(f'{name} state is {state}...')
					print('*** Something went wrong ***')
					break
				else:
					sleep(2)
					print(f'{name} state is {state}...')
				state = get_nat_state(name, ec2)
			print(f'Creating private nat: {name}, number of secondary ips: {number_of_secondary_ips}')
	except Exception as err:
		print(f'Error found: {err}...')


# This function deletes the nat gateway
def delete_nat(name, ec2):
	try:
		resources = ec2.delete_nat_gateway(
			#DryRun=True|False,
			NatGatewayId=get_nat_id(name, ec2)
		)
		state = resources["NatGateway"]["State"]
		while True:
			if state == 'deleted':
				print(f'{name} state is {state}...')
				break
		else:
			sleep(2)
			print(f'{name} state is {state}...')
		state = get_nat_state(name, ec2)
	except Exception as err:
		print(f'Deleting nat {name}...')


