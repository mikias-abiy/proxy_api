#!/usr/bin/python3

"""
user.py:
    This module contain the defination of the class User.
"""

from datetime import datetime

from storm.locals import DateTime,\
    Int, Unicode, JSON, ReferenceSet

from models.db_models.deposit import Deposit
from models.db_models.order import Order
from models import storage

class User:
    '''
    User:
        Defination of class that contains user information.
    '''
    __storm_table__ = 'users'

    user_id = Int(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    username = Unicode()
    first_name = Unicode()
    balance = Int()
    referrer_id = Int()
    deposits = ReferenceSet(user_id, Deposit.user_id)
    orders = ReferenceSet(user_id, Order.user_id)
    ongoing_order = JSON()

    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.username = kwargs.get('username', "")
        self.first_name = kwargs.get('first_name', "")
        self.referrer_id = kwargs.get('referrer_id', None)
        self.balance = 0
        self.ongoing_order = {}
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()
