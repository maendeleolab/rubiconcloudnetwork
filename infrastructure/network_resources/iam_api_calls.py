#!/usr/bin/env python3
import json
import boto3



def create_iam_role(role_name, policy, iam):
    try:
        resources = iam.create_role(
            # Path='string',
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(policy),
            Description=role_name,
            # MaxSessionDuration=123,
            # PermissionsBoundary='string',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': role_name
                },
            ]
        )
        print(resources)
    except Exception as err:
        print(f'Error found: {err}...')



def create_role(role_name, allowed_services, iam):
    """
    Creates a role that lets a list of specified services assume the role.

    :param role_name: The name of the role.
    :param allowed_services: The services that can assume the role.
    :return: The newly created role.
    """
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": service},
                "Action": "sts:AssumeRole",
            }
            for service in allowed_services
        ],
    }

    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        print(role)
    except Exception as err:
        print(err)
    else:
        return role



def attach_policy(role_name, policy_arn, iam):
	try:
		resources = iam.attach_role_policy(
				RoleName=role_name,
				PolicyArn=policy_arn
		)
		print(resources)
	except Exception as err:
		print(err)



def create_profile(profile_name, iam):
	try:
		resources = iam.create_instance_profile(
				InstanceProfileName=profile_name,
				#Path='string',
				Tags=[
						{
								'Key': 'Name',
								'Value': profile_name
						},
				]
		)
		print(resources)
	except Exception as err:
		print(err)



def get_profile_arn(profile_name, iam):
	try:
		resources = iam.get_instance_profile(
				InstanceProfileName=profile_name
		)
		print(f'Profile: {profile_name}, arn: {resources["InstanceProfile"]["Arn"]}')
		return resources["InstanceProfile"]["Arn"]
	except Exception as err:
		print(f'Error found: {err}...')



def get_profile_data(profile_name, iam):
	try:
		resources = iam.get_instance_profile(
				InstanceProfileName=profile_name
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



def adding_role_to_profile(profile_name, role_name, iam):
	try:
		resources = iam.add_role_to_instance_profile(
				InstanceProfileName=profile_name,
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



def remove_role_from_profile(profile_name, role_name, iam):
	try:
		resources = iam.remove_role_from_instance_profile(
				InstanceProfileName=profile_name,
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



def delete_profile(profile_name, iam):
	try:
		resources = iam.delete_instance_profile(
				InstanceProfileName=profile_name
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



def detach_policy_from_role(role_name, policy_arn, iam):
	try:
		resources = iam.detach_role_policy(
				RoleName=role_name,
				PolicyArn=policy_arn
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



def remove_role(role_name, iam):
	try:
		resources = iam.delete_role(
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')


