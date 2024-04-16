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
from models.db_models.proxy_type import ProxyType
from handlers.paginator import keyboards

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

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith('_proxy') and len(call.data.split("_")) == 2)
def callback_proxy(call):
    """
    """

    user_id = int(call.data.split('_')[0])

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        types.InlineKeyboardButton("IPV4", callback_data=f'{user_id}_ipv4_proxy'),
        types.InlineKeyboardButton("Residential", callback_data=f'{user_id}_resident_proxy'),
        types.InlineKeyboardButton("ISP", callback_data=f'{user_id}_isp_proxy'),
        types.InlineKeyboardButton("Mobile", callback_data=f'{user_id}_mobile_proxy')
    )

    msg = """\

"""
    
    bot.edit_message_text("Choose type of Proxy", call.message.chat.id, call.message.id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call:
                            call.data.endswith("_proxy"))
def callback_proxytype(call):
    """
    """

    user_id = int(call.data.split('_')[0])
    proxytype = call.data.split("_")[1]

    uim.create_ongoing_order(user_id, proxytype)

    proxy_type = storage.store.get(ProxyType, proxytype)
    
    countries = proxy_type.countries
    
    for i, j in enumerate(keyboards):
        if j["id"] == call.message.chat.id:
            del keyboards[i]

    data = []

    i = 0
    for country in countries:
        name = country['name'].split(' ')[-1] if proxytype == 'ipv4' else country['name']
        c_id = country['code'] if proxytype == 'resident' else country['id']
        uim.set_ongoing_order_temp(user_id, (name, c_id))

        cb_datas = {'resident': 'resident_location', 'mobile': 'mobile_location', 'ipv4_isp': 'ipv4_isp_location'}
        cb_data = cb_datas[proxytype] if proxytype in ['resident', 'mobile'] else cb_datas['ipv4_isp']
        
        data.append((f"{name}", f"{user_id}_{i}_{cb_data}"))
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
Choose {"Location" if proxytype not in ['resident'] else "Plan"} for {proxytype.capitalize()} proxy:
"""

    bot.edit_message_text(
        msg,
        call.message.chat.id, call.message.id,
        reply_markup=keyboard.send_keyboard()
    )