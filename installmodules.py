#!/usr/bin/env python3
'''Script that installs all required modules to run the data scraper.'''
import os

print('INSTALLING MODULES. DO NOT EXIT PROGRAM OR TURN OFF COMPUTER DURING '
    'INSTALLATION.')
os.system('pip install requests beautifulsoup4 selenium pandas openpyxl xlrd')
print('All done.')
