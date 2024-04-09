#!/usr/bin/python3

"""
period.py:
    This module contain the defination of the class Period.
"""

from datetime import datetime
import uuid

from storm.locals import DateTime,\
    Int, Unicode

from models import storage


class Period:
    '''
    Period:
        Defination of class that contains proxy usage period information.
    '''
    __storm_table__ = 'periods'

    period_id = Unicode(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    name = Unicode()
    price = Int()

    def __init__(self, period_id, name, price):
        self.period_id = period_id
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.name = name
        self.price = price
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()