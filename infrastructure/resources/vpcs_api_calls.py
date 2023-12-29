#!/usr/bin/env python3

import boto3
import sys

# client_session(profile_name, service, region)
# ec2 = client_session('default', 'ec2', 'us-east-1')
# ec2 is used to return the "profile_name" (IAM role for the account),
# the service name (in this scenario ec2) and region id.
# This permits us to reuse the functions for any account and region.

# This is a function to describe resources tag names
# The main objective is to access the vlaue of the tag key "Name"


def describe_vpc_resources(name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs'][0]['Tags']:
            return item['Value']

    except Exception as err:
        print(f'Resource {name} does not exist. Error found: {err}...')
# describe_vpc_resources(name, ec2)

# This is a function to describe all the resources


def describe_some(ec2):
    resources = ec2.describe_vpcs(
    )
    return resources
# describe_some(ec2)

# This is a function to describe the resources ids


def get_vpc_id(resource_name, ec2):
    try:
        resources = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        resource_name,
                    ]
                },
            ]
        )
        for item in resources['Vpcs']:
            return item['VpcId']
    except Exception as err:
        print(f'Unable to describe vpc. See error {err}...')

# get_vpc_ids(resource_name, ec2)

# This is a function to create resources


def create_vpc_resources(name, cidr, ec2):
    try:
        results = describe_vpc_resources(name, ec2)
        if results == name:
            print(f'Vpc: {name} already exists...')
            pass
        elif results != name:
            print(f'Creating {name}...')
            resources = ec2.create_vpc(
                CidrBlock=cidr,
                # AmazonProvidedIpv6CidrBlock=True|False,
                # Ipv6Pool='string',
                # Ipv6CidrBlock='string',
                # Ipv4IpamPoolId='string',
                # Ipv4NetmaskLength=123,
                # Ipv6IpamPoolId='string',
                # Ipv6NetmaskLength=123,
                # DryRun=True|False,
                InstanceTenancy='default',
                # Ipv6CidrBlockNetworkBorderGroup='string',
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': name
                            },
                        ]
                    },
                ]
            )
            print(f'Created vpc id: {resources["Vpc"]["VpcId"]}...')
            return resources
    except Exception as err:
        print(f'Error found: {err}...')

# create_vpc_resources(name, cidr, ec2)

# The function adds an additional cidr to the vpc


def add_vpc_cidr_block(resource_id, cidr, ec2):
    try:
        if cidr == None:
            pass
        else:
            resources = ec2.associate_vpc_cidr_block(
                # AmazonProvidedIpv6CidrBlock=True|False,
                CidrBlock=cidr,
                VpcId=resource_id
            )
            print(f'Cidr: {cidr} is associated to VpcId: {resource_id}...')
    except Exception as err:
        print(f'Error found: {err}...')

# The functions modify resources attributes


def modify_dns_hostnames(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableDnsHostnames={
                'Value': value  # True|False
            }
        )
        print(f'Vpc Id: {resource_id} DNS Hostnames Attribute Modified...')
    except Exception as err:
        print(f'Error found: {err}...')

# modify_dns_hostnames(describe_ids(name), value, ec2)


def modify_dns_support(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableDnsSupport={
                'Value': value  # True|False
            }
        )
        print(f'Vpc Id: {resource_id} DNS Support Attribute Modified...')
    except Exception as err:
        print(f'Error found: {err}...')

# modify_dns_support(describe_ids(name), value, ec2)


def modify_network_address_usage_metrics(resource_id, value, ec2):
    try:
        resources = ec2.modify_vpc_attribute(
            VpcId=resource_id,
            EnableNetworkAddressUsageMetrics={
                'Value': value  # True|False
            }
        )
        print(
            f'Vpc Id: {resource_id} Network Address Usage Metrics Attribute Modified...')
    except Exception as err:
        print(f'Error found: {err}...')

# modify_network_address_usage_metrics(describe_ids(name), value, ec2)

# This is a function to delete resources


def delete_vpc_resources(resource, ec2):
    try:
        if resource == None:
            pass
        else:
            print(f'Delete vpc...')
            resources = ec2.delete_vpc(
                VpcId=resource,
                # DryRun=True|False
            )
    except Exception as err:
        print(f'Error found: {err}...')

# delete_vpc_resources(describe_ids(), ec2)
