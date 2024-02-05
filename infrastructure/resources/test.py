#!/usr/bin/env python3


from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.endpoints_api_calls import *
from resources.prefixlists_api_calls import *
from resources.prefixlist_template import deploy_prefixlist 
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


def code_test():
	get_vpce_id('rubiconcloud_vpce', ec2)
