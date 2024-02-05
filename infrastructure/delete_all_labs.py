#!/usr/bin/env python3

from resources.vpc_peerings_api_calls import delete_vpc_peering
from resources.delete_resources import delete_all
from resources.account_profiles import assume_profile_creds, \
    client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
iam = client_session('default', 'iam', 'us-east-1')
cw_logs = client_session('default', 'logs', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')


# delete individual vpc peering
delete_vpc_peering('boto3_vpc1_and_vpc2_peering', ec2)
delete_vpc_peering(
'boto3_vpc3_and_vpc1_peering', 
ec2=client_session('default', 'ec2', 'us-west-2')
)

# delete all
delete_all(
    'boto3_vpc1',  # vpc_name,
    ec2,
    iam,
    cw_logs,
    elbv2,
)
delete_all(
    'boto3_vpc2',  # vpc_name,
    ec2,
    iam,
    cw_logs,
    elbv2,
)
delete_all(
    'boto3_vpc3',  # vpc_name,
    ec2=client_session('default', 'ec2', 'us-west-2'),
    iam=client_session('default', 'iam', 'us-west-2'),
    cw_logs=client_session('default', 'logs', 'us-west-2'),
    elbv2=client_session('default', 'elbv2', 'us-west-2'),
)
