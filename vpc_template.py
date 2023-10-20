#!/usr/bin/env python3

import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')

def describe_resources():
  resources = ec2.describe_vpcs(
      Filters=[
	  {
	      'Name': 'tag:Name',
	      'Values': [
		  'boto3_vpc1',
	      ]
	  },
      ]
  )
  for item in resources['Vpcs'][0]['Tags']:
    print(item['Value'])

describe_resources()

def create_resources():
  resources = ec2.create_vpc(
      CidrBlock='10.100.0.0/20',
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
		      'Value': 'boto3_vpc1'
		  },
	      ]
	  },
      ]
  )

  print(resources)

