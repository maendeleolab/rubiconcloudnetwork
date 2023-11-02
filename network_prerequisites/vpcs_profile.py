#!/usr/bin/env python3

from vpcs_api_calls import *
from subnets_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

vpc1 = 'boto3_vpc1'
az1 = 'us-east-1a'
az2 = 'us-east-1b'

# Create vpc
create_vpc_resources(vpc1,'10.10.0.0/20', ec2)
# Modify dns attributes
modify_dns_hostnames(get_vpc_ids(vpc1, ec2), True, ec2)
modify_dns_support(get_vpc_ids(vpc1, ec2), True, ec2)
# Modify network address usage metrics
modify_network_address_usage_metrics(get_vpc_ids(vpc1, ec2), True, ec2)
# Add an additonal cidr
add_vpc_cidr_block(get_vpc_ids(vpc1, ec2), '10.11.0.0/20', ec2)
# Create public subnet in AZ 
# Primary cidr public subnet in Az1
deploy_subnet(vpc1+'_public_1a_pri', az1, '10.10.1.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Primary cidr public subnet in Az2
deploy_subnet(vpc1+'_public_1b_pri', az2, '10.10.2.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Secondary cidr public subnet in Az1
deploy_subnet(vpc1+'_public_1a_sec', az1, '10.11.1.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Secondary cidr public subnet in Az2
deploy_subnet(vpc1+'_public_1b_sec', az2, '10.11.2.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Create private subnet in AZ 
# Primary cidr private subnet in Az1
deploy_subnet(vpc1+'_private_1a_pri', az1, '10.10.8.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Primary cidr private subnet in Az2
deploy_subnet(vpc1+'_private_1b_pri', az2, '10.10.9.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Secondary cidr private subnet in Az1
deploy_subnet(vpc1+'_private_1a_sec', az1, '10.11.8.0/24', get_vpc_ids(vpc1, ec2), ec2)
# Secondary cidr private subnet in Az2
deploy_subnet(vpc1+'_private_1b_sec', az2, '10.11.9.0/24', get_vpc_ids(vpc1, ec2), ec2)


