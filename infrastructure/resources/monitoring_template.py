#!/usr/bin/env python3


from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.prefixlists_api_calls import *
from resources.prefixlist_template import deploy_prefixlist
from resources.security_group_template import deploy_privaterfc1918_sg
from resources.monitoring_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
cw_logs = client_session('default', 'logs', 'us-east-1')



def deploy_monitoring(
                  log_group_name,
                  days, 
                  cw_logs,
									vpc_name,
									ec2
	):
	create_log_bucket(log_group_name, cw_logs)
	update_retention_policy(log_group_name, days, cw_logs)
	describe_log_bucket(log_group_name, cw_logs)
	create_flowlogs(
						log_group_name, #log_group_name,
						get_role_arn('boto3_flowlogs_role', iam), #role_name,
						get_vpc_id(vpc_name, ec2), #resource_ids,
						'VPC', #resource_type,
						'ALL', #traffic_type,
						'cloud-watch-logs', #log_destination_type,
						'60', #aggregation_time
						ec2
		)


