#!/usr/bin/env python3

from vpcs_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1 = 'boto3_vpc1'

#Create vpc "networkdev1"
create_vpc_resources(vpc1,'10.10.0.0/20', ec2)
modify_dns_hostnames(describe_vpc_ids(vpc1, ec2), True, ec2)

# vpc "networkdev2"
create_vpc_resources('boto3_vpc2','10.20.0.0/20', ec2)

print(describe_vpc_ids('boto3_vpc1', ec2))
