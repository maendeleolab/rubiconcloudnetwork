#!/usr/bin/env python3

from resources.instance_template import lab_instance, get_instance_id
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.elb_template import deploy_elb, register_elb_targets
from resources.endpoint_template import dualstack_endpoint_service, vpce
from vpcs import vpc1, vpc2, vpc3
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
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
iam=client_session('default', 'iam', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')


# Create dualstack ipv6 subnets in vpc1 (consumer vpc)
#vpc_ipv6_block = get_ipv6_cidr('boto3_vpc1', ec2)
#deploy_ipv6_subnet(
#	ec2,
#	'boto3_vpc1_private_1a_ipv6', # resource name
#	'us-east-1a', # az_id,
#	vpc_ipv6_block+'1::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc1', ec2), # vpc_id, 
#	'10.10.10.0/24' # ipv4 cidr is must when using load balancers
#	)
#deploy_ipv6_subnet(
#	ec2,
#	'boto3_vpc1_private_1b_ipv6', # resource name
#	'us-east-1b', # az_id, 
#	vpc_ipv6_block+'2::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc1', ec2), # vpc_id, 
#	'10.10.11.0/24' # ipv4 cidr is must when using load balancers
#	)
#
#
## Create dualstack ipv6 subnets in vpc2 (provider vpc)
## Note: As of 1/29/24. Dualstack elb requires your subnet
## to have both ipv4 and ipv6 cidr assigned to the subnet
#vpc_ipv6_block = get_ipv6_cidr('boto3_vpc2', ec2)
#deploy_ipv6_subnet(
#	ec2,
#	'boto3_vpc2_private_1a_ipv6', # resource name
#	'us-east-1a', # az_id,
#	vpc_ipv6_block+'1::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc2', ec2), # vpc_id, 
#	'10.20.10.0/24' # ipv4 cidr is must when using load balancers
#	)
#deploy_ipv6_subnet(
#	ec2,
#	'boto3_vpc2_private_1b_ipv6', # resource name
#	'us-east-1b', # az_id, 
#	vpc_ipv6_block+'2::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc2', ec2), # vpc_id, 
#	'10.20.11.0/24' # ipv4 cidr is must when using load balancers
#	)
#
#ec2_uswest2=client_session('default', 'ec2', 'us-west-2')
## Create dualstack ipv6 subnets in vpc3 (consumer vpc)
#vpc_ipv6_block = get_ipv6_cidr('boto3_vpc3', ec2_uswest2)
#deploy_ipv6_subnet(
#	ec2_uswest2,
#	'boto3_vpc3_private_1a_ipv6', # resource name
#	'us-west-2a', # az_id,
#	vpc_ipv6_block+'1::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc3', ec2_uswest2), # vpc_id,
#	'10.30.10.0/24' # ipv4 cidr is must when using load balancers
#)
#deploy_ipv6_subnet(
#	ec2_uswest2,
#	'boto3_vpc3_private_1b_ipv6', # resource name
#	'us-west-2b', # az_id, 
#	vpc_ipv6_block+'2::/64', # ipv6 subnet
#	False, # ipv6_only (True or False)
#	get_vpc_id('boto3_vpc3', ec2_uswest2), # vpc_id, 
#	'10.30.11.0/24', # ipv4 cidr is must when using load balancers
#)


# Deploy target group and elb in vpc2 (provider vpc)
deploy_elb(
  'vpc2-rubiconcloud-targets', #targets_name,
  'TCP', #protocol='TCP',
  '5555', #port='5555',
  get_vpc_id('boto3_vpc2', ec2), #vpc_id,
  'TCP', #health_protocol='TCP',
  '30', #health_interval='30',
  '10', #health_timeout='10',
  '5', #healthy_count='5',
  '10', #unhealthy_count='10',
  'instance', #target_type,
  'internal', #scheme=None,
  'vpc2-rubiconcloud-elb', #elb_name,
  get_subnet_id('boto3_vpc2_private_1a_ipv6', ec2), #subnet1,
  get_subnet_id('boto3_vpc2_private_1b_ipv6', ec2), #subnet2,
  get_sg_id('boto3_vpc2_rubiconcloud_elb', ec2), #elb_sg,
  'network', #elb_type,
  'ipv4', #target_address_type='ipv4' or 'ipv6',
  'dualstack', #ip_address_type='ipv4' or 'dualstack',
  elbv2
  )

# Create target instances in vpc2 (provider vpc)
lab_instance(
	'vpc2_rubiconcloud_target_1', #name,
	'ami-0fc5d935ebf8bc3bc', #ami,
	't3.medium', #instance_type,
	'maendeleolabKey', #key_pair,
	'boto3_vpc2_private', #security-group,
	'boto3_vpc2_private_1a_ipv6', #subnet,
	False, #public_ip,
	'resources/basic_script.sh', #user_data script
  True, # assign ipv6 to interface
	ec2
	)
lab_instance(
	'vpc2_rubiconcloud_target_2', #name,
	'ami-0fc5d935ebf8bc3bc', #ami,
	't3.medium', #instance_type,
	'maendeleolabKey', #key_pair,
	'boto3_vpc2_private', #security-group,
	'boto3_vpc2_private_1b_ipv6', #subnet,
	False, #public_ip,
	'resources/basic_script.sh', #user_data script
  True, # assign ipv6 to interface
	ec2
	)


# register targets (instances) with target group
# in vpc2 (provider vpc)
register_elb_targets(
  'vpc2-rubiconcloud-targets', #targets_name,
  get_instance_id('vpc2_rubiconcloud_target_1', ec2), #instance_id,
  '5555', #port='5555',
  elbv2
)
register_elb_targets(
  'vpc2-rubiconcloud-targets', #targets_name,
  get_instance_id('vpc2_rubiconcloud_target_2', ec2), #instance_id,
  '5555', #port='5555',
  elbv2
)


# create the dualstack endpoint service
# in vpc2 (provider vpc)
dualstack_endpoint_service(
  'rubiconcloud_service', #name,
  'vpc2-rubiconcloud-elb', #network_lb
	ec2
)


# create vpc endpoint in vpc1 (consumer vpc)
vpce(
  'Interface', # endpoint_type _>'Interface'|'Gateway'|'GatewayLoadBalancer'
  'boto3_vpc1', # vpc_name,
  'rubiconcloud_service', #service_name,
  'dualstack', # ip_address_type -> 'ipv4'|'dualstack'|'ipv6'
  False, # privatedns -> true or false
  'rubiconcloud_vpce', #endpoint_name,
  ec2
  )
