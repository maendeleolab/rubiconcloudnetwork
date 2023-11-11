

## [Description](#Description)

We are building modular scripts to build, monitor and manage cloud network infrastructures.<br>
Check out our project board [here](https://github.com/users/maendeleolab/projects/3/views/1?pane=info)

## [Prerequisites](#Prerequisites)

**Note: Must have AWS CLI installed and configured on your system.**<br>
[Follow this link to install awscli v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) <br>
Create a folder, access the folder then create your virtual environment and activate it.
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
├── LICENSE
├── README.md
├── aws_org
│   └── template.py
├── network_prerequisites
│   ├── account_profiles.py
│   ├── delete_resources.py
│   ├── network_access_lists_api_calls.py
│   ├── prefix_lists_api_calls.py
│   ├── route_tables_api_calls.py
│   ├── security_groups_api_calls.py
│   ├── subnets_api_calls.py
│   ├── vpcs_api_calls.py
│   └── vpc_template.py
└── requirements.txt
```

## [Usage](#Usage)
Further details on how to work with this project are referenced in the project wiki.<br>
Access the [wiki page](https://github.com/maendeleolab/rubiconcloudnetwork/wiki) to continue.

Happy rubiconcloudnetworking! 



