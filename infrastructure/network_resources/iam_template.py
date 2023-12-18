#!/usr/bin/env python3


#from network_resources.account_profiles import assume_profile_creds,\
#client_sessioni
from iam_api_calls import *
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
iam = client_session('default', 'iam', 'us-east-1')


#allowed_services=['ec2.amazonaws.com']
#
#create_role(
#           'ssm_role_for_connect', 
#           allowed_services, 
#           iam
#)
#
#attach_policy(
#           'ssm_role_for_connect', # role_name, 
#           'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore', # policy_arn, 
#           iam
#)
#
#create_profile(
#          'ssm-instance-profile', #profile_name, 
#           iam
#)
#
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
#
#get_profile_data('ssm-instance-profile', iam)
remove_role_from_profile('ssm-instance-profile', 'ssm_role_for_connect', iam)
delete_profile('ssm-instance-profile', iam)
detach_policy_from_role('ssm_role_for_connect', 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore', iam)
remove_role('ssm_role_for_connect', iam)
