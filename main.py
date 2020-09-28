#!/usr/bin/env python
import requests
import telebot
from telebot.types import Message
from convert import convert
from decimal import Decimal

TOKEN = ''
help_ = """e"""

amount = ''
from_ = ''
to_ = ''
date = ''
result = ''

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', 'author'])
def start_handler(message: Message):
    if str(message.text) == '/start':
        bot.reply_to(message, "Привет, я бот, который может конвертировать валюту за выбранный день, чтобы начать, напиши: +")
    elif str(message.text) == '/help':
        bot.reply_to(message, help_)
    elif str(message.text) == '/author':
        bot.reply_to(message, "")

@bot.message_handler(content_types=["text"])
def convert_handler(message: Message):
    msg = bot.send_message(message.chat.id, "Введите количество валюты")
    bot.register_next_step_handler(msg, step_1)

def step_1(message):
    global amount
    amount = str(message.text)
    msg = bot.send_message(message.chat.id, """Введите ISO-код вашей валюты \n(К примеру: RUR-рубль EUR-евро USD-доллар): """)
    bot.register_next_step_handler(msg, step_2)

def step_2(message):
    global from_
    from_ = str(message.text).upper()
    msg = bot.send_message(message.chat.id,
                           "Введите ISO-код валюты, в которую хотите первести: ")
    bot.register_next_step_handler(msg, step_3)

def step_3(message):
    global to_
    to_ = str(message.text).upper()
    msg = bot.send_message(message.chat.id,
                           "Введите дату (пример: 17/02/2005): ")
    bot.register_next_step_handler(msg, step_4)

def step_4(message: Message):
    global date
    global result
    date = str(message.text)
    if date == '-':
        date = ''
    try:
        result = convert(Decimal(amount), from_, to_, date, requests)
    except Exception as e:
        print(e)
        result = "Ой! Что-то не получилось, возможно вы неправильно ввели ISO-код валюты"
    bot.send_message(message.chat.id, result)

bot.polling()
