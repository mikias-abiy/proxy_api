#!/usr/bin/python3

from models.proxy_seller_api import ProxySellerAPI
from config import PROXY_SELLER_API_TOKEN

ps_api = ProxySellerAPI({'key': PROXY_SELLER_API_TOKEN})