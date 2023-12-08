#!/usr/bin/env python3
from time import sleep

# This function returns the prefix list name


def get_prefixlist_name(prefixlist, ec2):
    try:
        resources = ec2.describe_managed_prefix_lists(
            # DryRun=True|False,
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        prefixlist,
                    ]
                },
            ],
        )
        print(
            f'Prefix-list name: {resources["PrefixLists"][0]["PrefixListName"]}')
        return resources['PrefixLists'][0]['PrefixListName']
    except Exception as err:
        print(f'prefix-list "{prefixlist}" not found...')

# This function checks if cidr entry already exists in prefix-list


def verify_if_cidr_entry_exists(prefixlist_id, cidr_entry, ec2):
    try:
        resources = ec2.get_managed_prefix_list_entries(
            # DryRun=True|False,
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
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            prefixlist_id,
                        ]
                    },
                ]
                # DryRun=True|False,
            )
            for item in resources["PrefixLists"]:
                print(f'Prefix-list name: {item["PrefixListId"]}')
                return item['PrefixListId']
    except Exception as err:
        print(f'Error found: {err}...')

# This function returns the prefix-list version
# This is needed when modifying the prefix-list


def get_prefixlist_version(prefixlist_id, ec2):
    try:
        if prefixlist_id == None:
            pass
            print(f"Prefix-list {prefixlist_id} doesn't exist...")
        else:
            resources = ec2.describe_managed_prefix_lists(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            prefixlist_id,
                        ]
                    },
                ]
                # DryRun=True|False,
            )
            for item in resources["PrefixLists"]:
                print(f'Prefix-list version: {item["Version"]}')
                return item['Version']
    except Exception as err:
        print(f'Error found: {err}...')


# This function returns the prefix-list state
# This is needed when modifying the prefix-list
# We check for the state before adding more entries
def get_prefixlist_state(prefixlist_id, ec2):
    try:
        if prefixlist_id == None:
            pass
            print(f"Prefix-list {prefixlist_id} doesn't exist...")
        else:
            resources = ec2.describe_managed_prefix_lists(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            prefixlist_id,
                        ]
                    },
                ]
                # DryRun=True|False,
            )
            for item in resources["PrefixLists"]:
                print(f'Prefix-list version: {item["State"]}')
                return item['State']
    except Exception as err:
        print(f'Error found: {err}...')


# This function creates a prefix list for ipv4 addresses
def create_prefixlist(name, cidr_entry, max_entries, ec2):
    try:
        if name == get_prefixlist_name(name, ec2):
            print(f"Prefix-list {name} exists...")
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


def add_entries_to_prefixlist(
        prefixlist_name,
        prefixlist_id,
        state,
        cidr_entry,
        description,
        ec2):
    try:
        if verify_if_cidr_entry_exists(prefixlist_id, cidr_entry, ec2) == cidr_entry:
            print(f'Cidr {cidr_entry} already exists...')
            pass
        while True:
            if state == 'create-complete' or state == 'modify-complete':
                resources = ec2.modify_managed_prefix_list(
                    # DryRun=True|False,
                    PrefixListId=prefixlist_id,
                    CurrentVersion=get_prefixlist_version(
                        prefixlist_name, ec2),
                    # PrefixListName='string',
                    AddEntries=[
                        {
                            'Cidr': cidr_entry,
                            'Description': description
                        },
                    ],
                )
                print(
                    f'Adding Cidr {cidr_entry} to prefix-list {prefixlist_name}...')
                break
            else:
                sleep(2)
            state = get_prefixlist_state(prefixlist_name, ec2)
            print(f'Prefix-list {prefixlist_name} state {state}...')
    except Exception as err:
        print(f'Error found: {err}...')

# This function removes entries from the prefix list


def remove_entries_from_prefixlist(prefixlist_name, prefixlist_id, cidr_entry, ec2):
    try:
        resources = ec2.modify_managed_prefix_list(
            # DryRun=True|False,
            PrefixListId=prefixlist_id,
            CurrentVersion=get_prefixlist_version(prefixlist_name, ec2),
            # PrefixListName='string',
            RemoveEntries=[
                {
                    'Cidr': cidr_entry
                },
            ],
        )
    except Exception as err:
        print(f'Error found: {err}...')

# This function removes entries from the prefix list


def update_max_entries_of_prefixlist(prefixlist_name, prefixlist_id, state, max_entries, ec2):
    try:
        while True:
            if state == 'create-complete' or state == 'modify-complete':
                resources = ec2.modify_managed_prefix_list(
                    # DryRun=True|False,
                    PrefixListId=prefixlist_id,
                    # CurrentVersion=get_prefixlist_version(prefixlist_name, ec2),
                    # PrefixListName='string',
                    MaxEntries=max_entries
                )
                print(f'Modifying max entries for {prefixlist_name}...')
                break
            else:
                sleep(2)
            state = get_prefixlist_state(prefixlist_name, ec2)
            print(f'Prefix-list {prefixlist_name} state {state}...')
    except Exception as err:
        print(f'Error found: {err}...')
# This function deletes prefix lists


def delete_prefixlist(prefixlist_id, ec2):
    try:
        if prefixlist_id == None:
            pass
        else:
            resources = ec2.delete_managed_prefix_list(
                # DryRun=True|False,
                PrefixListId=prefixlist_id
            )
            print(f'Delete {prefixlist_id}...')
    except Exception as err:
        print(f'Error found: {err}...')
