#!/usr/bin/env python3
import json
import boto3
from resources.visibility import *


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
        logger.error(f'Error found in "create_iam_role": {err}...')


# This creates a role and includes the trust policy
def create_role(
					role_name, 
					allowed_services, 
					iam
	):
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
        print(f'Create role: {role["Role"]["Arn"]}...')

    except Exception as err:
        logger.error(f'Error found in "create_role": {err}..')
    else:
        return role


def attach_policy(
							role_name, 
							policy_arn,
							iam
	):
	try:
		resources = iam.attach_role_policy(
				RoleName=role_name,
				PolicyArn=policy_arn
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "attach_policy": {err}...')


# This function attaches a policy to a role
# Not easy to use alone, It specifically created
# to be reused with create_policy_document
def attach_policy_doc(
							role_name, 
							policy_arn,
							policy_doc, 
							iam
	):
	try:
		resources = iam.attach_role_policy(
				RoleName=role_name,
				PolicyArn=policy_arn
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "attach_policy": {err}...')


# This function creates a policy doc and attaches it to a role
# in one shot.
def create_policy_document(role_name, policy_name, policy_doc, iam):
	try:
		resources = iam.create_policy(
				PolicyName=policy_name,
				PolicyDocument=policy_doc,
				Description=policy_name,
				Tags=[
						{
								'Key': 'Name',
								'Value': policy_name
						},
				]
		)
		print(f'Policy arn: {resources["Policy"]["Arn"]}...')
		policy_arn = resources["Policy"]["Arn"]
		attach_policy_doc(
									role_name,
									policy_arn,
									policy_doc,
									iam
			)

	except Exception as err:
		logger.error(f'Error found in "create_policy_document": {err}..')


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
		logger.error(f'Error found in "create_profile": {err}..')


def get_policy_arn(policy_name, iam):
	try:
		resources = iam.list_policies(
				Scope='Local',
				OnlyAttached=True,
				#MaxItems=123
		)
		if resources["Policies"][0]["PolicyName"] == policy_name:
			print(f'Policy Arn: {resources["Policies"][0]["Arn"]}...')
			return resources["Policies"][0]["Arn"]
	except Exception as err:
		logger.error(f'Error found in "get_policy_arn": {err}...')


def get_profile_arn(profile_name, iam):
	try:
		resources = iam.get_instance_profile(
				InstanceProfileName=profile_name
		)
		return resources["InstanceProfile"]["Arn"]
	except Exception as err:
		logger.error(f'Error found in "get_profile_arn": {err}...')


def get_role_arn(role_name, iam):
	try:
		resources = iam.get_role(
				RoleName=role_name
		)
		print(f'role arn: {resources["Role"]["Arn"]}')
		return resources["Role"]["Arn"]
	except Exception as err:
		logger.error(f'Error found in "get_role_arn": {err}...')


def get_profile_data(profile_name, iam):
	try:
		resources = iam.get_instance_profile(
				InstanceProfileName=profile_name
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "get_profile_data": {err}...')


def adding_role_to_profile(profile_name, role_name, iam):
	try:
		resources = iam.add_role_to_instance_profile(
				InstanceProfileName=profile_name,
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "adding_role_to_profile": {err}...')


def remove_role_from_profile(profile_name, role_name, iam):
	try:
		resources = iam.remove_role_from_instance_profile(
				InstanceProfileName=profile_name,
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "remove_role_from_profile": {err}...')


def delete_profile(profile_name, iam):
	try:
		resources = iam.delete_instance_profile(
				InstanceProfileName=profile_name
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "delete_profile": {err}...')


def detach_policy_from_role(role_name, policy_name, iam):
	try:
		resources = iam.detach_role_policy(
				RoleName=role_name,
				PolicyArn=get_policy_arn(policy_name, iam)
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "detach_policy_from_role": {err}...')


def remove_role(role_name, iam):
	try:
		resources = iam.delete_role(
				RoleName=role_name
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "remove_role": {err}...')


