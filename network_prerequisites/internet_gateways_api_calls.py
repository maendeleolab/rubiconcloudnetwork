#!/usr/bin/env python3



# This function returns the internet gateway tag "Name" key
def get_igw_name(igw_name, ec2):
  try:
    if igw_name == None:
      pass
    else:
      resources = ec2.describe_internet_gateways(
        Filters=[
          {
            'Name': 'tag:Name',
              'Values': [
                  igw_name,
              ]
          },
        ],
        #DryRun=True|False,
      )
      for item in resources['InternetGateways'][0]['Tags']:
        print(f'Resource name: {item["Value"]}...')
        return item['Value']
  except Exception as err:
    print(f'Error found: {err}...')


# This function returns the internet gateway id
def get_igw_id(igw_name, ec2):
  try:
    if igw_name == None:
      pass
    else:
      resources = ec2.describe_internet_gateways(
        Filters=[
          {
            'Name': 'tag:Name',
              'Values': [
                  igw_name,
              ]
          },
        ],
        #DryRun=True|False,
      )
      for item in resources['InternetGateways']:
        print(f'{igw_name}: {item["InternetGatewayId"]}...')
        return item['InternetGatewayId']
  except Exception as err:
    print(f'Error found: {err}...')


# This function returns the state of the internet gateway attachment
def get_igw_attachment_state(igw_name, ec2):
  try:
    if igw_name == None:
      pass
    else:
      resources = ec2.describe_internet_gateways(
        #DryRun=True|False,
        InternetGatewayIds=[
        igw_name,
         ],
      )
      for item in resources['InternetGateways'][0]['Attachments']:
        print(f'Internet gateway: {igw_name}, state: {item["State"]}...')
        return item['State']
  except Exception as err:
    print(f'Error found: {err}...')

# This function creates the internet gateway
def create_igw(igw, ec2):
  try:
    if get_igw_name(igw, ec2) == igw:
      print(f'Internet Gateway: {igw} already exists...')
      pass
    else:
      resources = ec2.create_internet_gateway(
          TagSpecifications=[
              {
                  'ResourceType': 'internet-gateway',
                  'Tags': [
                      {
                          'Key': 'Name',
                          'Value': igw
                      },
                  ]
              },
          ],
          #DryRun=True|False
      )
      print(f'{igw}: {resources["InternetGateway"]["InternetGatewayId"]}...')
  except Exception as err:
    print(f'Error found: {err}...')

# This function attaches the internet gateway to a vpc
def create_igw_attachment(igw_name, vpc_id, ec2):
	try:
		resources = ec2.attach_internet_gateway(
				#DryRun=True|False,
				InternetGatewayId=get_igw_id(igw_name, ec2),
				VpcId=vpc_id
		)
		print(f'Attaching igw: {igw_name} to vpc id: {vpc_id}...')
	except Exception as err:
		print(f'Error found: {err}...')

# This function deletes the internet gateway
def delete_igw(igw_id, ec2):
  try:
    if igw_id == None:
      pass
    else:
      print(f'Delete {igw_id}...')
      resources = ec2.delete_internet_gateway(
          #DryRun=True|False,
          InternetGatewayId=igw_id
      )
  except Exception as err:
    print(f'Error found: {err}...')

