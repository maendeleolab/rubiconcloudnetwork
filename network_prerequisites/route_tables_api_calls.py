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

# This returns the route table id
def get_vpc_route_table_id(table_name, ec2):
  try:
    if table_name == None:
      pass
    else:
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
      for item in resources['RouteTables']:
        print(f'{table_name}:{item["RouteTableId"]}')
        return item['RouteTableId']
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
def create_subnet_association_to_route_table(table_id, subnet_id, ec2):
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

