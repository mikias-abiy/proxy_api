
#!/usr/bin/python3

"""
proxy_type.py:
    This module contain the defination of the class ProxyType.
"""

from datetime import datetime

from storm.locals import DateTime,\
    Unicode, JSON

from models import storage


class ProxyType:
    '''
    ProxyType:
        Defination of class that contains information about proxy_type
    '''
    __storm_table__ = 'proxy_types'

    type = Unicode(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    countries = JSON(allow_none=True)
    plans = JSON(allow_none=True)
    periods = JSON(allow_none=True)

    def __init__(self, type, countries, plans, periods):
        self.type = type
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.countries = countries
        self.plans = plans
        self.periods = periods
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()
