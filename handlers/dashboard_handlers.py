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


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_dashboard"))
def callback_dashboard(call):
    """
    """

    user_id = int(call.data.split("_")[0])

    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.row(
        types.InlineKeyboardButton(
            "Topup", callback_data=f'{user_id}_topup'
        ),
        types.InlineKeyboardButton(
            "Orders", callback_data=f'{user_id}_orders'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            "Balance", callback_data=f'{user_id}_balance'
        ),
    )

    bot.edit_message_text(
        "Dashboard options:", call.message.chat.id,
        call.message.id, reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_orders'))
def callback_orders(call):
    """
    """

    user_id = int(call.data.split("_")[0])

    data = []

    btns = ['IPV4', 'Resident', 'ISP', 'Mobile']

    for btn in btns:
        data.append((f"{btn}", f"{user_id}_orders_{btn.lower()}_user"))

    json_dict  = {
        'id': call.message.chat.id,
        'object': Keyboard(
            chat_id=call.message.chat.id, data=data, row_width=4, rows_per_page=4,
            button_text_mode=1, text_index=0, callback_index=1,
            next_page="➡️", previous_page="⬅️" 
        )
    }

    keyboards.append(json_dict)

    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    bot.edit_message_text("Choose Proxy Type:", call.message.chat.id, call.message.id, reply_markup=keyboard.send_keyboard())


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith((
                                '_orders_ipv4_user', '_orders_resident_user', 
                                '_orders_mobile_user', '_orders_isp_user'
                            )))
def callback_orders_type_user(call):
    """
    """
    user_id = int(call.data.split("_")[0])
    proxytype = call.data.split("_")[-2]

    response_orders =[]

    proxy_list = ps_api.proxyList(proxytype)['items']

    print(proxy_list)

    orders = storage.store.find(Order, Order.user_id == user_id)

    for order in orders:
        for proxy in proxy_list:
            if int(proxy['order_id']) == order.order_id:
                response_orders.append(proxy)

    if len(response_orders):
        msg_ipv4 = f"{proxytype.capitalize()} Proxy List\n"

        for order in response_orders:
            msg_ipv4 += f"""
IP: {order['ip']}
Port HTTP: {order['port_http']}
Port Socks: {order['port_socks']}
Country: {order['country']}

Credentials
Login: {order['login']}
Password: {order['password']}

"""
        bot.send_message(call.message.chat.id, msg_ipv4)
    else:
        bot.send_message(call.message.chat.id, "You have No orders")


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_balance"))
def callback_balance(call):
    """
    """

    user_info = uim.get(int(call.data.split("_")[0]))

    msg = f"Balance: {user_info.balance} USD"

    bot.edit_message_text(msg, call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_topup"))
def callback_topup(call):
    """
    """

    user_id = int(call.data.split("_")[0])

    markup = types.InlineKeyboardMarkup()
    for i in range(5, 101, 20):
        markup.row(
            types.InlineKeyboardButton(
                f'{i}$', callback_data=f'{user_id}_{i}_topup_amount'
            ),
            types.InlineKeyboardButton(
                f'{i + 5}$', callback_data=f'{user_id}_{i + 5}_topup_amount'
            ),
            types.InlineKeyboardButton(
                f'{i + 10}$', callback_data=f'{user_id}_{i + 10}_topup_amount'
            ),
            types.InlineKeyboardButton(
                f'{i + 15}$', callback_data=f'{user_id}_{i + 15}_topup_amount'
            )
        )

    msg = "Choose the amount you want to topup with."

    bot.edit_message_text(
        msg, call.message.chat.id, call.message.id, reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_topup_amount"))
def callback_topup_amount(call):
    """
    """

    data = call.data.split("_")
    user_id = int(data[0])
    user_info = uim.get(user_id)
    amount = data[1]

    methods = ps_api.balancePaymentsList()

    markup = types.InlineKeyboardMarkup()

    for i in range(0, len(methods), 2):
        markup.row(
            types.InlineKeyboardButton(
                f"{methods[i]['name']}",
                callback_data=f"{user_id}_{methods[-1]['id']}_{amount}_topup_method"
            ),
            types.InlineKeyboardButton(
                f"{methods[i + 1]['name']}",
                callback_data=f"{user_id}_{methods[-1]['id']}_{amount}_topup_method"
            ),
        )

    if len(methods) % 2 != 0:
        markup.row(
            types.InlineKeyboardButton(
                f"{methods[-1]['name']}",
                callback_data=f"{user_id}_{methods[-1]['id']}_{amount}_topup_method"
            )
        )

    msg = "Choose the method you want topup with."

    bot.edit_message_text(msg, call.message.chat.id, call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_topup_method"))
def callback_topup_method(call):
    """
    """

    data = call.data.split("_")
    user_id = int(data[0])
    user_info = uim.get(user_id)
    amount = data[2]
    method_id = data[1]

    link = ps_api.balanceAdd(amount, method_id)

    pairs = link.split('?')[-1]
    pairs = pairs.split('&')

    order_id = pairs[0].split('=')[-1]
    payment_id = pairs[1].split('=')[-1]
    hash = pairs[2].split('=')[-1]    


    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton(
            'Verify Payment', 
            callback_data=f"verify_topup_{payment_id}_{amount}_{user_info.user_id}"
        )
    )

    msg = f"Use this link to make your payment:\n{link}"

    bot.edit_message_text(msg, call.message.chat.id, call.message.id, reply_markup=markup)