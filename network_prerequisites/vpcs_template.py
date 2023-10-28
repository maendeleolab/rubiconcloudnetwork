#!/usr/bin/env python3

import boto3, sys

# Creating a boto3 object for the client to interact with
# the ec2 service in aws
ec2 = boto3.client('ec2', region_name='us-east-1')

# This is a function to describe resources tag names
def describe_resources(name):
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

# This is a function to describe all the resources
def describe_some():
  resources = ec2.describe_vpcs(
  )
  return resources
  #describe_some()

# This is a function to describe the resources ids
def describe_ids(name):
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
    for item in resources['Vpcs']:
        return item['VpcId']
  except Exception as err:
    print(f'Unable to describe vpc. See error {err}...')
         
#describe_ids()

# This is a function to create resources
def create_resources(name, cidr):
  try:
    results = describe_resources(name)
    if results == name:
      print(f'{name} already exists...')
      pass
    elif results != name:
      resources = ec2.create_vpc(
          CidrBlock=cidr,
          #AmazonProvidedIpv6CidrBlock=True|False,
          #Ipv6Pool='string',
          #Ipv6CidrBlock='string',
          #Ipv4IpamPoolId='string',
          #Ipv4NetmaskLength=123,
          #Ipv6IpamPoolId='string',
          #Ipv6NetmaskLength=123,
          #DryRun=True|False,
          InstanceTenancy='default',
          #Ipv6CidrBlockNetworkBorderGroup='string',
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
      return resources
  except Exception as err:
    print(f'Found error: {err}...')

#create_resources()

# This function modifies resources attributes
def modify_resources(resource, value):
  try:
    resources = ec2.modify_vpc_attribute(
        EnableDnsHostnames={
            'Value': value #True|False
        },
        EnableDnsSupport={
            'Value': value #True|False
        },
        VpcId=resource,
        EnableNetworkAddressUsageMetrics={
            'Value': value #True|False
        }
    )
  except Exception as err:
    print(f'Error found: {resource}...')

#modify_resources(describe_ids())

# This is a function to delete resources
def delete_resources(resource):
  try:
    resources = ec2.delete_vpc(
        VpcId=resource,
        #DryRun=True|False
    )
  except Exception as err:
    print(f'Error found: {err}...')


#delete_resources(describe_ids())
