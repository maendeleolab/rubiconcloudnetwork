#!/usr/bin/env python3

from resources.iam_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
iam = client_session('default', 'iam', 'us-east-1')

#services
services_list=['vpc-flow-logs.amazonaws.com']
ssm_services=['ec2.amazonaws.com']

#policies
flowlogs_policy = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
})


def create_ssm_role(name, iam):
	create_role(
						 name, 
						 ssm_services, 
						 iam
	)

	attach_policy(
						 name, # role_name, 
						 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore', # policy_arn, 
						 iam
	)

	create_profile(
						'ssm-instance-profile', #profile_name, 
						 iam
	)

	#adding_role_to_profile(
	#          'ssm-instance-profile', #profile_name, 
	#          'ssm_role_for_connect', #role_name, 
	#          iam
	#)

	#get_profile_data('ssm-instance-profile', iam)


def flowlogs_iam_functions(iam):
	create_role(
					'boto3_flowlogs_role', #role_name, 
					services_list, #allowed_services, 
					iam
	)
	#attach_policy(
	#					'boto3_flowlogs_role', #role_name,
	#					'boto3_flowlogs_policy', #policy_name,
	#					flowlogs_policy, #policy_doc,
	#					iam
  #)
	create_policy_document(
	'boto3_flowlogs_role', #role_name, 
	'boto3_flowlogs_policy', #policy_name, 
	flowlogs_policy, #policy_doc, 
	iam
	)
