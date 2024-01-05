#!/usr/bin/env python3

import boto3, sys

# Creating a boto3 object for the client to interact with
# the ec2 service in aws
org = boto3.client('organizations', region_name='us-east-1')


def describe_org():
  resources = org.describe_organization()
  print(resources)

def get_org_policy(org):
  resources = org.describe_organization()
  print(resources['Organization']['AvailablePolicyTypes'])

def create_member_account(email, account_name, org):
  resources = org.create_account(
      Email=email,
      AccountName=account_name,
      #RoleName='string',
      #IamUserAccessToBilling='ALLOW'|'DENY',
      Tags=[
	  {
	      'Key': 'Name',
	      'Value': account_name
	  },
      ]
  )
  print(resources)

def create_org(org):
	resources = org.create_organization(
			#FeatureSet='ALL'|'CONSOLIDATED_BILLING'

	)

def create_org_unit(parent_id, unit_name, org):
	resources = org.create_organizational_unit(
			ParentId=parent_id,
			Name=unit_name,
			Tags=[
					{
							'Key': 'Name',
							'Value': unit_name
					},
			]
	)


