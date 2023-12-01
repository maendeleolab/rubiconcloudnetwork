#!/usr/bin/env python3



def get_vpc_peering_id(name, ec2):
resources = ec2.describe_vpc_peering_connections(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                name,
            ]
        },
    ],
    #DryRun=True|False,
    MaxResults=200
)





response = client.accept_vpc_peering_connection(
    DryRun=True|False,
    VpcPeeringConnectionId='string'
)



response = client.delete_vpc_peering_connection(
    DryRun=True|False,
    VpcPeeringConnectionId='string'
)



response = client.modify_vpc_peering_connection_options(
    AccepterPeeringConnectionOptions={
        'AllowDnsResolutionFromRemoteVpc': True|False,
        'AllowEgressFromLocalClassicLinkToRemoteVpc': True|False,
        'AllowEgressFromLocalVpcToRemoteClassicLink': True|False
    },
    DryRun=True|False,
    RequesterPeeringConnectionOptions={
        'AllowDnsResolutionFromRemoteVpc': True|False,
        'AllowEgressFromLocalClassicLinkToRemoteVpc': True|False,
        'AllowEgressFromLocalVpcToRemoteClassicLink': True|False
    },
    VpcPeeringConnectionId='string'
)



