#!/usr/bin/env python3


# This returns the route table tag key "Name"
def describe_vpc_route_table(table_name, ec2):
  try:
    resources = ec2.describe_route_tables(
        Filters=[
            {
              'Name': 'tag:Name',
                'Values': [
                    table_name,
                ]
            }
        ]
        #DryRun=True|False,
    )
    for item in resources['RouteTables'][0]['Tags']:
      return item['Value']
  except Exception as err:
    print(f'Error found: {err}...')



# This returns the route table associations state
def get_route_table_association_state(table_name, ec2):
  try:
    resources = ec2.describe_route_tables(
        Filters=[
            {
              'Name': 'tag:Name',
                'Values': [
                    table_name,
                ]
            }
        ]
        #DryRun=True|False,
    )
    for item in resources['RouteTables'][0]['Associations']:
      print(f'Route table: {table_name} is {item["AssociationSate"]["State"]}')
      return item['AssociationSate']['State']
  except Exception as err:
    print(f'Error found: {err}...')



# This returns the route table id
def get_vpc_route_table_id(table_name, ec2):
	try:
		resources = ec2.describe_route_tables(
			Filters=[
					{
						'Name': 'tag:Name',
							'Values': [
									table_name,
							]
					}
			]
		#DryRun=True|False,
		)
		print(f'Updated route table: {resources["RouteTables"][0]["RouteTableId"]}')
		return resources['RouteTables'][0]['RouteTableId']
	except Exception as err:
		print(f'Error found: {err}...')



# This creates a vpc route table
def create_vpc_route_table(vpc_id, table_name, ec2):
  try:
    result = describe_vpc_route_table(table_name, ec2)
    if result == table_name:
      print(f'Route Table: {table_name} already exists...')
      pass
    else:
      print(f'Creating {table_name}...')
      resources = ec2.create_route_table(
          #DryRun=True|False,
          VpcId=vpc_id,
          TagSpecifications=[
              {
                  'ResourceType': 'route-table',
                  'Tags': [
                      {
                          'Key': 'Name',
                          'Value': table_name
                      }
                  ]
              }
          ]
      )
  except Exception as err:
    print(f'Found error: {err}...')



# This creates a subnet association to a route table
def create_subnet_association_to_route_table(table_id,subnet_id, ec2):
  try:
    if subnet_id == None:
      pass
    else:
      resources = ec2.associate_route_table(
          #DryRun=True|False,
          RouteTableId=table_id,
          SubnetId=subnet_id,
      )
      print(f'{subnet_id} is associated to {table_id}...')
  except Exception as err:
    print(f'Error found: {err}...')



# This creates a gateway route table association
def create_gateway_association_to_route_table(table_id, gateway_id, ec2):
  try:
    if gateway_id == None:
      pass
    else:
      resources = ec2.associate_route_table(
          #DryRun=True|False,
          RouteTableId=table_id,
          GatewayId=gateway_id
      )
      print(f'{gateway_id} is associated to {table_id}...')
  except Exception as err:
    print(f'Error found: {err}...')



# This function creates a vpc route table entry for
# internet gateway or virtual private gateway
def vpc_route_entry_to_gateway(route_table_id, dst_ipv4cidr, gateway_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				GatewayId=gateway_id,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry using prefixlist
def vpc_route_entry_for_prefixlist(route_table_id, dst_ipv4cidr, prefixlist_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				DestinationPrefixListId=prefixlist_id,
				#DryRun=True|False,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry for vpc endpoint
def vpc_route_entry_for_endpoint(route_table_id, dst_ipv4cidr, endpoint_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				VpcEndpointId=endpoint_id,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry to nat gateway
def vpc_route_entry_to_nat_id(route_table_id, dst_ipv4cidr, nat_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				NatGatewayId=nat_id,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry to transit gateway
def vpc_route_entry_to_tgw(route_table_id, dst_ipv4cidr, tgw_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				TransitGatewayId=tgw_id,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry to network interface
def vpc_route_entry_to_interface(route_table_id, dst_ipv4cidr, interface_id, ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				NetworkInterfaceId=interface_id,
				RouteTableId=route_table_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry for vpc peering
def vpc_route_entry_for_vpc_peering(route_table_id, 
                                   dst_ipv4cidr,
                                   vpc_peering_id, 
                                   ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				RouteTableId=route_table_id,
				VpcPeeringConnectionId=vpc_peering_id,
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This function creates a vpc route table entry to core network (cloudwan)
def vpc_route_entry_to_core_network(route_table_id, 
                                    dst_ipv4cidr,
                                    corenetworkarn, 
                                    ec2):
	try:
		resources = ec2.create_route(
				DestinationCidrBlock=dst_ipv4cidr,
				#DestinationIpv6CidrBlock=dst_ipv6cidr,
				#DryRun=True|False,
				#EgressOnlyInternetGatewayId='string',
				#LocalGatewayId='string',
				#CarrierGatewayId='string',
				RouteTableId=route_table_id,
				CoreNetworkArn=corenetworkarn
		)
		print(resources)
	except Exception as err:
		print(f'Error found: {err}...')



# This deletes the route table
def delete_vpc_route_table(table_id, ec2):
  try:
    if table_id == None:
      pass
    else:
      print('Delete...')
      resources = ec2.delete_route_table(
          #DryRun=True|False,
          RouteTableId=table_id
      )
  except Exception as err:
    print(f'Error found: {err}...')

