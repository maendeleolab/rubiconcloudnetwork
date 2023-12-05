#!/usr/bin/env python3

#from network_resources import vpcs_api_calls
from network_resources.delete_resources import delete_all
from network_resources.account_profiles import assume_profile_creds,\
client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
#ec2 = client_session('default', 'ec2', 'us-east-1')



delete_all(
					 'boto3_vpc1', #vpc_name,
           ec2=client_session('default', 'ec2', 'us-east-1')
				 )


