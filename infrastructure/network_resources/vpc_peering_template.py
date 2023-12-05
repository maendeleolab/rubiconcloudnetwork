#!/usr/bin/env python3

#from network_resources.vpcs_api_calls import *
#from network_resources.account_profiles import assume_profile_creds, client_session
from vpcs_api_calls import *
from vpc_peerings_api_calls import *
from sts_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
sts = client_session('default', 'sts', 'us-east-1')


#create_vpc_peering(
#                   'boto3_vpc1_and_vpc2_peering', #connection_name,
#                   get_vpc_id('boto3_vpc1', ec2), #local_vpc_id,
#                   get_vpc_id('boto3_vpc2', ec2), #peer_vpc_id,
#                   'us-east-1', #peer_region (optional),
#                   get_user_identity(sts), #peer_account_number (optional),
#                   ec2
# )

accept_vpc_peering('boto3_vpc1_and_vpc2_peering', ec2)


