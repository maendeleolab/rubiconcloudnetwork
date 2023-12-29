#!/usr/bin/env python3


#from resources.vpcs_api_calls import *
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
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


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


