#!/usr/bin/env python3

from vpcs_api_calls import *
from subnets_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1 = 'boto3_vpc1'

# Create vpc
create_vpc_resources(vpc1,'10.10.0.0/20', ec2)
# Modify dns attributes
modify_dns_hostnames(get_vpc_ids(vpc1, ec2), True, ec2)
modify_dns_support(get_vpc_ids(vpc1, ec2), True, ec2)
# Modify network address usage metrics
modify_network_address_usage_metrics(get_vpc_ids(vpc1, ec2), True, ec2)
# Add an additonal cidr
add_vpc_cidr_block(get_vpc_ids(vpc1, ec2), '10.11.0.0/20', ec2)
# Create a subnet in a AZ 
deploy_subnet('boto3_vpc1_private_1a', 'us-east-1a', '10.11.0.0/24', get_vpc_ids(vpc1, ec2), ec2)
# vpc "networkdev2"
create_vpc_resources('boto3_vpc2','10.20.0.0/20', ec2)
add_vpc_cidr_block(get_vpc_ids('boto3_vpc2', ec2), '10.21.0.0/20', ec2)
deploy_subnet('boto3_vpc2_private_1a', 'us-east-1a', '10.21.0.0/24', get_vpc_ids('boto3_vpc2', ec2), ec2)

print(get_vpc_ids('boto3_vpc1', ec2))
