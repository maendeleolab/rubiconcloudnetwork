#!/usr/bin/env python3

# from resources import vpcs_api_calls
#from resources.vpc_template import deploy_vpc
#from resources.vpc_peering_template import same_account_vpc_peering
#from resources.nat_gateway_template import deploy_public_nat_gateways
#from resources.elastic_ip_template import assign_public_ipv4
from resources.endpoint_template import connect_endpoint
#from resources.instance_template import lab_instance
#from resources.iam_template import create_ssm_role, flowlogs_iam_functions
#from resources.monitoring_template import deploy_monitoring, test
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
#from resources.route_tables_api_calls import *
#from resources.internet_gateways_api_calls import *
#from resources.iam_api_calls import *
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
#iam=client_session('default', 'iam', 'us-east-1')
#cw_logs = client_session('default', 'logs', 'us-east-1')

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
connect_endpoint(
		'boto3_vpc3_connect_endpoint', #name,
		'boto3_vpc3_private_1a_ipv6', #subnet,
		'boto3_vpc3_private', #sg,
		False, #preserve_client_ip,
		ec2=client_session('default', 'ec2', 'us-west-2')
)


