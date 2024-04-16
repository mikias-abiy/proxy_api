#!/usr/bin/python3

# Local module and package imports
from api.bot import bot

keyboards = []

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