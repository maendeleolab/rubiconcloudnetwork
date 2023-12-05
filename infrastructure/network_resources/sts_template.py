#!/usr/bin/env python3

from sts_api_calls import *
from account_profiles import assume_profile_creds, client_session

# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
sts = client_session('default', 'sts', 'us-east-1')


get_user_identity(sts)
