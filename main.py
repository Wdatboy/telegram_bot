import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS
import googletrans
from googletrans import Translator

my_bot = telebot.TeleBot('5946052011:AAEPKT8-_6MwvMn7uAjwt13d_SYhFgQ-sBc')

@my_bot.message_handler(commands=['weather'])
def weather(message):
    msg = my_bot.send_message(message.chat.id, 'Введите город:')
    my_bot.register_next_step_handler(msg, input_gorod)

# @my_bot.message_handler(command=['translate'])
# def translate(message):
#     my_bot.send_message(message.chat.id, 'Введите язык, на который вы хотите перевести текст:', input_language)

@my_bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Обновить бота')
    item2 = types.KeyboardButton('Погода')
    item3 = types.KeyboardButton('Переводчик')
    markup.add(item1, item2, item3)
    if message.from_user.username == None or message.from_user.last_name == None:
        my_bot.send_message(message.chat.id, f"Привет, <b> {message.from_user.first_name} </b> !", parse_mode="html")
    elif message.from_user.first_name == None or message.from_user.last_name == None:
        my_bot.send_message(message.chat.id, f"Привет, <b> {message.from_user.username} </b> !", parse_mode="html")
    else:
        my_bot.send_message(message.chat.id, f"Привет, <b> {message.from_user.last_name} </b> !", parse_mode="html")
    my_bot.send_message(message.chat.id, 'Выберете кнопку', reply_markup=markup)


def input_gorod(message):
    x = message.text
    translator = Translator()
    end_text = translator.translate(x, dest='en', src='ru')
    end_text = end_text.text.lower()
    if 'choi' in end_text:
        end_text = 'choya'
    if 'razdolnoe' in end_text:
        end_text = 'rozdolne'
    elif 'feodosia' in end_text:
        end_text = 'feodosiya'
    elif 'evpatoria' in end_text:
        end_text = 'eupatoria'
    elif 'yo' in end_text:
        end_text = end_text.replace('yo', 'e')
    elif 'soviet' in end_text:
        end_text = end_text.replace('soviet', 'sovetskij')
    if '-' in end_text:
        end_text = end_text.replace('-', '_')
    elif ' ' in end_text:
        end_text = end_text.replace(' ', '_')
    elif ',' in end_text:
        end_text = end_text.replace(',', '')
    elif "'" in end_text:
        end_text = end_text.replace("'", '')

    req = requests.get(f'https://world-weather.ru/pogoda/russia/{end_text}')
    html = BS(req.content, 'html.parser')
    if req.status_code == 200:
        if html.find('div', attrs={'id': 'weather-now-number'}):
            my_bot.send_message(message.chat.id, f"Погода сейчас: {html.find('div', attrs={'id': 'weather-now-number'}).text}", parse_mode='html')
            my_bot.send_message(message.chat.id, html.find('span', attrs={'class': 'dw-into'}).text[:-8], parse_mode='html')
        else:
            my_bot.send_message(message.chat.id, 'Попробуйте написать город по-другому!', parse_mode='html')
            weather(message)
    else:
        my_bot.send_message(message.chat.id, 'Попробуйте написать город по-другому!', parse_mode='html')
        weather(message)

@my_bot.message_handler(command=['translate'])
def translate(message):
    my_bot.send_message(message.chat.id, 'Введите язык, на который хотите перевести:', parse_mode='html')
    translator = Translator()
    name_trans = translator.translate(message, dest='en', src='ru')
    my_bot.send_message(message.chat.id, 'Введите язык, с которого будет производиться перевод:')
    name_trans = name_trans.text.lower()
    name = translator.translate(message, dest='en', src='ru')
    name = name.text.lower()
    languages = googletrans.LANGUAGES
    for k, v in languages.items():
        if name in v:
            name = k
            break
    for k, v in languages.items():
        if name_trans in v:
            name_trans = k
            break
    end_text = translator.translate(message, dest=f'{name_trans}', src=f'{name}')
    end_text = end_text.text
    my_bot.send_message(message.chat.id, end_text, parse_mode='html')

str = 'сука, шлюха, блять, нахуй, пидор, kurwa, pierdol'
arr = str.split(', ')
@my_bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text.lower() == 'погода':
        weather(message)
    if message.text.lower() == 'обновить бота':
        start(message)
    if message.text.lower() == 'переводчик':
        translate(message)
    for i in range(len(arr)):
        if arr[i] in message.text.lower():
            my_bot.send_message(message.chat.id, 'Не матерись!')
            break


my_bot.polling(none_stop=True)