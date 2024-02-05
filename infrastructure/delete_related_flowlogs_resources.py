#!/usr/bin/env python3

# from resources import vpcs_api_calls
from resources.delete_resources import delete_flowlogs_config, test
from resources.account_profiles import assume_profile_creds, \
    client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')
iam = client_session('default', 'iam', 'us-east-1')
cw_logs = client_session('default', 'logs', 'us-east-1')

delete_flowlogs_config(
	'boto3_vpc1', #vpc name
	ec2,
	iam,
	cw_logs
	)
delete_flowlogs_config(
	'boto3_vpc2', #vpc name
	ec2,
	iam,
	cw_logs
	)
delete_flowlogs_config(
	'boto3_vpc3', #vpc name
	ec2=client_session('default', 'ec2', 'us-west-2'),
	iam,
	cw_logs=client_session('default', 'ec2', 'us-west-2')
	)

