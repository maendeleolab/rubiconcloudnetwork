#!/usr/bin/env python3

#This function returns the default acl
def tag_default_acl(ec2):
	try:
		resources = ec2.describe_network_acls(
				#DryRun=True|False,
		)
		for item in resources['NetworkAcls']:
			if item['IsDefault'] == True:
				print(f'acl id: {item["NetworkAclId"]} is default..')
				ec2.create_tags(
				#DryRun=True|False,
				Resources=[
						item["NetworkAclId"],
				],
				Tags=[
						{
								'Key': 'Name',
								'Value': 'default'
						},
					]
				)
				print('Adding tag: "Name":"default"...')
	except Exception as err:
		print(f'Error found: {err}...')

#This function returns the acl id
def get_acl_id(acl_name, ec2):
	try:
		resources = ec2.describe_network_acls(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										acl_name,
								]
						},
				],
				#DryRun=True|False,
				#NetworkAclIds=[
				#    'string',
				#],
		)
		for item in resources['NetworkAcls']:
			return item['NetworkAclId']
	except Exception as err:
		print(f'Error found: {err}...')


#This function returns the acl name
def get_acl_name(acl_name, ec2):
	try:
		resources = ec2.describe_network_acls(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										acl_name,
								]
						},
				],
				#DryRun=True|False,
				#NetworkAclIds=[
				#    'string',
				#],
		)
		for item in resources['NetworkAcls'][0]['Tags']:
			return item['Value']
	except Exception as err:
		print(f'Error found: {err}...')


#This function returns the acl association id
def get_acl_association_id(acl_name, ec2):
	try:
		resources = ec2.describe_network_acls(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										acl_name,
								]
						},
				],
				#DryRun=True|False,
				#NetworkAclIds=[
				#    'string',
				#],
		)
		for item in resources['NetworkAcls'][0]['Associations']:
			return item['NetworkAclAssociationId']
	except Exception as err:
		print(f'Error found: {err}...')

# This function creates a network acl
def create_vpc_acl(acl_name, vpc_id, ec2):
	try:
		if get_acl_name(acl_name, ec2) == acl_name:
			print(f'Acl {acl_name} already exists...')
			pass
		else:
			resources = ec2.create_network_acl(
					#DryRun=True|False,
					VpcId=vpc_id,
					TagSpecifications=[
							{
									'ResourceType': 'network-acl',
									'Tags': [
											{
													'Key': 'Name',
													'Value': acl_name
											},
									]
							},
					]
			)
			print(f'Creating acl {acl_name} for vpc id {vpc_id}...')
	except Exception as err:
		print(f'Error found: {err}...')

# This function creates network acl entries
def add_entry_to_vpc_acl(acl_name, 
                    cidr_entry, 
                    in_or_out,
                    port_range_from, 
                    port_range_to, 
                    protocol_number, 
                    rule_action, 
                    rule_number,
                    ec2 
                  ):
	try:
		resources = ec2.create_network_acl_entry(
					CidrBlock=cidr_entry,
					#DryRun=True|False,
					Egress=in_or_out, #True|False
					#Ipv6CidrBlock='string',
					NetworkAclId=get_acl_id(acl_name, ec2),
					PortRange={
							'From': int(port_range_from),
							'To': int(port_range_to)
					},
					Protocol=protocol_number,
					RuleAction=rule_action, #'allow'|'deny'
					RuleNumber=int(rule_number)
			)
		print(f'Adding acl entry: {rule_action} -> {cidr_entry} in {acl_name}...')
	except Exception as err:
		print(f'Error found: {err}...')

# This function creates network acl entries for ICMP only
def add_icmp_to_vpc_acl(acl_name, 
                    cidr_entry, 
                    icmp_code,
                    icmp_type,
                    in_or_out,
                    port_range_from, 
                    port_range_to, 
                    protocol_number, 
                    rule_action, 
                    rule_number,
                    ec2 
                  ):
	try:
		resources = ec2.create_network_acl_entry(
					CidrBlock=cidr_entry,
					#DryRun=True|False,
					Egress=in_or_out, #True|False
					IcmpTypeCode={
							'Code': int(icmp_code),
							'Type': int(icmp_type)
					},
					#Ipv6CidrBlock='string',
					NetworkAclId=get_acl_id(acl_name, ec2),
					PortRange={
							'From': int(port_range_from),
							'To': int(port_range_to)
					},
					Protocol=protocol_number,
					RuleAction=rule_action, #'allow'|'deny'
					RuleNumber=int(rule_number)
			)
		print(f'Adding icmp entry: {rule_action} -> {cidr_entry} in {acl_name}...')
	except Exception as err:
		print(f'Error found: {err}...')


# This function associates acl to a subnet
def associate_acl_to_subnet(default_acl, acl_name, ec2):
	try:
		resources = ec2.replace_network_acl_association(
				AssociationId=get_acl_association_id(default_acl, ec2),
				#DryRun=True|False,
				NetworkAclId=get_acl_id(acl_name, ec2)
		)
		print(f'associating {acl_name}...')
	except Exception as err:
		print(f'Error found: {err}...')


# This function removes acl entries
def remove_entry_from_vpc_acl(acl_name, in_or_out, rule_number, ec2):
	try:
		resources = ec2.delete_network_acl_entry(
				#DryRun=True|False,
				Egress=in_or_out, #True|False,
				NetworkAclId=get_acl_id(acl_name, ec2),
				RuleNumber=rule_number
		)
		print(f'Removing rule_number {rule_number} from acl_name...')
	except Exception as err:
		print(f'Error found: {err}...')


# This function deletes acl 
def delete_vpc_acl(acl_name, ec2):
	try:
		resources = ec2.delete_network_acl(
				#DryRun=True|False,
				NetworkAclId=get_acl_id(acl_name, ec2)
		)
		print(f'Deleting acl {acl_name}...')
	except Exception as err:
		print(f'Error found: {err}...')


