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
                            call.data.endswith("_mobile_location"))
def callback_mobile_location(call):
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
        if country_id == country['id']:
            operators = country['operators']

    buttons = {}

    if operators.get('shared', None):
        buttons['Shared'] = {'callback_data': f"{user_id}_shared_mobile_operator_type"}
    if operators.get('dedicated', None):
        buttons['Dedicated'] = {'callback_data': f"{user_id}_dedicated_mobile_operator_type"}
    
    markup = quick_markup(buttons, row_width=2)

    msg = f"""\
Choose Type of Operator:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_mobile_operator_type"))
def callback_mobile_operator_type(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    operator_type = call.data.split('_')[1]
    country_id =  uim.get(user_id).ongoing_order['country_id'] 
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_operator_type(user_id, operator_type)    

    proxy_type = storage.store.get(ProxyType, proxytype)

    countries = proxy_type.countries

    for country in countries:
        if country_id == country['id']:
            operators = country['operators'][operator_type]
    
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]

    data = []

    i = 0
    for operator in operators:
        name = operator['name']
        o_id = operator['id']
        uim.set_ongoing_order_temp(user_id, (name, o_id))

        data.append((f"{name}", f"{user_id}_{i}_mobile_operator"))
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
Choose Operator:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_mobile_operator"))
def callback_mobile_operator(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split('_')[1])
    info = uim.get_ongoing_order_temp(user_id)[idx]
    operator =  info[0]
    operator_id = info[1]
    operator_type = uim.get(user_id).ongoing_order['operator_type'] 
    country_id = uim.get(user_id).ongoing_order['country_id'] 
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_operator(user_id, operator, operator_id)    

    proxy_type = storage.store.get(ProxyType, proxytype)

    countries = proxy_type.countries

    for country in countries:
        if country_id == country['id']:
            operators = country['operators'][operator_type]
    
    for operator in operators:
        if operator['id'] == operator_id:
            rotations = operator['rotations']

    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]

    data = []

    i = 0
    for rotation in rotations:
        name = rotation['name']
        r_id = rotation['id']
        uim.set_ongoing_order_temp(user_id, (name, r_id))

        data.append((f"{name}", f"{user_id}_{i}_mobile_operator_rotation"))
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
Choose Operator Rotation:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_mobile_operator_rotation'))
def callback_mobile_operator_rotation(call):
    """
    """
    user_id = int(call.data.split('_')[0])
    idx = int(call.data.split("_")[1] )
    info = uim.get_ongoing_order_temp(user_id)[idx]
    rotation = info[0]
    rotation_id = info[1]
    proxytype = uim.get(user_id).ongoing_order['proxytype']

    uim.set_ongoing_order_rotation(user_id, rotation, rotation_id)    

    proxy_type = storage.store.get(ProxyType, proxytype)
    periods = proxy_type.periods
    buttons = {}
    
    for period in periods:
        name = period['name']
        p_id = period['id']
        buttons[name] = {'callback_data': f"{user_id}_{name}_{p_id}_mobile_period"}

    markup = quick_markup(buttons, row_width=2)

    bot.edit_message_text(
        f"Choose how long you will use the proxy:",
        call.message.chat.id, call.message.id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_mobile_period'))
def callback_set_quantity(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    period = call.data.split("_")[1]
    period_id = call.data.split("_")[2]

    uim.set_ongoing_order_period(user_id, period, period_id)

    bot.register_next_step_handler(call.message, cmd_mobile_order_calc)

    bot.edit_message_text(
        f"Quantity of proxy ip addresses:",
        call.message.chat.id, call.message.id,
        reply_markup=None)



@bot.message_handler(func=lambda message:
                     message.text.isdigit())
def cmd_mobile_order_calc(message):
    """
    """

    user_id = message.from_user.id
    quantity = int(message.text)

    uim.set_ongoing_order_quantity(user_id, quantity)

    user_info = uim.get(user_id)
    order_info = user_info.ongoing_order

    bot.clear_reply_handlers(message)

    response = ps_api.orderCalcMobile(
        order_info['country_id'], order_info['period_id'], order_info['quantity'],
        order_info['operator_type'], order_info['operator_id'], order_info['rotation_id'],
        None, None
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

Operator Type: {order_info['operator_type']}
Operator: {order_info['operator']}
Rotation: {order_info['rotation']}

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
                "Checkout Order", callback_data=f"{user_id}_mobile_order_make"
            )
        )

    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_mobile_order_make'))
def callback_mobile_order_make(call):
    """
    """

    user_id = int(call.data.split("_")[0])
    user_info = uim.get(user_id)

    order_info = user_info.ongoing_order


    response = ps_api.orderMakeMobile(
            order_info['country_id'], order_info['period_id'], order_info['quantity'],
            order_info['operator_type'], order_info['operator_id'], order_info['rotation_id'],
            None, None
        )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            'Check',
            callback_data=f"{user_id}_{response['orderId']}_mobile_order_status"
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
        callback_mobile_order_status(call, order_id=response['orderId'])
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_mobile_order_status'))
def callback_mobile_order_status(call, order_id=None):
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
        callback_mobile_order_status(call, order_id)
        return

    msg = f"""
IP: {proxy['ip']}
Port HTTP: {proxy['port_http']}
Port Socks: {proxy['port_socks']}
Country: {proxy['country']}
Operator Type: {order_info['operator_type']}
Operator: {order_info['operator']}
Rotation: {order_info['rotation']}

Credentials
Login: {proxy['login']}
Password: {proxy['password']}

Thank You for using our service.
"""

    bot.edit_message_text(
        msg, call.message.chat.id, call.message.id, reply_markup=None
    )