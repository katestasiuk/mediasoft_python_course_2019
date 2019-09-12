import telebot
from telebot import types
from datetime import datetime
import pytz
from pytz import timezone
from pytz import common_timezones
import datetime
from telebot import apihelper

dt = datetime.datetime.now()
fmt = '%H:%M:%S %Z%z'
apihelper.proxy = {'https':'23.237.173.102:3128'}
bot = telebot.TeleBot('920238732:AAHXx2uahTn45Txb7WyFUJX5wJkkQgbssIY')

def check_city(city: str):     #проверка, есть ли город в базе часовых поясов
    for i in common_timezones:
        if city in i:
            return dt.astimezone(pytz.timezone(i)).strftime(fmt)

def several_zones(zone: str):   #обработка ситуации, когда в базе часовых поясов найдено >1 совпадения
    zones_select = []
    for i in common_timezones:
        if zone in i:
            zones_select.append(i)
    return zones_select

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Please enter a city name in English')
    
@bot.message_handler(content_types=['text'])
def collect_city(message):
    converted_message = message.text.title().replace(" ", "_")   #полученное сообщение приводится к виду Текст_Текст в соответствии с форматированием данных в базе часовых поясов
    if len(several_zones(converted_message)) > 1:
        bot.send_message(message.from_user.id, 'Please be more specific. There are too many matches for {}'.format(message.text))
    elif not check_city(converted_message):
        bot.send_message(message.from_user.id, 'Please try another city')
    else:
        result = check_city(converted_message)
        bot.send_message(message.from_user.id, 'The local time in {} is: {}'.format(message.text, result))

bot.polling()
