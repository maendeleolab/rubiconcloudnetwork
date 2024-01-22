#!/usr/bin/env python3


from resources.vpcs_api_calls import *
from resources.subnets_api_calls import *
from resources.route_tables_api_calls import *
from resources.internet_gateways_api_calls import *
from resources.prefixlists_api_calls import *
from resources.elbs_api_calls import *
from resources.prefixlist_template import deploy_prefixlist
from resources.security_group_template import deploy_privaterfc1918_sg
from resources.account_profiles import assume_profile_creds, client_session


# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')


def deploy_elb(
	targets_name,
	protocol,
	port,
	vpc_id,
	health_protocol,
	health_interval,
	health_timeout,
	healthy_count,
	unhealthy_count,
	target_type,
	scheme,
	elb_name,
	subnet1,
	subnet2,
	elb_sg,
	elb_type,
	ip_address_type,
	elbv2
	):
	create_targets(
							elbv2,
							vpc_id,
							target_type,
							ip_address_type,
							targets_name,
							protocol,
							port,
							health_protocol,
							health_interval,
							health_timeout,
							healthy_count,
							unhealthy_count,
	)


	create_elb(
				elb_name,
				subnet1,
				subnet2,
				elb_sg,
				elbv2,
				elb_type,
				ip_address_type,
				scheme,
	)


	listeners(
				targets_name,
				elb_name,
				port,
				protocol,
				elbv2
	)


def register_elb_targets(
									target_name,
									instance_id,
									port,
									elbv2
	):
		register_target(
									target_name,
									instance_id,
									port,
									elbv2
		)


def destroy_elb(
	target_name,
	elb_name,
	instance
	):
	deregister_target(
								target_name,
								instance_id,
								elbv2
	)



	delete_targets(target_name, elbv2)


	delete_elb(elb_name, elbv2)
