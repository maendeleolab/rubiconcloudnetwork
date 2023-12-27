#!/usr/bin/env python3


#from network_resources.vpcs_api_calls import *
#from network_resources.subnets_api_calls import *
#from network_resources.route_tables_api_calls import *
#from network_resources.internet_gateways_api_calls import *
#from network_resources.account_profiles import assume_profile_creds, client_session
from network_resources.iam_template import create_ssm_role
from network_resources.vpcs_api_calls import *
from network_resources.instances_api_calls import *
from network_resources.subnets_api_calls import *
from network_resources.route_tables_api_calls import *
from network_resources.internet_gateways_api_calls import *
from network_resources.iam_api_calls import *
from network_resources.security_groups_api_calls import *
from network_resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
iam = client_session('default', 'iam', 'us-east-1')


user_data = '''
git clone
https://github.com/maendeleolab/toolbox.git\
 && cd toolbox && ./networkingTools/prerequisites.sh '
'''


def lab_instance(
	name,
	ami,
	instance_type,
	key_pair,
	sg,
	subnet,
	public_ip,
	ec2
	):
	create_ssm_role('ssm_role_for_connect', iam)
	deploy_instances(
		name, #instance_name,
		ami, #image,
		instance_type, #instance_type,
		key_pair, # key_name,
		'1', # max_count,
		'1', # min_count,
		True, # monitoring (boolean True or False),
		get_sg_id(sg, ec2), # security_group_ids,
		get_subnet_id(subnet, ec2), # subnet_id,
		public_ip, # associate public ip is boolean True or False
		#get_profile_arn('ssm-instance-profile', iam), # profile arn
		'ssm-instance-profile', # profile name
		user_data,
		ec2
		)

