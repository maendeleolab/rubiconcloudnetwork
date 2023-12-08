#!/usr/bin/env python3

from network_resources.elastic_ips_api_calls import *
from network_resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# vpc_name = 'boto3_vpc1'

# Create an ipv4 elastic ip


def assign_public_ipv4(vpc_name,
                       ec2=client_session('default', 'ec2', 'us-east-1')
                       ):
    allocate_public_ipv4(vpc_name+'_public_nat1', ec2)
    allocate_public_ipv4(vpc_name+'_public_nat2', ec2)
