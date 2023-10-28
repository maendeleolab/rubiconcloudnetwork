#!/usr/bin/env python3

from vpcs_template import * 

#Create vpcs
create_resources('boto3_vpc1','10.10.0.0/20')
create_resources('boto3_vpc2','10.20.0.0/20')
