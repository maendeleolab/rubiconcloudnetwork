#!/usr/bin/env python3


from resources.vpcs_api_calls import *
#from resources.subnets_api_calls import *
#from resources.route_tables_api_calls import *
#from resources.internet_gateways_api_calls import *
#from resources.prefixlists_api_calls import *
#from resources.enpoints_api_calls import *
#from resources.enpoints_api_calls import *
#from resources.prefixlist_template import deploy_prefixlist
#from resources.security_group_template import deploy_privaterfc1918_sg
#from resources.account_profiles import assume_profile_creds, client_session
from resources.endpoints_api_calls import *
from resources.elbs_api_calls import *
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')


def connect_endpoint(
                name, 
                subnet, 
                sg, 
                preserve_client_ip, 
                ec2
	):
	create_connect_endpoint( 
											 name, #endpoint_name,
											 get_subnet_id(subnet ,ec2), #subnet_id,
											 get_sg_id(sg, ec2), #sg_id,
											 preserve_client_ip, #preserve_client_ip,
											 ec2
		)


def dualstack_endpoint_service(
	name,
	network_lb,
  ec2
	):
	vpc_endpoint_service(
								ec2, # client
								name, # endpoint name
								False, # acceptance true or false
								'ipv4', # ipv4
								'ipv6', # ipv6
								#'', # private dns name
								get_elb_arn(network_lb, elbv2), # network load balancer arn
								#'' # gateway load balnacer arn
	)
	# Explicitly allowing all principal for simplicity
	modify_service_permissions(
		name,
		'*', #principals,
		ec2
		)


def vpce(
	endpoint_type, #'Interface'|'Gateway'|'GatewayLoadBalancer'
	vpc_name,
	service_name,
	ip_address_type, #'ipv4'|'dualstack'|'ipv6'
	privatedns, # true or false
	endpoint_name,
	ec2
	):
	create_vpce(
		endpoint_type, #'Interface'|'Gateway'|'GatewayLoadBalancer'
		get_vpc_id(vpc_name, ec2), # vpc id
		service_name,
		get_subnet_id(vpc_name+'_private_1a_ipv6', ec2), # az1,
		get_subnet_id(vpc_name+'_private_1b_ipv6', ec2), # az2,
		get_sg_id(vpc_name+'_vpce', ec2), # endpoint_sg,
		ip_address_type, #'ipv4'|'dualstack'|'ipv6'
		privatedns, # true or false
		endpoint_name,
		ec2
		)
