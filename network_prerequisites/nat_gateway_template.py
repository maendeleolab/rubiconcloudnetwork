#!/usr/bin/env python3

from subnets_api_calls import *
from elastic_ips_api_calls import *
from nat_gateways_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')

# public nat
create_public_nat('boto3_public_nat1', # name of public nat resource 
                  get_subnet_id('boto3_vpc1_public_1a_pri', ec2), # subnet id
                  get_allocation_id('boto3_public_nat1', ec2), # elastic ip
                  ec2 # client session
)
create_public_nat('boto3_public_nat2', # name of public nat resource 
                  get_subnet_id('boto3_vpc1_public_1b_pri', ec2), # subnet id
                  get_allocation_id('boto3_public_nat2', ec2), # elastic ip
                  ec2 # client session
)

# private nat
create_private_nat('boto3_private_nat1', # name of private nat resource
                   get_subnet_id('boto3_vpc1_private_1a_pri', ec2), # subnet id
                   '1', # number_of_secondary_ips, 
                   ec2 # client session
)
#create_private_nat('boto3_private_nat2', # name of private nat resource
#                   get_subnet_id('boto3_vpc1_private_1b_pri', ec2), # subnet id
#                   '1', # number_of_secondary_ips, 
#                   ec2 # client session
#)

