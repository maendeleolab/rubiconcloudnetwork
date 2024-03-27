#!/usr/bin/env python3

from resources.vpn_api_calls import *
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.prefixlists_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')

create_ipsec_vpn(
  customer_gateway,
  vpn_gateway,
  transit_gateway,
  static_routing, #True or False
  tunnel_inside_ip_version, #V4 or V6
  ike_version,
  name,
  local_network,
  remote_network,
  outside_ip_type,
  ec2
  )


