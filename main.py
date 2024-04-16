#!/usr/bin/python3

# Standard modules and packages
import logging

# Local modules and packages
from api.bot import bot
from handlers import command_handlers, dashboard_handlers,\
    order_ipv4_isp_handlers, order_resident_handlers, order_mobile_handlers


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    bot.infinity_polling()
