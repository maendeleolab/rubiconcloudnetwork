

## [Description](#Description)

The objective of this project is to develop simple modular functions to deploy resources in AWS using Python Boto3.<br>
The main focus is on networking hands-on experience.<br>
Check out my project board [here](https://github.com/users/maendeleolab/projects/3/views/1?pane=info)

## [Prerequisites](#Prerequisites)

**Note:**<br>
**Linux environment is a must. Please consider using Windows Subsystem for Linux, if your system is a Windows machine.**<br>
**Must have AWS CLI installed and configured on your system.**<br>
[Follow this link to install awscli v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) <br>
Create a folder, access it, then create your virtual environment and activate it.
```
# Create folder
mkdir project
cd project
# Create a virtual environment named "labs"
python3 -m venv labs
# Activate it
source labs/bin/activate
```

Clone the project.
```
git clone https://github.com/maendeleolab/rubiconcloudnetwork.git
# Access your folder
cd rubiconcloudnetwork
```

Install the prerequisites
```
pip install -r requirements.txt
```

## [Folders_structure](#Folders_structure)

```
.
├── LICENSE
├── README.md
├── aws_org
│   └── template.py
├── infrastructure
│   ├── __init__.py
│   ├── resources
│   │   ├── __init__.py
│   │   ├── account_profiles.py
│   │   ├── delete_resources.py
│   │   ├── elastic_ip_template.py
│   │   ├── elastic_ips_api_calls.py
│   │   ├── internet_gateways_api_calls.py
│   │   ├── nat_gateway_template.py
│   │   ├── nat_gateways_api_calls.py
│   │   ├── network_access_list_template.py
│   │   ├── network_access_lists_api_calls.py
│   │   ├── prefixlist_template.py
│   │   ├── prefixlists_api_calls.py
│   │   ├── route_tables_api_calls.py
│   │   ├── security_group_template.py
│   │   ├── security_groups_api_calls.py
│   │   ├── subnets_api_calls.py
│   │   ├── vpc_peerings_api_calls.py
│   │   ├── vpc_template.py
│   │   └── vpcs_api_calls.py
│   |
|   └── vpc_peering_lab.py
|   |___ More labs ............
└── requirements.txt
```

## [Usage](#Usage)
Further details on how to work with this project are referenced in the project wiki.<br>
Access the [wiki page](https://github.com/maendeleolab/rubiconcloudnetwork/wiki) to continue.

Happy rubiconcloudnetworking! 



