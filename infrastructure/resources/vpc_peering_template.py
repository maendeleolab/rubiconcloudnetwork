#!/usr/bin/env python3


# from resources.vpcs_api_calls import *
# from resources.account_profiles import assume_profile_creds, client_session
from resources.vpcs_api_calls import *
from resources.vpc_peerings_api_calls import *
from resources.sts_api_calls import *
from resources.route_tables_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
# We are using sts to get the account id of the user making the call
# this useful to not expose the account id in the code. I am getting
# away with this b/c the vpc peering is in the same account.
# If the peer vpc is in another account, we will have to statically
# define it in the code.
sts = client_session('default', 'sts', 'us-east-1')


# This function is only vpc peering connections created
# from inside the same account.
# It creates the connection, it accepts it and modifies the dns
def same_account_vpc_peering(vpc_peering_name,
                             requester_vpc,  # local_vpc_id
                             accepter_dst_ipv4cidr,
                             accepter_vpc,  # peer_vpc_id
                             requester_dst_ipv4cidr,
                             accepter_region,  # peer region
                             ec2,
                             ec2_remote,
                             sts=client_session('default', 'sts', 'us-east-1')
                             ):
  # create request
    create_vpc_peering(
        vpc_peering_name,  # connection_name,
        get_vpc_id(requester_vpc, ec2),  # local_vpc_id,
        get_vpc_id(accepter_vpc, ec2),  # peer_vpc_id,
        accepter_region,  # peer_region,
        get_user_identity(sts),  # peer_account_number,
        ec2
    )
  # accept request
    accept_vpc_peering(vpc_peering_name, ec2, ec2_remote)
    modify_vpc_peering(ec2,
                       vpc_peering_name,
                       accepter_dns=True,
                       requester_dns=True
                       )
  # create route in requester route table to peer connection in private az1 and
  # az2
    vpc_route_entry_for_vpc_peering(
        get_vpc_route_table_id(requester_vpc+'_private_rt_pri_az1', ec2),
        accepter_dst_ipv4cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2),
        ec2
    )
    vpc_route_entry_for_vpc_peering(
        get_vpc_route_table_id(requester_vpc+'_private_rt_pri_az2', ec2),
        accepter_dst_ipv4cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2),
        ec2)
  # create route in accepter route table to peer connection in private az1 and
  # az2
    vpc_route_entry_for_vpc_peering(
        get_vpc_route_table_id(accepter_vpc+'_private_rt_pri_az1', ec2),
        requester_dst_ipv4cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2),
        ec2)
    vpc_route_entry_for_vpc_peering(
        get_vpc_route_table_id(accepter_vpc+'_private_rt_pri_az2', ec2),
        requester_dst_ipv4cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2),
        ec2)


def diff_region_ipv6vpc_peering(vpc_peering_name,
                                requester_vpc,  # local_vpc_id
                                accepter_dst_cidr,
                                accepter_vpc,  # peer_vpc_id
                                requester_dst_cidr,
                                accepter_region,  # peer region
                                ec2_local,
                                ec2_remote,
                                sts_remote
                                ):
  # create request
    create_vpc_peering(
        vpc_peering_name,  # connection_name,
        get_vpc_id(requester_vpc, ec2_local),  # local_vpc_id,
        get_vpc_id(accepter_vpc, ec2_remote),  # peer_vpc_id,
        accepter_region,  # peer_region,
        get_user_identity(sts_remote),  # peer_account_number,
        ec2_local
    )
  # accept request
    tag_it(
        get_vpc_peering_connection_id(vpc_peering_name, ec2_local), # resource_id,
        'Name',  # Key1,
        vpc_peering_name,  # value1,
        ec2_remote
    )
    accept_vpc_peering(vpc_peering_name, ec2_local, ec2_remote)
    modify_vpc_peering(ec2_local,
                       vpc_peering_name,
                       accepter_dns=True,
                       requester_dns=True
                       )
    modify_vpc_peering(ec2_remote,
                       vpc_peering_name,
                       accepter_dns=True,
                       requester_dns=True
                       )
  # create route in requester route table to peer connection in private az1 and
  # az2
    ipv6_route_entry_for_vpc_peering(
        get_vpc_route_table_id(requester_vpc+'_protected_ipv6_rt_az1', ec2_local),
        accepter_dst_cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2_local),
        ec2_local
    )
    ipv6_route_entry_for_vpc_peering(
        get_vpc_route_table_id(requester_vpc+'_protected_ipv6_rt_az2', ec2_local),
        accepter_dst_cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2_local),
        ec2_local)
  # create route in accepter route table to peer connection in private az1 and
  # az2
    ipv6_route_entry_for_vpc_peering(
        get_vpc_route_table_id(accepter_vpc+'_protected_ipv6_rt_az1', ec2_remote),
        requester_dst_cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2_remote),
        ec2_remote
    )
    ipv6_route_entry_for_vpc_peering(
        get_vpc_route_table_id(accepter_vpc+'_protected_ipv6_rt_az2', ec2_remote),
        requester_dst_cidr,
        get_vpc_peering_connection_id(vpc_peering_name, ec2_remote),
        ec2_remote
    )

# This function is only used for connections between two different accounts
# We only initiate the request. The peer account must accpet it.
# We also define the peer account in the code


def diff_account_vpc_peering(vpc_peering_name,
                             requester_vpc,  # local_vpc_id
                             accepter_vpc,  # peer_vpc_id
                             accepter_region,  # peer region
                             accepter_account_number,
                             ec2=client_session('default', 'ec2', 'us-east-1')
                             ):

    create_vpc_peering(
        vpc_peering_name,  # connection_name,
        get_vpc_id(requester_vpc, ec2),  # local_vpc_id,
        get_vpc_id(accepter_vpc, ec2),  # peer_vpc_id,
        accepter_region,  # peer_region,
        accepter_account_number,  # peer_account_number,
        ec2
    )
