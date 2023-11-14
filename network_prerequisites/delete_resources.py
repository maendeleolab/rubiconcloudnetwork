#!/usr/bin/env python3

from vpcs_api_calls import *
from subnets_api_calls import *
from route_tables_api_calls import *
from internet_gateways_api_calls import *
from prefixlists_api_calls import *
from network_access_list_template import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


vpc1 = 'boto3_vpc1'

#delete_vpc_acl(vpc1, ec2)
delete_prefixlist(get_prefixlist_id('privaterfc1918', ec2), ec2)
delete_igw(get_igw_id(vpc1, ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_public_1a_pri', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_public_1b_pri', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_public_1a_sec', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_public_1b_sec', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_private_1a_pri', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_private_1b_pri', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_private_1a_sec', ec2), ec2)
delete_subnet_resources(get_subnet_id(vpc1+'_private_1b_sec', ec2), ec2)
delete_vpc_route_table(get_vpc_route_table_id(vpc1+'_private_rt_pri', ec2), ec2)
delete_vpc_route_table(get_vpc_route_table_id(vpc1+'_private_rt_sec', ec2), ec2)
delete_vpc_route_table(get_vpc_route_table_id(vpc1+'_public_rt_pri', ec2), ec2)
delete_vpc_route_table(get_vpc_route_table_id(vpc1+'_public_rt_sec', ec2), ec2)
delete_vpc_resources(get_vpc_id(vpc1, ec2), ec2)
