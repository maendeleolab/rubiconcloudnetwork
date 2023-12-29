#!/usr/bin/env python3


import logging

logger = logging.getLogger('lab')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s:%(message)s')
file_handler = logging.FileHandler('scripts.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



#logger.debug('Created debug log')
