#!/usr/bin/env python3

from time import sleep

# This function returns the connection id


def get_vpc_peering_connection_id(name, ec2):
    try:
        resources = ec2.describe_vpc_peering_connections(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        name,
                    ]
                },
            ],
            # DryRun=True|False,
            # MaxResults=200
        )
        print(f'Peering connection id:\
		{resources["VpcPeeringConnections"][0]["VpcPeeringConnectionId"]}')
        return resources["VpcPeeringConnections"][0]["VpcPeeringConnectionId"]
    except Exception as err:
        print(f'Error found: {err}...')


# This function returns the connection name
def get_vpc_peering_connection_name(name, ec2):
    try:
        resources = ec2.describe_vpc_peering_connections(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        name,
                    ]
                },
            ],
            # DryRun=True|False,
            # NextToken='string'
            # MaxResults=200
        )
        for item in resources['VpcPeeringConnections'][0]['Tags']:
            print(f'Vpc peering: {item["Value"]}')
            return item["Value"]
    except Exception as err:
        print(f'Error found: {err}...')


# This function returns the connection status
def get_vpc_peering_connection_status(name, ec2):
    try:
        resources = ec2.describe_vpc_peering_connections(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        name,
                    ]
                },
            ],
            # DryRun=True|False,
            # NextToken='string'
            # MaxResults=200
        )
        print(
            f' Status: {resources["VpcPeeringConnections"][0]["Status"]["Code"]}')
        return resources['VpcPeeringConnections'][0]['Status']['Code']
    except Exception as err:
        print(f'Error found: {err}...')


# This function creates the vpc peering request
def create_vpc_peering(
    connection_name,
    local_vpc_id,
    peer_vpc_id,
    peer_region,
    peer_account_number,
    ec2
):
    try:
        resources = ec2.create_vpc_peering_connection(
            # DryRun=True|False,
            PeerOwnerId=peer_account_number,
            PeerVpcId=peer_vpc_id,
            VpcId=local_vpc_id,
            PeerRegion=peer_region,
            TagSpecifications=[
                {
                    'ResourceType': 'vpc-peering-connection',
                    'Tags': [
                                    {
                                        'Key': 'Name',
                                        'Value': connection_name
                                    },
                    ]
                },
            ]
        )
        print(f'Connection: {connection_name} initiated...')
        print(f'Status: {resources["VpcPeeringConnection"]["Status"]}')
    except Exception as err:
        print(f'Error found: {err}...')


# This function accepts the vpc peering connection
def accept_vpc_peering(name, ec2):
    try:
        while True:
            if get_vpc_peering_connection_status(name, ec2) == 'pending-acceptance':
                resources = ec2.accept_vpc_peering_connection(
                    # DryRun=True|False,
                    VpcPeeringConnectionId=get_vpc_peering_connection_id(
                        name, ec2)
                )
                print(
                    f'{name} status: {get_vpc_peering_connection_status(name, ec2)}')
                return get_vpc_peering_connection_status(name, ec2)
                break
            elif get_vpc_peering_connection_status(name, ec2) == 'active':
                break
            else:
                sleep(2)
                print(
                    f'Status: {get_vpc_peering_connection_status(name, ec2)}...')
            get_vpc_peering_connection_status(name, ec2)
    except Exception as err:
        print(f'Error found: {err}...')


# This function deletes the vpc peering connection
def delete_vpc_peering(vpc_peering_name, ec2):
    try:
        resources = ec2.delete_vpc_peering_connection(
            # DryRun=True|False,
            VpcPeeringConnectionId=get_vpc_peering_connection_id(
                vpc_peering_name, ec2)
        )
        print(f'Deleting Vpc peering connection: {name}...')
        print(f'Status: {get_vpc_peering_connection_status(name, ec2)}')
    except Exception as err:
        print(f'Error found: {err}...')


# This function modifies the vpc peering connection
def modify_vpc_peering(ec2, vpc_peering_name, accepter_dns=False, requester_dns=False):
    try:
        response = ec2.modify_vpc_peering_connection_options(
            AccepterPeeringConnectionOptions={
                'AllowDnsResolutionFromRemoteVpc': accepter_dns,  # True|False,
            },
            # DryRun=True|False,
            RequesterPeeringConnectionOptions={
                'AllowDnsResolutionFromRemoteVpc': requester_dns,  # True|False,
            },
            VpcPeeringConnectionId=get_vpc_peering_connection_id(
                vpc_peering_name, ec2)
        )
    except Exception as err:
        print(f'Error found: {err}...')
