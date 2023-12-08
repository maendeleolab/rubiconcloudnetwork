#!/usr/bin/env python3

# from network_resources import vpcs_api_calls
from network_resources.vpc_template import deploy_vpc
from network_resources.vpc_peering_template import same_account_vpc_peering
from network_resources.account_profiles import assume_profile_creds, \
    client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# We are using sts to get the account id of the user making the call
# this useful to not expose the account id in the code. I am getting
# away with this b/c the vpc peering is in the same account.
# If the peer vpc is in another account, we will have to statically
# define it in the code.
# sts = client_session('default', 'sts', 'us-east-1')


# vpc1
deploy_vpc(
    'boto3_vpc1',  # vpc_name,
    '10.10.0.0/20',  # primary_vpc_cidr,
    '10.11.0.0/20',  # secondary_cidr,
    'us-east-1a',  # az1,
    'us-east-1b',  # az2,
    '10.10.1.0/24',  # az1_pri_cidr_public_subnet,
    '10.10.2.0/24',  # az2_pri_cidr_public_subnet,
    '10.11.1.0/24',  # az1_sec_cidr_public_subnet,
    '10.11.2.0/24',  # az2_sec_cidr_public_subnet,
    '10.10.8.0/24',  # az1_pri_cidr_private_subnet,
    '10.10.9.0/24',  # az2_pri_cidr_private_subnet,
    '10.11.8.0/24',  # az1_sec_cidr_private_subnet,
    '10.11.8.0/24',  # az2_sec_cidr_private_subnet,
    ec2=client_session('default', 'ec2', 'us-east-1')
)


# vpc2
deploy_vpc(
    'boto3_vpc2',  # vpc_name,
    '10.20.0.0/20',  # primary_vpc_cidr,
    '10.21.0.0/20',  # secondary_cidr,
    'us-east-1a',  # az1,
    'us-east-1b',  # az2,
    '10.20.1.0/24',  # az1_pri_cidr_public_subnet,
    '10.20.2.0/24',  # az2_pri_cidr_public_subnet,
    '10.21.1.0/24',  # az1_sec_cidr_public_subnet,
    '10.21.2.0/24',  # az2_sec_cidr_public_subnet,
    '10.20.8.0/24',  # az1_pri_cidr_private_subnet,
    '10.20.9.0/24',  # az2_pri_cidr_private_subnet,
    '10.21.8.0/24',  # az1_sec_cidr_private_subnet,
    '10.21.8.0/24',  # az2_sec_cidr_private_subnet,
    ec2=client_session('default', 'ec2', 'us-east-1')
)

# This function is only vpc peering connections created
# from inside the same account.
# It creates the connection, it accepts it and modifies the dns.
# It creates routes for the requester and requester vpc route table
same_account_vpc_peering('boto3_vpc1_and_vpc2_peering',
                         'boto3_vpc1',  # requester_vpc
                         '10.20.0.0/20',  # requester_dst_ipv4cidr
                                        'boto3_vpc2',  # accepter_vpc,
                         '10.10.0.0/20',  # accepter_dst_ipv4cidr
                                        'us-east-1',  # accepter_region
                                        # client session
                                        ec2=client_session(
                                            'default', 'ec2', 'us-east-1'),
                                        # accepter account
                                        sts=client_session(
                                            'default', 'sts', 'us-east-1')
                         )
