#!/usr/bin/env python3


#from network_resources.vpcs_api_calls import *
#from network_resources.subnets_api_calls import *
#from network_resources.route_tables_api_calls import *
#from network_resources.internet_gateways_api_calls import *
#from network_resources.prefixlists_api_calls import *
#from network_resources.enpoints_api_calls import *
#from network_resources.enpoints_api_calls import *
#from network_resources.prefixlist_template import deploy_prefixlist
#from network_resources.security_group_template import deploy_privaterfc1918_sg
#from network_resources.account_profiles import assume_profile_creds, client_session
from endpoints_api_calls import *
from subnets_api_calls import *
from security_groups_api_calls import *
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


create_connect_endpoint( 
                    'boto3_vpc1_connect_endpoint', #endpoint_name,
                     get_subnet_id('boto3_vpc1_private_1b_pri' ,ec2), #subnet_id,
                     get_sg_id('boto3_vpc1_private', ec2), #sg_id,
                     False, #preserve_client_ip,
                     ec2
  )

get_connect_endpoint_state('boto3_vpc1', ec2)
#delete_connect_endpoint(
#                'boto3_vpc1_connect_endpoint', 
#                ec2
#)
