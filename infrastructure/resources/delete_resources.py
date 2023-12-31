#!/usr/bin/env python3

from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.prefixlists_api_calls import *
from resources.network_access_lists_api_calls import *
from resources.security_groups_api_calls import *
from resources.elastic_ips_api_calls import *
from resources.nat_gateways_api_calls import *
from resources.vpc_peerings_api_calls import *
from resources.endpoints_api_calls import *
from resources.iam_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')

AmazonSSMManagedInstanceCore = 'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore'


def delete_all(
    vpc_name,
    ec2=client_session('default', 'ec2', 'us-east-1'),
    iam=client_session('default', 'iam', 'us-east-1')
		):
		delete_connect_endpoint(
                    vpc_name+'_connect_endpoint',
										ec2
		)
		remove_role_from_profile(
                    'ssm-instance-profile',
                    'ssm_role_for_connect',
                    iam
    )
		delete_profile('ssm-instance-profile', iam)
		detach_policy_from_role(
                    'ssm_role_for_connect',
                    AmazonSSMManagedInstanceCore,
                    iam
    )
		remove_role('ssm_role_for_connect', iam)
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
		delete_subnet_resources(
										 get_subnet_id(vpc_name+'_public_1a_pri', ec2), 
										 ec2
		)
		delete_subnet_resources(
										 get_subnet_id(vpc_name+'_public_1b_pri', ec2), 
										 ec2
		)
		delete_subnet_resources(
										 get_subnet_id(vpc_name+'_public_1a_sec', ec2), 
										 ec2
		)
		delete_subnet_resources(
                     get_subnet_id(vpc_name+'_public_1b_sec', ec2), 
                     ec2
    )
		delete_subnet_resources(
                    get_subnet_id(vpc_name+'_private_1a_pri', ec2), 
                    ec2
    )
		delete_subnet_resources(
                   get_subnet_id(vpc_name+'_private_1b_pri', ec2), 
                   ec2
    )
		delete_subnet_resources(
                  get_subnet_id(vpc_name+'_private_1a_sec', ec2), 
                  ec2
    )
		delete_subnet_resources(
                  get_subnet_id(vpc_name+'_private_1b_sec', ec2), 
                  ec2
    )
		delete_vpc_acl(vpc_name, ec2)
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_private_rt_pri_az1', ec2), 
                  ec2
    )
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_private_rt_pri_az2', ec2), 
                  ec2
    )
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_private_rt_sec_az1', ec2), 
                  ec2
    )
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_private_rt_sec_az2', ec2), 
                  ec2
    )
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2), 
                  ec2
    )
		delete_vpc_route_table(
                  get_vpc_route_table_id(vpc_name+'_public_rt_sec', ec2), 
                  ec2
    )
		delete_vpc_resources(get_vpc_id(vpc_name, ec2), ec2)
