#!/usr/bin/env python3

# from resources import vpcs_api_calls
from resources.vpc_template import deploy_vpc
#from resources.vpc_peering_template import same_account_vpc_peering
#from resources.nat_gateway_template import deploy_public_nat_gateways
#from resources.elastic_ip_template import assign_public_ipv4
#from resources.endpoint_template import connect_endpoint
#from resources.instance_template import lab_instance
from resources.iam_template import create_ssm_role
#from resources.monitoring_template import deploy_monitoring, test
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
#from resources.iam_api_calls import *
#from resources.endpoints_api_calls import *
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
#cw_logs = client_session('default', 'logs', 'us-east-1')

# vpc1
def vpc1(ec2):
	deploy_vpc(
			'boto3_vpc1',  # vpc_name,
			'10.10.0.0/20',  # primary_vpc_cidr,
			'10.11.0.0/20',  # secondary_cidr,
			True, # pri amazon provided ipv6 cidr set to true or false
			False, # sec amazon provided ipv6 cidr set to true or false
			'us-east-1a',  # az1,
			'us-east-1b',  # az2,
			'10.10.1.0/24',  # az1_pri_cidr_public_subnet,
			'10.10.2.0/24',  # az2_pri_cidr_public_subnet,
			'10.11.1.0/24',  # az1_sec_cidr_public_subnet,
			'10.11.2.0/24',  # az2_sec_cidr_public_subnet,
			'10.10.8.0/24',  # az1_pri_cidr_private_subnet,
			'10.10.9.0/24',  # az2_pri_cidr_private_subnet,
			'10.11.8.0/24',  # az1_sec_cidr_private_subnet,
			'10.11.9.0/24',  # az2_sec_cidr_private_subnet,
			ec2
	)
# vpc2
def vpc2(ec2):
	deploy_vpc(
			'boto3_vpc2',  # vpc_name,
			'10.20.0.0/20',  # primary_vpc_cidr,
			'10.21.0.0/20',  # secondary_cidr,
			True, # pri amazon provided ipv6 cidr set to true or false
			False, # sec amazon provided ipv6 cidr set to true or false
			'us-east-1a',  # az1,
			'us-east-1b',  # az2,
			'10.20.1.0/24',  # az1_pri_cidr_public_subnet,
			'10.20.2.0/24',  # az2_pri_cidr_public_subnet,
			'10.21.1.0/24',  # az1_sec_cidr_public_subnet,
			'10.21.2.0/24',  # az2_sec_cidr_public_subnet,
			'10.20.8.0/24',  # az1_pri_cidr_private_subnet,
			'10.20.9.0/24',  # az2_pri_cidr_private_subnet,
			'10.21.8.0/24',  # az1_sec_cidr_private_subnet,
			'10.21.9.0/24',  # az2_sec_cidr_private_subnet,
			ec2
	)
# vpc3
def vpc3(ec2):
	deploy_vpc(
			'boto3_vpc3',  # vpc_name,
			'10.30.0.0/20',  # primary_vpc_cidr,
			'10.31.0.0/20',  # secondary_cidr,
			True, # pri amazon provided ipv6 cidr set to true or false
			False, # sec amazon provided ipv6 cidr set to true or false
			'us-west-2a',  # az1,
			'us-west-2b',  # az2,
			'10.30.1.0/24',  # az1_pri_cidr_public_subnet,
			'10.30.2.0/24',  # az2_pri_cidr_public_subnet,
			'10.31.1.0/24',  # az1_sec_cidr_public_subnet,
			'10.31.2.0/24',  # az2_sec_cidr_public_subnet,
			'10.30.8.0/24',  # az1_pri_cidr_private_subnet,
			'10.30.9.0/24',  # az2_pri_cidr_private_subnet,
			'10.31.8.0/24',  # az1_sec_cidr_private_subnet,
			'10.31.9.0/24',  # az2_sec_cidr_private_subnet,
			ec2
	)


# run directly
def main():
	try:
		vpc1(ec2)
		vpc2(ec2)
		vpc3(ec2=client_session('default', 'ec2', 'us-west-2'))
	except Exception as err:
		logger.error(f'Error found in "main": {err}...')
	finally:
		create_ssm_role('ssm_role_for_connect', iam)
if __name__ == '__main__':
	main()

