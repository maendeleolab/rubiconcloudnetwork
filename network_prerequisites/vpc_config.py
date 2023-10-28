#!/usr/bin/env python3

from vpcs_template import describe_resources, describe_ids, describe_some
from vpcs_template import create_resources


#describe_resources('boto3_vpc1')
#print('\nPrinting next item...\n')
#describe_resources('NetworkDevEgress')
#print('\nPrinting all items...\n')
#describe_some()
#print('\nPrinting item id...\n')
#print(describe_ids('boto3_vpc1'))
print('\nCreating vpc...\n')
create_resources('boto3_vpc1','10.100.0.0/20')
print('\nCreating another vpc...\n')
create_resources('boto3_vpc2','10.200.0.0/20')
