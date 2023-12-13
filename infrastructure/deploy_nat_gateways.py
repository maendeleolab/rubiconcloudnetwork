#!/usr/bin/env python3

from network_resources.vpcs_api_calls import *
from network_resources.subnets_api_calls import *
from network_resources.route_tables_api_calls import *
from network_resources.internet_gateways_api_calls import *
from network_resources.nat_gateway_template import deploy_public_nat_gateways
from network_resources.elastic_ip_template import assign_public_ipv4
from network_resources.account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


# Deploys ipv4 elastic ips
# 2 elastic ips are created in each vpc
assign_public_ipv4('boto3_vpc1',
                   ec2=client_session('default', 'ec2', 'us-east-1')
                   )
assign_public_ipv4('boto3_vpc2',
                   ec2=client_session('default', 'ec2', 'us-east-1')
                   )

# Deploys 2 public nat gateways in two AZs in the public subnets
deploy_public_nat_gateways('boto3_vpc1',
                    ec2=client_session('default', 'ec2', 'us-east-1')
                    )
deploy_public_nat_gateways('boto3_vpc2',
                    ec2=client_session('default', 'ec2', 'us-east-1')
                    )
