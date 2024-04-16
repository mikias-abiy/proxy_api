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
    
    def create_ongoing_order(self, user_id, proxytype):
        """
        create_ongoing_order: creats an ongoing_order dict that tracks the option
                              the user entered to order proxy.

        Args:
            user_id (int): The telegram id of the user.
            proxytype (str): The proxy type the user choose.
        """
        self.__users[user_id].ongoing_order = {}
        self.__users[user_id].ongoing_order['proxytype'] = proxytype

        self.__users[user_id].save()

    def set_ongoing_order_temp(self, user_id, data):
        """
        set_ongoing_order_temp: sets the temporary information on the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            data (any): The data to append to the temporary list.
        """
        if self.__users[user_id].ongoing_order.get('temp', None) is None:
            self.__users[user_id].ongoing_order['temp'] = []    
        self.__users[user_id].ongoing_order['temp'].append(data)
        self.__users[user_id].save()
    
    def get_ongoing_order_temp(self, user_id):
        """
        get_ongoing_order_temp: gets the temporary information on the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
        """
        l = list(self.__users[user_id].ongoing_order['temp'])
        self.__users[user_id].ongoing_order.pop('temp')
        self.__users[user_id].save()
        print("List: ", l)
        return (l)

    def set_ongoing_order_country(self, user_id, country, country_id):
        """
        set_ongoing_order_country: sets the country information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            country (str): The name of the country.
            country_id (int): The id of the country the user choose.
        """
        self.__users[user_id].ongoing_order['country'] = country
        self.__users[user_id].ongoing_order['country_id'] = country_id
        self.__users[user_id].save()
    
    def set_ongoing_order_operator_type(self, user_id, operator_type):
        """
        set_ongoing_order_operator_type:
            sets the operator type information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            operator_type (str): dynacmic or shared.
        """
        self.__users[user_id].ongoing_order['operator_type'] = operator_type
        self.__users[user_id].save()


    def set_ongoing_order_operator(self, user_id, operator, operator_id):
        """
        set_ongoing_order_operator:
            sets the operator information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            operator (str): The name of the operator.
            operator_id (int): The id of the operator the user choose.
        """
        self.__users[user_id].ongoing_order['operator'] = operator
        self.__users[user_id].ongoing_order['operator_id'] = operator_id
        self.__users[user_id].save()

    def set_ongoing_order_rotation(self, user_id, rotation, rotation_id):
        """
        set_ongoing_order_rotation:
            sets the rotation information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            rotation (str): The name of the rotation.
            rotation_id (int): The id of the rotation the user choose.
        """
        self.__users[user_id].ongoing_order['rotation'] = rotation
        self.__users[user_id].ongoing_order['rotation_id'] = rotation_id
        self.__users[user_id].save()

    def set_ongoing_order_region(self, user_id, region):
        """
        set_ongoing_order_region: sets the region information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            region (str): The name of the region.
        """
        self.__users[user_id].ongoing_order['region'] = region
        self.__users[user_id].save()
    
    def set_ongoing_order_city(self, user_id, city):
        """
        set_ongoing_order_city: sets the city information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            city (str): The name of the city.
        """
        self.__users[user_id].ongoing_order['city'] = city
        self.__users[user_id].save()

    def set_ongoing_order_isp(self, user_id, isp):
        """
        set_ongoing_order_isp: sets the isp information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            isp (str): The name of the isp.
        """
        self.__users[user_id].ongoing_order['isp'] = isp
        self.__users[user_id].save()
    
    def set_ongoing_order_plan(self, user_id, plan, plan_id):
        """
        set_ongoing_order_plan: sets the plan information of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            plan (str): The name of the plan.
            plan_id (int): The id of the plan the user choose.
        """
        self.__users[user_id].ongoing_order['plan'] = plan
        self.__users[user_id].ongoing_order['plan_id'] = plan_id
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
    
    def set_ongoing_order_price(self, user_id, price, currency):
        """
        set_ongoing_order_price: sets the price of the ongoing order.

        Args:
            user_id (int): The telegram id of the user.
            price (int): The price of the proxy the user set.
            currency (str): The currecy the price is specified in.
        """
        self.__users[user_id].ongoing_order['price'] = price
        self.__users[user_id].ongoing_order['currency'] = currency
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