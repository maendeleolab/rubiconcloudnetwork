#!/usr/bin/env python3

# This function returns the prefix list name
def get_prefixlist_name(prefixlist, ec2):
  try:
    if prefixlist == None:
      pass
      print(f"Prefix-list {prefixlist} doesn't exist...")
  else:
    resources = ec2.describe_managed_prefix_lists(
	#DryRun=True|False,
	Filters=[
	    {
		'Name': 'tag:Name',
		'Values': [
		    prefixlist,
		]
	    },
	],
    )
    print(f'Prefix-list name: {resources['PrefixLists']['PrefixListName']}')
    return resources['PrefixLists']['PrefixListName']
  except Exception as err:
    print(f'Error found: {err}...')

# This function checks if cidr entry already exists in prefix-list
def verify_if_cidr_entry_exists(prefixlist_id, cidr_entry, ec2):
  try:
    resources = ec2.get_managed_prefix_list_entries(
    #DryRun=True|False,
    PrefixListId=prefixlist_id,
    )
    for entry in resources['Entries']:
      if entry['Cidr'] == cidr_entry:
        print(f'Cidr : {entry["Cidr"]}')
        return entry['Cidr']
  except Exception as err:
    print(f'Error found: {err}...')

# This function returns the prefix list id
def get_prefixlist_id(prefixlist_id, ec2):
  try:
    if prefixlist_id == None:
      pass
      print(f"Prefix-list {prefixlist_id} doesn't exist...")
  else:
    resources = ec2.describe_managed_prefix_lists(
	#DryRun=True|False,
    )
    print(f'Prefix-list name: {resources['PrefixLists']['PrefixListId']}')
    return resources['PrefixLists']['PrefixListId']
  except Exception as err:
    print(f'Error found: {err}...')

# This function creates a prefix list for ipv4 addresses
def create_prefixlist(name, cidr_entry, max_entries, ec2):
  try:
    if name == get_prefixlist_name(name, ec2):
      print(f"Prefix-list {name} doesn't exist...")
      pass
    else:
      print(f'Creating prefix-list {name}...')
      resources = ec2.create_managed_prefix_list(
          # DryRun=True|False,
          PrefixListName=name,
          Entries=[
          {
              'Cidr': cidr_entry,
              'Description': name
          },
          ],
          MaxEntries=max_entries,
          TagSpecifications=[
          {
              'ResourceType': 'prefix-list',
              'Tags': [
              {
                  'Key': 'Name',
                  'Value': name
              },
              ]
          },
          ],
          AddressFamily='IPv4',
      )
  except Exception as err:
    print(f'Error found: {err}...')

# This function adds new entries to the prefix list
def add_entries_to_prefixlist(prefixlist_id, cidr_entry, description, ec2):
  try:
    if get_prefixlist_name == prefixlist_id:
      print(f"Prefix-list {prefixlist_id} does'nt exist...")
      pass
    elif verify_if_cidr_entry_exists(prefixlist_id, cidr_entry, ec2) == cidr_entry:
      print(f'Cidr {cidr_entry} already exists...')
      pass
    else:
      print(f'Adding Cidr {cidr_entry} to prefix-list {prefixlist}...')
      resources = ec2.modify_managed_prefix_list(
          #DryRun=True|False,
          PrefixListId=prefixlist_id,
          #CurrentVersion=123,
          #PrefixListName='string',
          AddEntries=[
          {
              'Cidr': cidr_entry,
              'Description': description
          },
          ],
      )
  except Exception as err:
    print(f'Error found: {err}...')

# This function removes entries from the prefix list
def remove_entries_from_prefixlist(prefixlist, cidr_entry, ec2):
  resources = ec2.modify_managed_prefix_list(
      #DryRun=True|False,
      PrefixListId=prefixlist,
      #CurrentVersion=123,
      #PrefixListName='string',
      RemoveEntries=[
	  {
	      'Cidr': cidr_entry
	  },
      ],
  )

# This function removes entries from the prefix list
def update_max_entries_of_prefixlist(prefixlist, max_entries, ec2):
  resources = ec2.modify_managed_prefix_list(
      #DryRun=True|False,
      PrefixListId=prefixlist,
      #CurrentVersion=123,
      #PrefixListName='string',
      MaxEntries=max_entries
  )

# This function deletes prefix lists
def delete_prefixlist(prefixlist_id, ec2):
  try:
    if prefixlist_id == None:
      pass
    else:
      print(f'Delete {prefixlist_id}...')
      resources = ec2.delete_managed_prefix_list(
	  #DryRun=True|False,
	  PrefixListId=prefixlist_id
      )
  except Exception as err:
    print(f'Error found: {err}...')


