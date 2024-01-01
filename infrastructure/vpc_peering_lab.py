#!/usr/bin/env python3

# from resources import vpcs_api_calls
from resources.vpc_template import deploy_vpc
from resources.vpc_peering_template import same_account_vpc_peering
from resources.nat_gateway_template import deploy_public_nat_gateways
from resources.elastic_ip_template import assign_public_ipv4
from resources.endpoint_template import connect_endpoint
from resources.instance_template import lab_instance
from resources.iam_template import create_ssm_role
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.iam_api_calls import *
from resources.endpoints_api_calls import *
from resources.account_profiles import assume_profile_creds, \
    client_session


from resources.visibility import *

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

ec2=client_session('default', 'ec2', 'us-east-1')
iam=client_session('default', 'iam', 'us-east-1')

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
    '10.11.9.0/24',  # az2_sec_cidr_private_subnet,
    ec2
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
    '10.21.9.0/24',  # az2_sec_cidr_private_subnet,
    ec2
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
                                        ec2,
                                        # accepter account
                                        sts=client_session(
                                            'default', 'sts', 'us-east-1')
                         )


# Adding NAT gateways 
# Deploys ipv4 elastic ips
# 2 elastic ips are created in each vpc
assign_public_ipv4('boto3_vpc1',
                   ec2
                   )
assign_public_ipv4('boto3_vpc2',
                   ec2
                   )


# Deploys 2 public nat gateways in two AZs in the public subnets
deploy_public_nat_gateways('boto3_vpc1',
                    ec2
                    )
deploy_public_nat_gateways('boto3_vpc2',
                    ec2
                    )


# create instance profile
create_ssm_role('ssm-instance-profile', iam)


# Add instance connect endpoint
# This is allow users to access instance from the browser in the console
connect_endpoint(
		'boto3_vpc1_connect_endpoint', #name,
		'boto3_vpc1_private_1b_pri', #subnet,
		'boto3_vpc1_private', #sg,
		False, #preserve_client_ip,
		ec2
)
connect_endpoint(
		'boto3_vpc2_connect_endpoint', #name,
		'boto3_vpc2_private_1a_pri', #subnet,
		'boto3_vpc2_private', #sg,
		False, #preserve_client_ip,
		ec2
)


# Create instances
lab_instance(
		'boto3_vpc1', #name,
		'ami-0fc5d935ebf8bc3bc', #ami,
		't3.medium', #instance_type,
		'maendeleolabKey', #key_pair,
		'boto3_vpc1_private', #security-group,
		'boto3_vpc1_private_1b_pri', #subnet,
		False, #public_ip,
		ec2
)
lab_instance(
		'boto3_vpc2', #name,
		'ami-0fc5d935ebf8bc3bc', #ami,
		't3.medium', #instance_type,
		'maendeleolabKey', #key_pair,
		'boto3_vpc2_private', #security-group,
		'boto3_vpc2_private_1a_pri', #subnet,
		False, #public_ip,
		ec2
)


