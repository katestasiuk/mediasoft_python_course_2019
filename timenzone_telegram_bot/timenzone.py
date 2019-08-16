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
markup = types.InlineKeyboardMarkup(row_width=2)
itembtn1 = types.InlineKeyboardButton(text = 'My timezone', callback_data = 'my')
itembtn2 = types.InlineKeyboardButton(text = 'I will enter a city', callback_data = 'city')
markup.add(itembtn1, itembtn2)
zones = common_timezones

def several_zones(zone):
    zones_select = []
    for i in zones:
        if zone in i:
            zones_select.append(i)
    return zones_select

def check_city(city):
    for i in zones:
        if city in i:
            return dt.astimezone(pytz.timezone(i)).strftime(fmt)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Please enter a city name in English')
	
@bot.message_handler(content_types=['text'])
def collect_city(message):
    converted_message = message.text.title().replace(" ", "_")
    zone_check = several_zones(converted_message)
    result = check_city(converted_message)
    if len(zone_check) > 1:
        bot.send_message(message.from_user.id, 'Please be more specific. There are too many matches for {}'.format(message.text))
    elif result == None:
        bot.send_message(message.from_user.id, 'Please try another city')
    else:
        bot.send_message(message.from_user.id, 'The local time in {} is: {}'.format(message.text, result))


bot.polling()