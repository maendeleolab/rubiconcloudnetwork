#!/usr/bin/env python


from vpcs_api_calls import *
from prefixlists_api_calls import *
from security_groups_api_calls import *
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


# Create security group
create_sg('boto3_vpc1_private', get_vpc_id('boto3_vpc1', ec2), ec2)

