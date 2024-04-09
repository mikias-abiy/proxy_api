#!/usr/bin/python3

from telebot import TeleBot
from config import BOT_API_TOKEN

bot = TeleBot(BOT_API_TOKEN, threaded=False)
