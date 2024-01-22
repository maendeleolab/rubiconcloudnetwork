#!/usr/bin/env python3

from resources.instance_template import lab_instance
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.elb_template import deploy_elb
from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.security_groups_api_calls import *
from resources.iam_api_calls import *
from resources.endpoints_api_calls import *
from resources.elbs_api_calls import *
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

ec2=client_session('default', 'ec2', 'us-east-1')
iam=client_session('default', 'iam', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')



deploy_elb(
  'vpc2-rubiconcloud-targets', #targets_name,
  'TCP', #protocol='TCP',
  '5555', #port='5555',
  get_vpc_id('boto3_vpc2', ec2), #vpc_id,
  'TCP', #health_protocol='TCP',
  '30', #health_interval='30',
  '10', #health_timeout='10',
  '5', #healthy_count='5',
  '10', #unhealthy_count='10',
  'instance', #target_type,
  'internal', #scheme=None,
  'vpc2-rubiconcloud-elb', #elb_name,
  get_subnet_id('boto3_vpc2_private_1a_pri', ec2), #subnet1,
  get_subnet_id('boto3_vpc2_private_1b_pri', ec2), #subnet2,
  get_sg_id('rubiconcloud_elb', ec2), #elb_sg,
  'network', #elb_type,
  'ipv4', #ip_address_type='ipv4',
  elbv2
  )

# Create target instances
#lab_instance(
#    'vpc2_rubiconcloud_target_1', #name,
#    'ami-0fc5d935ebf8bc3bc', #ami,
#    't3.medium', #instance_type,
#    'maendeleolabKey', #key_pair,
#    'boto3_vpc2_private', #security-group,
#    'boto3_vpc2_private_1a_pri', #subnet,
#    False, #public_ip,
#    ec2
#)
#lab_instance(
#    'vpc2_rubiconcloud_target_2', #name,
#    'ami-0fc5d935ebf8bc3bc', #ami,
#    't3.medium', #instance_type,
#    'maendeleolabKey', #key_pair,
#    'boto3_vpc2_private', #security-group,
#    'boto3_vpc2_private_1b_pri', #subnet,
#    False, #public_ip,
#    ec2
#)
#
#register_elb_targets(
#  'vpc2-rubiconcloud-targets', #targets_name,
#  get_instance_id('vpc2_rubiconcloud_target_1', ec2), #instance_id,
#  '5555', #port='5555',
#  elbv2
#)
#register_elb_targets(
#  'vpc2-rubiconcloud-targets', #targets_name,
#  get_instance_id('vpc2_rubiconcloud_target_2', ec2), #instance_id,
#  '5555', #port='5555',
#  elbv2
#)
