#!/usr/bin/python3

"""
proxy_config.py:
    This module contain the defination of the class ProxyConfig.
"""

from datetime import datetime
import uuid

from storm.locals import DateTime,\
    Int, Unicode, UUID

from models import storage

class ProxyConfig:
    '''
    ProxyConfig:
        Defination of class that contains proxy configeration information.
    '''
    __storm_table__ = 'proxy_configs'

    proxy_config_id = UUID(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    provider = Unicode(allow_none=True)
    country_id = Int(allow_none=True)
    country = Unicode(allow_none=True)
    provider_id = Int(allow_none=True)
    period = Unicode(allow_none=True)

    def __init__(self, **kwargs):
        self.proxy_config_id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.provider = kwargs.get('provider', None)
        self.provider_id = kwargs.get('provider_id', None)
        self.country = kwargs.get('country', None)
        self.country_id = kwargs.get('country_id', None)
        self.period = kwargs.get('period', None)
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()
