#!/usr/bin/env python3




# This function creates a network acl

response = client.create_network_acl(
    DryRun=True|False,
    VpcId='string',
    TagSpecifications=[
        {
            'ResourceType': 'network-acl',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'string'
                },
            ]
        },
    ]
)
