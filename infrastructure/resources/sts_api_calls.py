#!/usr/bin/env python3
from resources.visibility import *

# This function is used to get the user account id
# to use for creating resources that require to reference
# the account id. e.g: vpc peering connections
def get_user_identity(sts):
    try:
        resources = sts.get_caller_identity()
        print(f'Account id: {resources["Account"]}')
        return resources["Account"]
    except Exception as err:
        logger.error(f'Error found: {err}...')
