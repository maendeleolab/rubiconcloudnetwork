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
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


deploy_instances(
  'test', #instance_name,
  'ami-0fc5d935ebf8bc3bc', #image,
  't2.micro', #instance_type,
  'test-KeyPair', # key_name,
  '1', # max_count,
  '1', # min_count,
  True, # monitoring (boolean True or False),
  'sg-0b9aaa57d3008be2d', # security_group_ids,
  'subnet-0979ba7d8194fa1c2', # subnet_id,
  #user_data,
  ec2
  )
