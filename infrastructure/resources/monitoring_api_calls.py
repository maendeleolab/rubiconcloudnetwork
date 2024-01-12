#!/usr/bin/env python3

from resources.visibility import *
from resources.iam_api_calls import *

def create_log_bucket(log_group_name, cw_logs):
	try:
		resources = cw_logs.create_log_group(
				logGroupName=log_group_name,
				#kmsKeyId='string',
				tags={
						'Name': log_group_name
				},
				#logGroupClass='STANDARD'|'INFREQUENT_ACCESS'
		)
	except Exception as err:
		logger.error(f'Error found in "create_log_bucket": {err}...')


def describe_log_bucket(log_group_name, cw_logs):
	try:
		resources = cw_logs.describe_log_groups(
		logGroupNamePrefix=log_group_name,
		#includeLinkedAccounts=True|False
		)
		print(resources)
	except Exception as err:
		logger.error(f'Error found in "describe_log_bucket": {err}...')


def update_retention_policy(log_group_name, days, cw_logs):
	try:
		resources = cw_logs.put_retention_policy(
				logGroupName=log_group_name,
				retentionInDays=int(days)
		)
	except Exception as err:
		logger.error(f'Error found in "update_retention_policy": {err}...')


def create_flowlogs(
							log_group_name, 
							role_name,
							#iam_role,
							resource_ids,
							resource_type,
							traffic_type,
							log_destination_type,
							#log_destination,
							aggregation_time,
							ec2
	):
	try:
		resources = ec2.create_flow_logs(
				#DryRun=True|False,
				#ClientToken='string',
				DeliverLogsPermissionArn=get_role_arn(role_name, iam),
				DeliverCrossAccountRole=get_role_arn(role_name, iam),
				LogGroupName=log_group_name,
				ResourceIds=[
						resource_ids,
				],
				#ResourceType='VPC'|'Subnet'|'NetworkInterface'|'TransitGateway'|'TransitGatewayAttachment',
				ResourceType=resource_type,
				#TrafficType='ACCEPT'|'REJECT'|'ALL',
				TrafficType=traffic_type,
				#LogDestinationType='cloud-watch-logs'|'s3'|'kinesis-data-firehose',
				LogDestinationType=log_destination_type,
				#LogDestination=log_destination, # arn or log group name
				LogFormat='${az-id} ${protocol} ${tcp-flags} ${srcaddr} ${srcport} \
						${dstaddr} ${dstport} ${packets} ${bytes} ${flow-direction} \
						${interface-id} ${log-status} ${action}',
				TagSpecifications=[
						{
								'ResourceType':'vpc-flow-log',
								'Tags': [
										{
												'Key': 'Name',
												'Value': log_group_name
										},
								]
						},
				],
				MaxAggregationInterval=int(aggregation_time),
				#DestinationOptions={
				#		'FileFormat': 'plain-text'|'parquet',
				#		'HiveCompatiblePartitions': True|False,
				#		'PerHourPartition': True|False
				#}
		)
	except Exception as err:
		logger.error(f'Error found in "create_flowlogs": {err}...')



