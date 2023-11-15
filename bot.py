import telebot
from telebot import types

bot = telebot.TeleBot('6442510200:AAHIEQsXG6ypotSBDDE3lmIj2NksGHrCArw')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_account = types.KeyboardButton('Создать профиль')
    markup.add(create_account)
    bot.send_message(message.chat.id, 'Я бот FoF. Здесь вы можете найти с кем подраться или потрахаться', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Создать профиль':
        bot.send_message(message.chat.id, 'Напиши имя')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    pass


bot.polling(none_stop=True, interval=0)