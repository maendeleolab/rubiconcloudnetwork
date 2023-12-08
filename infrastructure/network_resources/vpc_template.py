#!/usr/bin/env python3

from network_resources.vpcs_api_calls import *
from network_resources.subnets_api_calls import *
from network_resources.route_tables_api_calls import *
from network_resources.internet_gateways_api_calls import *
from network_resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')


def deploy_vpc(
    vpc_name,
    pri_vpc_cidr,
    sec_cidr,
    az1,
    az2,
    az1_pri_cidr_public_subnet,
    az2_pri_cidr_public_subnet,
    az1_sec_cidr_public_subnet,
    az2_sec_cidr_public_subnet,
    az1_pri_cidr_private_subnet,
    az2_pri_cidr_private_subnet,
    az1_sec_cidr_private_subnet,
    az2_sec_cidr_private_subnet,
    ec2=client_session('default', 'ec2', 'us-east-1')
):
    # Create vpc
    create_vpc_resources(
        vpc_name,
        pri_vpc_cidr,
        ec2
    )
    # Modify dns attributes
    modify_dns_hostnames(
        get_vpc_id(vpc_name, ec2),
        True,
        ec2
    )
    modify_dns_support(
        get_vpc_id(vpc_name, ec2),
        True,
        ec2
    )
    # Modify network address usage metrics
    modify_network_address_usage_metrics(
        get_vpc_id(vpc_name, ec2),
        True,
        ec2
    )
    # Add an additonal cidr
    add_vpc_cidr_block(
        get_vpc_id(vpc_name, ec2),
        sec_cidr,
        ec2
    )
    # Create public subnet in AZ
    # Primary cidr public subnet in Az1
    deploy_subnet(
        vpc_name+'_public_1a_pri',
        az1,
        az1_pri_cidr_public_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Primary cidr public subnet in Az2
    deploy_subnet(
        vpc_name+'_public_1b_pri',
        az2,
        az2_pri_cidr_public_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Secondary cidr public subnet in Az1
    deploy_subnet(
        vpc_name+'_public_1a_sec',
        az1,
        az1_sec_cidr_public_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Secondary cidr public subnet in Az2
    deploy_subnet(
        vpc_name+'_public_1b_sec',
        az2,
        az2_sec_cidr_public_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Create private subnet in AZ
    # Primary cidr private subnet in Az1
    deploy_subnet(
        vpc_name+'_private_1a_pri',
        az1,
        az1_pri_cidr_private_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Primary cidr private subnet in Az2
    deploy_subnet(
        vpc_name+'_private_1b_pri',
        az2,
        az2_pri_cidr_private_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2)
    # Secondary cidr private subnet in Az1
    deploy_subnet(
        vpc_name+'_private_1a_sec',
        az1,
        az1_sec_cidr_private_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Secondary cidr private subnet in Az2
    deploy_subnet(
        vpc_name+'_private_1b_sec',
        az2,
        az2_sec_cidr_private_subnet,
        get_vpc_id(vpc_name, ec2),
        ec2
    )
    # Create public vpc route table for primary and secondary cidrs
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_public_rt_pri',
        ec2
    )
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_public_rt_sec',
        ec2
    )
    # Create private vpc route tables for primary and secondary cidrs
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_private_rt_pri_az1',
        ec2
    )
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_private_rt_pri_az2',
        ec2
    )
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_private_rt_sec_az1',
        ec2
    )
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_private_rt_sec_az2',
        ec2
    )
    # Create subnet association to public route table
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2),
        get_subnet_id(vpc_name+'_public_1a_pri', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2),
        get_subnet_id(vpc_name+'_public_1b_pri', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_public_rt_sec', ec2),
        get_subnet_id(vpc_name+'_public_1a_sec', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_public_rt_sec', ec2),
        get_subnet_id(vpc_name+'_public_1b_sec', ec2),
        ec2
    )
    # Create subnet association to private route table
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az1', ec2),
        get_subnet_id(vpc_name+'_private_1a_pri', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az2', ec2),
        get_subnet_id(vpc_name+'_private_1b_pri', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_private_rt_sec_az1', ec2),
        get_subnet_id(vpc_name+'_private_1a_sec', ec2),
        ec2
    )
    create_subnet_association_to_route_table(
        get_vpc_route_table_id(vpc_name+'_private_rt_sec_az2', ec2),
        get_subnet_id(vpc_name+'_private_1b_sec', ec2),
        ec2
    )
    # Create internet gateway for the vpc
    create_igw(vpc_name, ec2)
    create_igw_attachment(vpc_name, get_vpc_id(vpc_name, ec2), ec2)
    get_igw_attachment_state(get_igw_id(vpc_name, ec2), ec2)
    # create route entries to the internet gateway in public route tables
    vpc_route_entry_to_gateway(
        get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2),
        '0.0.0.0/0',  # dst cidr
        get_igw_id(vpc_name, ec2),  # internet gateway id
        ec2
    )
