#!/usr/bin/env python

from resources.vpcs_api_calls import *
from resources.prefixlists_api_calls import *
from resources.security_groups_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')

# vpc1 = 'boto3_vpc1'

# Create security group


def deploy_privaterfc1918_sg(sg_name, vpc_name, ec2):
    create_sg(sg_name, get_vpc_id(vpc_name, ec2), ec2)
    # Add ingress rule
    # Note: Egress is allowed to any by default
    add_ingress_sg(get_sg_id(sg_name, ec2),  # this argument gets the id of sg
                   # from_port,
                   '-1',
                   # protocol_number,
                   '-1',
                   # description,
                   'allow all',
                   # prefixlist_id,
                   get_prefixlist_id(
        'privaterfc1918', ec2),
        # to_port,
        '-1',
        ec2
    )

def deploy_rubiconcloud_elb_sg(sg_name, vpc_name, ec2):
    create_sg(sg_name, get_vpc_id(vpc_name, ec2), ec2)
    # Add ingress rule
    # Note: Egress is allowed to any by default
    add_ingress_sg(get_sg_id(sg_name, ec2),  # this argument gets the id of sg
                   # from_port,
                   '-1',
                   # protocol_number,
                   '-1',
                   # description,
                   'allow all',
                   # prefixlist_id,
                   get_prefixlist_id(
        'rubiconcloud_elb', ec2),
        # to_port,
        '-1',
        ec2
    )
