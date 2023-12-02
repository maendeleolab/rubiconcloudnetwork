#!/usr/bin/env python3



# This function returns the allocation id
def get_allocation_id(name, ec2):
	try:
		resources = ec2.describe_addresses(
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
		for item in resources["Addresses"]:
			print(f'Allocation id: {item["AllocationId"]}')
			return item["AllocationId"]
	except Exception as err:
		print(f'Error found: {err}...')



# This function returns the allocation id
def get_address_name(name, ec2):
	try:
		resources = ec2.describe_addresses(
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
		for item in resources["Addresses"][0]['Tags']:
			print(f'Allocation id: {item["Value"]}')
			return item["Value"]
	except Exception as err:
		print(f'Error found: {err}...')



# This function returns the NetworkBorderGroup
def get_networkborder_group(name, ec2):
	try:
		resources = ec2.describe_addresses(
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
		for item in resources["Addresses"]:
			print(f'Allocation id: {item["NetworkBorderGroup"]}')
			return item["NetworkBorderGroup"]
	except Exception as err:
		print(f'Error found: {err}...')



# This function returns the association id
def get_association_id(name, ec2):
	try:
		resources = ec2.describe_addresses(
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
		for item in resources["Addresses"]:
			print(f'Association id: {item["AssociationId"]}')
			return item["AssociationId"]
	except Exception as err:
		print(f'Error found: {err}...')



# This function allocates a public ip address
# from aws public ipv4 pool
def allocate_public_ipv4(name, ec2):
	try:
		if get_address_name(name, ec2) == name:
			print(f'Address: {name} already exists...')
			pass
		else:
			resources = ec2.allocate_address(
					Domain='vpc',
					#Address='string',
					#PublicIpv4Pool='string',
					#NetworkBorderGroup='string',
					#CustomerOwnedIpv4Pool='string',
					#DryRun=True|False,
					TagSpecifications=[
							{
									'ResourceType':'elastic-ip',
									'Tags': [
											{
													'Key': 'Name',
													'Value': name
											},
									]
							},
					]
			)
			print(f'Allocated public ip: {resources["PublicIp"]}')
	except Exception as err:
		print(f'Error found: {err}...')



# This function disassociates the public ip from
# resources e.g: nat gateway
def detach_public_ipv4(name, ec2):
	try:
		resources = ec2.disassociate_address(
				AssociationId=get_association_id(name, ec2),
				#DryRun=True|False
		)
		print(f'Detaching address: {name}')
	except Exception as err:
		print(f'Error found: {err}...')



# This function releases the public ip
def release_public_ipv4_address(name, ec2):
	try:
		resources = ec2.release_address(
				AllocationId=get_allocation_id(name, ec2),
				#NetworkBorderGroup='string',
				#DryRun=True|False
		)
		print(f'Releasing allocation address: {name}')
	except Exception as err:
		print(f'Error found: {err}...')


