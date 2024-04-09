#!/usr/bin/python3

"""
user_manager.py:
    This module contains the defination of the UserInfoManger class.
"""

class UserManager:
    """
    UserManager: A model for object that manages / maps user to their
                  corresponding user object.

    This is a documentation for the constructor method of this Class.
    Args:
        None
    """
    
    __users = {}

    def create_user(self, user_id):
        """
        create_user: creats and entry and user object with the user_id
                      provided.

        Args:
            user_id (int): The telegram id of the user.
        """
        from models.db_models.user import User
        self.__users[user_id] = User(user_id=user_id)
        self.__users[user_id].save()
    
    def create_ongoing_order(self, user_id, proxy_locations):
        """
        create_ongoing_order: creats an ongoing_order dict that tracks the option
                              the user entered to order proxy.

        Args:
            user_id (int): The telegram id of the user.
            proxy_locations (str): The proxy locations the user choose.
        """
        self.__users[user_id].ongoing_order = {}
        self.__users[user_id].ongoing_order['proxy_locations'] = proxy_locations
        self.__users[user_id].save()
        
    def set_ongoing_order_country(self, user_id, country, country_id):
        """
        set_ongoing_order_country: sets the country information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            countr (int): The name of the country.
            country_id (int): The id of the country the user choose.
        """
        self.__users[user_id].ongoing_order['country'] = country
        self.__users[user_id].ongoing_order['country_id'] = country_id
        self.__users[user_id].save()
    
    def set_ongoing_order_period(self, user_id, period, period_id):
        """
        set_ongoing_order_period: sets the period information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            period (str): The name of the period.
            period_id (str): The id of the period the user chose.
        """
        self.__users[user_id].ongoing_order['period'] = period
        self.__users[user_id].ongoing_order['period_id'] = period_id
        self.__users[user_id].save()

    def set_ongoing_order_quantity(self, user_id, quantity):
        """
        set_ongoing_order_quantity: sets the quantity of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            quantity (int): The quantity of the proxy the user set.
        """
        self.__users[user_id].ongoing_order['quantity'] = quantity
        self.__users[user_id].save()
    
    def ongoing_order_done(self, user_id):
        """
        ongoing_order_done: deletes the ongoing order prop from the UserInfo obj.

        Args:
            user_id (int): The telegram id of the user.
        """
        self.__users[user_id].ongoing_order = {}
        self.save()

    def users(self):
        """
        users: return the dictionary of the user_id user object pair.

        Args:
            None
        """
        return (dict(self.__users))

    def get(self, user_id):
        """
        get: return the item with the provided user_id entry

        Args:
            user_id (int): The telegram id of the user.
        """
        
        try:
            return self.__users[user_id]
        except KeyError:
            return None

    def remove(self, user_id):
        """
        remove: removes an item from the dictionary.

        Args:
            user_id (int): The telegram id of the user.
        """
        del self.__users[user_id]

    def reload(self):
        """
        reload: reloads previously registered users before the bot stoped.
        """
        from models import storage

        users = storage.get('User')

        for user in users:
            self.__users[user.user_id] = user