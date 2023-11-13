#!/usr/bin/env python3

from prefixlists_api_calls import *
from account_profiles import assume_profile_creds, client_session
# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
ec2 = client_session('default', 'ec2', 'us-east-1')


prefixlist = 'privaterfc1918'


# Create managed prefix-lists 
#create_prefixlist(name, cidr_entry, max_entries, ec2):
create_prefixlist(prefixlist, '10.0.0.0/8', 50, ec2)
#def add_entries_to_prefixlist(prefixlist_name, 
                                 #prefixlist_id, 
                                 #state, 
                                 #cidr_entry, 
                                 #description, 
                                 #ec2):
add_entries_to_prefixlist(prefixlist,
                          get_prefixlist_id(prefixlist, ec2), 
                          get_prefixlist_state(prefixlist, ec2), 
                          '172.16.0.0/12', 
                          'privaterfc1918', 
                          ec2
                          )
add_entries_to_prefixlist(prefixlist,
                          get_prefixlist_id(prefixlist, ec2), 
                          get_prefixlist_state(prefixlist, ec2), 
                          '192.168.0.0/16', 
                          'privaterfc1918', 
                          ec2
                          )
remove_entries_from_prefixlist(prefixlist, 
                          get_prefixlist_id(prefixlist, ec2), 
                          '192.168.0.0/16', # cidr_entry to remove
                          ec2
                          )
update_max_entries_of_prefixlist(prefixlist, 
                         get_prefixlist_id(prefixlist,ec2),
                         get_prefixlist_state(prefixlist, ec2),
                         45, # max_entries 
                         ec2
                         )
