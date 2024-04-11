#!/usr/bin/python3

"""
order.py:
    This module contain the defination of the class Order.
"""

from datetime import datetime

from storm.locals import DateTime,\
    Int, Unicode

from models import storage


class Order:
    """
    Order:
        a class defination for Order object.
    """
    __storm_table__ = 'orders'

    order_id = Int(primary=True)
    created_at = DateTime()
    updated_at = DateTime()
    user_id = Int()
    provider = Unicode(allow_none=True)
    provider_id = Int(allow_none=True)
    amount_paid = Int(allow_none=True)
    rental_period = Unicode(allow_none=True)
    item_delivered = Unicode(allow_none=True)

    def __init__(self, order_id, user_id, amount_paid, rental_period, **kwargs):
        self.order_id = order_id
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.user_id = user_id
        self.amount_paid = amount_paid
        self.rental_period = rental_period
        self.provider = kwargs.get('provider', None)
        self.provider_id = kwargs.get('provider_id', None)
        self.item_delivered = kwargs.get('item_delivered', None)
        storage.new(self)

    def save(self):
        self.updated_at = datetime.now()
        storage.save()