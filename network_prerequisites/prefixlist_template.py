#!/usr/bin/env python3

from prefixlists_api_calls import *
from account_profiles import assume_profile_creds, client_session
# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


#def get_prefixlist_name(prefixlist, ec2):
#def verify_if_cidr_entry_exists(prefixlist_id, cidr_entry, ec2):
#def get_prefixlist_id(prefixlist_id, ec2):

# Create managed prefix-lists 
#create_prefixlist(name, cidr_entry, max_entries, ec2):
create_prefixlist('privaterfc1918', '10.0.0.0/8', 50, ec2)
#def add_entries_to_prefixlist(prefixlist_id, cidr_entry, description, ec2):
#def remove_entries_from_prefixlist(prefixlist, cidr_entry, ec2):
#def update_max_entries_of_prefixlist(prefixlist, max_entries, ec2):
