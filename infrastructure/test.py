#!/usr/bin/env python3
from vpcs import vpc3
from resources.ipv6_route_to_egress_only_igw import ipv6_egress_only_out
from resources.instance_template import lab_instance
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.elb_template import deploy_elb
from resources.delete_resources import test
from resources.test import code_test
from resources.vpcs_api_calls import *
from resources.vpc_peerings_api_calls import *
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
from resources.iam_api_calls import *
from resources.endpoints_api_calls import *
from resources.elbs_api_calls import *
from resources.instances_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.account_profiles import assume_profile_creds, \
    client_session


from resources.visibility import *

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# We are using sts to get the account id of the user making the call
# this useful to not expose the account id in the code. I am getting
# away with this b/c the vpc peering is in the same account.
# If the peer vpc is in another account, we will have to statically
# define it in the code.
# sts = client_session('default', 'sts', 'us-east-1')

ec2 = client_session('default', 'ec2', 'us-east-1')
iam = client_session('default', 'iam', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')

delete_ipv6_eigw('boto3_vpc3', ec2=client_session('default','ec2', 'us-west-2'))
