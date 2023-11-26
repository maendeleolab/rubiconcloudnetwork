#!/usr/bin/env python3

from elastic_ips_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1= 'boto3_vpc1'

allocate_public_ipv4(vpc1, ec2)

