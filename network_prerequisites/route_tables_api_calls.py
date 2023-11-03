#!/usr/bin/env python3


def create_vpc_route_table(table_name, ec2):
response = ec2.create_route_table(
    #DryRun=True|False,
    VpcId='string',
    TagSpecifications=[
        {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': table_name
                },
            ]
        },
    ]
)
