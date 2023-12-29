#!/usr/bin/env python3

from resources.prefixlists_api_calls import *
from resources.account_profiles import assume_profile_creds, client_session
# The client_session function explicitly define the profile_name,
# the service and region to use. This permits us to be granular.
# client_session(profile_name, service, region)
#ec2 = client_session('default', 'ec2', 'us-east-1')


# prefixlist = 'privaterfc1918'


# Create managed prefix-lists
def deploy_prefixlist(prefixlist_name,
                      first_cidr, max_entries,
                      cidrs_list,
                      ec2=client_session('default', 'ec2', 'us-east-1')
                      ):
    # create_prefixlist(name, cidr_entry, max_entries, ec2):
    create_prefixlist(prefixlist_name, first_cidr, max_entries, ec2)
    # Let's add entries
    for entry in cidrs_list:
        add_entries_to_prefixlist(prefixlist_name,  # prefixlist_name
                                  # prefixlist_id
                                  get_prefixlist_id(prefixlist_name, ec2),
                                  # state
                                  get_prefixlist_state(prefixlist_name, ec2),
                                  # entry
                                  entry,
                                  # description
                                  prefixlist_name,
                                  # client session
                                  ec2
                                  )


# Place holder for future use
# remove_entries_from_prefixlist(prefixlist,
#                          get_prefixlist_id(prefixlist, ec2),
#                          '192.168.0.0/16', # cidr_entry to remove
#                          ec2
#                          )
# update_max_entries_of_prefixlist(prefixlist,
#                         get_prefixlist_id(prefixlist,ec2),
#                         get_prefixlist_state(prefixlist, ec2),
#                         45, # max_entries
#                         ec2
#                         )
