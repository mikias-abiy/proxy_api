#!/usr/bin/python3

"""
deposit.py:
    This module contain the defination of the class Deposit.
"""

from datetime import datetime
import uuid

from storm.locals import DateTime,\
    Int, Unicode, UUID

from models import storage


class Deposit:
    '''
    Deposit
        Defination of class that contains user deposit information.
    '''
    __storm_table__ = 'deposits'

    tx_id = UUID(primary_key=True)
    created_at = DateTime()
    updated_at = DateTime()
    user_id = Int()
    address = Unicode()
    crypto = Unicode()
    amount = Int()

    def __init__(self, user_id, address, crypto, amount):
        self.tx_id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.user_id = user_id
        self.address = address
        self.crypto = crypto
        self.amount = amount
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()