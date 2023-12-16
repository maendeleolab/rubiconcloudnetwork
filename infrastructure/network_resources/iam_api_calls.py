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
				InstanceProfileName='string',
				Path='string',
				Tags=[
						{
								'Key': 'Name',
								'Value': profile_name
						},
				]
		)
	except Exception as err:
		print(err)


