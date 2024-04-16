#!/usr/bin/python3

import os
import json

from api.ps_api import ps_api
from models import storage
from models.db_models.proxy_type import ProxyType


#!/usr/bin/python3

from api.ps_api import ps_api
from models.db_models.proxy_type import ProxyType

from models import storage

types = ['ipv4', 'isp', 'mobile']

for type in types:
    response = ps_api.referenceList(type)['items']    
    countries = response['country']
    periods = response['period']

    ProxyType(type, countries=countries, plans=None, periods=periods)

response = ps_api.referenceList('resident')['items']    

plans = response['tarifs']

b = ps_api.residentGeo()

with open('geo.zip', 'wb') as f:
    f.write(b)
os.system('unzip geo.zip')
with open('geo.json', 'r') as f:
    countries = f.read()

ProxyType('resident', countries=countries, plans=plans, periods=None)