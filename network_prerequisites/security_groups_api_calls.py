#!/usr/bin/env python3


# This function creates a security-group
def create_sg(sg_name, ec2):
try:
resources = ec2.create_security_group(
    Description='string',
    GroupName='string',
    VpcId='string',
    TagSpecifications=[
        {
            'ResourceType':'security-group',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ],
    #DryRun=True|False
)
except Exception as err:
print(f'Error found: {err}...')
