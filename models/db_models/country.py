
#!/usr/bin/python3

"""
country.py:
    This module contain the defination of the class Country.
"""

from datetime import datetime

from storm.locals import DateTime,\
    Int, Unicode

from models import storage


class Country:
    '''
    Country:
        Defination of class that contains information about country
        where proxy are available and there information.
    '''
    __storm_table__ = 'countries'

    country_id = Int(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    name = Unicode()
    type = Unicode()

    def __init__(self, country_id, name, type):
        self.country_id = country_id
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.name = name
        self.type = type
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()
