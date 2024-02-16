#!/usr/bin/env python3

from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import get_ipv6_eigw_id


def ipv6_egress_only_out(
	route_table_id,
	dst_ipv6cidr,
	eigw_name,
	ec2
	):
		vpc_route_entry_to_egress_only_igw(
		#route_table_id,
		get_vpc_route_table_id(
		route_table_id, 
		ec2), 
		#dst_ipv6cidr,
		dst_ipv6cidr, 
		#eigw_id,
		get_ipv6_eigw_id(
		eigw_name, 
		ec2
		), 
		ec2
		)
