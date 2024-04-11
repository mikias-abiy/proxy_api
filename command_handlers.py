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


keyboards = []


@bot.message_handler(commands=['start'])
def cmd_start(message):
    """
    """

    user_id = message.from_user.id

    if uim.get(user_id) is None:
        uim.create_user(user_id)

    user_info = uim.get(user_id)
    user_info.user_name = message.from_user.username
    user_info.first_name = message.from_user.first_name
    user_info.save()

    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton(
            "Dashboard", callback_data=f'{user_id}_dashboard'
        ),
        types.InlineKeyboardButton("Proxy", callback_data=f'{user_id}_proxy'),
        types.InlineKeyboardButton("VPS", callback_data=f'{user_id}_vps')
    )
    markup.row(
        types.InlineKeyboardButton(
            "Information", callback_data=f'{user_id}_information'
        )
    )
    markup.row(
        types.InlineKeyboardButton("Channel", url='https://www.google.com/'),
        types.InlineKeyboardButton("Chat", url='https://www.google.com/')
    )

    bot.send_message(
        message.chat.id, "Welcome to the bot!", reply_markup=markup
    )


@bot.message_handler(func=lambda message:
                     message.text.isdigit())
def cmd_order_calc(message):
    """
    """

    user_id = message.from_user.id
    quantity = int(message.text)

    uim.set_ongoing_order_quantity(user_id, quantity)

    user_info = uim.get(user_id)
    order_info = user_info.ongoing_order

    if (
        order_info['proxy_locations'] == 'mix' and
        quantity not in [20, 50, 100, 200, 500, 1000, 2000]
    ):
        bot.send_message(
            message.chat.id,
            "Accepted quantities for Mix Country type are the following\n" +
            "20, 50, 100, 200, 500, 1000, 2000"
        )
        return

    bot.clear_reply_handlers(message)

    if order_info['proxy_locations'] == 'ipv4':
        response = ps_api.orderCalcIpv4(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None, f"{user_info.first_name}"
        )
    elif order_info['proxy_locations'] == 'mix':
        response = ps_api.orderCalcMix(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None, f"{user_info.first_name}"
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
                "Checkout Order", callback_data=f"{user_id}_order_make"
            )
        )

    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_orders'))
def callback_orders(call):
    """
    """

    user_id = int(call.data.split("_")[0])

    orders = storage.store.find(Order, Order.user_id == user_id)
    response_orders_ipv4 = []
    response_orders_mix = []

    proxy_list_ipv4 = ps_api.proxyList("ipv4")['items']
    proxy_list_mix = ps_api.proxyList("mix")['items']

    for order in orders:
        for proxy in proxy_list_ipv4:
            if int(proxy['order_id']) == order.order_id:
                response_orders_ipv4.append(proxy)

    for order in orders:
        for proxy in proxy_list_mix:
            if int(proxy['order_id']) == order.order_id:
                response_orders_ipv4.append(proxy)

    if len(response_orders_ipv4):
        msg_ipv4 = "Country Proxy List\n"

        for order in response_orders_ipv4:
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

    if len(response_orders_mix):
        msg_mix = "Mix Country Proxy List"
        for order in response_orders_ipv4:
            msg_mix += f"""
IP: {order['ip']}
Port HTTP: {order['port_http']}
Port Socks: {order['port_socks']}
Country: {order['country']}

Credentials
Login: {order['login']}
Password: {order['password']}

"""
        bot.send_message(call.message.chat.id, msg_mix)

    if len(response_orders_ipv4) and len(response_orders_mix):
        bot.send_message(call.message.chat.id, "You have No orders")


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_order_make'))
def callback_order_make(call):
    """
    """

    user_id = int(call.data.split("_")[0])
    user_info = uim.get(user_id)

    order_info = user_info.ongoing_order

    if order_info['proxy_locations'] == 'ipv4':
        response = ps_api.orderMakeIpv4(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None,
            f"{user_info.first_name}_{order_info['country_id']}_{order_info['period_id']}"
        )
    elif order_info['proxy_locations'] == 'mix':
        response = ps_api.orderCalcMix(
            order_info['country_id'], order_info['period_id'],
            order_info['quantity'], None, None,
            f"{user_info.first_name}_{order_info['country_id']}_{order_info['period_id']}"
        )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            'Check',
            callback_data=f"{user_id}_{response['orderId']}_order_status"
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
        callback_order_status(call, order_id=response['orderId'])
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_order_status'))
def callback_order_status(call, order_id=None):
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
        callback_order_status(call, order_id)
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



@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_proxy') and len(call.data.split("_")) == 2)
def callback_proxy(call):
    """
    """

    user_id = int(call.data.split('_')[0])

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    datacenter_button = types.InlineKeyboardButton("Datacenter", callback_data=f'{user_id}_datacenter_proxy')
    residential_button = types.InlineKeyboardButton("Residential", callback_data=f'{user_id}_residential_proxy')
    
    markup.add(datacenter_button, residential_button)

    bot.edit_message_text("Proxy options:", call.message.chat.id, call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_proxy"))
def callback_proxytype(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    proxytype = call.data.split("_")[1]

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if proxytype  in ["residential"]:
        # add user_id in call back
        plan1_button = types.InlineKeyboardButton("Plan 1", callback_data='by_type_proxy')
        plan2_button = types.InlineKeyboardButton("Plan 2", callback_data='by_type_proxy')
        plan3_button = types.InlineKeyboardButton("Plan 3", callback_data='by_type_proxy')
        plan4_button = types.InlineKeyboardButton("Plan 4", callback_data='by_type_proxy')
        plan5_button = types.InlineKeyboardButton("Plan 5", callback_data='by_type_proxy')
        
        markup.add(plan1_button,plan2_button,plan3_button,plan4_button,plan5_button)

    else:
        
        by_country_button = types.InlineKeyboardButton("By Country", callback_data=f'{user_id}_ipv4_proxy_locations')
        by_type_button = types.InlineKeyboardButton("Mix Country", callback_data=f'{user_id}_mix_proxy_locations')
        
        markup.add(by_country_button, by_type_button)
    
    
    bot.edit_message_text(
        f"{proxytype.capitalize()} options:",
        call.message.chat.id, call.message.id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_proxy_locations"))
def callback_choose_proxy_location(call):
    """
    """
    
    user_id = int(call.data.split('_')[0])
    proxy_locations = call.data.split("_")[1]

    uim.create_ongoing_order(user_id, proxy_locations)

    buttons = {}

    all_countries = storage.get('Country')
    countries = []

    for country in all_countries:
        if country.type == proxy_locations:
                countries.append(country)

    if proxy_locations == "ipv4":
        for i, j in enumerate(keyboards):
            if j["id"] == call.message.chat.id:
                del keyboards[i]
    
        data = []
    
        for country in countries:
            data.append((f"{country.name.split(' ')[-1]}", f"{user_id}_{country.name.split(' ')[-1]}_{country.country_id}_location"))

        json_dict  = {
            'id': call.message.chat.id,
            'object': Keyboard(
                chat_id=call.message.chat.id, data=data, row_width=3, rows_per_page=4,
                button_text_mode=1, text_index=0, callback_index=1,
                next_page="➡️", previous_page="⬅️" 
            )
        }

        keyboards.append(json_dict)

    elif proxy_locations == "mix":
        for country in countries:
            buttons[f"{country.name}"] = {'callback_data': f"{user_id}_{country.name}_{country.country_id}_location"}

    row_width = 4 if proxy_locations == "ipv4" else 3

    markup = quick_markup(buttons, row_width=row_width)
    keyboard = [keybrd['object'] for keybrd in keyboards if keybrd['id'] == call.message.chat.id]
    keyboard = keyboard[0] if len(keyboard) else None

    bot.edit_message_text(
        f"{proxy_locations.capitalize()} options:", call.message.chat.id, call.message.id,
        reply_markup=markup if proxy_locations == 'mix' else keyboard.send_keyboard()
    )


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_location'))
def callback_choose_period(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    country = call.data.split("_")[1]
    country_id = int(call.data.split("_")[2])

    uim.set_ongoing_order_country(user_id, country, country_id)    

    periods = storage.get('Period')
    
    buttons = {}
    
    for period in periods:
        buttons[period.name + ' : ' + str(period.price) + 'USD'] = {'callback_data': f"{user_id}_{period.name}_{period.period_id}_period"}

    markup = quick_markup(buttons, row_width=2)

    bot.edit_message_text(f"Period options:", call.message.chat.id, call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_period'))
def callback_set_quantity(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    period = call.data.split("_")[1]
    period_id = call.data.split("_")[2]
    proxy_locations = uim.get(user_id).ongoing_order['proxy_locations']

    uim.set_ongoing_order_period(user_id, period, period_id)

    bot.register_next_step_handler(call.message, cmd_order_calc)

    msg = f"""
Quantity of proxy:
{
"Quantity should only be from this choices 20 or 50 or 100 or 200 or 500 or 1000 or 2000"
if proxy_locations == 'mix' else
""
}
"""

    bot.edit_message_text(msg, call.message.chat.id, call.message.id, reply_markup=None)


@bot.callback_query_handler(func=lambda call:
                            call.data in ('previous_page', 'next_page'))
def callback_pagination_handler(call):
    """
    """

    for keyboard in keyboards:
        if keyboard["id"] == call.message.chat.id:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id, message_id=call.message.message_id,
                reply_markup=keyboard["object"].edit_keyboard(call)
            )