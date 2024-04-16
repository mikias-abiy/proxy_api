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
                            call.data.endswith('_ipv4_isp_location'))
def callback_choose_period(call):
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
    periods = proxy_type.periods
    buttons = {}
    
    for period in periods:
        name = period['name']
        p_id = period['id']
        buttons[name] = {'callback_data': f"{user_id}_{name}_{p_id}_ipv4_isp_period"}

    markup = quick_markup(buttons, row_width=2)

    bot.edit_message_text(
        f"Choose how long you will use the proxy:",
        call.message.chat.id, call.message.id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_ipv4_isp_period'))
def callback_set_quantity(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    period = call.data.split("_")[1]
    period_id = call.data.split("_")[2]

    uim.set_ongoing_order_period(user_id, period, period_id)

    bot.register_next_step_handler(call.message, cmd_ipv4_isp_order_calc)

    bot.edit_message_text(
        f"Quantity of proxy ip addresses:",
        call.message.chat.id, call.message.id,
        reply_markup=None)



@bot.message_handler(func=lambda message:
                     message.text.isdigit())
def cmd_ipv4_isp_order_calc(message):
    """
    """

    user_id = message.from_user.id
    quantity = int(message.text)

    uim.set_ongoing_order_quantity(user_id, quantity)

    user_info = uim.get(user_id)
    order_info = user_info.ongoing_order

    bot.clear_reply_handlers(message)


    if order_info['proxytype'] == 'ipv4':
        method = ps_api.orderCalcIpv4
    elif order_info['proxytype'] == 'isp':
        method = ps_api.orderCalcIsp
    response = method(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None,
            f"{user_info.first_name}_{order_info['country_id']}_{order_info['period_id']}"
        )

    uim.set_ongoing_order_price(
        user_id, response['total'], response['currency']
    )

    ready = True if user_info.balance >= int(order_info['price']) else False
    msg = f"""
Order Informatoin:

Country: {order_info['country']}
Period: {order_info['period']}
Quantity: {order_info['quantity']}

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

    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_ipv4_isp_order_make'))
def callback_ipv4_isp_order_make(call):
    """
    """

    user_id = int(call.data.split("_")[0])
    user_info = uim.get(user_id)

    order_info = user_info.ongoing_order

    if order_info['proxy_locations'] == 'ipv4':
        method = ps_api.orderMakeIpv4
    elif order_info['proxy_locations'] == 'mix':
        method = ps_api.orderCalcMix

    response = method(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None,
            f"{user_info.first_name}_{order_info['country_id']}_{order_info['period_id']}"
        )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            'Check',
            callback_data=f"{user_id}_{response['orderId']}_ipv4_isp_order_status"
        )
    )

    msg = """
You will be notified once your order is registered.
If you do not get a confirmation message in the next 5
minutes use this button to check manually.
"""

    bot.edit_message_text(
        msg, call.message.chat.id, call.message.id, reply_markup=markup
    )
    asyncio.create_task(
        callback_ipv4_isp_order_status(call, order_id=response['orderId'])
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_ipv4_isp_order_status'))
def callback_ipv4_isp_order_status(call, order_id=None):
    """
    """

    auto = False

    if order_id is None:
        order_id = int(call.data.split("_")[1])
    else:
        auto = True
        time.sleep(60 * 5)

    if not storage.store.find(Order, Order.order_id == order_id).is_empty():
        return

    user_id = int(call.data.split("_")[0])
    order_info = uim.get(user_id).ongoing_order

    proxy_list = ps_api.proxyList(order_info['proxy_locations'])['items']

    for proxy in proxy_list:
        if int(proxy['order_id']) == order_id:
            Order(
                int(proxy['order_id']), user_id,
                order_info['price'], order_info['period']
            )

    if int(proxy['order_id']) != order_id and not auto:
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(
                'Check',
                callback_data=f"{user_id}_{order_id}_order_status"
            )
        )
        msg = """\
Sorry still processing try again after another 5 minutes.
Sorry for the delay
"""
        bot.edit_message_text(msg, call.message.chat.id, call.message.id)
        return

    elif int(proxy['order_id']) != order_id and auto:
        callback_ipv4_isp_order_status(call, order_id)
        return

    msg = f"""
IP: {proxy['ip']}
Port HTTP: {proxy['port_http']}
Port Socks: {proxy['port_socks']}
Country: {proxy['country']}

Credentials
Login: {proxy['login']}
Password: {proxy['password']}

Thank You for using our service.
"""

    bot.edit_message_text(
        msg, call.message.chat.id, call.message.id, reply_markup=None
    )