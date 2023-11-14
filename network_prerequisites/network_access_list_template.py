#!/usr/bin/env python3

from network_access_lists_api_calls import *
from vpcs_api_calls import *
from subnets_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1 = 'boto3_vpc1'

## We are tagging all default acl with tag "Name":"default"
#tag_default_acl(ec2)
## Create acl
#create_vpc_acl('boto3_vpc1', get_vpc_id('boto3_vpc1', ec2), ec2)
## Add entry to acl ingress
#add_entry_to_vpc_acl(vpc1, 
#                    '10.20.9.0/24', #cidr_entry,
#                    False, #in_or_out, True is ingress and False is egress
#                    '22', #port_range_from,
#                    '22', #port_range_to,
#                    '6', #protocol_number,
#                    'deny', #rule_action,
#                    '110', #rule_number
#                    ec2
#                  )
## Add entry for icmp ingress
#add_icmp_to_vpc_acl(vpc1,
#                    '10.20.9.0/24',
#                    '-1', #icmp_code,
#                    '-1', #icmp_type,
#                    False, #in_or_out,
#                    '-1', #port_range_from,
#                    '-1', #port_range_to,
#                    '1', #protocol_number,
#                    'allow', #rule_action,
#                    '210', #rule_number,
#                    ec2
#                  )
## Add entry to acl egress
#add_entry_to_vpc_acl(vpc1, 
#                    '0.0.0.0/0', #cidr_entry,
#                    True, #in_or_out, True is ingress and False is egress
#                    '-1', #port_range_from,
#                    '-1', #port_range_to,
#                    '-1', #protocol_number,
#                    'allow', #rule_action,
#                    '310', #rule_number
#                    ec2
#                  )
# Associating all subnets associated to default acl to new acl
#print(find_default_acl_name('vpc-0c1aaca9227dd4d88', ec2))
#associate_acl_to_subnet(default_acl, acl_name, new_acl_vpc_id, ec2)
associate_acl_to_subnet(find_default_acl_name(get_vpc_id(vpc1, ec2), ec2),
                                            vpc1, 
                                            ec2
                                           )
remove_entry_from_vpc_acl(vpc1, 
                          False, #in_or_out, 
                          '210', #rule_number, 
                          ec2
                         )


