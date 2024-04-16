#!/usr/bin/python3

#!/usr/bin/python3

# Standard module imports
import asyncio
import time

# Telegram telebot API module imports
import telebot
from telebot import types
from telebot.util import quick_markup
from models.inline_pagination import Keyboard

# Local modules imports
from api.bot import bot
from api.ps_api import ps_api
from models import user_manager as uim
from models import storage
from models.db_models.order import Order
from handlers.paginator import keyboards
from models.db_models.proxy_type import ProxyType


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_resident_location"))
def callback_resident_location(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split("_")[1] )
    info = uim.get_ongoing_order_temp(user_id)[idx]
    country = info[0]
    country_id = info[1]
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_country(user_id, country, country_id)    

    proxy_type = storage.store.get(ProxyType, proxytype)

    countries = proxy_type.countries

    for country in countries:
        if country_id == country['code']:
            regions = country['regions']
    
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]

    data = []

    i = 0
    for region in regions:
        name = region['name']
        uim.set_ongoing_order_temp(user_id, name)
        data.append((f"{name}", f"{user_id}_{i}_resident_region"))
        i += 1

    json_dict  = {
        'id': call.message.chat.id,
        'object': Keyboard(
            chat_id=call.message.chat.id, data=data, row_width=3, rows_per_page=4,
            button_text_mode=1, text_index=0, callback_index=1,
            next_page="➡️", previous_page="⬅️" 
        )
    }

    keyboards.append(json_dict)

    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    msg = f"""\
Choose Region for Residential proxy:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_resident_region"))
def callback_resident_region(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split('_')[1])
    region = uim.get_ongoing_order_temp(user_id)[idx]
    country_id = uim.get(user_id).ongoing_order['country_id']
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    print(region)

    uim.set_ongoing_order_region(user_id, region)    

    proxy_type = storage.store.get(ProxyType, proxytype)

    countries = proxy_type.countries

    for country in countries:
        if country_id == country['code']:
            regions = country['regions']
 
    for reg in regions:
        if region == reg['name']:
            cities = reg['cities']

       
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]


    data = []

    i = 0
    for city in cities:
        name = city['name']
        uim.set_ongoing_order_temp(user_id, name)
        data.append((f"{name}", f"{user_id}_{i}_resident_city"))
        i += 1

    json_dict  = {
        'id': call.message.chat.id,
        'object': Keyboard(
            chat_id=call.message.chat.id, data=data, row_width=3, rows_per_page=4,
            button_text_mode=1, text_index=0, callback_index=1,
            next_page="➡️", previous_page="⬅️" 
        )
    }

    keyboards.append(json_dict)

    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    msg = f"""\
Choose City for Residential proxy:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_resident_city"))
def callback_resident_city(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split('_')[1])
    city = uim.get_ongoing_order_temp(user_id)[idx]
    region = uim.get(user_id).ongoing_order['region']
    country_id = uim.get(user_id).ongoing_order['country_id']
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_city(user_id, city)    

    proxy_type = storage.store.get(ProxyType, proxytype)

    countries = proxy_type.countries

    for country in countries:
        if country_id == country['code']:
            regions = country['regions']
 
    for reg in regions:
        if region == reg['name']:
            cities = reg['cities']

    for c in cities:
        if city == c['name']:
            isps = c['isps']
       
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]


    data = []

    i = 0
    for isp in isps:
        uim.set_ongoing_order_temp(user_id, isp)
        data.append((f"{isp}", f"{user_id}_{i}_resident_isp"))
        i += 1
    print(data)

    json_dict  = {
        'id': call.message.chat.id,
        'object': Keyboard(
            chat_id=call.message.chat.id, data=data, row_width=3, rows_per_page=4,
            button_text_mode=1, text_index=0, callback_index=1,
            next_page="➡️", previous_page="⬅️" 
        )
    }

    keyboards.append(json_dict)

    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    msg = f"""\
Choose ISP for Residential proxy:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_resident_isp"))
def callback_resident_isp(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split('_')[1])
    isp = uim.get_ongoing_order_temp(user_id)[idx]
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_isp(user_id, isp)

    proxy_type = storage.store.get(ProxyType, proxytype)
    
    plans = proxy_type.plans
    
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]

    data = []

    for plan in plans:
        name = plan['name']
        c_id = plan['id']
        data.append((f"{name}", f"{user_id}_{name}_{c_id}_resident_plan"))

    json_dict  = {
        'id': call.message.chat.id,
        'object': Keyboard(
            chat_id=call.message.chat.id, data=data, row_width=3, rows_per_page=4,
            button_text_mode=1, text_index=0, callback_index=1,
            next_page="➡️", previous_page="⬅️" 
        )
    }

    keyboards.append(json_dict)

    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    msg = f"""\
Choose {"Location" if proxytype not in ['resident'] else "Plan"} for {proxytype.capitalize()} proxy:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_resident_plan'))
def callback_resident_order_calc(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    plan = call.data.split('_')[1]
    plan_id = int(call.data.split('_')[2])

    uim.set_ongoing_order_plan(user_id, plan, plan_id)

    user_info = uim.get(user_id)
    order_info = user_info.ongoing_order


    response = ps_api.orderCalcResident(
        tarifId=order_info['plan_id'],
        coupon=None
    )

    uim.set_ongoing_order_price(
        user_id, response['total'], response['currency']
    )

    ready = True if user_info.balance >= int(order_info['price']) else False
    msg = f"""
Order Informatoin:

Country: {order_info['country']}
Region: {order_info['region']}
City: {order_info['city']}
ISP: {order_info['isp']}

Traffic Limit: {order_info['plan']}

Total Price: {order_info['price']} {order_info['currency']}
Your Balance: {user_info.balance}

{
"Press the key below to checkout your order."
 if ready else
"Sorry your balance is Insufficient topup and try again."
}
"""
    markup = None

    if ready:
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(
                "Checkout Order", callback_data=f"{user_id}_ipv4_isp_order_make"
            )
        )

    bot.edit_message_text(msg, call.message.chat.id, call.message.id, reply_markup=markup)

# Not Done End Point Error:
# Call to undefined method Crimson\Models\OrderResident::setTargetSectionId()