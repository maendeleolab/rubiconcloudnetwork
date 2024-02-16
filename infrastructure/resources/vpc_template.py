#!/usr/bin/env python3


from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.prefixlists_api_calls import *
from resources.prefixlist_template import deploy_prefixlist
from resources.security_group_template import deploy_privaterfc1918_sg
from resources.security_group_template import deploy_rubiconcloud_elb_sg
from resources.security_group_template import deploy_vpce_sg
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')


# prefixlist entries
privaterfc1918 = ['172.16.0.0/12', '192.168.0.0/16']
rubiconcloud_elb = ['1.1.1.1/32', '2.2.2.2/32']  # just place holders
allipv6 = ['']  # just a place holder


def deploy_vpc(
    vpc_name,
    pri_vpc_cidr,
    sec_cidr,
    pri_ipv6_cidr,
    sec_ipv6_cidr,
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
    ec2
):
    # Create vpc
    create_vpc_resources(
        vpc_name,
        pri_vpc_cidr,
        pri_ipv6_cidr,  # Amazon provided ipv6 - set to True or False
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
        sec_ipv6_cidr,  # Amazon provided ipv6 - set to True or False
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
    # Create private vpc route tables for ipv6 subnets
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_protected_ipv6_rt_az1',
        ec2
    )
    create_vpc_route_table(
        get_vpc_id(vpc_name, ec2),
        vpc_name+'_protected_ipv6_rt_az2',
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
    # Create subnet association to ipv6 route table
    # create_subnet_association_to_route_table(
    #    get_vpc_route_table_id(vpc_name+'_protected_ipv6_rt_az1', ec2),
    #    get_subnet_id(vpc_name+'_private_1a_ipv6', ec2),
    #    ec2
    # )
    # create_subnet_association_to_route_table(
    #    get_vpc_route_table_id(vpc_name+'_protected_ipv6_rt_az2', ec2),
    #    get_subnet_id(vpc_name+'_private_1b_ipv6', ec2),
    #    ec2
    # )
    # Create prefixlist
    deploy_prefixlist('privaterfc1918',  # prefixlist_name,
                      '10.0.0.0/8',  # first_cidr,
                      '50',  # max_entries,
                      # list(cidrs_list),
                      privaterfc1918,
                      'IPv4',
                      ec2
                      )
    deploy_prefixlist('allipv6',  # prefixlist_name,
                      '::/0',  # first_cidr,
                      '50',  # max_entries,
                      # list(cidrs_list),
                      allipv6,
                      'IPv6',
                      ec2
                      )
    deploy_prefixlist('rubiconcloud_elb',  # prefixlist_name,
                      '0.0.0.0/0',  # first_cidr,
                      '50',  # max_entries,
                      # list(cidrs_list),
                      rubiconcloud_elb,
                      'IPv4',
                      ec2
                      )
    # Create security groups
    deploy_privaterfc1918_sg(vpc_name+'_private', vpc_name, ec2)
    deploy_rubiconcloud_elb_sg(vpc_name+'_rubiconcloud_elb', vpc_name, ec2)
    deploy_vpce_sg(vpc_name+'_vpce', vpc_name, ec2)
    # Create internet gateway for the vpc
    create_igw(vpc_name, ec2)
    create_igw_attachment(vpc_name, get_vpc_id(vpc_name, ec2), ec2)
    get_igw_attachment_state(get_igw_id(vpc_name, ec2), ec2)
    # Create egress only internet gateway
    create_ipv6_eigw(vpc_name, get_vpc_id(vpc_name, ec2), ec2)
    # create route entries to the internet gateway in public route tables
    vpc_route_entry_to_gateway(
        get_vpc_route_table_id(vpc_name+'_public_rt_pri', ec2),
        '0.0.0.0/0',  # dst cidr
        get_igw_id(vpc_name, ec2),  # internet gateway id
        ec2
    )
