#!/usr/bin/env python3

from network_resources.vpcs_api_calls import *
from network_resources.subnets_api_calls import *
from network_resources.route_tables_api_calls import *
from network_resources.internet_gateways_api_calls import *
from network_resources.prefixlists_api_calls import *
from network_resources.network_access_lists_api_calls import *
from network_resources.security_groups_api_calls import *
from network_resources.elastic_ips_api_calls import *
from network_resources.nat_gateways_api_calls import *
from network_resources.vpc_peerings_api_calls import *
from network_resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
#ec2 = client_session('default', 'ec2', 'us-east-1')

#vpc_name = 'boto3_vpc_name'

def delete_all(
               vpc_name,
               ec2 = client_session('default', 'ec2', 'us-east-1')
  ):
  delete_vpc_peering('boto3_vpc1_and_vpc2_peering', ec2)
	delete_nat(vpc_name+'_public_nat1', ec2)
	delete_nat(vpc_name+'_public_nat2', ec2)
	delete_nat(vpc_name+'_private_nat1', ec2)
	delete_nat(vpc_name+'_private_nat2', ec2)
	detach_public_ipv4(vpc_name+'_public_nat1', ec2)
	detach_public_ipv4(vpc_name+'_public_nat2', ec2)
	release_public_ipv4_address(vpc_name+'_public_nat1', ec2)
	release_public_ipv4_address(vpc_name+'_public_nat2', ec2)
	delete_sg(get_sg_id(vpc_name+'_private', ec2), ec2)
	delete_prefixlist(get_prefixlist_id('privaterfc1918', ec2), ec2)
	detach_igw(vpc_name, get_vpc_id(vpc_name, ec2), ec2)
	delete_igw(get_igw_id(vpc_name, ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_public_1a_pri', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_public_1b_pri', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_public_1a_sec', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_public_1b_sec', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_private_1a_pri', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_private_1b_pri', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_private_1a_sec', ec2), ec2)
	delete_subnet_resources(get_subnet_id(vpc_name+'_private_1b_sec', ec2), ec2)
	delete_vpc_acl(vpc_name, ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_private_rt_pri_az1', ec2), ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_private_rt_pri_az2', ec2), ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_private_rt_sec_az1', ec2), ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_private_rt_sec_az2', ec2), ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2), ec2)
	delete_vpc_route_table(get_vpc_route_table_id(vpc_name+'_public_rt_sec', ec2), ec2)
	delete_vpc_resources(get_vpc_id(vpc_name, ec2), ec2)
