#!/usr/bin/env python3
import boto3
import sys
from resources.visibility import *

def create_ipsec_vpn(
	customer_gateway,
	vpn_gateway,
	transit_gateway,
	static_routing, #True or False
	tunnel_inside_ip_version, #V4 or V6
	ike_version,
	name,
	local_network,
	remote_network,
	outside_ip_type,
	ec2
	):
	try:
		resources = ec2.create_vpn_connection(
				CustomerGatewayId=customer_gateway,
				Type='ipsec.1',
				VpnGatewayId=vpn_gateway,
				TransitGatewayId=transit_gateway,
				#DryRun=True|False,
				Options={
						#'EnableAcceleration': True|False,
						'StaticRoutesOnly': static_routing, #True|False,
						'TunnelInsideIpVersion': tunnel_inside_ip_version, #'ipv4'|'ipv6',
						'TunnelOptions': [
								{
										#'TunnelInsideCidr': 'string',
										#'TunnelInsideIpv6Cidr': 'string',
										#'PreSharedKey': 'string',
										#'Phase1LifetimeSeconds': 123,
										#'Phase2LifetimeSeconds': 123,
										#'RekeyMarginTimeSeconds': 123,
										#'RekeyFuzzPercentage': 123,
										#'ReplayWindowSize': 123,
										#'DPDTimeoutSeconds': 123,
										#'DPDTimeoutAction': 'string',
										#'Phase1EncryptionAlgorithms': [
										#    {
										#        'Value': 'string'
										#    },
										#],
										#'Phase2EncryptionAlgorithms': [
										#    {
										#        'Value': 'string'
										#    },
										#],
										#'Phase1IntegrityAlgorithms': [
										#    {
										#        'Value': 'string'
										#    },
										#],
										#'Phase2IntegrityAlgorithms': [
										#    {
										#        'Value': 'string'
										#    },
										#],
										#'Phase1DHGroupNumbers': [
										#    {
										#        'Value': 123
										#    },
										#],
										#'Phase2DHGroupNumbers': [
										#    {
										#        'Value': 123
										#    },
										#],
										'IKEVersions': [
												{
														'Value': ike_version
												},
										],
										#'StartupAction': 'string',
										#'LogOptions': {
										#    'CloudWatchLogOptions': {
										#        'LogEnabled': True|False,
										#        'LogGroupArn': 'string',
										#        'LogOutputFormat': 'string'
										#    }
										#},
										#'EnableTunnelLifecycleControl': True|False
								},
						],
						'LocalIpv4NetworkCidr': local_network,
						'RemoteIpv4NetworkCidr': remote_network,
						#'LocalIpv6NetworkCidr': 'string',
						#'RemoteIpv6NetworkCidr': 'string',
						'OutsideIpAddressType': outside_ip_type, #private or public
						#'TransportTransitGatewayAttachmentId': 'string'
				},
				TagSpecifications=[
						{
								'ResourceType':'vpn-connection',
								'Tags': [
										{
												'Key': 'Name',
												'Value': name
										},
								]
						},
				]
		)
		print(f'Vpn connection id: {resources["VpnConnection"]["VpnConnectionId"]}')
	except Exception as err:
		logging.error(f'Found error in "create_ipsec_vpn()": {err}...')
