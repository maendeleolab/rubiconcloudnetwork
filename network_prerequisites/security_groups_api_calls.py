#!/usr/bin/env python3


# This function gets the security-group id
def get_sg_id(sg_name, ec2):
	try:
		resources = ec2.describe_security_groups(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										sg_name,
								]
						},
				],
				#DryRun=True|False,
				#NextToken='string',
				#MaxResults=123
		)
		print(f'Security-group ID: {resources["SecurityGroups"]["GroupId"]...')
		return resources["SecurityGroups"]["GroupId"]

	except Exception as err:
		print(f'Error found: {err}...')


# This function gets the name of the security-group
def get_sg_id(sg_name, ec2):
	try:
		resources = ec2.describe_security_groups(
				Filters=[
						{
								'Name': 'tag:Name',
								'Values': [
										sg_name,
								]
						},
				],
				#DryRun=True|False,
				#NextToken='string',
				#MaxResults=123
		)
		print(f'Security-group name: {resources["SecurityGroups"]["GroupName"]...')
		return resources["SecurityGroups"]["GroupName"]

	except Exception as err:
		print(f'Error found: {err}...')


# This function creates a security-group
def create_sg(sg_name, vpc_id, ec2):
  try:
    resources = ec2.create_security_group(
        Description=sg_name,
        GroupName=sg_name,
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType':'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': sg_name
                    },
                ]
            },
        ],
        #DryRun=True|False
    )
    print(f'Creating security-group: {sg_name}...')
  except Exception as err:
    print(f'Error found: {err}...')


# This function adds egress entries to a security-group
def add_egress_sg(sg_group_id, 
                  from_port, 
                  protocol_number, 
                  cidr_entry, 
                  description, 
                  prefixlist_id, 
                  to_port, 
                  ec2
                  ):
  try:
    resources = ec2.authorize_security_group_egress(
        #DryRun=True|False,
        GroupId=sg_group_id,
        IpPermissions=[
            {
                'FromPort': from_port,
                'IpProtocol': protocol_number,
                'PrefixListIds': [
                    {
                        'Description': description,
                        'PrefixListId': prefixlist_id
                    },
                ],
                'ToPort': to_port,
                    },
                ]
            },
        ],
    )
    print(f'Adding egress rule to security-group: {sg_group_id}...')
  except Exception as err:
    print(f'Error found: {err}...')

# This function adds ingress entries to a security-group
def add_ingress_sg(sg_group_id, 
                  from_port, 
                  protocol_number, 
                  cidr_entry, 
                  description, 
                  prefixlist_id, 
                  to_port, 
                  ec2
                  ):
  try:
    resources = ec2.authorize_security_group_ingress(
        #DryRun=True|False,
        GroupId=sg_group_id,
        IpPermissions=[
            {
                'FromPort': from_port,
                'IpProtocol': protocol_number,
                'PrefixListIds': [
                    {
                        'Description': description,
                        'PrefixListId': prefixlist_id
                    },
                ],
                'ToPort': to_port,
                    },
                ]
            },
        ],
    )
    print(f'Adding ingress rule to security-group: {sg_group_id}...')
  except Exception as err:
    print(f'Error found: {err}...')


# This function revokes the egress security-group
def remove_egress_sg(sg_group_id, 
                  from_port, 
                  protocol_number, 
                  cidr_entry, 
                  description, 
                  prefixlist_id, 
                  to_port, 
                  ec2
                  ):
  try:
    resources = ec2.revoke_security_group_egress(
        #DryRun=True|False,
        GroupId=sg_group_id,
        IpPermissions=[
            {
                'FromPort': from_port,
                'IpProtocol': protocol_number,
                'PrefixListIds': [
                    {
                        'Description': description,
                        'PrefixListId': prefixlist_id
                    },
                ],
                'ToPort': to_port,
                    },
                ]
            },
        ],
    )
    print(f'Adding egress rule to security-group: {sg_group_id}...')
  except Exception as err:
    print(f'Error found: {err}...')

# This function deletes a security group
def remove_ingress_sg(sg_group_id, 
                  from_port, 
                  protocol_number, 
                  cidr_entry, 
                  description, 
                  prefixlist_id, 
                  to_port, 
                  ec2
                  ):
  try:
    resources = ec2.revoke_security_group_egress(
        #DryRun=True|False,
        GroupId=sg_group_id,
        IpPermissions=[
            {
                'FromPort': from_port,
                'IpProtocol': protocol_number,
                'PrefixListIds': [
                    {
                        'Description': description,
                        'PrefixListId': prefixlist_id
                    },
                ],
                'ToPort': to_port,
                    },
                ]
            },
        ],
    )
    print(f'Adding egress rule to security-group: {sg_group_id}...')
  except Exception as err:
    print(f'Error found: {err}...')

# This funcion deletes security-groups

response = client.delete_security_group(
    GroupId='string',
    #GroupName='string',
    #DryRun=True|False
)


