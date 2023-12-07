#!/usr/bin/env python3

from network_resources.vpcs_api_calls import *
from network_resources.subnets_api_calls import *
from network_resources.route_tables_api_calls import *
from network_resources.internet_gateways_api_calls import *
from network_resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


get_vpc_route_table_id('boto3_vpc1_private_rt_pri_az1', ec2)

