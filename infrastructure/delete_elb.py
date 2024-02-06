#!/usr/bin/env python3

from resources.instance_template import lab_instance, get_instance_id
from resources.iam_template import create_ssm_role, flowlogs_iam_functions
from resources.elb_template import deploy_elb, register_elb_targets
from resources.endpoint_template import dualstack_endpoint_service, vpce
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

ec2 = client_session('default', 'ec2', 'us-east-1')
# iam=client_session('default', 'iam', 'us-east-1')
elbv2 = client_session('default', 'elbv2', 'us-east-1')


# delete elb related resources
delete_vpce('rubiconcloud_vpce', ec2)
delete_vpc_endpoint_service('rubiconcloud_service', ec2)
delete_elb('vpc2-rubiconcloud-elb', elbv2)

deregister_target(
    'vpc2-rubiconcloud-targets',
    get_instance_id('vpc2_rubiconcloud_target_1', ec2),
    '5555',
    elbv2
)
deregister_target(
'vpc2-rubiconcloud-targets',
get_instance_id('vpc2_rubiconcloud_target_2', ec2),
'5555',
elbv2
)
delete_targets('vpc2-rubiconcloud-targets', elbv2)
