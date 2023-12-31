#!/usr/bin/env python3


from resources.subnets_api_calls import *
from resources.elastic_ips_api_calls import *
from resources.nat_gateways_api_calls import *
from resources.route_tables_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# vpc_name = 'boto3_vpc1'


def deploy_public_nat_gateways(vpc_name,
                        ec2=client_session('default', 'ec2', 'us-east-1')
                        ):
    # public nat
    create_public_nat(vpc_name+'_public_nat1',  # name of public nat resource
                      get_subnet_id(vpc_name+'_public_1a_pri',
                                    ec2),  # subnet id
                      get_allocation_id(
                          vpc_name+'_public_nat1', ec2),  # elastic ip
                      ec2  # client session
                      )
    create_public_nat(vpc_name+'_public_nat2',  # name of public nat resource
                      get_subnet_id(vpc_name+'_public_1b_pri',
                                    ec2),  # subnet id
                      get_allocation_id(
                          vpc_name+'_public_nat2', ec2),  # elastic ip
                      ec2  # client session
                      )
    # Create route entry in private route tables pointing to public nat
    vpc_route_entry_to_nat_id(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az1', ec2),
        '0.0.0.0/0',  # dst_ipv4cidr,
        get_nat_id(vpc_name+'_public_nat1', ec2),  # nat_id,
        ec2
    )
    vpc_route_entry_to_nat_id(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az2', ec2),
        '0.0.0.0/0',  # dst_ipv4cidr,
        get_nat_id(vpc_name+'_public_nat2', ec2),  # nat_id,
        ec2
    )


def deploy_private_nat_gateways(vpc_name,
                        ec2=client_session('default', 'ec2', 'us-east-1')
                        ):

    # private nat
    create_private_nat(vpc_name+'_private_nat1',  # name of private nat resource
                       get_subnet_id(vpc_name+'_private_1a_pri',
                                     ec2),  # subnet id
                       '1',  # number_of_secondary_ips,
                       ec2  # client session
                       )
    create_private_nat(vpc_name+'_private_nat2',  # name of private nat resource
                       get_subnet_id(vpc_name+'_private_1b_pri',
                                     ec2),  # subnet id
                       '1',  # number_of_secondary_ips,
                       ec2  # client session
                       )
    # Create private nat
    vpc_route_entry_to_nat_id(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az1', ec2),
        '0.0.0.0/0',  # dst_ipv4cidr,
        get_nat_id(vpc_name+'_private_nat1', ec2),  # nat_id,
        ec2
    )
    vpc_route_entry_to_nat_id(
        get_vpc_route_table_id(vpc_name+'_private_rt_pri_az2', ec2),
        '0.0.0.0/0',  # dst_ipv4cidr,
        get_nat_id(vpc_name+'_private_nat2', ec2),  # nat_id,
        ec2
    )
