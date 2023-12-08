#!/usr/bin/env python


from vpcs_api_calls import *
from prefixlists_api_calls import *
from security_groups_api_calls import *
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1 = 'boto3_vpc1'

# Create security group
create_sg('boto3_vpc1_private', get_vpc_id(vpc1, ec2), ec2)
# Add ingress rule
# Note: Egress is allowed to any by default
add_ingress_sg(get_sg_id('boto3_vpc1_private', ec2),  # sg_name (this argument gets the id of sg)
               '-1',  # from_port,
               '-1',  # protocol_number,
               'allow all',  # description,
               get_prefixlist_id('privaterfc1918', ec2),  # prefixlist_id,
               '-1',  # to_port,
               ec2
               )
