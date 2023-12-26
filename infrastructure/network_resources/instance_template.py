#!/usr/bin/env python3

#from network_resources.vpcs_api_calls import *
#from network_resources.subnets_api_calls import *
#from network_resources.route_tables_api_calls import *
#from network_resources.internet_gateways_api_calls import *
#from network_resources.account_profiles import assume_profile_creds, client_session
from vpcs_api_calls import *
from instances_api_calls import *
from subnets_api_calls import *
from route_tables_api_calls import *
from internet_gateways_api_calls import *
from iam_api_calls import *
from security_groups_api_calls import *
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
iam = client_session('default', 'iam', 'us-east-1')


deploy_instances(
  'test_t3_medium', #instance_name,
  'ami-0fc5d935ebf8bc3bc', #image,
  't3.medium', #instance_type,
  'test-KeyPair', # key_name,
  '1', # max_count,
  '1', # min_count,
  True, # monitoring (boolean True or False),
  get_sg_id('boto3_vpc1_private', ec2), # security_group_ids,
  get_subnet_id('boto3_vpc1_private_1b_pri', ec2), # subnet_id,
  False, # associate public ip is boolean True or False
	#get_profile_arn('ssm-instance-profile', iam), # profile arn
	'ssm-instance-profile', # profile name
  #user_data,
  ec2
  )

get_instance_state('test_t3_medium', ec2)
#get_instance_name('test', ec2)
