#!/usr/bin/env python3


#from resources.account_profiles import assume_profile_creds,\
#client_sessioni
from resources.iam_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
iam = client_session('default', 'iam', 'us-east-1')


def create_ssm_role(name, iam):
	create_role(
						 name, 
						 'ec2.amazonaws.com', 
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

	#get_profile_arn(
	#           'ssm-instance-profile', #profile_name, 
	#           iam
	#)
	#
	#adding_role_to_profile(
	#          'ssm-instance-profile', #profile_name, 
	#          'ssm_role_for_connect', #role_name, 
	#          iam
	#)

	#get_profile_data('ssm-instance-profile', iam)
