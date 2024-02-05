#!/usr/bin/env python3

# from resources import vpcs_api_calls
from resources.vpc_template import deploy_vpc
from resources.vpc_peering_template import same_account_vpc_peering
from resources.vpc_peering_template import diff_region_ipv6vpc_peering
from resources.nat_gateway_template import deploy_public_nat_gateways
from resources.elastic_ip_template import assign_public_ipv4
from resources.endpoint_template import connect_endpoint
from resources.instance_template import lab_instance
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.monitoring_template import deploy_monitoring, test
from vpcs import vpc1, vpc2
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
cw_logs = client_session('default', 'logs', 'us-east-1')


# This function is only vpc peering connections created
# from inside the same account.
# It creates the connection, it accepts it and modifies the dns.
# It creates routes for the requester and requester vpc route table

# us-east-1
same_account_vpc_peering('boto3_vpc1_and_vpc2_peering',
						'boto3_vpc1',  # requester_vpc
						'10.20.0.0/20',  # accepter_dst_ipv4cidr
						'boto3_vpc2',  # accepter_vpc,
						'10.10.0.0/20',  # requester_dst_ipv4cidr
						'us-east-1',  # accepter_region
						# client session
						ec2=client_session('default', 'ec2', 'us-east-1'),
					  ec2_remote=client_session('default', 'ec2', 'us-east-1'),
						# accepter account
						sts=client_session('default', 'sts', 'us-east-1')
)

# us-west-2 to us-east-1
ec2_local=client_session('default','ec2','us-west-2')
ec2_remote=client_session('default', 'ec2','us-east-1')
diff_region_ipv6vpc_peering('boto3_vpc3_and_vpc1_peering', # vpc_peering_name,
					 'boto3_vpc3', # requester_vpc -> local_vpc_id
						get_ipv6_block('boto3_vpc1', ec2_remote), # accepter dst cidr
					 'boto3_vpc1', # accepter_vpc -> peer_vpc_id
						get_ipv6_block('boto3_vpc3', ec2_local), # requester dst cidr
					 'us-east-1', # accepter_region -> peer region
					 ec2_local,
					 ec2_remote,
					 sts_remote=client_session('default', 'sts', 'us-east-1')
)
