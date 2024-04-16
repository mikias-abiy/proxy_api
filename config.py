#!/usr/bin/python3

from dotenv import dotenv_values

F_ENV = '.env.mikias'

env_vars = dotenv_values(F_ENV)

BOT_API_TOKEN = env_vars['BOT_API_TOKEN']
PROXY_SELLER_API_TOKEN = env_vars['PROXY_SELLER_API_TOKEN']