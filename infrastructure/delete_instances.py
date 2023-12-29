#!/usr/bin/env python3

# from resources import vpcs_api_calls
from resources.instances_api_calls import *
from resources.endpoints_api_calls import *
from resources.account_profiles import assume_profile_creds, \
    client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


delete_instance('boto3_vpc1', ec2)
delete_instance('boto3_vpc2', ec2)

delete_connect_endpoint(
                'boto3_vpc1_connect_endpoint',
                ec2
)
delete_connect_endpoint(
                'boto3_vpc2_connect_endpoint',
                ec2
)
