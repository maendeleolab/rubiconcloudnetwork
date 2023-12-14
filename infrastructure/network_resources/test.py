#!/usr/bin/env python3


from vpcs_api_calls import *
from subnets_api_calls import *
from route_tables_api_calls import *
from internet_gateways_api_calls import *
from prefixlists_api_calls import *
from prefixlist_template import deploy_prefixlist 
from account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

# prefixlist entries
privaterfc1918 = ['172.16.0.0/12', '192.168.0.0/16']

deploy_prefixlist('privaterfc1918',  # prefixlist_name,
                      '10.0.0.0/8',  # first_cidr,
                      '50',  # max_entries,
                      # list(cidrs_list),
                      privaterfc1918,
                      ec2
                      )
