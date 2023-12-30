#!/usr/bin/env python3
import boto3

# This is a function to create a session
# to assume a specified role for account credentials

# logging
from resources.visibility import *


def assume_profile_creds(profile_name):
	try:
		# Creating a session to assume a specified role for credentials
		logger.info(boto3.Session(profile_name=profile_name))
		return boto3.Session(profile_name=profile_name)

	except Exception as err:
		logger.error(f'Error found in "assume_profile_creds": {err}...')


def client_session(profile_name, service, region):
	try:
		# Creating a boto3 object for the client to interact with
		# the ec2 service in aws
		logger.info(boto3.Session(profile_name=profile_name))
		return assume_profile_creds(profile_name).client(service, region_name=region)

	except Exception as err:
		logger.error(f'Error found in "client_session": {err}...')
