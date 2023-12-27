#!/usr/bin/env python3

# from network_resources import vpcs_api_calls
from network_resources.route_tables_api_calls import *
from network_resources.nat_gateways_api_calls import *
from network_resources.elastic_ips_api_calls import *
from network_resources.account_profiles import assume_profile_creds, \
    client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpcs = ['boto3_vpc1', 'boto3_vpc2']

# Delete route entries pointing to NAT gateways first
# Detach EIP association from NAT and release it
# Delete public and private NATs if any exists
for vpc_name in vpcs:
	delete_vpc_route_entry('0.0.0.0/0', vpc_name+'_private_rt_pri_az1', ec2)
	delete_vpc_route_entry('0.0.0.0/0', vpc_name+'_private_rt_pri_az2', ec2)
	delete_nat(vpc_name+'_public_nat1', ec2)
	delete_nat(vpc_name+'_public_nat2', ec2)
	delete_nat(vpc_name+'_private_nat1', ec2)
	delete_nat(vpc_name+'_private_nat2', ec2)
	detach_public_ipv4(vpc_name+'_public_nat1', ec2)
	detach_public_ipv4(vpc_name+'_public_nat2', ec2)
	release_public_ipv4_address(vpc_name+'_public_nat1', ec2)
	release_public_ipv4_address(vpc_name+'_public_nat2', ec2)
