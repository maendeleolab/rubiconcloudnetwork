#!/usr/bin/env python3

from resources.instance_template import lab_instance, get_instance_id
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.elb_template import deploy_elb, register_elb_targets
from resources.endpoint_template import dualstack_endpoint_service, vpce
from vpcs import vpc1, vpc2, vpc3
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
from resources.route_tables_api_calls import *
from resources.iam_api_calls import *
from resources.endpoints_api_calls import *
from resources.elbs_api_calls import *
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
#iam=client_session('default', 'iam', 'us-east-1')
#elbv2 = client_session('default', 'elbv2', 'us-east-1')


# vpc1
# Create dualstack ipv6 subnets in vpc1 (consumer vpc)
vpc_ipv6_block = get_ipv6_cidr('boto3_vpc1', ec2)
deploy_ipv6_subnet(
	ec2,
	'boto3_vpc1_private_1a_ipv6', # resource name
	'us-east-1a', # az_id,
	vpc_ipv6_block+'1::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc1', ec2), # vpc_id, 
	'10.10.10.0/24' # ipv4 cidr is must when using load balancers
	)
deploy_ipv6_subnet(
	ec2,
	'boto3_vpc1_private_1b_ipv6', # resource name
	'us-east-1b', # az_id, 
	vpc_ipv6_block+'2::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc1', ec2), # vpc_id, 
	'10.10.11.0/24' # ipv4 cidr is must when using load balancers
	)

# vpc2
# Create dualstack ipv6 subnets in vpc2 (provider vpc)
# Note: As of 1/29/24. Dualstack elb requires your subnet
# to have both ipv4 and ipv6 cidr assigned to the subnet
vpc_ipv6_block = get_ipv6_cidr('boto3_vpc2', ec2)
deploy_ipv6_subnet(
	ec2,
	'boto3_vpc2_private_1a_ipv6', # resource name
	'us-east-1a', # az_id,
	vpc_ipv6_block+'1::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc2', ec2), # vpc_id, 
	'10.20.10.0/24' # ipv4 cidr is must when using load balancers
	)
deploy_ipv6_subnet(
	ec2,
	'boto3_vpc2_private_1b_ipv6', # resource name
	'us-east-1b', # az_id, 
	vpc_ipv6_block+'2::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc2', ec2), # vpc_id, 
	'10.20.11.0/24' # ipv4 cidr is must when using load balancers
	)

# vpc3
ec2_uswest2=client_session('default', 'ec2', 'us-west-2')
# Create dualstack ipv6 subnets in vpc3 (consumer vpc)
vpc_ipv6_block = get_ipv6_cidr('boto3_vpc3', ec2_uswest2)
deploy_ipv6_subnet(
	ec2_uswest2,
	'boto3_vpc3_private_1a_ipv6', # resource name
	'us-west-2a', # az_id,
	vpc_ipv6_block+'1::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc3', ec2_uswest2), # vpc_id,
	'10.30.10.0/24' # ipv4 cidr is must when using load balancers
)
deploy_ipv6_subnet(
	ec2_uswest2,
	'boto3_vpc3_private_1b_ipv6', # resource name
	'us-west-2b', # az_id, 
	vpc_ipv6_block+'2::/64', # ipv6 subnet
	False, # ipv6_only (True or False)
	get_vpc_id('boto3_vpc3', ec2_uswest2), # vpc_id, 
	'10.30.11.0/24', # ipv4 cidr is must when using load balancers
)

# Create subnet association to ipv6 route table in vpc1, 2, and 3
# This is repeated code. I will create a template at a later time.
create_subnet_association_to_route_table(
		get_vpc_route_table_id('boto3_vpc1_protected_ipv6_rt_az1', ec2),
		get_subnet_id('boto3_vpc1_private_1a_ipv6', ec2),
		ec2
)
create_subnet_association_to_route_table(
		get_vpc_route_table_id('boto3_vpc1_protected_ipv6_rt_az2', ec2),
		get_subnet_id('boto3_vpc1_private_1b_ipv6', ec2),
		ec2
)
create_subnet_association_to_route_table(
		get_vpc_route_table_id('boto3_vpc2_protected_ipv6_rt_az1', ec2),
		get_subnet_id('boto3_vpc2_private_1a_ipv6', ec2),
		ec2
)
create_subnet_association_to_route_table(
		get_vpc_route_table_id('boto3_vpc2_protected_ipv6_rt_az2', ec2),
		get_subnet_id('boto3_vpc2_private_1b_ipv6', ec2),
		ec2
)
create_subnet_association_to_route_table(
		get_vpc_route_table_id(
		'boto3_vpc3_protected_ipv6_rt_az1', 
		ec2=client_session('default', 'ec2', 'us-west-2')
		),
		get_subnet_id(
		'boto3_vpc3_private_1a_ipv6', 
		ec2=client_session('default', 'ec2', 'us-west-2')),
		ec2=client_session('default', 'ec2', 'us-west-2')
)
create_subnet_association_to_route_table(
		get_vpc_route_table_id(
		'boto3_vpc3_protected_ipv6_rt_az2', 
		ec2=client_session('default', 'ec2', 'us-west-2')
		),
		get_subnet_id(
		'boto3_vpc3_private_1b_ipv6', 
		ec2=client_session('default', 'ec2', 'us-west-2')
		),
		ec2=client_session('default', 'ec2', 'us-west-2')
)


